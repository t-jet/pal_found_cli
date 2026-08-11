Subject: Review request — DEV-019 foundry-checkpoints CLI (3 ops)
Created: 2026-08-10T18:15:39
Updated: 2026-08-10T18:15:39
---
## Review request (CODEREVIEW-019)

DEV-019 is Resolved and ready for code review. Implementation committed at b0df380.

### Scope to review
- `src/foundry_cli/checkpoints/scripts/foundry_checkpoints_cli.py` — 3-op catalog (record get / get-batch / search), parser, JSON validation, PaginationHelper integration on `record search`, ACL guard (CHECKPOINTS), retry, output, error serialization
- `src/foundry_cli/checkpoints/__init__.py`, `scripts/__init__.py`, `metadata-allow-list.md` (3/3 PERMITTED)
- `pyproject.toml` — `foundry-checkpoints` entry point, package-data, ruff E402 scope
- `tests/test_foundry_checkpoints_cli.py` — 27 tests (catalog, parser, dispatch, pagination, ACL, metadata-only, attribution, timeout, error, output, console, privacy)

### Key decisions to verify
- `get_batch` body passed positionally (SDK signature `get_batch(self, body, ...)`)
- `record search` `where` required kwarg collected into pagination extra_kwargs
- Zero write operations; include_attribution=False

### Verification evidence
- compileall exit 0; ruff clean; mypy source 0 errors
- Full suite: 1267 passed, 0 failed; checkpoints branch coverage 88%
- DESIGN-019 approved and on disk
