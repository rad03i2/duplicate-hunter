## Summary

Describe the change and the problem it solves.

## Validation

- [ ] `ruff check src tests`
- [ ] `pytest`
- [ ] Documentation updated when user-facing behavior changed
- [ ] No secrets, personal paths, or generated private reports included

## File-safety review

If this change affects traversal, hashing, reporting, quarantine, destinations, or manifests, explain the safety impact here.

- [ ] Preview-first behavior is preserved
- [ ] No implicit duplicate deletion was introduced
- [ ] Duplicate decisions remain content-verified

## Notes

Add platform-specific details, limitations, or follow-up context if relevant.
