from __future__ import annotations

import hashlib
import os
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

CHUNK_SIZE = 1024 * 1024


@dataclass(frozen=True)
class FileRecord:
    path: str
    size: int
    sha256: str


@dataclass(frozen=True)
class DuplicateGroup:
    sha256: str
    size: int
    files: tuple[str, ...]

    @property
    def wasted_bytes(self) -> int:
        return self.size * (len(self.files) - 1)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["files"] = list(self.files)
        data["wasted_bytes"] = self.wasted_bytes
        return data


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_files(roots: Iterable[Path], recursive: bool = True, include_hidden: bool = False):
    seen: set[tuple[int, int]] = set()
    for root in roots:
        root = root.expanduser().resolve()
        if root.is_file():
            candidates = [root]
        elif root.is_dir():
            candidates = root.rglob("*") if recursive else root.glob("*")
        else:
            continue
        for path in candidates:
            try:
                if not path.is_file() or path.is_symlink():
                    continue
                if not include_hidden and any(part.startswith(".") for part in path.relative_to(root if root.is_dir() else root.parent).parts):
                    continue
                stat = path.stat()
                identity = (stat.st_dev, stat.st_ino)
                if identity in seen:
                    continue
                seen.add(identity)
                yield path, stat.st_size
            except (OSError, ValueError):
                continue


def find_duplicates(roots: Iterable[Path], *, recursive: bool = True, include_hidden: bool = False, min_size: int = 1) -> list[DuplicateGroup]:
    """Find byte-identical files efficiently: size -> partial hash -> full SHA-256."""
    by_size: dict[int, list[Path]] = defaultdict(list)
    for path, size in iter_files(roots, recursive, include_hidden):
        if size >= min_size:
            by_size[size].append(path)

    groups: list[DuplicateGroup] = []
    for size, paths in by_size.items():
        if len(paths) < 2:
            continue
        by_prefix: dict[str, list[Path]] = defaultdict(list)
        for path in paths:
            try:
                digest = hashlib.sha256()
                with path.open("rb") as handle:
                    digest.update(handle.read(64 * 1024))
                by_prefix[digest.hexdigest()].append(path)
            except OSError:
                continue
        for candidates in by_prefix.values():
            if len(candidates) < 2:
                continue
            by_hash: dict[str, list[str]] = defaultdict(list)
            for path in candidates:
                try:
                    by_hash[sha256_file(path)].append(str(path))
                except OSError:
                    continue
            for digest, files in by_hash.items():
                if len(files) > 1:
                    groups.append(DuplicateGroup(digest, size, tuple(sorted(files))))
    return sorted(groups, key=lambda g: (g.wasted_bytes, g.size), reverse=True)


def human_bytes(value: int) -> str:
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    number = float(value)
    for unit in units:
        if number < 1024 or unit == units[-1]:
            return f"{number:.1f} {unit}"
        number /= 1024
    return f"{value} B"
