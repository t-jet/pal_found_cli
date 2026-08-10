# TESTCASE-017 - Foundry Connectivity CLI QA test cases

## Scope

These cases cover DEV-STORY-017 and the complete approved surface of `foundry-connectivity`: 20 `foundry_sdk.v2.connectivity` operations across the Connection (7), FileImport (6), TableImport (6), and VirtualTable (1) client paths. They verify the exact catalog and parser, nested SDK routing and dispatch, JSON argument validation, the two cursor-paged list commands through `PaginationHelper` (`file_import.list`, `table_import.list`), the bounded JDBC-driver binary upload, the 13-operation write set, the packaged 7-permitted/13-blocked metadata-only policy, B3 tracing with `include_attribution=False`, retry and error behavior, output and log contracts, privacy (secrets never echoed), packaging, and regression gates.

> **Operation count note:** The story title and SAD-001 reference "15 operations". The vendored SDK (v1.102.0) exposes exactly **20** public operations across `Connection` (7), `FileImport` (6), `TableImport` (6), and `VirtualTable` (1), and DESIGN-017, the canonical environment-variable reference, and the metadata allow-list are concordant at 20 rows. This suite designs cases for the actual 20-operation surface.

Routine acceptance uses mocked async SDK transport and real installed SDK exception classes. Live credentials and live Foundry access are not required. An approved non-production smoke is optional and cannot replace the mandatory mocked evidence.

## Source baseline

- [DESIGN-017](../architecture/DESIGN-017-connectivity-cli.md), completed and closed for DEV-STORY-017.
- [DESIGN-005](../architecture/DESIGN-005-common-components.md), covering bounded streaming and SDK-native B3 tracing.
- [DESIGN-011](../architecture/DESIGN-011-aip-agents-cli.md), [DESIGN-012](../architecture/DESIGN-012-language-models-cli.md), [DESIGN-013](../architecture/DESIGN-013-models-cli.md), [DESIGN-014](../architecture/DESIGN-014-orchestration-cli.md), [DESIGN-016](../architecture/DESIGN-016-streams-cli.md) — the sibling namespace patterns this story mirrors (nested dispatch, metadata-only policy, cursor pagination).
- [ADR-001](../architecture/adr/ADR-001-exit-code-taxonomy.md), [ADR-002](../architecture/adr/ADR-002-call-timeout-defaults.md), [ADR-004](../architecture/adr/ADR-004-format-auto-algorithm.md), [ADR-005](../architecture/adr/ADR-005-log-format.md), [ADR-006](../architecture/adr/ADR-006-env-file-search-path.md), [ADR-007](../architecture/adr/ADR-007-operation-level-readonly.md).
- The canonical environment-variable reference and metadata allow-list (namespace `connectivity`, 20 rows; `connection.get`, `connection.get_configuration`, `connection.get_configuration_batch`, `file_import.get`, `file_import.list`, `table_import.get`, `table_import.list` PERMITTED, the other 13 BLOCKED in tier 3).
- Vendored SDK sources under `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/connectivity/` — the real `ConnectionClient`, `FileImportClient`, `TableImportClient`, and `VirtualTableClient` methods, request paths, and result types.
- DEV-STORY-017 ticket body, `release_notes`, and technical scope comment (authoritative 20-operation catalog, corrected from the stale 15).
- Implementation verified at HEAD `62c269f`: `src/foundry_cli/connectivity/`, `.claude/skills/foundry-connectivity/`, and `pyproject.toml` (entry point `foundry-connectivity`).

## Preconditions and shared fixtures

- Python 3.11 and 3.12 environments contain the project, development dependencies, and pinned `foundry-sdk`.
- Use a nested async SDK fake rooted at `client.connectivity` with exactly four public sub-clients: `Connection` (create, get, get_configuration, get_configuration_batch, update_export_settings, update_secrets, upload_custom_jdbc_drivers), `Connection.FileImport` (create, delete, execute, get, list, replace), `Connection.TableImport` (create, delete, execute, get, list, replace), and `Connection.VirtualTable` (create). A wrong, flattened, raw, or streaming route must fail the fixture. No other sub-client may be reachable from any catalog dispatch.
- The two list commands use `client.connectivity.Connection.FileImport.list` / `Connection.TableImport.list` through `with_raw_response` and `PaginationHelper`; page fakes return `SimpleNamespace(list=..., next_page_token=...)` so empty pages decode safely. No `PaginationHelper` may be invoked for any non-paginated command.
- `upload_custom_jdbc_drivers` fakes accept the raw `bytes` body and record it; the bounded file read (`_read_file_bounded`, 16 MiB cap) happens after the ACL decision and before client construction. `--file-name` must end with `.jar`.
- Use real installed SDK model validators for nested invalid-input checks and real `foundry_sdk._errors` classes for error taxonomy checks. Mock network transport; no service call is permitted.
- Set retry delay to zero, disable jitter, and use two retries unless a case states otherwise. Capture attempt number, timeout, attribution, and B3 values.
- Capture stdout, stderr, logs, SDK arguments, context variables, client/network constructors, and filesystem changes independently. Do not retain credential, token, JSON-body, or response sentinel values.
- The two cursor-paged commands emit pagination metadata (`pages_fetched`, `total_items`, `next_page_token`, `page_size`) as compact JSON to stderr via `PaginationHelper.emit_metadata()` per ADR-005. No download root or `BinaryDownloadHandler` is required by any case.
- Packaging cases build a clean local archive with dependency resolution disabled, install with `--no-deps`, and run from an arbitrary empty working directory without `PYTHONPATH`.
- Any optional live smoke uses an approved non-production Foundry tenant, synthetic connection/import resources, least-privilege credentials, and a cleanup plan. Credentials must never enter retained evidence.
- TESTEXEC records the commit, OS, Python and SDK versions, environment type, exact command, expected and actual stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, evidence reference, and PASS/FAIL/BLOCKED status for every case.

## Test data

| Name | Fixture |
| --- | --- |
| Connection RID | `ri.connection.main.test-conn` |
| Parent folder RID | `ri.compass.main.folder.test` |
| File import RID | `ri.connectivity.main.file-import.test` |
| Table import RID | `ri.connectivity.main.table-import.test` |
| Display name | `qa-conn-001` |
| Connection configuration JSON | `{"type": "s3", "bucket": "qa-bucket", "region": "us-east-1"}` |
| Worker JSON | `{"type": "ecs", "cpu": 2, "memory": 4096}` |
| Export settings JSON | `{"enabled": true, "destination": "ri.dataset.main.test"}` |
| Secrets JSON | `{"value": "sentinel-secret-017"}` |
| Filters JSON | `[{"type": "prefix", "value": "inbox/"}]` |
| Table import config JSON | `{"type": "postgres", "table": "qa_table"}` |
| Markings JSON | `["ri.marke.system.private"]` |
| JDBC driver file | `driver.jar` (bytes `jar-contents-017`) |
| JDBC driver file-name variants | `driver.jar` (valid), `driver.txt` (invalid extension), missing path, a file above the 16 MiB upload cap |
| List page fakes | empty page; one page; two pages with `next_page_token`; exhausted page token |
| Pagination flags | `--page-size 50`, `--page-token <tok>`, `--all`, `--max-pages 3`, `--max-pages 0` |
| Timeout boundaries | `1`, `30` (default), `3600`; invalid `0`, `3601`, non-integer text |
| Secret sentinels | `sentinel-secret-017`, `sentinel-token-secret`, `sentinel-body-secret`, `sentinel-response-secret`, `sentinel-attribution-rid` |

## Command and route inventory

Every inventory row is exercised by CNT-TC-001 through CNT-TC-003. Unless a case states otherwise, success writes one formatted result to stdout, writes no application data to stderr, exits `0`, and leaves no command-specific file.

| CLI command | Exact public SDK route and method | Required input | Optional input |
| --- | --- | --- | --- |
| `connection create --configuration-json ... --display-name ... --parent-folder-rid ... --worker-json ...` | `client.connectivity.Connection.create` | `--configuration-json`, `--display-name`, `--parent-folder-rid`, `--worker-json` | shared options |
| `connection get CONNECTION_RID` | `client.connectivity.Connection.get` | `connection_rid` | shared options |
| `connection get-configuration CONNECTION_RID` | `client.connectivity.Connection.get_configuration` | `connection_rid` | shared options |
| `connection get-configuration-batch --body-json ...` | `client.connectivity.Connection.get_configuration_batch` | `--body-json` | shared options |
| `connection update-export-settings CONNECTION_RID --export-settings-json ...` | `client.connectivity.Connection.update_export_settings` | `connection_rid`, `--export-settings-json` | shared options |
| `connection update-secrets CONNECTION_RID --secrets-json ...` | `client.connectivity.Connection.update_secrets` | `connection_rid`, `--secrets-json` | shared options |
| `connection upload-custom-jdbc-drivers CONNECTION_RID --file ... --file-name ...` | `client.connectivity.Connection.upload_custom_jdbc_drivers` | `connection_rid`, `--file`, `--file-name` (must end `.jar`) | shared options |
| `file-import create CONNECTION_RID --dataset-rid ... --display-name ... --filters-json ... --import-mode ...` | `client.connectivity.Connection.FileImport.create` | `connection_rid`, `--dataset-rid`, `--display-name`, `--filters-json`, `--import-mode` | `--branch-name`, `--subfolder`, shared options |
| `file-import delete CONNECTION_RID FILE_IMPORT_RID` | `client.connectivity.Connection.FileImport.delete` | `connection_rid`, `file_import_rid` | shared options |
| `file-import execute CONNECTION_RID FILE_IMPORT_RID` | `client.connectivity.Connection.FileImport.execute` | `connection_rid`, `file_import_rid` | shared options |
| `file-import get CONNECTION_RID FILE_IMPORT_RID` | `client.connectivity.Connection.FileImport.get` | `connection_rid`, `file_import_rid` | shared options |
| `file-import list CONNECTION_RID` | `client.connectivity.Connection.FileImport.list` | `connection_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages`, shared options |
| `file-import replace CONNECTION_RID FILE_IMPORT_RID --display-name ... --filters-json ... --import-mode ...` | `client.connectivity.Connection.FileImport.replace` | `connection_rid`, `file_import_rid`, `--display-name`, `--filters-json`, `--import-mode` | `--subfolder`, shared options |
| `table-import create CONNECTION_RID --config-json ... --dataset-rid ... --display-name ... --import-mode ...` | `client.connectivity.Connection.TableImport.create` | `connection_rid`, `--config-json`, `--dataset-rid`, `--display-name`, `--import-mode` | `--allow-schema-changes`, `--branch-name`, shared options |
| `table-import delete CONNECTION_RID TABLE_IMPORT_RID` | `client.connectivity.Connection.TableImport.delete` | `connection_rid`, `table_import_rid` | shared options |
| `table-import execute CONNECTION_RID TABLE_IMPORT_RID` | `client.connectivity.Connection.TableImport.execute` | `connection_rid`, `table_import_rid` | shared options |
| `table-import get CONNECTION_RID TABLE_IMPORT_RID` | `client.connectivity.Connection.TableImport.get` | `connection_rid`, `table_import_rid` | shared options |
| `table-import list CONNECTION_RID` | `client.connectivity.Connection.TableImport.list` | `connection_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages`, shared options |
| `table-import replace CONNECTION_RID TABLE_IMPORT_RID --config-json ... --display-name ... --import-mode ...` | `client.connectivity.Connection.TableImport.replace` | `connection_rid`, `table_import_rid`, `--config-json`, `--display-name`, `--import-mode` | `--allow-schema-changes`, shared options |
| `virtual-table create CONNECTION_RID --config-json ... --name ... --parent-rid ...` | `client.connectivity.Connection.VirtualTable.create` | `connection_rid`, `--config-json`, `--name`, `--parent-rid` | `--markings-json`, shared options |

No command may receive `attribution`, `preview`, `_sdk_internal`, an absent optional set to `None`, or any unsupported paging, stream, raw-response, or file flag. Pagination flags may exist only on `file-import list` and `table-import list`.

## Test cases

### CNT-TC-001 - Catalog, parser, help, and exact 20 surface

- Type: positive, structural, negative parser.
- Given the installed module and launcher, when the catalog and parser are inspected, then exactly 20 unique SDK specifications exist (Connection 7, FileImport 6, TableImport 6, VirtualTable 1), every inventory command parses, and pagination flags exist only on the two list commands.
- Command/function: `OP_SPECS`, `build_parser()`, `_spec_for()`, `_get_client()`, root/resource/operation `--help`, `main()` with missing resource/operation, unknown flags, missing required positionals/options, invalid choices/types.
- Prerequisites/fixtures: guarded config, client, network, and filesystem constructors.
- Steps: count `OP_SPECS`; assert the two list commands expose `--page-size`/`--page-token`/`--all`/`--max-pages` and all 18 others expose none; parse all 20 inventory commands; run all help surfaces; run every incomplete or malformed form.
- Expected stdout/stderr/exit: help on stdout and exit `0`; catalog count exactly `20`; parser errors as one JSON envelope on stdout with `exit_code: 1`, empty diagnostic stderr, no traceback, no config/client/network/filesystem call.
- Cleanup: restore `sys.argv` and capture streams.
- Evidence mapping: DESIGN-017 catalog; story scope comment; `test_catalog_contains_exact_20_operations`, `test_catalog_marks_exactly_two_paginated_operations`, `test_parser_accepts_every_declared_argument`, `test_parser_rejects_unknown_operation` (tests/test_foundry_connectivity_cli.py); verified live at HEAD `62c269f` (probe: `CONN_OP_SPECS: 20`, `{'connection': 7, 'file_import': 6, 'table_import': 6, 'virtual_table': 1}`, `PAGINATED_OPS` exactly the two list pairs, `--page-size`/`--all` present on `file-import list` and absent on `connection get`).

### CNT-TC-002 - Nested SDK routing across the four client paths

- Type: positive, structural, route identity.
- Given distinct fakes for `Connection`, `Connection.FileImport`, `Connection.TableImport`, and `Connection.VirtualTable`, when every inventory command runs, then each resolves the exact nested object and never a flattened or sibling route.
- Command/function: `_get_client()` and each dispatch path.
- Prerequisites/fixtures: fakes whose sibling routes fail on access.
- Steps: run one command per client path; assert the resolved resource object identity; assert no flattened `connectivity.*` method call.
- Expected stdout/stderr/exit: success results on stdout once, exit `0`, no unexpected stderr; no flattened `connectivity.*` method call.
- Cleanup: reset fakes and captures.
- Evidence mapping: DESIGN-017 nested dispatch; story AC 1; `test_catalog_contains_exact_20_operations` (all twenty resolve through the four nested client paths) plus the dispatch tests `test_connection_create_dispatches_exact_arguments`, `test_file_import_create_dispatches_with_filters_json`, `test_table_import_replace_omits_absent_optional`, `test_virtual_table_create_dispatches_with_markings`.

### CNT-TC-003 - Required inputs forwarded and absent optionals omitted

- Type: positive, structural.
- Given each inventory command, when dispatch runs, then required positionals/options reach the SDK call and every absent optional is omitted (never `None`).
- Command/function: all 20 dispatches.
- Prerequisites/fixtures: recording SDK fakes.
- Steps: run each command with only required inputs; run `file-import create`/`replace` with and without `--branch-name`/`--subfolder`; run `table-import create`/`replace` with and without `--allow-schema-changes`/`--branch-name`; run `virtual-table create` with and without `--markings-json`.
- Expected stdout/stderr/exit: SDK call arguments contain exactly the documented keys; success exits `0`; absent optionals absent from kwargs; `--allow-schema-changes` maps to a boolean flag value.
- Cleanup: clear fake call records.
- Evidence mapping: DESIGN-017 operation catalog; story AC 1; `test_connection_create_dispatches_exact_arguments`, `test_file_import_create_dispatches_with_filters_json`, `test_table_import_replace_omits_absent_optional`, `test_virtual_table_create_dispatches_with_markings`.

### CNT-TC-004 - JSON argument validation before client creation

- Type: positive, negative, boundary.
- Given every structured flag (`--configuration-json`, `--worker-json`, `--export-settings-json`, `--secrets-json`, `--filters-json`, `--config-json`, `--markings-json`, `--body-json`), when validation runs, then valid JSON with the documented top-level shape reaches the SDK and invalid or mis-shaped JSON exits `1` before client or network work.
- Command/function: JSON validators, `main()`.
- Prerequisites/fixtures: guarded factory/network constructors; real SDK validators for nested checks.
- Steps: supply valid payloads; supply malformed JSON text; supply valid JSON with the wrong top-level type (object vs array vs scalar); supply JSON whose nested fields violate SDK validators.
- Expected stdout/stderr/exit: valid inputs call the SDK and exit `0`; invalid inputs write one JSON user-input envelope to stdout, exit `1`, no traceback, and never echo the input payload into stdout/stderr/logs.
- Cleanup: clear captured sentinels.
- Evidence mapping: DESIGN-017 JSON validation contract; story AC 2; `test_invalid_configuration_json_rejected_before_client`, `test_filters_json_array_required_for_file_import` (valid decode and mis-shape rejection before client creation).

### CNT-TC-005 - Pagination contract: file-import list through PaginationHelper

- Type: positive, boundary, structural.
- Given a `ResourceIterator`-shaped page fake, when `file-import list` runs, then `--page-size`/`--page-token`/`--all`/`--max-pages` drive `PaginationHelper`, pages are aggregated into one array on stdout, and pagination metadata (`pages_fetched`, `total_items`, `next_page_token`, `page_size`) is emitted as compact JSON to stderr.
- Command/function: `file-import list` dispatch; `_fetch_raw_page()`, `_resolve_pagination_flags()`, `_paginate_operation()`, `PaginationHelper.paginate()` and `emit_metadata()`.
- Prerequisites/fixtures: empty page; single page with `next_page_token`; two pages; exhausted token; `HARD_MAX_BATCH_PAGES = 40` and `MAX_BATCH_PAGES` default 40 (`FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES`, default page size 100 via `FOUNDRY_AGENTIC_CLI_DEFAULT_PAGE_SIZE`).
- Steps: run without pagination flags (single page, default page size); run with `--page-size 50`; run with `--page-token` resume; run with `--all`; run with `--max-pages 3`; run with an exhausted token.
- Expected stdout/stderr/exit: success array on stdout and exit `0`; exactly the requested page bound fetched; stderr carries one metadata block per ADR-005; no metadata on non-paginated commands.
- Cleanup: clear page fakes and captures.
- Evidence mapping: DESIGN-017 paging contract; story AC 3; `test_file_import_list_uses_raw_response_and_helper`, `test_table_import_list_defaults_to_single_page` (raw-response decode and `SimpleNamespace(list=...)` empty-page guard), plus shared `PaginationHelper` tests in tests/test_pagination_helper.py.

### CNT-TC-006 - Pagination contract: table-import list and page bounds

- Type: positive, boundary, negative.
- Given the same pagination surface, when `table-import list` runs with `--all`/`--max-pages`, then the effective page batch respects `FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES` (hard cap 40) and degenerate values (`--max-pages 0`, non-positive `--page-size`) are rejected or clamped per the documented contract.
- Command/function: `table-import list` dispatch; `PaginationHelper` bound validation.
- Prerequisites/fixtures: page fakes; env `FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES` set to `3` and unset.
- Steps: run `--max-pages 1` (default); run `--max-pages 40`; run `--all` with env cap `3`; run `--max-pages 0`; run `--page-size 0`.
- Expected stdout/stderr/exit: valid bounds fetch the documented page count and exit `0` with one aggregated array; `--max-pages 0` and `--page-size 0` write one JSON user-input envelope on stdout and exit `1` before ACL/client/network work; metadata emitted to stderr.
- Cleanup: restore env and call records.
- Evidence mapping: DESIGN-017 paging contract; story AC 3; `test_table_import_list_defaults_to_single_page`, `test_catalog_marks_exactly_two_paginated_operations`, shared `PaginationHelper` bound tests in tests/test_pagination_helper.py.

### CNT-TC-007 - Bounded JDBC driver upload before client creation

- Type: positive, boundary, negative.
- Given a local `.jar` file, when `connection upload-custom-jdbc-drivers --file` runs, then the file content is read in a bounded and validated way after the ACL decision and passed as `bytes` to the SDK, with files above the 16 MiB upload cap, missing files, and non-`.jar` file names rejected before client construction.
- Command/function: `connection upload-custom-jdbc-drivers` dispatch; `_read_file_bounded()` and `_validate_jdbc_file_name()`.
- Prerequisites/fixtures: valid `driver.jar`; `driver.txt`; missing path; a file above the 16 MiB bound; guarded factory/transport.
- Steps: upload each variant; assert the SDK body bytes; attempt the oversized, missing, and non-`.jar` cases; inspect event order.
- Expected stdout/stderr/exit: valid `.jar` reaches the SDK as the exact byte content and exits `0`; oversized, missing, or non-`.jar` inputs write one JSON user-input envelope on stdout and exit `1` with no client or network call; `--file-name` without `.jar` is rejected with "file-name must end with .jar".
- Cleanup: remove temporary files.
- Evidence mapping: DESIGN-017 binary handling contract; story AC 5; `test_upload_custom_jdbc_drivers_reads_file_bounded`, `test_upload_custom_jdbc_drivers_rejects_non_jar`, `test_upload_custom_jdbc_drivers_rejects_missing_file` (tests/test_foundry_connectivity_cli.py).

### CNT-TC-008 - Secret inputs are never echoed

- Type: privacy, security, positive.
- Given secret-bearing `--secrets-json` and `--export-settings-json` inputs and secret-bearing response fixtures, when `connection update-secrets` and `connection update-export-settings` run, then secret values never appear in stdout, stderr, or logs, and the structured success/error output contains no secret sentinel.
- Command/function: `connection update-secrets`, `connection update-export-settings` dispatch; `_serialize_error()`.
- Prerequisites/fixtures: `sentinel-secret-017` embedded in inputs and mock responses; captured logs; parser error fakes.
- Steps: run both commands to success; run them with invalid JSON; scan stdout, stderr, and captured logs for the sentinel.
- Expected stdout/stderr/exit: exit `0` on success with a result that contains no secret; invalid JSON exits `1` with a user-input envelope that contains no secret; no secret appears in any stream or log.
- Cleanup: clear sentinels and captures.
- Evidence mapping: DESIGN-017 secrets handling contract; story AC 13; `test_update_secrets_never_echoes_values` (tests/test_foundry_connectivity_cli.py).

### CNT-TC-009 - Timeout boundaries and forwarding

- Type: positive, boundary, negative.
- Given CLI or configured timeouts, when execution starts, then values from 1 through 3600 seconds are accepted and the selected value reaches both retry handling and the SDK request; invalid values are rejected before ACL, scope, client, or filesystem work.
- Command/function: `_validate_timeout()`, representative commands with `--timeout`.
- Prerequisites/fixtures: values `1`, `30` (default), `3600`, CLI override `17`, configured default `42`, invalid `0`, `3601`, negative, and non-integer text.
- Steps: validate boundaries; execute with and without a CLI override; inspect retry construction and `request_timeout`; invoke each invalid value.
- Expected stdout/stderr/exit: valid requests produce one success result and exit `0`; retry and SDK receive the same chosen integer; invalid values write one JSON user-input envelope on stdout and exit `1` with no ACL/client/network call.
- Cleanup: restore config defaults and call records.
- Evidence mapping: ADR-002, DESIGN-017 invocation contract; story AC 12; `test_timeout_accepts_adr_002_bounds`, `test_invalid_timeout_returns_user_input_error` (tests/test_foundry_connectivity_cli.py).

### CNT-TC-010 - ACL precedence: global, namespace, and operation scopes

- Type: security, positive, negative.
- Given metadata-only and operation-level overrides, when ACL evaluates `CONNECTIVITY`, then permissive settings allow, blocking settings deny, and an operation override wins over the namespace setting.
- Command/function: `AccessControlGuard(cfg, "CONNECTIVITY").check()` for representative operations.
- Prerequisites/fixtures: packaged Connectivity allow-list and isolated environment variables.
- Steps: enable global metadata-only; check permitted and blocked operations; disable Connectivity metadata-only at namespace level; disable one operation explicitly; combine namespace read-only with an operation override.
- Expected stdout/stderr/exit: permitted checks return silently; blocked CLI calls write a structured ACL envelope to stdout, exit `8`, and do not create a client; the denying rule appears on stderr diagnostics; no secret appears.
- Cleanup: remove every ACL environment variable.
- Evidence mapping: DESIGN-017 access-control table; story AC 7; `test_acl_write_classification_matches_design`, `test_metadata_only_permits_exactly_7_blocks_13`, and `test_metadata_only_permits_seven_and_blocks_thirteen` (precedence exercised through the namespace runtime checks).

### CNT-TC-011 - Read-only mode blocks the 13-operation write set; semantic reads stay permitted

- Type: security, positive, negative.
- Given read-only mode enabled, when each write command runs, then `connection.create`, `connection.update_export_settings`, `connection.update_secrets`, `connection.upload_custom_jdbc_drivers`, `file_import.create`, `file_import.delete`, `file_import.execute`, `file_import.replace`, `table_import.create`, `table_import.delete`, `table_import.execute`, `table_import.replace`, and `virtual_table.create` exit `8` before client or filesystem effects, while `connection.get_configuration_batch` remains executable as a semantic read despite being a POST request.
- Command/function: `AccessControlGuard` + `main()` for each write command and `connection get-configuration-batch`.
- Prerequisites/fixtures: read-only environment; guarded factory/transport; response fakes.
- Steps: run all 13 write commands under read-only; run `connection get-configuration-batch` under read-only; inspect event order.
- Expected stdout/stderr/exit: each blocked write emits one ACL envelope and exit `8` with the denying rule on stderr; no SDK call occurs; the batch configuration read succeeds and exits `0`.
- Cleanup: clear read-only variables, captures, and records.
- Evidence mapping: DESIGN-017 read-only policy; story AC 7; `test_readonly_blocks_thirteen_write_operations`, `test_semantic_reads_permitted_under_readonly`, `test_connection_get_configuration_batch_is_semantic_read`.

### CNT-TC-012 - Metadata-only tier: exact 7 permitted / 13 blocked

- Type: security, positive, negative.
- Given metadata-only mode, when every operation is checked, then exactly the 7 documented reads (`connection.get`, `connection.get_configuration`, `connection.get_configuration_batch`, `file_import.get`, `file_import.list`, `table_import.get`, `table_import.list`) are permitted and the other 13 operations are blocked.
- Command/function: `AccessControlGuard` metadata-only evaluation over the full 20-op catalog.
- Prerequisites/fixtures: packaged Connectivity allow-list; the full catalog.
- Steps: assert the permitted set equals the 7 documented reads; assert every mutation and the JDBC driver upload is blocked.
- Expected stdout/stderr/exit: 7 permitted checks return silently; each of the 13 blocked CLI calls writes an ACL envelope and exits `8` with the denying rule on stderr; no client or file effect.
- Cleanup: clear metadata-only variables.
- Evidence mapping: DESIGN-017 metadata policy; story AC 8; `test_metadata_only_permits_exactly_7_blocks_13` and `test_metadata_only_permits_seven_and_blocks_thirteen`; verified live at HEAD `62c269f` (probe: `CONN_PERMITTED: 7` matching the allow-list exactly, `CONN_BLOCKED: 13`).

### CNT-TC-013 - Packaged metadata-only policy is fail closed and CWD independent

- Type: security, packaging, negative.
- Given the installed package with a missing or malformed packaged allow-list, when ACL runs, then it fails closed (no operation permitted) and the packaged policy resolves from an arbitrary working directory.
- Command/function: `_METADATA_ALLOWLIST_PATH`, `AccessControlGuard` from an installed wheel/editable launch.
- Prerequisites/fixtures: malformed/missing policy fixtures in an isolated environment; empty arbitrary CWD, no `PYTHONPATH`.
- Steps: probe policy path from the installed package; run a permitted-class check with malformed policy; run checks from the arbitrary CWD.
- Expected stdout/stderr/exit: malformed/missing policy blocks even previously-permitted operations (fail closed, exit `8`); packaged policy path resolves inside the installed package; valid packaged policy applies the 7/13 rule from any CWD.
- Cleanup: delete isolated environments and fixtures.
- Evidence mapping: DESIGN-017 fail-closed rule; story AC 8, 14; `test_metadata_only_permits_exactly_7_blocks_13` (parsed from the packaged allow-list); packaged-policy CWD independence follows the same pattern as `test_packaged_metadata_policy_is_cwd_independent` (tests/test_foundry_audit_cli.py) and is verified by the TESTEXEC-017 wheel/editable probe.

### CNT-TC-014 - include_attribution=False on client and invocation scope

- Type: positive, privacy, structural.
- Given a real factory and `invocation_scope`, when any command executes, then client creation and scope use `include_attribution=False`, no attribution environment handling is added, and surrounding attribution state is unchanged after success and failure.
- Command/function: `FoundryClientFactory`, `AsyncClientFactory.invocation_scope(cfg)`, `main()`.
- Prerequisites/fixtures: factory/scope spies; preset outer attribution RID and environment.
- Steps: execute a read and a failed command; capture `include_attribution` on client and scope; capture attribution state before and after.
- Expected stdout/stderr/exit: both capture points pass `include_attribution=False`; no attribution variable is read or written; outer attribution state and env are identical after success and failure; no W3C `traceparent`/`tracestate`.
- Cleanup: reset context tokens and env.
- Evidence mapping: DESIGN-017 attribution rule; story AC 9; `test_invocation_uses_include_attribution_false` (tests/test_foundry_connectivity_cli.py).

### CNT-TC-015 - B3 enabled at outbound transport

- Type: positive, tracing, transport integration.
- Given tracing enabled, when the client is created and an SDK request is prepared, then outbound transport carries one valid B3 multi-header context.
- Command/function: `AsyncClientFactory.invocation_scope(cfg)`, SDK request preparation, a representative read.
- Prerequisites/fixtures: enabled tracing config, clean SDK context, transport header capture.
- Steps: enter the real tracing scope through `main()`; capture headers at client creation and request preparation.
- Expected stdout/stderr/exit: success result and exit `0`; every capture has lowercase-hex `X-B3-TraceId` of 32 characters, `X-B3-SpanId` of 16 characters, and `X-B3-Sampled` `0` or `1`; no W3C header appears.
- Cleanup: reset SDK context tokens and environment variables.
- Evidence mapping: DESIGN-005 B3 contract; story AC 10; `test_b3_transport_headers_enabled_disabled_retry_stable_and_restored` (tests/test_foundry_audit_cli.py) and `test_generated_context_has_valid_nonzero_b3_values_and_resets` (tests/test_tracing_provider.py); the namespace outbound-header probe is recorded in TESTEXEC-017 evidence.

### CNT-TC-016 - B3 disabled, retry stability, and context restoration

- Type: negative, resilience, isolation.
- Given disabled tracing, retries, prior context, or a later formatter failure, when execution leaves the invocation, then disabled calls add no B3 headers, retry attempts share one enabled context, and prior values are restored on every exit path.
- Command/function: `main()` with real `TracingProvider` scope and captured SDK transport headers.
- Prerequisites/fixtures: enabled and disabled configs; first-attempt transport failure followed by success; preset prior trace/span/sampled values; formatter, SDK, timeout, and cancellation failures.
- Steps: run the disabled flow; run the enabled retry flow; run each failure with prior values; inspect every outbound header set and context after exit.
- Expected stdout/stderr/exit: disabled flow has no `X-B3-*`; enabled retry captures identical B3 values for client creation and every attempt; no `traceparent`/`tracestate`; success exits `0`; failures use their ADR code; prior context is exact after all runs with no cross-test leakage.
- Cleanup: reset context tokens in `finally`, clear trace env vars, clear captures.
- Evidence mapping: DESIGN-005 isolation contract; story AC 10, 11; `test_b3_scope_restores_prior_values_after_formatter_failure` (tests/test_foundry_audit_cli.py) and `test_execute_traced_carries_same_b3_context_across_attempts_and_restores` (tests/test_tracing_provider.py).

### CNT-TC-017 - Retry behavior and at-least-once disclosure

- Type: resilience, negative, boundary.
- Given retryable and non-retryable failures, when `RetryHandler` wraps a command, then transient conditions (503, exhausted 429, configured transport exceptions) are retried per ADR-002, and validation, authorization, and permanent errors are never retried.
- Command/function: `RetryHandler` around representative read, create, execute, replace, delete, and upload commands.
- Prerequisites/fixtures: HTTP 503-then-success; repeated 429; 400/401/403/404; delay and jitter disabled; attempt counters.
- Steps: run each sequence and count attempts; verify the at-least-once disclosure is documented for create, execute, replace, delete, and upload (retrying can duplicate syncs, re-run builds, or cost); verify reads are safe to retry.
- Expected stdout/stderr/exit: recovered 503 has one success result and exit `0`; exhausted 429 exits `7`; validation/auth/permanent errors exit once with codes `1`/`2`/`3`/`4`; no duplicate result or content leak; disclosure text present where applicable.
- Cleanup: clear retry state and sentinels.
- Evidence mapping: ADR-001/002, DESIGN-017 retry contract; story AC 11; retry tests in tests/unit_test_retry_error_output_log.py (`test_http_429_and_503_are_retryable`, `test_http_non_429_503_does_not_retry`, `test_success_after_one_retry`, `test_retry_exhaustion_raises`); at-least-once disclosure is a design-documented property captured in TESTEXEC-017 evidence.

### CNT-TC-018 - ADR-001 error taxonomy and structured envelopes

- Type: negative, error taxonomy.
- Given each supported failure class, when the CLI exits, then it writes one JSON error envelope to stdout with the exact ADR-001 code and keeps diagnostics separate on stderr.
- Command/function: representative commands through `main()`.
- Prerequisites/fixtures: user input, HTTP 401/403/404/429/503, timeout, cancellation, ACL denial, configuration failure, and unexpected exception fakes.
- Steps: inject each failure after the correct lifecycle point; parse stdout and stderr; verify skipped downstream work where applicable.
- Expected stdout/stderr/exit: codes are user input `1`, authentication `2`, permission `3`, not found `4`, timeout/cancellation `5`, server `6`, exhausted 429 `7`, ACL `8`, and configuration `9`; error envelope is JSON on stdout; NDJSON diagnostics, if any, are on stderr; no raw traceback, token, or body appears.
- Cleanup: clear injected exceptions, secrets, and temporary files.
- Evidence mapping: ADR-001, DESIGN-017 error contract; story AC 12, 13; `test_sdk_error_maps_to_server_error_exit_code`, `test_sdk_timeout_maps_to_timeout_exit_code` (tests/test_foundry_connectivity_cli.py) plus the shared error-taxonomy tests in tests/unit_test_retry_error_output_log.py (`test_auth_error_exit_code_2` through `test_http_503_returns_server_error_after_retry_exhaustion`).

### CNT-TC-019 - Output formats: JSON, TOON, auto, and pretty

- Type: positive, output, boundary.
- Given success results of each shape, when `--format json|toon|auto` and `--pretty` run, then single models, `None` results, paginated arrays, and structured errors follow the ADR-004 rules.
- Command/function: `OutputFormatter` via representative commands.
- Prerequisites/fixtures: a single `Connection`/`FileImport`/`TableImport`/`VirtualTable`, `None` results (`file-import delete`, `table-import delete`, `update-export-settings`, `update-secrets`), `BuildRid` results (`file-import execute`, `table-import execute`), a uniform list array, an empty list array, structured error.
- Steps: run each shape under each format; validate stdout parses as JSON where required; verify pretty indentation when enabled.
- Expected stdout/stderr/exit: exit `0`; auto selects TOON only for uniform non-empty arrays, otherwise JSON; empty/non-uniform output is JSON; `None` results serialize `null`/empty consistently; error output remains the structured JSON envelope.
- Cleanup: clear captures and models.
- Evidence mapping: ADR-004, DESIGN-017 output contract; story AC 12; `test_toon_output_format` (tests/test_foundry_connectivity_cli.py) plus shared `OutputFormatter` coverage in tests/unit_test_retry_error_output_log.py.

### CNT-TC-020 - NDJSON stderr, stream separation, and confidentiality

- Type: positive, output, confidentiality.
- Given successful create, paginated list, and secret-update runs, when logs and results flow, then success data appears once on stdout, diagnostics are NDJSON on stderr, and credential/body/response sentinels never appear anywhere.
- Command/function: representative create, list, and update commands.
- Prerequisites/fixtures: secret sentinels embedded in request/response fixtures; captured logs.
- Steps: run each command; scan stdout, stderr, and captured logs for sentinel values, raw request bodies, and secret values.
- Expected stdout/stderr/exit: exit `0`; stdout carries results/metadata envelopes only; stderr carries NDJSON diagnostics only (empty or safe); none of the sentinels, payloads, or bodies appear in any stream or log.
- Cleanup: clear sentinels and temporary files.
- Evidence mapping: ADR-005, DESIGN-017 log contract; story AC 12, 13; `test_update_secrets_never_echoes_values` plus the NDJSON stderr/log-setup tests in tests/unit_test_retry_error_output_log.py (TestNdJsonFormatter and log-setup stderr tests).

### CNT-TC-021 - Import, console boundary, help, and thin launcher

- Type: packaging, side-effect regression.
- Given the package and Claude launcher, when imported or asked for help, then they load without configuration, network, or filesystem side effects and use one event-loop boundary.
- Command/function: package import, launcher import, module `--help`, launcher `--help`, `console_main()`.
- Prerequisites/fixtures: empty arbitrary directory; guarded config/network/filesystem constructors; `asyncio.run` spy.
- Steps: import all Connectivity modules and launcher; invoke root and operation help; call `console_main()` with fake `main()`; inspect launcher source.
- Expected stdout/stderr/exit: imports produce no output or files; help exits `0` and names the 20 operations; `console_main()` calls `asyncio.run()` once and propagates the result; launcher delegates to packaged interfaces and contains no copied catalog, pagination, or ACL logic.
- Cleanup: remove subprocess directory and restore the event-loop spy.
- Evidence mapping: DESIGN-017 packaging contract; story AC 14; `test_console_main_wraps_async_entry` (tests/test_foundry_connectivity_cli.py); the thin-launcher pattern follows `test_claude_launcher_is_thin_and_reexports_packaged_interfaces` (tests/test_audit_console_wrapper.py) and import side-effect-freedom is verified by the TESTEXEC-017 subprocess probe.

### CNT-TC-022 - Wheel, editable install, entry-point preservation, and regression

- Type: installation, regression.
- Given local wheel and editable installs, when commands run from an arbitrary directory without `PYTHONPATH`, then `foundry-connectivity` and the Claude launcher work while existing console scripts and repository gates remain intact.
- Command/function: local wheel build; wheel and editable install; installed `foundry-connectivity --help`; Claude launcher help; full test, Ruff, mypy, and package checks.
- Prerequisites/fixtures: isolated virtual environments for Python 3.11 and 3.12; `PIP_NO_INDEX=1`; local build dependencies; snapshot of existing `[project.scripts]` entries.
- Steps: build without live dependency resolution; inspect wheel for the Connectivity policy; install wheel then editable form with `--no-deps`; run help and packaged ACL probe from arbitrary CWD; compare every pre-existing entry point; run focused Connectivity tests and full regression with branch coverage.
- Expected stdout/stderr/exit: every help and package check exits `0`; wheel contains `foundry_cli/connectivity/metadata-allow-list.md`; all 20 operations are listed; all prior console scripts remain; focused and full suites pass on both Python versions; Ruff and mypy pass; repository branch coverage is at least 80%; no command makes a live Foundry request.
- Cleanup: delete isolated builds and environments; retain command output in TESTEXEC evidence only.
- Evidence mapping: DESIGN-017 packaging and regression contract; story AC 14, 15; all `tests/test_foundry_connectivity_cli.py` cases (33 tests) and the configured `pyproject.toml` gates; full-suite pass at HEAD `62c269f` (64 focused connectivity+media_sets tests green).

## Traceability matrix

| Requirement area | Story/design criteria | Cases |
| --- | --- | --- |
| Exact 20 catalog, pagination placement, parser, help, nested routing, input omission | Story AC 1; scope comment; operation catalog | CNT-TC-001 through 003 |
| JSON argument validation, pre-client rejection | Story AC 2 | CNT-TC-004 |
| Pagination contract: file-import list and table-import list | Story AC 3 | CNT-TC-005, 006 |
| Bounded JDBC driver upload | Story AC 5 | CNT-TC-007 |
| ACL precedence, read-only 13-op write set, semantic read, fail-closed policy | Story AC 7, 8 | CNT-TC-010 through 013 |
| include_attribution=False and B3 only | Story AC 9, 10 | CNT-TC-014 through 016 |
| Retry, error taxonomy | Story AC 11, 13 | CNT-TC-017, 018 |
| Output formats, NDJSON, confidentiality | Story AC 12, 13 | CNT-TC-019, 020 |
| Secret suppression | Story AC 13 | CNT-TC-008, 020 |
| Imports, console, launcher, wheel/editable, regression gates | Story AC 14, 15 | CNT-TC-021, 022 |
| Positive, negative, boundary, security, resilience, structural, packaging | Complete design strategy | CNT-TC-001 through 022 |

All story acceptance criteria have at least one positive case and, where meaningful, a negative, boundary, security, or failure-path case. The 20-operation catalog is fully covered: Connection (7) via CNT-TC-001 through 003, 007 through 011 plus ACL cases; FileImport (6) via CNT-TC-001 through 006 plus ACL cases; TableImport (6) via CNT-TC-001 through 006 plus ACL cases; VirtualTable (1) via CNT-TC-001 through 003 plus ACL cases.

## Execution and approval criteria

TESTEXEC-017 may begin only after DEV, UNITTEST, CODEREVIEW, and TESTCASE-017 reach their required completed states and the approved commit is available. Execute all 22 cases with no live network access unless an approved non-production smoke is explicitly authorized.

For every case, record PASS, FAIL, or BLOCKED with the exact command, environment, expected result, actual result, stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, and linked evidence. Any failure requires a BUG-SUB before TESTEXEC-017 can close. Final QA sign-off also requires all linked defects to be terminal, every story acceptance criterion to have passing evidence, supported Python checks to pass, and repository branch coverage to remain at least 80%.
