from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from .core import find_duplicates, human_bytes


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="duplicate-hunter", description="Find byte-identical duplicate files safely.")
    p.add_argument("paths", nargs="+", type=Path, help="Files/directories to scan")
    p.add_argument("--no-recursive", action="store_true")
    p.add_argument("--include-hidden", action="store_true")
    p.add_argument("--min-size", type=int, default=1, metavar="BYTES")
    p.add_argument("--json", dest="json_path", type=Path, help="Write machine-readable report")
    p.add_argument("--quarantine", type=Path, help="Move extra copies to this directory")
    p.add_argument("--apply", action="store_true", help="Actually quarantine; otherwise preview only")
    return p


def _unique_destination(directory: Path, source: Path) -> Path:
    candidate = directory / source.name
    counter = 1
    while candidate.exists():
        candidate = directory / f"{source.stem}.{counter}{source.suffix}"
        counter += 1
    return candidate


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.min_size < 0:
        print("error: --min-size must be >= 0", file=sys.stderr)
        return 2
    groups = find_duplicates(args.paths, recursive=not args.no_recursive, include_hidden=args.include_hidden, min_size=args.min_size)
    total = sum(g.wasted_bytes for g in groups)
    print(f"Duplicate groups: {len(groups)} | Recoverable: {human_bytes(total)}")
    for index, group in enumerate(groups, 1):
        print(f"\n[{index}] {len(group.files)} files | {human_bytes(group.size)} each | recoverable {human_bytes(group.wasted_bytes)}")
        print(f"    SHA-256 {group.sha256}")
        for i, path in enumerate(group.files):
            print(f"    {'KEEP' if i == 0 else 'DUP '} {path}")

    report = {"generated_at": datetime.now(timezone.utc).isoformat(), "groups": [g.to_dict() for g in groups], "recoverable_bytes": total}
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.quarantine:
        moves = [(Path(path), group.sha256) for group in groups for path in group.files[1:]]
        print(f"\nQuarantine candidates: {len(moves)}")
        if args.apply:
            args.quarantine.mkdir(parents=True, exist_ok=True)
            manifest = []
            for source, digest in moves:
                if not source.exists():
                    continue
                destination = _unique_destination(args.quarantine, source)
                shutil.move(str(source), destination)
                manifest.append({"source": str(source), "destination": str(destination), "sha256": digest})
            manifest_path = args.quarantine / "duplicate-hunter-manifest.json"
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"Moved {len(manifest)} files. Manifest: {manifest_path}")
        else:
            print("Preview only. Add --apply to move duplicate copies; originals are never auto-deleted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
