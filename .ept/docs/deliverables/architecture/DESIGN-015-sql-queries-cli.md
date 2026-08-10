# DESIGN-015 - Foundry SQL Queries CLI

| Field | Value |
| --- | --- |
| Story | DEV-STORY-015 |
| Status | Completed; ready for implementation |
| Date | 2026-08-10 |
| Scope | `foundry-sql-queries` CLI and Claude skill, 5 SqlQueries API v2 operations |

## Technical summary

Add a SqlQueries namespace CLI exposing exactly 5 public `foundry_sdk.v2.sql_queries` operations through the single `SqlQuery` client path. The CLI uses the SDK's public nested client and excludes preview and internal parameters.

Every command supports the shared `--timeout`, `--format`, and `--pretty` options. JSON-shaped inputs are parsed and validated locally before the client is created. Optional SDK arguments are omitted when the user does not provide them. The client factory and `invocation_scope` use `include_attribution=False`; this namespace must not add attribution configuration (outside FR-ATTR-4 scope).

## Evidence and governing references

This design follows:

- SRS-001 FR-ACL, FR-ERR, FR-OUT, FR-PAG, FR-TRACE, FR-ASYNC, FR-DL, and the privacy requirements;
- SAD-001 namespace packaging and stateless CLI structure (EPIC-006, DEV-STORY-015 entry);
- DESIGN-005 tracing, retry, binary-download, and common-component integration contracts;
- DESIGN-010 patterns for bounded streamed downloads;
- DESIGN-011 patterns for an immutable operation catalog, exact nested SDK dispatch, packaged policy, and SDK-native error handling;
- DESIGN-012 patterns for JSON argument validation and output contracts;
- DESIGN-013 patterns for streamed byte-result handling via `BinaryDownloadHandler`;
- ADR-001 exit codes, ADR-002 timeouts, ADR-004 format selection, ADR-005 logging, ADR-006 configuration search, and ADR-007 read-only precedence;
- the canonical environment-variable reference, which defines operation enablement and read-only overrides (namespace `sql_queries`, 5 rows);
- the canonical metadata allow-list, which blocks 4 of the 5 operations in tier 3;
- vendored SDK sources under `foundry_sdk/v2/sql_queries/` (`_client.py` and `sql_query.py`).

## Operation catalog

CLI names use kebab-case. Catalog keys and ACL paths use snake_case. `OP_SPECS` contains exactly 5 unique entries.

| # | CLI command | SDK dispatch | Required input | Optional input | HTTP and result |
| ---: | --- | --- | --- | --- | --- |
| 1 | `query cancel` | `client.sql_queries.SqlQuery.cancel` | `sql_query_id` | — | `POST /v2/sqlQueries/{sqlQueryId}/cancel`; None |
| 2 | `query execute` | `client.sql_queries.SqlQuery.execute` | `--query` | `--fallback-branch-ids-json` | `POST /v2/sqlQueries/execute`; `QueryStatus` |
| 3 | `query execute-ontology` | `client.sql_queries.SqlQuery.execute_ontology` | `--query` | `--dry-run`, `--parameters-json`, `--row-limit` | `POST /v2/sqlQueries/executeOntology`; Arrow bytes |
| 4 | `query get-results` | `client.sql_queries.SqlQuery.get_results` | `sql_query_id` | `--output` | `GET /v2/sqlQueries/{sqlQueryId}/getResults`; Arrow bytes (`ARROW_TABLE` response mode) |
| 5 | `query get-status` | `client.sql_queries.SqlQuery.get_status` | `sql_query_id` | — | `GET /v2/sqlQueries/{sqlQueryId}/getStatus`; `QueryStatus` |

The SqlQueries namespace has a single `SqlQuery` resource client with no nested sub-clients; all 5 operations route directly through `client.sql_queries.SqlQuery`. `preview` parameters are excluded.

### Paging contract

No operation in the SqlQueries namespace returns a `ResourceIterator` or exposes a server cursor. `PaginationHelper` and `--page-size`/`--page-token`/`--all`/`--max-pages` flags are not required.

### Arrow byte results

Two operations return Arrow data as `bytes`: `query execute-ontology` (synchronous Arrow result) and `query get-results` (long-polling `ARROW_TABLE` response mode, server timeout up to 1 minute). Both acquire a streaming SDK response where available, pass it to `BinaryDownloadHandler` before opening the destination, write atomically to `.foundry-data/downloads/`, emit the standard metadata envelope on stdout, and close the response on success or failure. Access control runs before any client construction or filesystem effect.

## Access and runtime policy

The write set is `sql_query.cancel`, `sql_query.execute`, and `sql_query.execute_ontology` (3 operations). All three verbs (`cancel`, `execute`) are already in the shared `AccessControlGuard` write-verb set; `execute_ontology` inherits the `execute` verb classification. `sql_query.get_results` and `sql_query.get_status` are semantic reads despite `get_results` using a GET with byte payload. Read-only mode blocks the complete write set unless a canonical override permits it.

Metadata-only policy is fail closed. It permits exactly 1 operation (`sql_query.get_status`) and blocks the remaining 4 (cancel, execute, execute_ontology, get_results), matching the canonical allow-list. Namespace and exact-operation controls are evaluated before the client is constructed and before any output file is touched.

Use SDK-native B3 tracing through `invocation_scope` and restore context after success and failure. Retry only the ADR-approved transient conditions and disclose at-least-once behavior because retrying `execute`, `execute_ontology`, or `cancel` can duplicate work or cost. `get_results` is safe to retry while the query is still running (server long-poll).

## Component breakdown

- `src/foundry_cli/sql_queries/` — command catalog, parser, dispatch, JSON validators, download integration, packaged metadata-only policy.
- Claude skill and launcher for `foundry-sql-queries`.
- Focused unit and integration test modules.
- `pyproject.toml` console entry point, package data, and quality-tool scope.

## Estimates and sprint fit

| Sub-task | Assignee | Estimated hours |
| --- | --- | --- |
| DESIGN-015 | tech-lead | 6 |
| DEV-015 | python-developer | 16 |
| UNITTEST-015 | python-developer | 12 |
| CODEREVIEW-015 | tech-lead | 6 |
| TESTCASE-015 | qa-engineer | 8 |
| TESTEXEC-015 | qa-engineer | 8 |
| DEVOPS-015 | devops-engineer | 3 |
| **Total** | | **59** |

The story fits within one sprint (the 5-operation catalog is smaller than the 20-operation orchestration story, and the 59h budget is consistent with the established grooming norm). No split into additional stories is required.

## Risks

Duplicate billable or mutating effects under at-least-once retries (execute, execute_ontology, cancel); large Arrow result downloads bounded by `FOUNDRY_AGENTIC_CLI_MAX_DOWNLOAD_BYTES`; `get_results` long-poll interaction with the per-call timeout (ADR-002); SDK schema drift; packaged-policy drift; and shared ACL classification changes.
