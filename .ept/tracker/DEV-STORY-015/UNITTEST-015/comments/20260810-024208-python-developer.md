Subject: Unit tests complete - results and coverage
Created: 2026-08-10T02:42:08
Updated: 2026-08-10T02:42:08
---
## Unit tests complete (UNITTEST-015)

### Deliverable
- `tests/test_foundry_sql_queries_cli.py` — 29 test functions, all real unit tests (all SDK transport mocked; no live Foundry connection anywhere).

### Coverage areas (per DESIGN-015 acceptance criteria)
- Exact 5-operation catalog with per-op spec structure
- Parser surface: every declared argument accepted; unknown/missing operation → exit 1 envelope
- Nested dispatch: `client.sql_queries.SqlQuery.<method>` routing with exact kwargs for all 5 ops
- JSON validation: invalid JSON / wrong shapes → CLIInputError before client creation
- Arrow downloads (execute_ontology, get_results): streaming → BinaryDownloadHandler, atomic write, metadata envelope, unsafe filenames rejected, response closed
- Access control: READONLY blocks the 3-op write set (exit 8, zero client creation); semantic reads get_results/get_status permitted; metadata-only permits exactly get_status (1/4 policy parsed from packaged allow-list)
- Attribution suppression (include_attribution=False on factory + scope)
- Timeout validation (ADR-002 1..3600); invalid timeout stops before ACL/client
- Output formats (json/toon), privacy (sensitive values never echoed), console boundary (asyncio.run mocked)

### Results
- **Pass rate**: 29/29 passed, 0 failed (100%).
- **Coverage**: sql_queries namespace 89% branch — exceeds the ≥80% project gate.
- **Full regression**: 1146 passed, 0 failed, total 86.09% branch.
- **Command**: `pytest tests/test_foundry_sql_queries_cli.py --cov=foundry_cli.sql_queries --cov-report=term-missing -q`
- **Commit**: `0c88063`.

### Time reported
estimated_hours: 12, time_spent_hours: 6.
