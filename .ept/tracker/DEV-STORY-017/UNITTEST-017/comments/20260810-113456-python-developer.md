Subject: Tests complete — results and coverage
Created: 2026-08-10T11:34:56
Updated: 2026-08-10T11:34:56
---
## Test suite

File: tests/test_foundry_connectivity_cli.py (33 tests, 88% branch coverage).

Coverage per acceptance criteria:
- All 20 operations exercised; exact catalog count and (resource, operation, client_path, method) tuples asserted.
- Pagination tested for file-import list and table-import list (page-token chaining, --max-pages, single-page default) via with_raw_response + PaginationHelper.
- ACL write/read classification tested: 13 writes blocked under READONLY; get_configuration_batch semantic read permitted; classification asserted via AccessControlGuard._is_write_operation.
- Metadata-only policy: packaged allow-list parses to exactly 7 permitted / 13 blocked; runtime blocks all 13 writes and permits 7 reads under FOUNDRY_AGENTIC_CLI_METADATA_ONLY.
- Attribution: include_attribution=False on invocation_scope and create.
- Binary upload: upload-custom-jdbc-drivers bounded read after ACL before client; non-.jar and missing-file rejection.
- Secrets privacy: update-secrets values never echoed to stdout.
- JSON validation, timeouts (1..3600), error taxonomy (exit 6/5), TOON output, console boundary.

Results: 33/33 pass; full suite 1214 passed (up from 1148), 86.28% branch; ruff/mypy/compileall/bandit clean. Committed at 62c269f.
