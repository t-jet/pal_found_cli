Subject: Unit test results + coverage — foundry-checkpoints CLI
Created: 2026-08-10T18:07:44
Updated: 2026-08-10T18:07:44
---
## Unit test results (UNITTEST-019)

### Deliverable
- `tests/test_foundry_checkpoints_cli.py` (verified on disk; commit b0df380)

### Coverage areas (per test plan and unittest type instructions)
- Catalog: exactly 3 OP_SPECS; exact resource/operation/client_path/method rows; single resource; PAGINATED_OPS = {record.search}
- Parser: all declared args accepted; unknown op rejected; pagination flags only on `record search` (get/get-batch assert no page flags)
- Dispatch: get (positional record_rid + request_timeout); get-batch body positionally (SDK positional `body`); search via with_raw_response (where kwarg, sort_direction)
- Pagination: cursor chaining across pages; default single page; page_size=100; metadata emitted via PaginationHelper
- JSON validation: `--where-json` must be object; `--records-json` must be list; invalid input rejected before client creation (factory.create_calls == 0)
- Access control: READONLY permits all 3 (zero writes); metadata-only permits exactly 3/3 (allow-list parse + runtime guard)
- Privacy: include_attribution=False on scope+create; sensitive values not echoed in error envelopes
- Timeouts (1..3600 bounds; invalid stops before ACL/client), error taxonomy (exit codes), output formats (json/toon), console boundary (one asyncio.run)

### Results
- Focused suite: 52 passed (checkpoints + data_health combined), 0 failed
- Full project suite: **1267 passed, 0 failed** (baseline 1215 + 52 new)
- Checkpoints per-namespace branch coverage: **88%** (gate 80%)
- All SDK transport mocked; no live Foundry connection (unit tests are real unit tests)
- Environment leakage checked: FOUNDRY_AGENTIC_CLI_METADATA_ONLY / READONLY / token vars scrubbed before runs
- Time reported: see time_spent_hours field update
