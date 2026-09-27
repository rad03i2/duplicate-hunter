# Changelog

All notable repository changes are documented here.

The project follows the version declared in `pyproject.toml`.

## Unreleased

### Documentation and identity

- Added a dedicated Duplicate Hunter visual identity and vector project artwork.
- Reorganized the main README around the verified detection pipeline and safety model.
- Added separate English and Arabic guides.
- Added architecture and brand documentation.
- Added GitHub issue and pull-request templates.
- Expanded contribution and security guidance.
- Fixed two pre-existing Ruff import findings in `core.py` without changing runtime behavior.

No runtime behavior was changed by these repository-quality updates.

## 1.0.0

Current functional baseline:

- staged duplicate discovery using size, a 64 KiB prefix SHA-256 digest, and full SHA-256 confirmation;
- recursive or non-recursive scanning of multiple paths;
- hidden-entry opt-in and symbolic-link skipping;
- minimum-size filtering;
- recoverable-space calculation;
- JSON audit reports;
- preview-first quarantine with explicit `--apply`;
- collision-safe quarantine destinations;
- quarantine manifest output;
- Ruff and Pytest validation in a Linux/Windows/macOS GitHub Actions matrix.
