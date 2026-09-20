# Security Policy

Duplicate Hunter operates on local files, so filesystem safety is part of its security model.

## Supported version

The current `main` branch and latest release are supported.

## Reporting

Please report security issues privately to the repository owner through an appropriate GitHub private reporting channel when available. Do not publish sensitive filesystem paths or personal files in a public issue.

## Safety guarantees and boundaries

- The project does not require network access or credentials.
- Duplicate confirmation uses SHA-256 content hashing.
- Symbolic links are skipped.
- Quarantine is preview-only unless `--apply` is explicitly supplied.
- The application never intentionally deletes detected duplicates.
- Users should maintain backups for important data; concurrent filesystem changes can invalidate a scan between discovery and action.

Maintainer: **Radwan Abdulhadi Ahmed (@rad03i2)**
