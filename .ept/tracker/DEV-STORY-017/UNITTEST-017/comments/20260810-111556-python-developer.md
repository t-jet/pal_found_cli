Subject: Test plan
Created: 2026-08-10T11:15:56
Updated: 2026-08-10T11:15:56
---
## Test plan

File: tests/test_foundry_connectivity_cli.py (mirror test_foundry_streams_cli.py / test_foundry_models_cli.py).

Coverage:
- Catalog: exactly 20 ops, unique pairs, exact (resource, operation, client_path, method) tuples; PAGINATED_OPS frozenset.
- Parser: every declared argument for all 20 ops; unknown op rejection.
- Dispatch: each op routes to exact nested SDK client; optional args omitted when absent; JSON args decoded and validated (configuration-json, worker-json, export-settings-json, secrets-json, body-json, filters-json, config-json, markings-json); secrets inputs never echoed.
- Pagination: file-import list / table-import list use with_raw_response + PaginationHelper (page-token chaining, --max-pages, --all, stderr metadata).
- Binary upload: upload-custom-jdbc-drivers reads file bounded after ACL before client; .jar suffix validation.
- ACL: 13 writes blocked under READONLY; get_configuration_batch semantic read permitted; write classification asserted via AccessControlGuard check.
- Metadata-only: 7 permitted / 13 blocked against packaged allow-list.
- Attribution: include_attribution=False on scope and create.
- Errors/timeouts/output formats/privacy/console boundary.
