# DESIGN-020 - Foundry Data Health CLI

| Field | Value |
| --- | --- |
| Story | DEV-STORY-020 |
| Status | Completed; ready for implementation |
| Date | 2026-08-10 |
| Scope | `foundry-data-health` CLI and Claude skill, 6 Data Health API v2 operations |

## Technical summary

Add a Data Health namespace CLI exposing exactly 6 public `foundry_sdk.v2.data_health` operations across the `Check` client and its nested `CheckReport` client. The CLI uses the SDK's public nested clients and excludes preview and internal parameters.

Every command supports the shared `--timeout`, `--format`, and `--pretty` options. JSON-shaped inputs are parsed and validated locally before the client is created. Optional SDK arguments are omitted when the user does not provide them. The client factory and `invocation_scope` use `include_attribution=False`; this namespace is outside FR-ATTR-4 scope and must not add attribution configuration.

> **Operation count note:** The story title and SAD-001 reference "4 operations". The vendored SDK (v1.102.0) exposes exactly **6** public operations (`Check` 4: create, delete, get, replace; `CheckReport` 2: get, get_latest). The canonical environment-variable reference and the metadata allow-list are concordant at 6 rows each. The count is corrected here (same precedent as DEV-STORY-016 streams 17 to 15 and DEV-STORY-017 connectivity 15 to 20).

## Evidence and governing references

This design follows:

- SRS-001 FR-ACL, FR-TRACE, FR-ASYNC, FR-OUT, FR-ERR, and the privacy requirements;
- SAD-001 namespace packaging and stateless CLI structure (EPIC-007, DEV-STORY-020 entry);
- DESIGN-005 tracing, retry, and common-component integration contracts;
- DESIGN-011 patterns for an immutable operation catalog, exact nested SDK dispatch, packaged policy, and SDK-native error handling;
- DESIGN-012 patterns for JSON argument validation and output contracts;
- DESIGN-017 patterns for `replace`-class write classification;
- ADR-001 exit codes, ADR-002 timeouts, ADR-004 format selection, ADR-005 logging, ADR-006 configuration search, and ADR-007 read-only precedence;
- the canonical environment-variable reference, which defines operation enablement and read-only overrides (namespace `data_health`, 6 rows);
- the canonical metadata allow-list, which blocks 3 of the 6 operations in tier 3;
- vendored SDK sources under `foundry_sdk/v2/data_health/` (`_client.py`, `check.py`, `check_report.py`).

## Operation catalog

CLI names use kebab-case. Catalog keys and ACL paths use snake_case. `OP_SPECS` contains exactly 6 unique entries.

| # | CLI command | SDK dispatch | Required input | Optional input | HTTP and result |
| ---: | --- | --- | --- | --- | --- |
| 1 | `check create` | `client.data_health.Check.create` | `--config-json` | `--intent` | `POST /v2/dataHealth/checks`; `Check` |
| 2 | `check delete` | `client.data_health.Check.delete` | `check_rid` | — | `DELETE /v2/dataHealth/checks/{checkRid}`; None |
| 3 | `check get` | `client.data_health.Check.get` | `check_rid` | — | `GET /v2/dataHealth/checks/{checkRid}`; `Check` |
| 4 | `check replace` | `client.data_health.Check.replace` | `check_rid`, `--config-json` | `--intent` | `PUT /v2/dataHealth/checks/{checkRid}`; `Check` |
| 5 | `check-report get` | `client.data_health.Check.CheckReport.get` | `check_rid`, `check_report_rid` | — | `GET /v2/dataHealth/checks/{checkRid}/checkReports/{checkReportRid}`; `CheckReport` |
| 6 | `check-report get-latest` | `client.data_health.Check.CheckReport.get_latest` | `check_rid` | `--limit` | `GET /v2/dataHealth/checks/{checkRid}/checkReports/getLatest`; `GetLatestCheckReportsResponse` |

The Data Health namespace routes through `client.data_health.Check`, with `check_report` operations dispatched through the nested `Check.CheckReport` accessor. `preview` parameters are excluded. The `--config-json` input for `create`/`replace` is the `CheckConfig` discriminated union (`type` discriminator across all check config kinds); `--intent` is an optional string note.

### Paging contract

No operation returns a `ResourceIterator` or a server cursor. `check_report get_latest` takes an integer `--limit` (default 10, maximum 100) that bounds a single response; it is not a cursor and must not route through `PaginationHelper`. Pagination flags are not required.

### Access and runtime policy

The write set is `check.create`, `check.delete`, and `check.replace` (3 operations). The shared `AccessControlGuard` write-verb set already classifies `create` and `delete`; `replace` inherits the replace-class write classification (same as `file_import.replace`/`table_import.replace` in the connectivity namespace). `check.get`, `check_report.get`, and `check_report.get_latest` are semantic reads. Read-only mode blocks the complete write set unless a canonical override permits it.

Metadata-only policy is fail closed. It permits exactly 3 operations (`check.get`, `check_report.get`, `check_report.get_latest`) and blocks the remaining 3 (`check.create`, `check.delete`, `check.replace`), matching the canonical allow-list. Namespace and exact-operation controls are evaluated before the client is constructed.

Use SDK-native B3 tracing through `invocation_scope` and restore context after success and failure. Retry only the ADR-approved transient conditions and disclose at-least-once behavior because retrying `check.create` or `check.replace` can duplicate checks or re-run validation.

## Component breakdown

- `src/foundry_cli/data_health/` — command catalog, parser, dispatch, JSON validator for `--config-json`, packaged metadata-only policy.
- Claude skill and launcher for `foundry-data-health`.
- Focused unit and integration test modules.
- `pyproject.toml` console entry point, package data, and quality-tool scope.

## Estimates and sprint fit

| Sub-task | Assignee | Estimated hours |
| --- | --- | --- |
| DESIGN-020 | tech-lead | 6 |
| DEV-020 | python-developer | 16 |
| UNITTEST-020 | python-developer | 12 |
| CODEREVIEW-020 | tech-lead | 6 |
| TESTCASE-020 | qa-engineer | 8 |
| TESTEXEC-020 | qa-engineer | 8 |
| DEVOPS-020 | devops-engineer | 3 |
| **Total** | | **59** |

The story fits within one sprint (6 operations across two nested client paths, no pagination, no binary handling). No split into additional stories is required.

## Risks

SDK schema drift on the `CheckConfig` discriminated union and `CheckReport` snapshot; `replace` type-change restriction (`ModifyingCheckTypeNotSupported`) surfaced as an SDK error; duplicate create/replace effects under at-least-once retries; packaged-policy drift; and shared ACL classification changes.
