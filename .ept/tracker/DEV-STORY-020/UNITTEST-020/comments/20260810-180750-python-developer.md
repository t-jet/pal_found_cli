Subject: Unit test results + coverage — foundry-data-health CLI
Created: 2026-08-10T18:07:50
Updated: 2026-08-10T18:07:50
---
## Unit test results (UNITTEST-020)

### Deliverable
- `tests/test_foundry_data_health_cli.py` (verified on disk; commit b0df380)

### Coverage areas (per test plan and unittest type instructions)
- Catalog: exactly 6 OP_SPECS (check 4 + check_report 2); exact resource/operation/client_path/method rows; 2 resources
- Parser: all declared args accepted; `--config-json` required for create/replace; `--limit` int; unknown op rejected; no pagination flags anywhere
- Dispatch: check create/delete/get/replace to `client.data_health.Check`; check-report get/get-latest through nested `Check.CheckReport`; config as decoded dict; intent optional omitted when absent; limit forwarded/omitted
- JSON validation: `--config-json` must be object; invalid/absent rejected before client creation
- Access control: READONLY blocks exactly 3 writes (create/delete/replace incl. replace-class write classification); semantic reads permitted; metadata-only permits exactly 3 (check.get, check_report.get, check_report.get_latest) and blocks 3 (allow-list parse + runtime guard)
- Privacy: include_attribution=False on scope+create; sensitive values not echoed
- Timeouts, error taxonomy, output formats, console boundary

### Results
- Focused suite: 52 passed (checkpoints + data_health combined), 0 failed
- Full project suite: **1267 passed, 0 failed** (baseline 1215 + 52 new)
- Data health per-namespace branch coverage: **90%** (gate 80%)
- All SDK transport mocked; no live Foundry connection (unit tests are real unit tests)
- Environment leakage checked: FOUNDRY_AGENTIC_CLI_METADATA_ONLY / READONLY / token vars scrubbed before runs
- Time reported: see time_spent_hours field update
