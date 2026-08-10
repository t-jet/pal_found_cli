Subject: New to Open triage complete
Created: 2026-08-10T02:17:09
Updated: 2026-08-10T02:17:09
---
## New → Open triage

- **Status**: DEV-015 confirmed New → transitioned to Open.
- **Documentation studied**: DESIGN-015 (5-op catalog), canonical env-var reference (sql_queries 5 rows), metadata allow-list (1/4 policy), DESIGN-013/014 for the canonical CLI structure, shared common library (`AccessControlGuard`, `ErrorSerializer`, `OutputFormatter`, `RetryHandler`, `BinaryDownloadHandler`, `ConfigLoader`, `AsyncClientFactory`).
- **SDK surface verified**: `foundry_sdk.v2.sql_queries.SqlQueryClient` exposes exactly 5 public operations — cancel(sql_query_id), execute(query, fallback_branch_ids?, serialization_format?), execute_ontology(query, branch?, dry_run?, ontology_identifier?, parameters?, row_limit?, scenario_rid?, table_providers?), get_results(sql_query_id), get_status(sql_query_id). `preview` excluded. No ResourceIterator → no pagination. get_results/execute_ontology return bytes.
- **Critical thinking**: CLI resource subcommand is `query` (kebab of `sql_query`), consistent with DESIGN-015 CLI table (`query cancel`, `query execute`, `query execute-ontology`, `query get-results`, `query get-status`) and the canonical `<resource> <operation>` CLI pattern. ACL paths stay `sql_query.*` (snake_case).
- **Questions**: none — all requirements clear.
- **Blockers**: none. Links: Contains LINK-00519, ParentChild LINK-00520, RelatesTo CODEREVIEW-015 LINK-00531/532, Blocks LINK-00534/535 — all registered and correct.
- **Required fields**: status, assignee (python-developer), priority (High), dates — validated.
