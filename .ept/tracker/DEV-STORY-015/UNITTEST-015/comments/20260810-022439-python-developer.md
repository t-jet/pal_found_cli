Subject: Test plan
Created: 2026-08-10T02:24:39
Updated: 2026-08-10T02:24:39
---
## Test plan — foundry-sql-queries CLI unit tests

### Deliverables
- `tests/test_foundry_sql_queries_cli.py` — real unit tests (all SDK transport mocked; no live connections)

### Coverage areas (per DESIGN-015 + DEV-015 catalog)
- Exact 5-operation catalog and per-op spec structure (resource/operation/client_path/method/positional/required/optional)
- Parser surface: every declared argument accepted; unknown op → CLIInputError; missing operation → exit 1 envelope
- Nested dispatch: `client.sql_queries.SqlQuery.<method>` routing for all 5 ops with exact kwargs (request_timeout)
- JSON validation: invalid JSON, wrong shapes → CLIInputError before client creation
- Download operations (execute_ontology, get_results): streaming response → BinaryDownloadHandler; atomic write; metadata envelope; unsafe filenames rejected; response closed on success/failure
- Access control: READONLY blocks cancel/execute/execute_ontology (exit 8, no client); semantic reads get_results/get_status permitted; metadata-only permits exactly get_status (1/4 policy parsed from packaged allow-list)
- Timeout validation (ADR-002 1..3600); invalid timeout stops before ACL/client
- Output formats (json/toon/auto), privacy (no sensitive values echoed), console boundary (console_main exit code)
- Coverage ≥80% branch on the new namespace required

### Verification
- Run: `pytest tests/test_foundry_sql_queries_cli.py --cov=foundry_cli.sql_queries --cov-report=term-missing`
- Document pass count and coverage in the results comment.
