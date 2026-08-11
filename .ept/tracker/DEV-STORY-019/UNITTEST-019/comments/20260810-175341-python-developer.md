Subject: Unit test plan — foundry-checkpoints CLI
Created: 2026-08-10T17:53:41
Updated: 2026-08-10T17:53:41
---
## Unit test plan (UNITTEST-019)
Focused unit and integration tests for the 3-operation checkpoints CLI. All SDK transport mocked; no live Foundry connection.

### Coverage targets (per DESIGN-019 and unittest type instructions)
- Catalog: exactly 3 OP_SPECS; exact resource/operation/client_path/method rows; single resource
- Parser: every declared argument accepted; unknown operation rejected; pagination flags only on `record search`
- Dispatch: get/get-batch/search dispatch to `client.checkpoints.Record` with correct positional/kwargs; absent optionals omitted; `request_timeout` forwarded
- Pagination: `record search` uses `with_raw_response` + PaginationHelper; page-token chaining; default single page; `--all`/`--max-pages` bounds; metadata emitted to stderr
- JSON validation: `--where-json` must be a JSON object; `--records-json` must be a JSON list; invalid input rejected before client creation
- Access control: zero writes under READONLY (all 3 permitted); metadata-only permits exactly 3/3; ACL denial exit 8
- Privacy: include_attribution=False on scope and create; sensitive values not echoed in error envelopes
- Timeouts, error taxonomy (exit codes), output formats (json/toon), console boundary
- Packaging: metadata-allow-list.md exists and parses to exactly the 3 permitted operations

### Deliverables
- `tests/test_foundry_checkpoints_cli.py`
