Subject: Review request — DEV-020 foundry-data-health CLI (6 ops)
Created: 2026-08-10T18:15:43
Updated: 2026-08-10T18:15:43
---
## Review request (CODEREVIEW-020)

DEV-020 is Resolved and ready for code review. Implementation committed at b0df380.

### Scope to review
- `src/foundry_cli/data_health/scripts/foundry_data_health_cli.py` — 6-op catalog (check create/delete/get/replace + check-report get/get-latest), nested dispatch through `Check.CheckReport`, JSON validation of `--config-json`, ACL guard (DATA_HEALTH), retry, output, error serialization
- `src/foundry_cli/data_health/__init__.py`, `scripts/__init__.py`, `metadata-allow-list.md` (3 PERMITTED / 3 BLOCKED)
- `pyproject.toml` — `foundry-data-health` entry point, package-data, ruff E402 scope
- `tests/test_foundry_data_health_cli.py` — 25 tests (catalog, parser, dispatch, JSON validation, ACL write classification incl. replace, metadata-only, attribution, timeout, error, output, console, privacy)

### Key decisions to verify
- 6-op catalog (corrected from stale 4 per DESIGN-020)
- `config` decoded dict for CheckConfig/ReplaceCheckConfig discriminated unions
- Write set create/delete/replace; no pagination; include_attribution=False

### Verification evidence
- compileall exit 0; ruff clean; mypy source 0 errors
- Full suite: 1267 passed, 0 failed; data health branch coverage 90%
- DESIGN-020 approved and on disk
