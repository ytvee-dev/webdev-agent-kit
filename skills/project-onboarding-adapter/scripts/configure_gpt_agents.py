#!/usr/bin/env python3
"""Plan/apply project-local GPT roles. No network, model calls, or runtime routing."""

import argparse
import base64
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
import tomllib
import uuid
from pathlib import Path

STATE = ".agents/project/model-routing-state.json"
BACKUPS = ".agents/project/model-routing-backups"
CONFIG = ".codex/config.toml"
BEGIN = "# BEGIN webdev-agent-kit model roles"
END = "# END webdev-agent-kit model roles"
ROLES = {
    "wdk_lookup": "Gather bounded evidence and paths. Do not edit files or run fixers.",
    "wdk_worker": "Implement one explicit low-risk slice. Edit only assigned files.",
    "wdk_complex": "Resolve one ambiguous or cross-boundary slice within assigned scope.",
    "wdk_reviewer": (
        "Review the diff against acceptance criteria using frontend-quality-reviewer. "
        "Follow common/independent-review-rules.md. Do not edit files or run fixers. "
        "Do not claim independence if the implementation conversation was inherited. "
        "A clean review is valid; do not invent findings."
    ),
}
COMMON = (
    "Follow host instructions and the installed .agents/AGENTS.md policy. "
    "Use the assigned skill and only the references needed for this slice. "
    "Preserve approvals, acceptance criteria, file ownership and the remaining "
    "shared retry budget. Do not change agent configuration, install tools, "
    "add unauthorized tests, or spawn more agents. Use agreed existing checks. "
    "Return concise evidence, changed paths, verification and blockers. "
    "Request escalation with evidence instead of broadening scope or retrying "
    "without a new hypothesis. Never treat a role name as proof of model identity."
)


def digest(data):
    return hashlib.sha256(data).hexdigest() if data is not None else None


def encode(data):
    return base64.b64encode(data).decode() if data is not None else None


def decode(value):
    return base64.b64decode(value, validate=True) if value is not None else None


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def text(value, label):
    if not isinstance(value, str) or not value.strip() or len(value) > 2000:
        raise ValueError(f"{label}: expected nonempty bounded text")
    return value


def keys(value, required, label):
    if not isinstance(value, dict) or set(value) != set(required):
        raise ValueError(f"{label}: expected keys {', '.join(sorted(required))}")


def validate_request(request):
    keys(
        request,
        {
            "schema_version",
            "client",
            "client_version",
            "auth_mode",
            "format",
            "observed_at",
            "availability_evidence",
            "cost_basis",
            "models",
            "roles",
        },
        "request",
    )
    if request["schema_version"] != 1 or request["client"] != "codex":
        raise ValueError("Only schema 1 and the Codex client are supported")
    if request["format"] not in {"standalone", "registered"}:
        raise ValueError("Unsupported client configuration format")
    if request["auth_mode"] not in {"chatgpt", "api-key"}:
        raise ValueError(
            "Confirm the Codex authentication mode without reading secrets"
        )
    for name in (
        "client_version",
        "observed_at",
        "availability_evidence",
        "cost_basis",
    ):
        text(request[name], name)
    models = request["models"]
    if not isinstance(models, dict) or not models:
        raise ValueError("A confirmed available GPT catalog is required")
    for model, entry in models.items():
        if not re.fullmatch(r"gpt-[A-Za-z0-9][A-Za-z0-9._-]*", model):
            raise ValueError("Only explicit GPT model IDs are supported")
        keys(entry, {"efforts", "modalities"}, model)
        for field in ("efforts", "modalities"):
            values = entry[field]
            if (
                not isinstance(values, list)
                or not values
                or any(not isinstance(v, str) or not v for v in values)
                or len(values) != len(set(values))
            ):
                raise ValueError(f"{model}: invalid {field}")
        if "text" not in entry["modalities"]:
            raise ValueError(f"{model}: text input support is required")
    keys(request["roles"], ROLES, "roles")
    for role, binding in request["roles"].items():
        keys(binding, {"model", "effort", "reason"}, role)
        model = text(binding["model"], "model")
        effort = text(binding["effort"], "effort")
        text(binding["reason"], "reason")
        if model not in models or effort not in models[model]["efforts"]:
            raise ValueError(f"{role}: model or effort is not in the confirmed catalog")


def safe_path(root, relative):
    """Reject links and nonregular targets; no writes outside the explicit host."""
    parts = Path(relative).parts
    if not parts or Path(relative).is_absolute() or ".." in parts:
        raise ValueError("Unsafe managed path")
    path = root
    for index, part in enumerate(parts):
        path = path / part
        if path.is_symlink():
            raise ValueError(f"Refusing symlink: {relative}")
        if path.exists():
            info = path.stat()
            if index < len(parts) - 1 and not stat.S_ISDIR(info.st_mode):
                raise ValueError(f"Not a directory: {relative}")
            if index == len(parts) - 1 and (
                not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
            ):
                raise ValueError(f"Not an unlinked regular file: {relative}")
    return path


def read(root, relative):
    path = safe_path(root, relative)
    return path.read_bytes() if path.exists() else None


def split_config(data):
    source = (data or b"").decode("utf-8")
    parsed = tomllib.loads(source)
    lines = source.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == BEGIN]
    ends = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == END]
    if not starts and not ends:
        return parsed, source, ""
    if len(starts) != 1 or len(ends) != 1 or ends[0] < starts[0]:
        raise ValueError("Malformed or repeated managed configuration block")
    a, b = starts[0], ends[0] + 1
    return parsed, "".join(lines[:a] + lines[b:]), "".join(lines[a:b])


def role_paths(fmt):
    directory = "agents" if fmt == "standalone" else "wdk-agents"
    return {name: f".codex/{directory}/{name}.toml" for name in ROLES}


def render_role(name, binding, fmt):
    # JSON quoting is valid TOML for these bounded strings; never interpolate code.
    fields = {}
    if fmt == "standalone":
        fields.update(name=name, description=ROLES[name])
    fields.update(model=binding["model"], model_reasoning_effort=binding["effort"])
    if name in {"wdk_lookup", "wdk_reviewer"}:
        fields["sandbox_mode"] = "read-only"
    fields["developer_instructions"] = COMMON + " " + ROLES[name]
    source = "# Managed by WebDev Agent Kit; local model binding, not a skill.\n"
    source += "".join(
        f"{k} = {json.dumps(v, ensure_ascii=False)}\n" for k, v in fields.items()
    )
    tomllib.loads(source)
    return source.encode()


def plan(root, request):
    validate_request(request)
    for pointer in (".agents/AGENTS.md", ".agents/adapters/codex.md"):
        if read(root, pointer) is None:
            raise ValueError(
                "Expected an installed Codex project bundle at this host root"
            )
    fmt = request["format"]
    paths = role_paths(fmt)
    raw_state = read(root, STATE)
    state = json.loads(raw_state) if raw_state else None
    if raw_state is not None:
        keys(
            state,
            {"schema_version", "format", "request_hash", "files", "block_hash"},
            "state",
        )
        if state["schema_version"] != 1 or state["format"] != fmt:
            raise ValueError(
                "Existing state requires explicit migration, not format switching"
            )
        if set(state["files"]) != set(paths.values()):
            raise ValueError("Unexpected managed state paths")
        for path, expected in state["files"].items():
            if digest(read(root, path)) != expected:
                raise ValueError(f"User change or missing managed file: {path}")
    config = read(root, CONFIG)
    parsed, outside, old_block = split_config(config)
    agents = parsed.get("agents", {})
    if not isinstance(agents, dict):
        raise ValueError("Invalid agents configuration")
    if agents.get("enabled") is False:
        raise ValueError("Subagents are explicitly disabled; settings are preserved")
    if state:
        if digest(old_block.encode()) != state["block_hash"]:
            raise ValueError("Managed registration block changed")
    elif old_block:
        raise ValueError("Unowned registration block; explicit migration is required")
    outside_agents = tomllib.loads(outside).get("agents", {})
    if not isinstance(outside_agents, dict) or set(ROLES) & outside_agents.keys():
        raise ValueError("Existing user agent name collides with a Kit role")
    # Check the name field, not just filenames, in all auto-discovered project roles.
    agent_dir = safe_path(root, ".codex/agents/.probe").parent
    if agent_dir.exists():
        for path in agent_dir.glob("*.toml"):
            rel = path.relative_to(root).as_posix()
            entry = tomllib.loads(read(root, rel).decode("utf-8"))
            if entry.get("name") in ROLES and not (state and rel in state["files"]):
                raise ValueError(f"Existing auto-discovered agent collides: {rel}")
    outputs = {
        path: render_role(name, request["roles"][name], fmt)
        for name, path in paths.items()
    }
    for path in outputs:
        if not state and read(root, path) is not None:
            raise ValueError(f"Refusing to adopt or overwrite an unowned file: {path}")
    block = ""
    if fmt == "registered":
        nl = "\r\n" if b"\r\n" in (config or b"") else "\n"
        block = BEGIN + nl
        for name, path in paths.items():
            block += (
                f"[agents.{name}]{nl}"
                f"description = {json.dumps(ROLES[name])}{nl}"
                f"config_file = {json.dumps(path.removeprefix('.codex/'))}{nl}"
            )
        block += END + nl
        prefix = outside + (nl if outside and not outside.endswith("\n") else "")
        updated = (prefix + block).encode()
        result = tomllib.loads(updated.decode())
        for name in ROLES:
            result["agents"].pop(name)
        before = tomllib.loads(outside)
        if "agents" not in before and not result["agents"]:
            del result["agents"]
        if before != result:
            raise ValueError("Configuration merge would alter unrelated values")
        outputs[CONFIG] = updated
    outputs[STATE] = json_bytes(
        {
            "schema_version": 1,
            "format": fmt,
            "request_hash": digest(json_bytes(request)),
            "files": {p: digest(outputs[p]) for p in paths.values()},
            "block_hash": digest(block.encode()),
        }
    )
    return {
        p: (read(root, p), data) for p, data in outputs.items() if read(root, p) != data
    }


def atomic_write(root, relative, data):
    path = safe_path(root, relative)
    if data is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o600
    fd, temp = tempfile.mkstemp(prefix=".wdk-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp, mode)
        safe_path(root, relative)
        os.replace(temp, path)
    finally:
        Path(temp).unlink(missing_ok=True)


def apply(root, changes, writer=atomic_write):
    if not changes:
        return {"status": "unchanged", "activation": "unverified", "changed": []}
    # This is recoverable multi-file installation, not a multi-file atomic commit.
    lock = safe_path(root, ".agents/project/.model-routing.lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    with lock.open("x"):
        pass
    transaction = uuid.uuid4().hex
    journal_path = f"{BACKUPS}/{transaction}/journal.json"
    try:
        for path, (before, _) in changes.items():
            if read(root, path) != before:
                raise ValueError(f"Concurrent change before installation: {path}")
        directory = safe_path(root, journal_path).parent
        directory.mkdir(parents=True, mode=0o700)
        os.chmod(directory, 0o700)
        journal = {
            p: {"before": encode(b), "after": digest(a)}
            for p, (b, a) in changes.items()
        }
        atomic_write(root, journal_path, json_bytes(journal))
        for path, (before, after) in changes.items():
            if read(root, path) != before:
                raise ValueError(f"Concurrent change during installation: {path}")
            writer(root, path, after)
    except Exception:
        conflicts = []
        for path, (before, after) in reversed(changes.items()):
            current = read(root, path)
            if current == before:
                continue
            if current == after:
                atomic_write(root, path, before)
            else:
                conflicts.append(path)
        if conflicts:
            raise ValueError(
                f"Rollback blocked by external edits: {conflicts}"
            ) from None
        raise
    finally:
        lock.unlink()
    return {
        "status": "configured",
        "activation": "unverified",
        "changed": list(changes),
        "transaction": transaction,
    }


def rollback(root, transaction):
    if not re.fullmatch(r"[0-9a-f]{32}", transaction):
        raise ValueError("Invalid transaction ID")
    raw = read(root, f"{BACKUPS}/{transaction}/journal.json")
    if raw is None:
        raise ValueError("Missing rollback journal")
    journal = json.loads(raw)
    allowed = {
        STATE,
        CONFIG,
        *role_paths("standalone").values(),
        *role_paths("registered").values(),
    }
    if not isinstance(journal, dict) or not journal or not set(journal) <= allowed:
        raise ValueError("Unexpected rollback paths")
    changes = {}
    for path, entry in journal.items():
        keys(entry, {"before", "after"}, "journal entry")
        current = read(root, path)
        original = decode(entry["before"])
        if current == original:
            continue  # Already restored, including partial automatic rollback.
        if digest(current) != entry["after"]:
            raise ValueError(f"Rollback would overwrite later user work: {path}")
        changes[path] = (current, original)
    result = apply(root, changes)
    if changes:
        result["status"] = "rolled-back"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--request", type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument(
        "--approve", action="store_true", help="Use only after explicit user permission"
    )
    parser.add_argument("--rollback", metavar="TRANSACTION")
    args = parser.parse_args()
    try:
        if not args.root.is_dir() or args.root.is_symlink():
            raise ValueError("Host root must be an existing real directory")
        root = args.root.resolve()
        if args.rollback:
            if args.request or args.apply or not args.approve:
                raise ValueError("Rollback requires --approve and no --request/--apply")
            result = rollback(root, args.rollback)
        else:
            if not args.request or (args.apply and not args.approve):
                raise ValueError("A request is required; writes also require --approve")
            request = json.loads(args.request.read_text(encoding="utf-8"))
            changes = plan(root, request)
            result = (
                apply(root, changes)
                if args.apply
                else {
                    "status": "proposed",
                    "activation": "unverified",
                    "changed": list(changes),
                }
            )
        print(json.dumps(result))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        # Do not dump request/config contents or credentials into logs.
        print(f"GPT role setup blocked: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
