# TESTCASE-015 - Foundry SQL Queries CLI QA test cases

## Scope

These cases cover DEV-STORY-015 and the complete approved surface of `foundry-sql-queries`: 5 `foundry_sdk.v2.sql_queries` operations routed through the single `SqlQuery` client path (`cancel`, `execute`, `execute_ontology`, `get_results`, `get_status`). They verify the exact catalog and parser, nested SDK routing and dispatch, JSON argument validation, the Arrow byte-result downloads with bounded atomic persistence, access control precedence and the 3-operation write set, the packaged 1-permitted/4-blocked metadata-only policy, attribution suppression, B3 tracing, retry and error behavior, output and log contracts, privacy, packaging, and regression gates.

Routine acceptance uses mocked async SDK transport and real installed SDK exception classes. Live credentials and live Foundry access are not required. An approved non-production smoke is optional and cannot replace the mandatory mocked evidence.

## Source baseline

- [DESIGN-015](../architecture/DESIGN-015-sql-queries-cli.md), completed and closed for DEV-STORY-015.
- [DESIGN-005](../architecture/DESIGN-005-common-components.md), covering bounded binary streaming, atomic persistence, and SDK-native B3 tracing.
- [DESIGN-010](../architecture/DESIGN-010-audit-cli.md), [DESIGN-011](../architecture/DESIGN-011-aip-agents-cli.md), [DESIGN-012](../architecture/DESIGN-012-language-models-cli.md), [DESIGN-013](../architecture/DESIGN-013-models-cli.md) — the sibling namespace patterns this story mirrors (nested dispatch, binary downloads, metadata-only policy).
- [ADR-001](../architecture/adr/ADR-001-exit-code-taxonomy.md), [ADR-002](../architecture/adr/ADR-002-call-timeout-defaults.md), [ADR-004](../architecture/adr/ADR-004-format-auto-algorithm.md), [ADR-005](../architecture/adr/ADR-005-log-format.md), [ADR-006](../architecture/adr/ADR-006-env-file-search-path.md), [ADR-007](../architecture/adr/ADR-007-operation-level-readonly.md).
- The canonical environment-variable reference and metadata allow-list (namespace `sql_queries`, 5 rows; `sql_query.get_status` PERMITTED, the other 4 BLOCKED in tier 3).
- Vendored SDK sources under `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/sql_queries/` — the real `SqlQueryClient` methods (cancel, execute, execute_ontology, get_results, get_status), request paths, and result types.
- DEV-STORY-015 ticket body and technical scope comment `20260810-013256-architect` (authoritative 5-operation catalog).
- Implementation expected under `src/foundry_cli/sql_queries/`, `.claude/skills/foundry-sql-queries/`, and `pyproject.toml`.

## Preconditions and shared fixtures

- Python 3.11 and 3.12 environments contain the project, development dependencies, and pinned `foundry-sdk`.
- Use a nested async SDK fake rooted at `client.sql_queries.SqlQuery` with exactly the five public methods. A wrong, flattened, raw, or streaming route must fail the fixture. The namespace has no other public sub-clients.
- Byte-returning calls (`execute_ontology`, `get_results`) use public-only response fakes compatible with `BinaryDownloadHandler`; any private attribute access fails the case. `get_results` uses the long-poll `ARROW_TABLE` response mode with a server timeout up to one minute.
- Use real installed SDK model validators for nested invalid-input checks and real `foundry_sdk._errors` classes for error taxonomy checks. Mock network transport; no service call or billable query execution is permitted.
- Set retry delay to zero, disable jitter, and use two retries unless a case states otherwise. Capture attempt number, timeout, attribution, and B3 values.
- Capture stdout, stderr, logs, SDK arguments, context variables, client/network constructors, and filesystem changes independently. Do not retain credential, token, query, input, content, or downloaded-byte sentinel values.
- Each download case uses a fresh temporary root and a small byte limit. Path cases monitor the parent directory for escapes.
- Packaging cases build a clean local archive with dependency resolution disabled, install with `--no-deps`, and run from an arbitrary empty working directory without `PYTHONPATH`.
- Any optional live smoke uses an approved non-production Foundry tenant, synthetic query text, least-privilege credentials, and a cleanup plan. Credentials must never enter retained evidence.
- TESTEXEC records the commit, OS, Python and SDK versions, environment type, exact command, expected and actual stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, evidence reference, and PASS/FAIL/BLOCKED status for every case.

## Test data

| Name | Fixture |
| --- | --- |
| Query ID | `ri.sqlqueries.main.query.test` |
| SQL query text | `SELECT col FROM \`ri.foundry.main.dataset.test\`` |
| Fallback branches JSON | `["master"]` |
| Parameters JSON | `{"positional": ["p1", "p2"]}` |
| Row limit | `100` |
| Download limit | `5` bytes |
| Byte payloads | empty; `abc`; `abcde`; `abcdefghi` followed by unread sentinel chunk |
| Output names | safe `results.arrow`; unsafe `../escape`, `..\escape`, `/absolute`, `nul\0name`, `.`, `..` |
| Timeout boundaries | `1`, `3600`; invalid `0`, `3601`, non-integer text |
| Secret sentinels | `sentinel-token-secret`, `sentinel-query-secret`, `sentinel-content-secret`, `sentinel-bytes-secret`, `sentinel-attribution-rid` |

## Command and route inventory

Every inventory row is exercised by SQL-TC-001 through SQL-TC-006. Unless a case states otherwise, success writes one formatted result to stdout, writes no application data to stderr, exits `0`, and leaves only documented download effects.

| CLI command | Exact public SDK route and method | Required input | Optional input |
| --- | --- | --- | --- |
| `query cancel QUERY_ID` | `client.sql_queries.SqlQuery.cancel` | `sql_query_id` | shared options |
| `query execute --query ...` | `client.sql_queries.SqlQuery.execute` | `--query` | `--fallback-branch-ids-json`, shared options |
| `query execute-ontology --query ...` | `client.sql_queries.SqlQuery.execute_ontology` | `--query` | `--dry-run`, `--parameters-json`, `--row-limit`, shared options |
| `query get-results QUERY_ID --output ...` | `client.sql_queries.SqlQuery.get_results` | `sql_query_id`, `--output` | shared options |
| `query get-status QUERY_ID` | `client.sql_queries.SqlQuery.get_status` | `sql_query_id` | shared options |

No command may receive `attribution`, `preview`, `_sdk_internal`, an absent optional set to `None`, or any unsupported paging, stream, raw-response, or file flag. The SqlQueries namespace has no nested sub-clients and no paginated (ResourceIterator) operation; no pagination flags may exist in `OP_SPECS` or the parser.

## Test cases

### SQL-TC-001 - Catalog, parser, help, and exact 5 surface

- Type: positive, structural, negative parser.
- Given the installed module and launcher, when the catalog and parser are inspected, then exactly 5 unique SDK specifications exist, every inventory command parses, and no pagination flag exists anywhere in the surface.
- Command/function: `OP_SPECS`, `build_parser()`, `_spec_for()`, `_get_client()`, root/resource/operation `--help`, `main()` with missing resource/operation, unknown flags, missing required positionals/options, invalid choices/types.
- Prerequisites/fixtures: guarded config, client, network, and filesystem constructors.
- Steps: count `OP_SPECS`; assert no `--page-size`/`--page-token`/`--all`/`--max-pages` flag in any parser; parse all 5 inventory commands; run all help surfaces; run every incomplete or malformed form.
- Expected stdout/stderr/exit: help on stdout and exit `0`; catalog count exactly `5`; parser errors as one JSON envelope on stdout with `exit_code: 1`, empty diagnostic stderr, no traceback, no config/client/network/filesystem call.
- Cleanup: restore `sys.argv` and capture streams.
- Evidence mapping: DESIGN-015 catalog; story AC 1, 14; `test_catalog_contains_exact_5_operations`, `test_catalog_marks_exactly_two_download_operations`, `test_parser_accepts_every_declared_argument`, `test_parser_rejects_unknown_operation`; absence of pagination flags and `--help` behavior are verified by those catalog/parser tests plus the module `--help` probe recorded in TESTEXEC-015 evidence.

### SQL-TC-002 - Nested SDK routing through the single SqlQuery client

- Type: positive, structural, route identity.
- Given a fake rooted at `client.sql_queries.SqlQuery` whose sibling routes fail on access, when every inventory command runs, then each resolves the exact SqlQuery method and never a flattened, nested, raw, or streaming route.
- Command/function: `_get_client()` and each dispatch path.
- Prerequisites/fixtures: fake whose flattened and streaming routes fail on access.
- Steps: run one command per catalog row; assert the resolved method identity; assert no `sql_queries.*` flat call and no `with_streaming_response`/`with_raw_response` access.
- Expected stdout/stderr/exit: success results on stdout once, exit `0`, no unexpected stderr; no flattened or private route access.
- Cleanup: reset fakes and captures.
- Evidence mapping: DESIGN-015 nested dispatch; story AC 1; `test_catalog_contains_exact_5_operations` (all five route through the single `SqlQuery` client path) plus the dispatch tests `test_cancel_dispatches_to_sql_query_cancel`, `test_execute_dispatches_with_query_and_optional_json`, `test_get_status_dispatches_and_omits_absent_optional`.

### SQL-TC-003 - Required inputs forwarded and absent optionals omitted

- Type: positive, structural.
- Given each inventory command, when dispatch runs, then required positionals/options reach the SDK call and every absent optional is omitted (never `None`).
- Command/function: all 5 dispatches.
- Prerequisites/fixtures: recording SDK fakes.
- Steps: run each command with only required inputs; run `query execute` with and without `--fallback-branch-ids-json`; run `query execute-ontology` with each optional present and absent (`--dry-run`, `--parameters-json`, `--row-limit`); run `query get-results` with and without `--output`.
- Expected stdout/stderr/exit: SDK call arguments contain exactly the documented keys; success exits `0`; absent optionals absent from kwargs; `get_results` requests the `ARROW_TABLE` response mode.
- Cleanup: clear fake call records.
- Evidence mapping: DESIGN-015 operation catalog; story AC 1; `test_get_status_dispatches_and_omits_absent_optional` (absent optionals omitted) and `test_execute_dispatches_with_query_and_optional_json` (optional `--fallback-branch-ids-json` present).

### SQL-TC-004 - JSON argument validation before client creation

- Type: positive, negative, boundary.
- Given every structured flag (`--fallback-branch-ids-json`, `--parameters-json`), when validation runs, then valid JSON with the documented top-level shape reaches the SDK and invalid or mis-shaped JSON exits `1` before client or network work.
- Command/function: JSON validators, `main()`.
- Prerequisites/fixtures: guarded factory/network constructors; real SDK validators for nested checks.
- Steps: supply valid payloads; supply malformed JSON text; supply valid JSON with the wrong top-level type (object vs array vs scalar); supply JSON whose nested fields violate SDK validators.
- Expected stdout/stderr/exit: valid inputs call the SDK and exit `0`; invalid inputs write one JSON user-input envelope to stdout, exit `1`, no traceback, and never echo the input payload into stdout/stderr/logs.
- Cleanup: clear captured sentinels.
- Evidence mapping: DESIGN-015 JSON validation contract; story AC 2; `test_execute_dispatches_with_query_and_optional_json` (valid decode) and `test_invalid_fallback_branch_json_rejected_before_client`, `test_invalid_parameters_json_rejected_before_client` (invalid or mis-shaped JSON rejected before client creation).

### SQL-TC-005 - Arrow byte results download below the byte limit

- Type: positive, boundary.
- Given a public byte stream shorter than the byte limit, when `query execute-ontology` or `query get-results` runs, then the full payload is atomically published and reported as non-truncated.
- Command/function: the two byte-result commands through `BinaryDownloadHandler`.
- Prerequisites/fixtures: three-byte stream, five-byte limit, safe filename, public-only response fake; for `get_results`, a long-poll response fake.
- Steps: download; inspect SDK arguments, context closure, saved bytes, result envelope, and directory contents.
- Expected stdout/stderr/exit: JSON metadata envelope on stdout, no content on stdout/stderr, exit `0`; file contains `abc`; `file_size` and `source_size` are `3`; `truncated` false; one published file remains under `.foundry-data/downloads/`.
- Cleanup: remove the temporary download root.
- Evidence mapping: DESIGN-015 bounded download design; story AC 5; `test_execute_ontology_writes_atomically_and_reports_metadata` and `test_get_results_download_requires_output_and_closes_response` (below-limit atomic persistence, metadata envelope, response closure).

### SQL-TC-006 - Arrow byte results above the limit use one probe byte

- Type: boundary, security.
- Given content above the limit followed by a sentinel chunk, when the download reaches the bound, then it stores only the allowed prefix and observes no more than one extra byte.
- Command/function: the two byte-result commands through `BinaryDownloadHandler`.
- Prerequisites/fixtures: `abcdefghi`, unread sentinel chunk, five-byte limit, stream index counter.
- Steps: download and inspect stored bytes, source fields, iterator reads, and context cleanup.
- Expected stdout/stderr/exit: JSON envelope on stdout, exit `0`; file contains `abcde`; `file_size: 5`, `truncated: true`, `source_size: null`, `source_size_at_least: 6`; sentinel chunk is not read or logged.
- Cleanup: remove the temporary root and stream fake.
- Evidence mapping: DESIGN-015 bounded download design; story AC 5; shared handler tests `test_unknown_length_reads_only_limit_plus_one_and_hashes_stored_prefix` and `test_known_oversize_stops_after_prefix_and_keeps_declared_size` (tests/test_binary_download.py); the namespace above-limit probe is recorded in TESTEXEC-015 evidence.

### SQL-TC-007 - Download failure and cancellation clean atomically

- Type: negative, cancellation, filesystem security.
- Given a stream failure or `asyncio.CancelledError` after partial bytes, when download aborts, then no partial or temporary file remains and all stream contexts close.
- Command/function: the two byte-result commands, `main()` cancellation path.
- Prerequisites/fixtures: failing byte stream for `OSError` and cancellation; fresh root.
- Steps: run both failures after one chunk; inspect all descendants and closure flags; run cancellation through `main()`.
- Expected stdout/stderr/exit: stream `OSError` uses a structured server-error envelope and exits `6`; cancellation uses a structured timeout envelope and exits `5`; no content bytes, traceback, or temporary path leak; download root contains no file; stream and response context close.
- Cleanup: remove root and restore cancellation state.
- Evidence mapping: DESIGN-015 download atomicity; story AC 5, 13; `test_stream_failure_removes_partial_and_temporary_files` (tests/test_binary_download.py) and `test_signal_cancellation_maps_to_timeout_error` (tests/unit_test_retry_error_output_log.py).

### SQL-TC-008 - Unsafe output names are rejected before publication

- Type: negative, path security.
- Given traversal, absolute, separator, NUL, dot, or dot-dot filenames, when download validates the name, then it rejects the request without creating the download root or an outside file.
- Command/function: the byte-result download commands with `--output` (in practice `query get-results --output`, the only command registering the output flag; `execute-ontology` persists under its operation-derived default filename through `BinaryDownloadHandler`).
- Prerequisites/fixtures: unsafe-name table and monitored parent directory.
- Steps: try every unsafe name; inspect root, parent, response context, stdout, and stderr.
- Expected stdout/stderr/exit: structured user-input envelope on stdout and exit `1`; no traceback or content on stderr; no root or escaped file; response context exits.
- Cleanup: remove monitored temporary parent.
- Evidence mapping: DESIGN-015 path and error contracts; story AC 5, 7; `test_download_rejects_unsafe_filename` (namespace) and `test_unsafe_filename_is_rejected_before_root_creation` (tests/test_binary_download.py).

### SQL-TC-009 - ACL precedence: global, namespace, and operation scopes

- Type: security, positive, negative.
- Given metadata-only and operation-level overrides, when ACL evaluates `SQL_QUERIES`, then permissive settings allow, blocking settings deny, and an operation override wins over the namespace setting.
- Command/function: `AccessControlGuard(cfg, "SQL_QUERIES").check()` for representative operations.
- Prerequisites/fixtures: packaged SQL Queries allow-list and isolated environment variables.
- Steps: enable global metadata-only; check permitted and blocked operations; disable SQL Queries metadata-only at namespace level; disable one operation explicitly; combine namespace read-only with an operation override.
- Expected stdout/stderr/exit: permitted checks return silently; blocked CLI calls write a structured ACL envelope to stdout, exit `8`, and do not create a client or path; the denying rule appears on stderr diagnostics; no secret appears.
- Cleanup: remove every ACL environment variable.
- Evidence mapping: DESIGN-015 access-control table; story AC 6, 7; `test_readonly_blocks_three_write_operations`, `test_semantic_reads_permitted_under_readonly`, `test_acl_denial_reports_rule`, `test_metadata_only_runtime_blocks_blocked_ops_and_permits_get_status` (precedence exercised through the namespace runtime checks).

### SQL-TC-010 - Read-only mode blocks the write set; semantic reads stay reads

- Type: security, positive, negative.
- Given read-only mode enabled, when each write command runs, then `query cancel`, `query execute`, and `query execute-ontology` exit `8` before client or filesystem effects, while `query get-results` and `query get-status` remain executable as semantic reads.
- Command/function: `AccessControlGuard` + `main()` for each write command and the two reads.
- Prerequisites/fixtures: read-only environment; guarded factory/transport; byte and status fakes.
- Steps: run all 3 write commands under read-only; run both reads under read-only; inspect event order and filesystem.
- Expected stdout/stderr/exit: each blocked write emits one ACL envelope and exit `8` with the denying rule on stderr; no SDK call and no download file created; both reads succeed and exit `0`.
- Cleanup: clear read-only variables, captures, and roots.
- Evidence mapping: DESIGN-015 read-only policy; story AC 6; `test_readonly_blocks_three_write_operations` and `test_semantic_reads_permitted_under_readonly`.

### SQL-TC-011 - Metadata-only tier: exact 1 permitted / 4 blocked

- Type: security, positive, negative.
- Given metadata-only mode, when every operation is checked, then exactly `sql_query.get_status` is permitted and the other 4 operations are blocked.
- Command/function: `AccessControlGuard` metadata-only evaluation over the full 5-op catalog.
- Prerequisites/fixtures: packaged SQL Queries allow-list; the full catalog.
- Steps: assert the permitted set equals `{sql_query.get_status}`; assert cancel, execute, execute_ontology, and get_results are blocked.
- Expected stdout/stderr/exit: the 1 permitted check returns silently; each of the 4 blocked CLI calls writes an ACL envelope and exits `8` with the denying rule on stderr; no client or file effect.
- Cleanup: clear metadata-only variables.
- Evidence mapping: DESIGN-015 metadata policy; story AC 8; `test_metadata_only_permits_exactly_1_blocks_4` and `test_metadata_only_runtime_blocks_blocked_ops_and_permits_get_status`.

### SQL-TC-012 - Packaged metadata-only policy is fail closed and CWD independent

- Type: security, packaging, negative.
- Given the installed package with a missing or malformed packaged allow-list, when ACL runs, then it fails closed (no operation permitted) and the packaged policy resolves from an arbitrary working directory.
- Command/function: `_METADATA_ALLOWLIST_PATH`, `AccessControlGuard` from an installed wheel/editable launch.
- Prerequisites/fixtures: malformed/missing policy fixtures in an isolated environment; empty arbitrary CWD, no `PYTHONPATH`.
- Steps: probe policy path from the installed package; run a permitted-class check with malformed policy; run checks from the arbitrary CWD.
- Expected stdout/stderr/exit: malformed/missing policy blocks even previously-permitted operations (fail closed, exit `8`); packaged policy path resolves inside the installed package; valid packaged policy applies the 1/4 rule from any CWD.
- Cleanup: delete isolated environments and fixtures.
- Evidence mapping: DESIGN-015 fail-closed rule; story AC 8, 14; `test_metadata_only_permits_exactly_1_blocks_4` (parsed from the packaged allow-list); packaged-policy CWD independence follows the same pattern as `test_packaged_metadata_policy_is_cwd_independent` (tests/test_foundry_audit_cli.py) and is verified by the TESTEXEC-015 wheel/editable probe.

### SQL-TC-013 - include_attribution=False on client and invocation scope

- Type: positive, privacy, structural.
- Given a real factory and `invocation_scope`, when any command executes, then client creation and scope use `include_attribution=False`, no attribution environment handling is added, and surrounding attribution state is unchanged after success and failure.
- Command/function: `FoundryClientFactory`, `AsyncClientFactory.invocation_scope(cfg)`, `main()`.
- Prerequisites/fixtures: factory/scope spies; preset outer attribution RID and environment.
- Steps: execute a read and a failed command; capture `include_attribution` on client and scope; capture attribution state before and after.
- Expected stdout/stderr/exit: both capture points pass `include_attribution=False`; no `FOUNDRY_*` attribution variable is read or written; outer attribution state and env are identical after success and failure; no W3C `traceparent`/`tracestate`.
- Cleanup: reset context tokens and env.
- Evidence mapping: DESIGN-015 attribution rule; story AC 9; `test_invocation_uses_include_attribution_false`.

### SQL-TC-014 - B3 enabled at outbound transport

- Type: positive, tracing, transport integration.
- Given tracing enabled, when the client is created and an SDK request is prepared, then outbound transport carries one valid B3 multi-header context.
- Command/function: `AsyncClientFactory.invocation_scope(cfg)`, SDK request preparation, a representative read.
- Prerequisites/fixtures: enabled tracing config, clean SDK context, transport header capture.
- Steps: enter the real tracing scope through `main()`; capture headers at client creation and request preparation.
- Expected stdout/stderr/exit: success result and exit `0`; every capture has lowercase-hex `X-B3-TraceId` of 32 characters, `X-B3-SpanId` of 16 characters, and `X-B3-Sampled` `0` or `1`; no W3C header appears.
- Cleanup: reset SDK context tokens and environment variables.
- Evidence mapping: DESIGN-005 B3 contract; story AC 10; `test_b3_transport_headers_enabled_disabled_retry_stable_and_restored` (tests/test_foundry_audit_cli.py) and `test_generated_context_has_valid_nonzero_b3_values_and_resets` (tests/test_tracing_provider.py); the namespace outbound-header probe is recorded in TESTEXEC-015 evidence.

### SQL-TC-015 - B3 disabled, retry stability, and context restoration

- Type: negative, resilience, isolation.
- Given disabled tracing, retries, prior context, or a later formatter failure, when execution leaves the invocation, then disabled calls add no B3 headers, retry attempts share one enabled context, and prior values are restored on every exit path.
- Command/function: `main()` with real `TracingProvider` scope and captured SDK transport headers.
- Prerequisites/fixtures: enabled and disabled configs; first-attempt transport failure followed by success; preset prior trace/span/sampled values; formatter, SDK, timeout, and cancellation failures.
- Steps: run the disabled flow; run the enabled retry flow; run each failure with prior values; inspect every outbound header set and context after exit.
- Expected stdout/stderr/exit: disabled flow has no `X-B3-*`; enabled retry captures identical B3 values for client creation and every attempt; no `traceparent`/`tracestate`; success exits `0`; failures use their ADR code; prior context is exact after all runs with no cross-test leakage.
- Cleanup: reset context tokens in `finally`, clear trace env vars, clear captures.
- Evidence mapping: DESIGN-005 isolation contract; story AC 10, 11; `test_b3_scope_restores_prior_values_after_formatter_failure` (tests/test_foundry_audit_cli.py) and `test_execute_traced_carries_same_b3_context_across_attempts_and_restores` (tests/test_tracing_provider.py).

### SQL-TC-016 - Retry behavior and at-least-once disclosure

- Type: resilience, negative, boundary.
- Given retryable and non-retryable failures, when `RetryHandler` wraps a command, then transient conditions (503, exhausted 429, configured transport exceptions) are retried per ADR-002, and validation, authorization, and permanent errors are never retried.
- Command/function: `RetryHandler` around representative read, `execute`, and `cancel` commands.
- Prerequisites/fixtures: HTTP 503-then-success; repeated 429; 400/401/403/404; delay and jitter disabled; attempt counters.
- Steps: run each sequence and count attempts; verify the at-least-once disclosure is documented for `execute`, `execute_ontology`, and `cancel` (retrying can duplicate work or cost); verify `get_results` is retried while the query is still running (long-poll).
- Expected stdout/stderr/exit: recovered 503 has one success result and exit `0`; exhausted 429 exits `7`; validation/auth/permanent errors exit once with codes `1`/`2`/`3`/`4`; no duplicate result or content leak; disclosure text present where applicable.
- Cleanup: clear retry state and sentinels.
- Evidence mapping: ADR-001/002, DESIGN-015 retry contract; story AC 11; retry tests in tests/unit_test_retry_error_output_log.py (`test_http_429_and_503_are_retryable`, `test_http_non_429_503_does_not_retry`, `test_success_after_one_retry`, `test_retry_exhaustion_raises`); at-least-once disclosure is a design-documented property captured in TESTEXEC-015 evidence.

### SQL-TC-017 - ADR-001 error taxonomy and structured envelopes

- Type: negative, error taxonomy.
- Given each supported failure class, when the CLI exits, then it writes one JSON error envelope to stdout with the exact ADR-001 code and keeps diagnostics separate on stderr.
- Command/function: representative commands through `main()`.
- Prerequisites/fixtures: user input, HTTP 401/403/404/429/503, timeout, cancellation, ACL denial, configuration failure, and unexpected exception fakes.
- Steps: inject each failure after the correct lifecycle point; parse stdout and stderr; verify skipped downstream work where applicable.
- Expected stdout/stderr/exit: codes are user input `1`, authentication `2`, permission `3`, not found `4`, timeout/cancellation `5`, server `6`, exhausted 429 `7`, ACL `8`, and configuration `9`; error envelope is JSON on stdout; NDJSON diagnostics, if any, are on stderr; no raw traceback, token, query, or content appears.
- Cleanup: clear injected exceptions, secrets, and temporary roots.
- Evidence mapping: ADR-001, DESIGN-015 error contract; story AC 12, 13; `test_sdk_error_maps_to_exit_code` (namespace) plus the shared error-taxonomy tests in tests/unit_test_retry_error_output_log.py (`test_auth_error_exit_code_2` through `test_http_503_returns_server_error_after_retry_exhaustion`).

### SQL-TC-018 - Timeout boundaries and forwarding

- Type: positive, boundary, negative.
- Given CLI or configured timeouts, when execution starts, then values from 1 through 3600 seconds are accepted and the selected value reaches both retry handling and the SDK request; invalid values are rejected before ACL, scope, client, or filesystem work.
- Command/function: `_validate_timeout()`, representative commands with `--timeout`.
- Prerequisites/fixtures: values `1`, `30`, `3600`, CLI override `17`, configured default `42`, invalid `0`, `3601`, negative, and non-integer text.
- Steps: validate boundaries; execute with and without a CLI override; inspect retry construction and `request_timeout`; invoke each invalid value.
- Expected stdout/stderr/exit: valid requests produce one success result and exit `0`; retry and SDK receive the same chosen integer; invalid values write one JSON user-input envelope on stdout and exit `1` with no ACL/client/network/filesystem call.
- Cleanup: restore config defaults and call records.
- Evidence mapping: ADR-002, DESIGN-015 invocation contract; story AC 12; `test_timeout_accepts_adr_002_bounds`, `test_invalid_timeout_stops_before_acl_or_client`.

### SQL-TC-019 - Output formats: JSON, TOON, auto, and pretty

- Type: positive, output, boundary.
- Given success results of each shape, when `--format json|toon|auto` and `--pretty` run, then single models, `None` results, download metadata envelopes, and structured errors follow the ADR-004 rules.
- Command/function: `OutputFormatter` via representative commands.
- Prerequisites/fixtures: a single `QueryStatus` (`get_status`), a `None` result (`cancel`), a `QueryStatus` from `execute`, download metadata envelopes, structured error.
- Steps: run each shape under each format; validate stdout parses as JSON where required; verify pretty indentation when enabled.
- Expected stdout/stderr/exit: exit `0`; auto selects TOON only for uniform non-empty arrays, otherwise JSON; empty/non-uniform output is JSON; `cancel` with `None` result serializes `null`/empty consistently; download cases emit the metadata envelope; error output remains the structured JSON envelope.
- Cleanup: clear captures and models.
- Evidence mapping: ADR-004, DESIGN-015 output contract; story AC 12; `test_output_toon_and_json_formats` (namespace) plus shared `OutputFormatter` coverage in tests/unit_test_retry_error_output_log.py.

### SQL-TC-020 - NDJSON stderr, stream separation, and confidentiality

- Type: positive, output, confidentiality.
- Given successful execute, status, and download runs, when logs and results flow, then success data appears once on stdout, diagnostics are NDJSON on stderr, and credential/query/input/content/byte sentinels never appear anywhere.
- Command/function: representative execute, status, and download commands.
- Prerequisites/fixtures: secret sentinels embedded in request/response fixtures; captured logs.
- Steps: run each command; scan stdout, stderr, and captured logs for sentinel values, raw content bytes, and request/response bodies.
- Expected stdout/stderr/exit: exit `0`; stdout carries results/metadata envelopes only; stderr carries NDJSON diagnostics only (empty or safe); none of the sentinels, payload bytes, tokens, or bodies appear in any stream or log.
- Cleanup: clear sentinels and temporary files.
- Evidence mapping: ADR-005, DESIGN-015 log contract; story AC 12, 13; `test_sensitive_values_not_echoed_in_errors` (namespace) plus the NDJSON stderr/log-setup tests in tests/unit_test_retry_error_output_log.py (TestNdJsonFormatter and log-setup stderr tests).

### SQL-TC-021 - Import, console boundary, help, and thin launcher

- Type: packaging, side-effect regression.
- Given the package and Claude launcher, when imported or asked for help, then they load without configuration, network, or filesystem side effects and use one event-loop boundary.
- Command/function: package import, launcher import, module `--help`, launcher `--help`, `console_main()`.
- Prerequisites/fixtures: empty arbitrary directory; guarded config/network/filesystem constructors; `asyncio.run` spy.
- Steps: import all SQL Queries modules and launcher; invoke root and operation help; call `console_main()` with fake `main()`; inspect launcher source.
- Expected stdout/stderr/exit: imports produce no output or files; help exits `0` and names the 5 operations; `console_main()` calls `asyncio.run()` once and propagates the result; launcher delegates to packaged interfaces and contains no copied catalog, download, or ACL logic.
- Cleanup: remove subprocess directory and restore the event-loop spy.
- Evidence mapping: DESIGN-015 packaging contract; story AC 14; `test_console_main_uses_one_asyncio_run_boundary` (namespace); the thin-launcher pattern follows `test_claude_launcher_is_thin_and_reexports_packaged_interfaces` (tests/test_audit_console_wrapper.py) and import side-effect-freedom is verified by the TESTEXEC-015 subprocess probe.

### SQL-TC-022 - Wheel, editable install, entry-point preservation, and regression

- Type: installation, regression.
- Given local wheel and editable installs, when commands run from an arbitrary directory without `PYTHONPATH`, then `foundry-sql-queries` and the Claude launcher work while existing console scripts and repository gates remain intact.
- Command/function: local wheel build; wheel and editable install; installed `foundry-sql-queries --help`; Claude launcher help; full test, Ruff, mypy, and package checks.
- Prerequisites/fixtures: isolated virtual environments for Python 3.11 and 3.12; `PIP_NO_INDEX=1`; local build dependencies; snapshot of existing `[project.scripts]` entries.
- Steps: build without live dependency resolution; inspect wheel for the SQL Queries policy; install wheel then editable form with `--no-deps`; run help and packaged ACL probe from arbitrary CWD; compare every pre-existing entry point; run focused SQL Queries tests and full regression with branch coverage.
- Expected stdout/stderr/exit: every help and package check exits `0`; wheel contains `foundry_cli/sql_queries/metadata-allow-list.md`; all 5 operations are listed; all prior console scripts remain; focused and full suites pass on both Python versions; Ruff and mypy pass; repository branch coverage is at least 80%; no command makes a live Foundry request.
- Cleanup: delete isolated builds and environments; retain command output in TESTEXEC evidence only.
- Evidence mapping: DESIGN-015 packaging and regression contract; story AC 14, 15; all `tests/test_foundry_sql_queries_*` cases and the configured `pyproject.toml` gates.

## Traceability matrix

| Requirement area | Story/design criteria | Cases |
| --- | --- | --- |
| Exact 5 catalog, no pagination, parser, help, nested routing, input omission | Story AC 1, 14; operation catalog | SQL-TC-001 through 003 |
| JSON argument validation, pre-client rejection | Story AC 2 | SQL-TC-004 |
| Arrow byte downloads: bounded, atomic, closure, paths | Story AC 5, 13 | SQL-TC-005 through 008 |
| ACL precedence, read-only 3-op write set, semantic reads, fail-closed policy | Story AC 6, 7, 8 | SQL-TC-009 through 012 |
| include_attribution=False and B3 only | Story AC 9, 10 | SQL-TC-013 through 015 |
| Retry, error taxonomy, timeouts | Story AC 11, 12 | SQL-TC-016 through 018 |
| Output formats, NDJSON, confidentiality | Story AC 12, 13 | SQL-TC-019, 020 |
| Imports, console, launcher, wheel/editable, regression gates | Story AC 14, 15 | SQL-TC-021, 022 |
| Positive, negative, boundary, security, resilience, structural, packaging | Complete design strategy | SQL-TC-001 through 022 |

All story acceptance criteria have at least one positive case and, where meaningful, a negative, boundary, security, or failure-path case.

## Execution and approval criteria

TESTEXEC-015 may begin only after DEV, UNITTEST, CODEREVIEW, and TESTCASE-015 reach their required completed states and the approved commit is available. Execute all 22 cases with no live network access unless an approved non-production smoke is explicitly authorized.

For every case, record PASS, FAIL, or BLOCKED with the exact command, environment, expected result, actual result, stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, and linked evidence. Any failure requires a BUG-SUB before TESTEXEC-015 can close. Final QA sign-off also requires all linked defects to be terminal, every story acceptance criterion to have passing evidence, supported Python checks to pass, and repository branch coverage to remain at least 80%.
