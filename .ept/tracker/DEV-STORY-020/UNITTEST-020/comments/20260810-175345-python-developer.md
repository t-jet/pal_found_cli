Subject: Unit test plan — foundry-data-health CLI
Created: 2026-08-10T17:53:45
Updated: 2026-08-10T17:53:45
---
## Unit test plan (UNITTEST-020)
Focused unit and integration tests for the 6-operation data health CLI. All SDK transport mocked; no live Foundry connection.

### Coverage targets (per DESIGN-020 and unittest type instructions)
- Catalog: exactly 6 OP_SPECS (check 4 + check_report 2); exact resource/operation/client_path/method rows
- Parser: every declared argument accepted; `--config-json` required for create/replace; `--limit` int; unknown operation rejected; no pagination flags anywhere
- Dispatch: check create/delete/get/replace and check-report get/get-latest dispatch to correct nested clients (`client.data_health.Check` and `.Check.CheckReport`); `config` passed as decoded dict; `intent` optional; `limit` forwarded; absent optionals omitted
- JSON validation: `--config-json` must be a JSON object; invalid input rejected before client creation
- Access control: READONLY blocks exactly the 3 writes (create/delete/replace) — replace write-classified; semantic reads permitted; metadata-only permits exactly 3 (get, check_report get/get_latest) and blocks 3
- Privacy: include_attribution=False; sensitive values not echoed
- Timeouts, error taxonomy, output formats, console boundary
- Packaging: metadata-allow-list.md parses to exactly the 3 permitted operations

### Deliverables
- `tests/test_foundry_data_health_cli.py`
