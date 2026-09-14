#!/usr/bin/env python3
"""Package an exact review surface in local plan-scoped storage; never run tests."""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

MAX_BYTES = 5 * 1024 * 1024


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args, ok=(0,)):
    path_options = ["--literal-pathspecs"] if args[0] in {"diff", "ls-files"} else []
    result = subprocess.run(
        ["git", "--no-pager", *path_options, "-C", str(root), *args],
        capture_output=True,
        timeout=30,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    )
    if result.returncode not in ok:
        # Do not echo arbitrary repository configuration or diff contents.
        raise ValueError(f"git {args[0]} failed with exit {result.returncode}")
    return result.stdout


def local_path(root, value, allow_leaf_link=False):
    parts = PurePosixPath(value)
    if (
        not value
        or value != parts.as_posix()
        or parts.is_absolute()
        or ".." in parts.parts
        or "\\" in value
        or ":" in value
        or ".git" in parts.parts
    ):
        raise ValueError("Expected a repository-relative path without traversal")
    current = root
    for index, part in enumerate(parts.parts):
        current /= part
        if current.is_symlink() and not (
            allow_leaf_link and index == len(parts.parts) - 1
        ):
            raise ValueError("Refusing a symlinked path")
    return current


def resolve_commit(root, value):
    resolved = git(
        root, "rev-parse", "--verify", "--end-of-options", value + "^{commit}"
    )
    sha = resolved.decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", sha):
        raise ValueError("Expected a commit revision")
    return sha


def snapshot(root, paths):
    names = (
        git(
            root,
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
            "--",
            *paths,
        )
        .decode("utf-8")
        .split("\0")
    )
    result = {}
    for name in sorted(set(names) - {""}):
        path = local_path(root, name, allow_leaf_link=True)
        if path.is_symlink():
            result[name] = digest(("symlink:" + os.readlink(path)).encode())
        elif not path.exists():
            result[name] = None
        elif path.is_file():
            if path.stat().st_size > MAX_BYTES:
                raise ValueError(
                    "Review file exceeds the size budget; narrow the scope"
                )
            result[name] = digest(path.read_bytes())
        else:
            raise ValueError("Submodules/directories need a separate explicit review")
    return result


def package(root, plan, base, head="HEAD", worktree=False, paths=()):
    root = Path(root).resolve(strict=True)
    actual = Path(git(root, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    if actual != root:
        raise ValueError("--root must identify the actual worktree root")
    plan_path = local_path(root, plan)
    if not plan_path.is_file():
        raise ValueError("A reachable canonical plan is required")
    plan_data = plan_path.read_bytes()
    for path in paths:
        local_path(root, path, allow_leaf_link=True)
    if worktree and not paths:
        raise ValueError("Working-tree capture requires explicit --path ownership")
    base_sha = resolve_commit(root, base)
    head_sha = resolve_commit(root, head)
    git(root, "merge-base", "--is-ancestor", base_sha, head_sha)
    current_head = resolve_commit(root, "HEAD")
    if worktree and head_sha != current_head:
        raise ValueError("Working-tree capture must use the current HEAD")
    before = snapshot(root, paths) if worktree else {}
    diff_args = ["diff", "--no-ext-diff", "--no-textconv", "-U8", base_sha]
    if not worktree:
        diff_args.append(head_sha)
    diff = git(root, *diff_args, "--", *paths)
    untracked = []
    if worktree:
        untracked = sorted(
            set(
                git(
                    root,
                    "ls-files",
                    "--others",
                    "--exclude-standard",
                    "-z",
                    "--",
                    *paths,
                )
                .decode()
                .split("\0")
            )
            - {""}
        )
        for name in untracked:
            file = local_path(root, name)
            if not file.is_file():
                raise ValueError(
                    "Untracked nonregular files need explicit separate evidence"
                )
            diff += git(
                root,
                "diff",
                "--no-index",
                "--no-ext-diff",
                "--no-textconv",
                "-U8",
                "--",
                os.devnull,
                name,
                ok=(0, 1),
            )
    metadata = {
        "schema_version": 1,
        "plan": plan,
        "plan_sha256": digest(plan_data),
        "base": base_sha,
        "head": head_sha,
        "surface": "working-tree" if worktree else "committed-range",
        "owned_paths": list(paths),
        "file_sha256": before,
        "untracked_files": untracked,
        "verification": "not-run-by-packager",
    }
    commits = git(root, "log", "--oneline", f"{base_sha}..{head_sha}")
    stat_args = ["diff", "--no-ext-diff", "--no-textconv", "--stat", base_sha]
    if not worktree:
        stat_args.append(head_sha)
    stat = git(root, *stat_args, "--", *paths)
    content = (
        b"# Review package\n\n## Snapshot metadata\n\n"
        + json.dumps(metadata, indent=2, sort_keys=True).encode()
        + b"\n\n## Commits\n\n"
        + commits
        + b"\n## Tracked diff summary\n\n"
        + stat
        + b"\n## Diff (includes listed untracked files)\n\n"
        + diff
    )
    if len(content) > MAX_BYTES:
        raise ValueError("Review package exceeds the size budget; narrow the scope")
    if plan_path.read_bytes() != plan_data or (
        worktree
        and (
            snapshot(root, paths) != before
            or resolve_commit(root, "HEAD") != current_head
        )
    ):
        raise ValueError("Code or plan changed while packaging; capture again")
    run_id = digest(plan.encode())[:16]
    relative = f".agents/project/runs/{run_id}/review-{digest(content)[:20]}.diff"
    output = local_path(root, relative)
    if not git(root, "check-ignore", "--no-index", "--", relative, ok=(0, 1)).strip():
        raise ValueError(
            "Local review storage must be git-ignored; request a scoped ignore change first"
        )
    if output.exists():
        if not output.is_file() or output.read_bytes() != content:
            raise ValueError("Refusing to overwrite another artifact")
        status = "unchanged"
    else:
        output.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
        # Exclusive creation also refuses a file/symlink inserted after the check.
        fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
        status = "created"
    return {"path": relative, "sha256": digest(content), "status": status, **metadata}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--worktree", action="store_true")
    parser.add_argument("--path", action="append", default=[])
    args = parser.parse_args()
    try:
        result = package(
            args.root, args.plan, args.base, args.head, args.worktree, args.path
        )
        # The caller passes the artifact path on, without loading the diff itself.
        print(
            json.dumps(
                {
                    key: result[key]
                    for key in ("path", "sha256", "status", "base", "head", "surface")
                }
            )
        )
        return 0
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"Review package blocked: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
