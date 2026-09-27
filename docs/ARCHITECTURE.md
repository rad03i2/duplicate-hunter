# Duplicate Hunter Architecture

This document describes the behavior that exists in the current codebase. It is not a roadmap.

## Runtime components

| Component | Responsibility |
|---|---|
| `src/duplicate_hunter/core.py` | File traversal, hashing, duplicate grouping, recoverable-byte calculation |
| `src/duplicate_hunter/cli.py` | Argument parsing, console output, JSON reporting, quarantine preview/apply |
| `tests/test_core.py` | Core detection, filtering, recursion, hashing, size formatting |
| `tests/test_cli.py` | JSON output and quarantine behavior |
| `.github/workflows/ci.yml` | Cross-platform Ruff and Pytest matrix |

## Detection flow

```text
Input paths
   │
   ▼
iter_files()
   │
   ├─ resolve each root
   ├─ recurse unless --no-recursive
   ├─ skip symbolic links
   ├─ skip hidden entries unless requested
   ├─ skip unreadable/invalid entries
   └─ de-duplicate filesystem identities
   │
   ▼
group candidates by exact size
   │
   ▼
SHA-256(first 64 KiB)
   │
   ▼
full SHA-256 for remaining candidates
   │
   ▼
DuplicateGroup
   │
   ├─ sorted file paths
   ├─ exact file size
   ├─ full SHA-256
   └─ wasted_bytes = size × (file_count - 1)
```

The prefix stage is only a performance filter. The application requires a matching full SHA-256 value before files are placed in the same duplicate group.

## Core data model

### `DuplicateGroup`

A group stores:

- the shared full SHA-256 digest;
- the size of one file;
- a sorted tuple of file paths.

`wasted_bytes` is computed as:

```text
file size × (number of files - 1)
```

This represents the theoretical space associated with redundant copies while keeping one file.

### Filesystem identity

During one traversal, the scanner records `(st_dev, st_ino)`. If that identity has already been seen, it is skipped. This prevents the same underlying file from being counted more than once through hard links during a scan.

## Quarantine flow

Quarantine starts from every group except its first sorted path:

```text
duplicate group
   │
   ├─ first path ───────────────► KEEP
   │
   └─ remaining paths
          │
          ▼
     preview candidate list
          │
          ├─ no --apply ────────► stop, no moves
          │
          └─ --apply
                │
                ├─ create quarantine directory
                ├─ resolve destination name collisions
                ├─ shutil.move(...)
                └─ write duplicate-hunter-manifest.json
```

The manifest contains source path, destination path, and the duplicate group's SHA-256 value for each moved file.

## Safety invariants in the current implementation

1. Duplicate grouping is content-based.
2. Symbolic links are not followed as duplicate candidates.
3. Quarantine is preview-only without `--apply`.
4. The program does not call a delete operation for detected duplicates.
5. Unreadable files are skipped.
6. One path from each duplicate group is retained by the quarantine workflow.
7. Destination filename collisions are resolved instead of overwritten.

## Known boundaries

- A filesystem can change between scanning and acting.
- Full SHA-256 confirmation still requires reading candidate files completely.
- Visual similarity is outside the current scope.
- Archive contents are not inspected.
- Automatic manifest-driven restore is not implemented.

## CI contract

The current workflow installs the package in editable mode plus `pytest` and `ruff`, then runs:

```bash
ruff check src tests
pytest
```

The matrix covers Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.
