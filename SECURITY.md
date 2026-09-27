# Security Policy

Duplicate Hunter operates directly on local files, so filesystem safety is part of the security model.

## Supported code

Security fixes target the current `main` branch and the latest published project version.

## Reporting a vulnerability

Please use an appropriate private GitHub security-reporting channel when one is available for the repository. Do not publish sensitive paths, private file names, report contents, personal data, or exploit details in a public issue.

When reporting, include the smallest reproducible example possible and remove personal filesystem information.

## Current safety guarantees

The implementation currently provides these boundaries:

- no network client, account flow, credentials, or telemetry are required;
- duplicate confirmation uses full SHA-256 content hashing;
- symbolic links are skipped;
- hard-linked references to the same filesystem identity are not counted twice during a scan;
- unreadable entries are skipped;
- quarantine is preview-only unless `--apply` is explicitly supplied;
- one file from every duplicate group is kept by the quarantine workflow;
- quarantine destination collisions are renamed rather than overwritten;
- detected duplicates are not automatically deleted.

## Important limits

Duplicate Hunter cannot guarantee that files remain unchanged between scanning and quarantine. Another process can rename, replace, modify, lock, or remove a file after it was examined.

For important data:

1. keep a separate backup;
2. inspect the quarantine preview;
3. avoid applying changes while another process is actively modifying the scanned tree;
4. treat JSON reports and manifests as potentially sensitive because they may contain file paths.

Automatic restore from the quarantine manifest is not part of the current implementation.

## Dependency and CI posture

The package itself has no declared runtime dependency beyond Python. Development CI installs `pytest` and `ruff` to run the current test and lint suite.

Maintainer: **Radwan Abd alhady Ahmed (@rad03i2)**
