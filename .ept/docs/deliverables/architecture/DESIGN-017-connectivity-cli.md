# DESIGN-017 - Foundry Connectivity CLI

| Field | Value |
| --- | --- |
| Story | DEV-STORY-017 |
| Status | Completed; ready for implementation |
| Date | 2026-08-10 |
| Scope | `foundry-connectivity` CLI and Claude skill, 20 Connectivity API v2 operations |

## Technical summary

Add a Connectivity namespace CLI exposing exactly 20 public `foundry_sdk.v2.connectivity` operations across the `Connection`, `FileImport`, `TableImport`, and `VirtualTable` client paths. The CLI uses the SDK's public nested clients and excludes preview and internal parameters.

Every command supports the shared `--timeout`, `--format`, and `--pretty` options. JSON-shaped inputs are parsed and validated locally before the client is created. Optional SDK arguments are omitted when the user does not provide them. The client factory and `invocation_scope` use `include_attribution=False`; this namespace is outside FR-ATTR-4 scope and must not add attribution configuration.

> **Operation count note:** The story title and SAD-001 reference "15 operations". The vendored SDK (v1.102.0) exposes exactly **20** public operations across `Connection` (7), `FileImport` (6), `TableImport` (6), and `VirtualTable` (1). The canonical environment-variable reference and the metadata allow-list are concordant at 20 rows each. This design implements the actual SDK surface; the stale "15" count is corrected here and in the story comments.

## Evidence and governing references

This design follows:

- SRS-001 FR-ACL, FR-ERR, FR-OUT, FR-PAG, FR-TRACE, FR-ASYNC, and the privacy requirements;
- SAD-001 namespace packaging and stateless CLI structure (EPIC-006, DEV-STORY-017 entry);
- DESIGN-005 tracing, retry, and common-component integration contracts;
- DESIGN-011 patterns for an immutable operation catalog, exact nested SDK dispatch, packaged policy, and SDK-native error handling;
- DESIGN-012 patterns for JSON argument validation and output contracts;
- DESIGN-016 patterns for operation-count correction, access policy, and risk disclosure;
- ADR-001 exit codes, ADR-002 timeouts, ADR-004 format selection, ADR-005 logging, ADR-006 configuration search, and ADR-007 read-only precedence;
- the canonical environment-variable reference, which defines operation enablement and read-only overrides (namespace `connectivity`, 20 rows);
- the canonical metadata allow-list, which blocks 13 of the 20 operations in tier 3;
- vendored SDK sources under `foundry_sdk/v2/connectivity/` (`_client.py`, `connection.py`, `file_import.py`, `table_import.py`, `virtual_table.py`).

## Operation catalog

CLI names use kebab-case. Catalog keys and ACL paths use snake_case. `OP_SPECS` contains exactly 20 unique entries.

| # | CLI command | SDK dispatch | Required input | Optional input | HTTP and result |
| ---: | --- | --- | --- | --- | --- |
| 1 | `connection create` | `client.connectivity.Connection.create` | `--configuration-json`, `--display-name`, `--parent-folder-rid`, `--worker-json` | — | `POST /v2/connectivity/connections`; `Connection` |
| 2 | `connection get` | `client.connectivity.Connection.get` | `connection_rid` | — | `GET /v2/connectivity/connections/{connectionRid}`; `Connection` |
| 3 | `connection get-configuration` | `client.connectivity.Connection.get_configuration` | `connection_rid` | — | `GET /v2/connectivity/connections/{connectionRid}/getConfiguration`; `ConnectionConfiguration` |
| 4 | `connection get-configuration-batch` | `client.connectivity.Connection.get_configuration_batch` | `--body-json` | — | `POST /v2/connectivity/connections/getConfigurationBatch`; `GetConfigurationConnectionsBatchResponse` |
| 5 | `connection update-export-settings` | `client.connectivity.Connection.update_export_settings` | `connection_rid`, `--export-settings-json` | — | `POST /v2/connectivity/connections/{connectionRid}/updateExportSettings`; None |
| 6 | `connection update-secrets` | `client.connectivity.Connection.update_secrets` | `connection_rid`, `--secrets-json` | — | `POST /v2/connectivity/connections/{connectionRid}/updateSecrets`; None |
| 7 | `connection upload-custom-jdbc-drivers` | `client.connectivity.Connection.upload_custom_jdbc_drivers` | `connection_rid`, `--file`, `--file-name` | — | `POST /v2/connectivity/connections/{connectionRid}/uploadCustomJdbcDrivers`; `Connection` |
| 8 | `file-import create` | `client.connectivity.Connection.FileImport.create` | `connection_rid`, `--dataset-rid`, `--display-name`, `--filters-json`, `--import-mode` | `--branch-name`, `--subfolder` | `POST /v2/connectivity/connections/{connectionRid}/fileImports`; `FileImport` |
| 9 | `file-import delete` | `client.connectivity.Connection.FileImport.delete` | `connection_rid`, `file_import_rid` | — | `DELETE /v2/connectivity/connections/{connectionRid}/fileImports/{fileImportRid}`; None |
| 10 | `file-import execute` | `client.connectivity.Connection.FileImport.execute` | `connection_rid`, `file_import_rid` | — | `POST /v2/connectivity/connections/{connectionRid}/fileImports/{fileImportRid}/execute`; `BuildRid` |
| 11 | `file-import get` | `client.connectivity.Connection.FileImport.get` | `connection_rid`, `file_import_rid` | — | `GET /v2/connectivity/connections/{connectionRid}/fileImports/{fileImportRid}`; `FileImport` |
| 12 | `file-import list` | `client.connectivity.Connection.FileImport.list` | `connection_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages` | `GET /v2/connectivity/connections/{connectionRid}/fileImports`; `ResourceIterator[FileImport]` |
| 13 | `file-import replace` | `client.connectivity.Connection.FileImport.replace` | `connection_rid`, `file_import_rid`, `--display-name`, `--filters-json`, `--import-mode` | `--subfolder` | `PUT /v2/connectivity/connections/{connectionRid}/fileImports/{fileImportRid}`; `FileImport` |
| 14 | `table-import create` | `client.connectivity.Connection.TableImport.create` | `connection_rid`, `--config-json`, `--dataset-rid`, `--display-name`, `--import-mode` | `--allow-schema-changes`, `--branch-name` | `POST /v2/connectivity/connections/{connectionRid}/tableImports`; `TableImport` |
| 15 | `table-import delete` | `client.connectivity.Connection.TableImport.delete` | `connection_rid`, `table_import_rid` | — | `DELETE /v2/connectivity/connections/{connectionRid}/tableImports/{tableImportRid}`; None |
| 16 | `table-import execute` | `client.connectivity.Connection.TableImport.execute` | `connection_rid`, `table_import_rid` | — | `POST /v2/connectivity/connections/{connectionRid}/tableImports/{tableImportRid}/execute`; `BuildRid` |
| 17 | `table-import get` | `client.connectivity.Connection.TableImport.get` | `connection_rid`, `table_import_rid` | — | `GET /v2/connectivity/connections/{connectionRid}/tableImports/{tableImportRid}`; `TableImport` |
| 18 | `table-import list` | `client.connectivity.Connection.TableImport.list` | `connection_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages` | `GET /v2/connectivity/connections/{connectionRid}/tableImports`; `ResourceIterator[TableImport]` |
| 19 | `table-import replace` | `client.connectivity.Connection.TableImport.replace` | `connection_rid`, `table_import_rid`, `--config-json`, `--display-name`, `--import-mode` | `--allow-schema-changes` | `PUT /v2/connectivity/connections/{connectionRid}/tableImports/{tableImportRid}`; `TableImport` |
| 20 | `virtual-table create` | `client.connectivity.Connection.VirtualTable.create` | `connection_rid`, `--config-json`, `--name`, `--parent-rid` | `--markings-json` | `POST /v2/connectivity/connections/{connectionRid}/virtualTables`; `VirtualTable` |

### Paging contract

`file-import list` and `table-import list` return `core.ResourceIterator` and accept `page_size`/`page_token`. The CLI exposes `--page-size`, `--page-token`, `--all`, and `--max-pages` via `PaginationHelper`, emitting the next-page token to stderr as compact JSON per ADR-005. The remaining 18 operations are single-call.

### Binary handling

No operation returns a streamed file download, so `BinaryDownloadHandler` is not required for reads. `connection upload-custom-jdbc-drivers` uploads local file content as a `bytes` body; the CLI reads the file from `--file` after the ACL decision and before client construction, bounded by the standard upload size limit. `--file-name` must end with `.jar`.

### Secrets handling

`connection update-secrets` and `connection update-export-settings` transmit secrets over TLS and the server decrypts them in memory. The CLI never echoes secret values back to stdout or stderr; inputs arrive only via `--secrets-json`/`--export-settings-json` and are not logged.

## Access and runtime policy

The write set is `connection.create`, `connection.update_export_settings`, `connection.update_secrets`, `connection.upload_custom_jdbc_drivers`, `file_import.create`, `file_import.delete`, `file_import.execute`, `file_import.replace`, `table_import.create`, `table_import.delete`, `table_import.execute`, `table_import.replace`, and `virtual_table.create` (13 operations). Read-only mode blocks the complete write set unless a canonical override permits it. `connection.get_configuration_batch` is a POST request but a semantic read (returns configuration data, mutates nothing) and is classified as a read.

Metadata-only policy is fail closed. It permits exactly 7 operations (`connection.get`, `connection.get_configuration`, `connection.get_configuration_batch`, `file_import.get`, `file_import.list`, `table_import.get`, `table_import.list`) and blocks the remaining 13 (all mutations and all binary uploads), matching the canonical allow-list. Namespace and exact-operation controls are evaluated before the client is constructed.

Use SDK-native B3 tracing through `invocation_scope` and restore context after success and failure. Retry only the ADR-approved transient conditions and disclose at-least-once behavior because retrying create, execute, replace, update, delete, or upload can duplicate syncs, re-run builds, or cost.

## Component breakdown

- `src/foundry_cli/connectivity/` — command catalog, parser, dispatch, JSON validators, pagination integration, packaged metadata-only policy.
- Claude skill and launcher for `foundry-connectivity`.
- Focused unit and integration test modules.
- `pyproject.toml` console entry point, package data, and quality-tool scope.

## Estimates and sprint fit

| Sub-task | Assignee | Estimated hours |
| --- | --- | --- |
| DESIGN-017 | tech-lead | 6 |
| DEV-017 | python-developer | 16 |
| UNITTEST-017 | python-developer | 12 |
| CODEREVIEW-017 | tech-lead | 6 |
| TESTCASE-017 | qa-engineer | 8 |
| TESTEXEC-017 | qa-engineer | 8 |
| DEVOPS-017 | devops-engineer | 3 |
| **Total** | | **59** |

The story fits within one sprint (20 operations; 4 client paths with two paged commands and a bounded binary upload). No split into additional stories is required.

## Risks

Duplicate syncs or builds under at-least-once retries (create, execute, replace, delete); secret exposure if inputs are logged (must be suppressed); JDBC driver upload size limits; pagination volume on `file_import.list`/`table_import.list`; the stale "15-operation" count in the story title and SAD-001 (corrected to 20); packaged-policy drift; and shared ACL classification changes.
