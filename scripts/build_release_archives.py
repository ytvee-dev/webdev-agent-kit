#!/usr/bin/env python3

import argparse
import gzip
import hashlib
import io
import re
import shutil
import stat
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
RELEASE_TARGETS = (
    "codex",
    "claude-code",
    "cursor",
    "vs-code-codex",
    "vs-code-claude",
)
CLAUDE_TARGETS = {"claude-code", "vs-code-claude"}
VERSION_PATTERN = re.compile(r"^v?\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


def tar_info(arcname, *, is_dir, mode=0o644, size=0):
    info = tarfile.TarInfo(arcname)
    info.type = tarfile.DIRTYPE if is_dir else tarfile.REGTYPE
    info.mode = 0o755 if is_dir else mode
    info.size = 0 if is_dir else size
    info.mtime = 0
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    return info


def add_tree(archive, source, archive_root, *, excluded_top_level=()):
    archive.addfile(tar_info(f"{archive_root}/", is_dir=True))
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if relative.parts and relative.parts[0] in excluded_top_level:
            continue
        arcname = f"{archive_root}/{relative.as_posix()}"
        if path.is_dir():
            archive.addfile(tar_info(f"{arcname}/", is_dir=True))
            continue
        if not path.is_file():
            raise ValueError(f"Unsupported release artifact path: {path}")
        data = path.read_bytes()
        mode = stat.S_IMODE(path.stat().st_mode)
        archive.addfile(
            tar_info(arcname, is_dir=False, mode=mode, size=len(data)),
            io.BytesIO(data),
        )


def build_archive(target, output_path):
    source = DIST / target
    if not source.is_dir():
        raise FileNotFoundError(f"Missing generated target: {source}")
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.PAX_FORMAT) as archive:
        if target in CLAUDE_TARGETS:
            add_tree(archive, source, "webdev-agent-kit")
        else:
            excluded = (".cursor",) if target == "cursor" else ()
            add_tree(archive, source, ".agents", excluded_top_level=excluded)
            if target == "cursor":
                add_tree(archive, source / ".cursor", ".cursor")
    with output_path.open("wb") as output:
        with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as stream:
            stream.write(buffer.getvalue())


def write_checksums(output_dir):
    paths = sorted(output_dir.glob("*.tar.gz"))
    lines = [
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}"
        for path in paths
    ]
    (output_dir / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_archives(output_dir, version, targets=RELEASE_TARGETS):
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError(f"Invalid release version: {version}")
    output_dir.mkdir(parents=True, exist_ok=True)
    built = []
    for target in targets:
        if target not in RELEASE_TARGETS:
            raise ValueError(f"Unknown release target: {target}")
        versioned = output_dir / f"webdev-agent-kit-{target}-{version}.tar.gz"
        stable = output_dir / f"webdev-agent-kit-{target}.tar.gz"
        build_archive(target, versioned)
        shutil.copy2(versioned, stable)
        built.extend((versioned, stable))
    write_checksums(output_dir)
    return built


def main():
    parser = argparse.ArgumentParser(
        description="Build deterministic client-specific release archives."
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument(
        "--target",
        choices=RELEASE_TARGETS,
        action="append",
        help="Build only selected release targets; repeat for multiple targets.",
    )
    args = parser.parse_args()
    targets = tuple(dict.fromkeys(args.target or RELEASE_TARGETS))
    built = build_archives(args.output, args.version, targets)
    print(f"Built {len(built)} release archives in {args.output}")


if __name__ == "__main__":
    main()
