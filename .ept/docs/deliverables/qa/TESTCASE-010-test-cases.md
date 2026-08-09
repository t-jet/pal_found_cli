# TESTCASE-010 - Foundry Audit CLI QA test cases

## Scope

These cases cover DEV-STORY-010 and both `foundry-audit` operations:

- `log-file list` through `client.audit.Organization.LogFile.with_raw_response.list`
- `log-file content` through `client.audit.Organization.LogFile.with_streaming_response.content`

Coverage includes the catalog and parser, strict dates and cursors, exact-page pagination, ACL precedence, bounded atomic downloads, retry and timeout behavior, ADR-001 errors, B3 propagation, output and log safety, installed packaging, and regression gates. Tests use fakes, temporary directories, and local package builds. They must not call a live Foundry service.

## Source baseline

- [DESIGN-010](../architecture/DESIGN-010-audit-cli.md), approved for DEV-STORY-010.
- [DESIGN-005](../architecture/DESIGN-005-common-components.md), which defines bounded unknown-length downloads and SDK-native B3 context.
- [ADR-001](../architecture/adr/ADR-001-exit-code-taxonomy.md) and [ADR-002](../architecture/adr/ADR-002-call-timeout-defaults.md).
- Implementation commits `0c705b8`, `b4e241c`, `af5b4e3`, and `87d817c`.
- Implementation under `src/foundry_cli/audit/`, `.claude/skills/foundry-audit/`, and `pyproject.toml`.
- Existing developer tests in `tests/test_foundry_audit_cli.py` and `tests/test_audit_console_wrapper.py` provide executable fixtures and assertion references. Their presence does not count as QA execution evidence.

## Preconditions and shared fixtures

- Python 3.11 and 3.12 environments contain the project and development dependencies.
- No live Foundry credentials are required. Remove or replace real credentials in the test process.
- SDK list calls use an async raw-response fake whose `decode()` result has `data` and `next_page_token`.
- SDK content calls use a public-only async streamed-response fake with `aiter_bytes()`. Any private attribute access fails the case.
- Retry delays and jitter are disabled in fakes. Attempts remain observable.
- Each download case uses a fresh temporary root and a small byte limit.
- stdout and stderr are captured independently. Secrets use sentinel values that must never appear in either stream.
- Packaging cases build from the local checkout with dependency resolution disabled. They run from an arbitrary directory without `PYTHONPATH`.
- TESTEXEC records the tested commit, Python version, OS, exact command, expected result, actual result, and retained output for every case.

## Test data

| Name | Value |
|---|---|
| Organization RID | `ri.organization.test` |
| Log file ID | `audit-log-001` |
| Initial date range | `2026-08-01` through `2026-08-02` |
| Continuation token | `cursor-002` |
| Page size | `2` |
| Download limit | `5` bytes |
| Below-limit content | `abc` |
| Exact-limit content | `abcde` |
| Above-limit content | `abcdefghi` followed by an unread sentinel chunk |
| Safe output name | `audit.bin` |
| Unsafe names | `../escape`, `..\escape`, `/absolute`, `nul\0name`, `.`, `..` |
| Secret sentinels | `token-secret`, `audit-body-secret`, `cursor-secret` |

## Test cases

### AUD-TC-001 - Catalog, parser, and nested route

- Type: positive, structural.
- Behavior: Given the Audit module, when its catalog and parser are inspected, then exactly two unique operations use the approved nested SDK route and declared arguments.
- Command/function: `OP_SPECS`, `build_parser()`, `_spec_for()`, `_get_client()`.
- Prerequisites/fixtures: nested fake client with `audit.Organization.LogFile`; parser argument sets for both operations.
- Steps: Assert the two `(resource, operation)` pairs; parse all positionals and options; resolve the client; reject an unknown resource or operation.
- Expected stdout/stderr/exit: No output for function checks; parsed commands are `log-file list` and `log-file content`; unknown selection maps to JSON user-input error on stdout, empty diagnostic stderr, exit `1`.
- Cleanup: Restore `sys.argv` and fake client state.
- Evidence mapping: DESIGN-010 operation catalog, story AC 1, 4, and 8; `test_catalog_contains_exact_two_unique_nested_operations`, `test_parser_accepts_every_declared_argument`, `test_get_client_uses_exact_audit_organization_log_file_route`.

### AUD-TC-002 - Help, missing commands, and parser failures

- Type: positive and negative CLI.
- Behavior: Given each help surface or incomplete syntax, when parsing runs, then help exits cleanly while invalid syntax becomes a structured user-input error without loading configuration or creating a client.
- Command/function: module and launcher `--help`; `main()` with no command, only `log-file`, unknown flags, missing positionals, or an invalid integer.
- Prerequisites/fixtures: config and factory constructors that fail if called on parser errors.
- Steps: Invoke root and both operation help paths; invoke every incomplete or malformed form.
- Expected stdout/stderr/exit: Help text on stdout and exit `0`; parser errors as one JSON envelope on stdout with `exit_code: 1`; no traceback, secret, config call, SDK call, or download path.
- Cleanup: Restore arguments and capture streams.
- Evidence mapping: DESIGN-010 unit coverage and story AC 3 and 8; `test_help_exits_zero_and_names_operations`, `test_missing_command_returns_one_without_loading_config`, `test_argparse_failures_are_json_user_input_errors_on_stdout`.

### AUD-TC-003 - Strict dates and initial cursor rule

- Type: positive, boundary, negative.
- Behavior: Given initial and continuation list requests, when dates and cursors are validated, then real `YYYY-MM-DD` dates become `datetime.date` objects and only an initial request requires `--start-date`.
- Command/function: `_parse_iso_date()`, `_validate_list_cursor()`, `log-file list`.
- Prerequisites/fixtures: valid dates, leap day, malformed forms, impossible dates, empty token, and a non-empty token.
- Steps: Parse valid dates; run an initial request with and without start date; run a continuation with token and no start date; try malformed and impossible dates.
- Expected stdout/stderr/exit: Valid inputs reach the raw SDK fake with `date` objects and exit `0`; invalid or missing initial date writes JSON user-input error to stdout, writes no audit data to stderr, exits `1`, and skips ACL and client creation.
- Cleanup: Clear arguments and fake call records.
- Evidence mapping: DESIGN-010 date contract and story AC 1 and 3; `test_parse_iso_date_accepts_none_and_real_dates`, `test_parse_iso_date_rejects_non_strict_or_impossible_dates`, `test_initial_list_requires_start_date`, `test_continuation_token_allows_missing_start_date`, `test_main_invalid_date_stops_before_acl_and_client`.

### AUD-TC-004 - Timeout boundaries and forwarding

- Type: positive and boundary.
- Behavior: Given CLI or configured timeouts, when execution starts, then values from 1 through 3600 seconds are accepted and the selected value reaches both retry handling and the SDK request.
- Command/function: `_validate_timeout()`, both CLI operations with `--timeout`.
- Prerequisites/fixtures: values `1`, `30`, `3600`, CLI override `17`, and configured default `42`.
- Steps: Validate both boundaries and a normal value; execute with and without a CLI override; inspect retry construction and `request_timeout`.
- Expected stdout/stderr/exit: Valid requests produce one success envelope/result and exit `0`; retry and SDK receive the same chosen integer; no unexpected stderr.
- Cleanup: Restore config defaults and call records.
- Evidence mapping: ADR-002, DESIGN-010 invocation contract; `test_timeout_accepts_adr_002_bounds`, `test_main_passes_selected_timeout_to_retry_and_sdk`.

### AUD-TC-005 - Invalid timeout fails before access or SDK work

- Type: negative and boundary.
- Behavior: Given `0`, `3601`, a negative value, or a non-integer timeout, when validation runs, then the CLI rejects it before ACL, scope, client, or filesystem work.
- Command/function: `_validate_timeout()`, both CLI commands.
- Prerequisites/fixtures: guarded constructors and a fresh download root.
- Steps: Invoke each invalid value through parser or direct validation and inspect side effects.
- Expected stdout/stderr/exit: One JSON user-input envelope on stdout, no audit data or traceback on stderr, exit `1`, no ACL/client call, and no download root.
- Cleanup: Remove temporary root if a failed assertion created it.
- Evidence mapping: ADR-002 and story AC 3 and 7; `test_timeout_rejects_values_outside_adr_002_bounds`, `test_main_rejects_timeout_before_acl_or_client`.

### AUD-TC-006 - Raw first page, empty page, and continuation

- Type: positive and edge.
- Behavior: Given raw SDK pages, when list fetches its default batch or a supplied cursor, then it decodes exactly one server page, forwards every argument, and preserves the returned cursor.
- Command/function: `_fetch_list_page()`, `_list_log_files()`, `log-file list`.
- Prerequisites/fixtures: one populated page, one empty page, and one continuation page.
- Steps: Run the default request, an empty response, and a continuation without start date; inspect raw wrapper, decode count, SDK kwargs, records, and helper state.
- Expected stdout/stderr/exit: List data appears once on stdout; exit `0`; stderr metadata reports `pages_fetched: 1`, exact `total_items`, page size, and remaining token when present. Empty/non-uniform output is JSON.
- Cleanup: Reset page fakes and captures.
- Evidence mapping: DESIGN-010 pagination steps and story AC 1; `test_fetch_list_page_uses_raw_wrapper_and_decodes_sdk_page`, `test_list_default_fetches_one_raw_server_page_and_keeps_cursor`.

### AUD-TC-007 - Exact multi-page count, EOF, and 40-page cap

- Type: positive and boundary.
- Behavior: Given more pages than requested, early EOF, or more than 40 pages, when `--batch-pages` runs, then it counts actual server pages, stops at EOF, and never fetches page 41.
- Command/function: `_list_log_files()` with batches `2`, `8`, `40`, and `999`.
- Prerequisites/fixtures: deterministic cursor chain with one item per page.
- Steps: Fetch two pages; request eight where EOF occurs on page two; request 999 from a 45-page chain.
- Expected stdout/stderr/exit: Aggregated records appear once on stdout; exit `0`; metadata reports exact pages and items; the capped case makes 40 calls and returns the page-41 cursor without fetching it.
- Cleanup: Clear page chain and captured metadata.
- Evidence mapping: DESIGN-010 pagination design and story AC 2; `test_list_stops_at_eof_and_forwards_each_cursor`, `test_list_hard_caps_batch_at_40_actual_pages`.

### AUD-TC-008 - Pagination retry resets state

- Type: resilience and regression.
- Behavior: Given a transient failure on a later page, when the complete pagination attempt retries, then a fresh helper restarts from the original cursor and publishes only successful counters and records.
- Command/function: `RetryHandler.execute(_list_log_files, ...)`.
- Prerequisites/fixtures: page one succeeds, page two fails once, then both pages succeed; delay and jitter disabled.
- Steps: Execute two-page pagination; record cursors and helper counters across attempts.
- Expected stdout/stderr/exit: Call order is initial, second, initial, second; final records contain no duplicates; metadata reports two pages and two items once; exit `0`; failed-attempt output is absent.
- Cleanup: Reset retry fake and capture buffers.
- Evidence mapping: DESIGN-010 pagination retry rule and story AC 2 and 7; `test_pagination_retry_restarts_helper_without_duplicate_counts`.

### AUD-TC-009 - Retryable 503 and exhausted 429

- Type: resilience and negative.
- Behavior: Given retryable server and rate-limit responses, when retries run, then a later 503 success returns normally while exhausted 429 uses the rate-limit code.
- Command/function: list and content through `RetryHandler`.
- Prerequisites/fixtures: HTTP 503 then success; repeated HTTP 429; configured transport/timeout exception fake.
- Steps: Run each sequence and count attempts.
- Expected stdout/stderr/exit: Recovered 503 has one success result and exit `0`; exhausted 429 has one JSON error envelope on stdout and exit `7`; diagnostics remain NDJSON on stderr; no duplicate result or content leak.
- Cleanup: Clear retry state and secret sentinels.
- Evidence mapping: DESIGN-010 retry/error contract and story AC 7; `test_raw_page_retries_503_and_exhausts_429`, `test_main_serializes_exact_adr_exit_codes`.

### AUD-TC-010 - Metadata-only ACL policy and precedence

- Type: security, positive, negative.
- Behavior: Given metadata-only and operation-level overrides, when ACL evaluates `AUDIT`, then `log_file.list` is permitted, `log_file.content` is blocked, and a specific operation override wins over the namespace setting.
- Command/function: `AccessControlGuard(cfg, "AUDIT").check()` for both operations.
- Prerequisites/fixtures: packaged Audit allow-list and isolated environment variables.
- Steps: Enable global metadata-only mode; check both operations; then disable Audit metadata-only at namespace level and explicitly disable list.
- Expected stdout/stderr/exit: Permitted checks return silently; blocked CLI call writes a structured ACL envelope to stdout, exits `8`, and does not create a client or path; no secret appears in stderr.
- Cleanup: Remove every ACL environment variable.
- Evidence mapping: DESIGN-010 access-control table and story AC 5; `test_metadata_only_allows_list_and_blocks_content`, `test_acl_operation_disable_precedes_namespace_metadata_override`.

### AUD-TC-011 - ACL precedes tracing, client, and filesystem work

- Type: security and ordering.
- Behavior: Given an ACL denial and pre-existing SDK context values, when content starts, then ACL rejects before invocation scope, client construction, SDK transport, or download mutation and leaves prior context unchanged.
- Command/function: `main()` for `log-file content`.
- Prerequisites/fixtures: guard that raises `AccessControlError`; factory, scope, transport, and filesystem sentinels that fail if touched; preset B3 `ContextVar` values.
- Steps: Invoke content under denial; inspect event list, context values, and temporary root.
- Expected stdout/stderr/exit: One ACL JSON envelope on stdout, safe NDJSON or empty stderr, exit `8`; only ACL event occurs; all prior B3 values remain exact; no client call or filesystem entry.
- Cleanup: Reset B3 tokens, ACL variables, and temporary root.
- Evidence mapping: DESIGN-010 execution order and story AC 5 and 6; `test_acl_runs_before_factory_construction` plus QA assertion for context preservation.

### AUD-TC-012 - Packaged ACL policy works from arbitrary CWD

- Type: security and packaging.
- Behavior: Given an installed wheel or editable package launched outside the repo, when metadata-only ACL checks run, then the packaged allow-list is found and applies the same list/content policy.
- Command/function: installed Python process importing `_METADATA_ALLOWLIST_PATH` and `AccessControlGuard`.
- Prerequisites/fixtures: local wheel and editable installs, arbitrary empty working directory, no `PYTHONPATH`, metadata-only enabled.
- Steps: Verify the policy file exists in the wheel; install each form; run list and content checks from the arbitrary directory.
- Expected stdout/stderr/exit: Probe prints only `list=PERMITTED content=BLOCKED`, stderr is empty, exit `0`; policy path resolves inside the installed package.
- Cleanup: Delete isolated virtual environment and build directory.
- Evidence mapping: DESIGN-010 ACL and packaging contracts, story AC 5 and 8; `test_packaged_metadata_policy_is_cwd_independent`, `test_wheel_and_editable_installs_work_from_arbitrary_cwd_without_pythonpath`.

### AUD-TC-013 - Unknown-length content below limit

- Type: positive and boundary.
- Behavior: Given a public stream shorter than the byte limit, when content downloads, then the full payload is atomically published and reported as non-truncated.
- Command/function: `_download_content()` through `with_streaming_response.content`.
- Prerequisites/fixtures: three-byte stream, five-byte limit, safe filename, public-only response fake.
- Steps: Download; inspect SDK arguments, context closure, saved bytes, result envelope, and directory contents.
- Expected stdout/stderr/exit: JSON download envelope on stdout, no content on stdout/stderr, exit `0`; file contains `abc`; `file_size` and `source_size` are `3`; `truncated` is false; one published file remains.
- Cleanup: Remove the temporary download root.
- Evidence mapping: DESIGN-010 bounded content design and story AC 4; `test_content_streams_unknown_length_with_one_byte_probe` below-limit parameter.

### AUD-TC-014 - Unknown-length content exactly at limit

- Type: boundary.
- Behavior: Given content exactly equal to the limit, when the handler probes EOF, then it reports a complete download rather than truncation.
- Command/function: `_download_content()`.
- Prerequisites/fixtures: five-byte stream and five-byte limit.
- Steps: Download; inspect file, source accounting, probe completion, and response cleanup.
- Expected stdout/stderr/exit: JSON envelope only on stdout, exit `0`; file is exactly `abcde`; `file_size` and `source_size` are `5`; `truncated` is false; stream and response context close.
- Cleanup: Remove the temporary root.
- Evidence mapping: DESIGN-010 one-byte-probe rule and story AC 4; exact-limit parameter of `test_content_streams_unknown_length_with_one_byte_probe`.

### AUD-TC-015 - Unknown-length content above limit uses one probe byte

- Type: boundary and security.
- Behavior: Given content above the limit followed by a sentinel chunk, when download reaches the bound, then it stores only the allowed prefix and observes no more than one extra byte.
- Command/function: `_download_content()`.
- Prerequisites/fixtures: `abcdefghi`, unread sentinel chunk, five-byte limit, stream index counter.
- Steps: Download and inspect stored bytes, source fields, iterator reads, and context cleanup.
- Expected stdout/stderr/exit: JSON envelope on stdout, exit `0`; file contains `abcde`; `file_size: 5`, `truncated: true`, `source_size: null`, and `source_size_at_least: 6`; sentinel chunk is not read or logged.
- Cleanup: Remove the temporary root and stream fake.
- Evidence mapping: DESIGN-010 bounded content design and story AC 4; above-limit parameter of `test_content_streams_unknown_length_with_one_byte_probe`.

### AUD-TC-016 - Public streaming API and unavailable headers

- Type: structural and security.
- Behavior: Given the current SDK has no public response-header accessor, when content downloads, then the adapter uses only the public stream and passes all unavailable header values as `None`.
- Command/function: `_download_content()` and source inspection.
- Prerequisites/fixtures: public-only response fake that records attempted private access; spy `BinaryDownloadHandler`.
- Steps: Execute content; inspect handler arguments and source for eager or private SDK calls.
- Expected stdout/stderr/exit: Success JSON and exit `0`; `content_length`, `content_encoding`, and `mime_type` are `None`; namespace is `audit`; operation is `log_file.content`; no `._response` or eager `client.content()` access occurs.
- Cleanup: Restore handler class and fake response.
- Evidence mapping: DESIGN-010 bounded content step 4 and story AC 4; `test_content_passes_all_unavailable_headers_as_none`, `test_source_never_uses_eager_content_private_sdk_fields_or_w3c`.

### AUD-TC-017 - Stream failure and cancellation clean atomically

- Type: negative, cancellation, filesystem security.
- Behavior: Given a stream failure or `asyncio.CancelledError` after partial bytes, when content aborts, then no partial or temporary file remains and all stream contexts close.
- Command/function: `_download_content()` and `main()` cancellation path.
- Prerequisites/fixtures: failing byte stream for `OSError` and cancellation; fresh root.
- Steps: Run both failures after one chunk; inspect all descendants and closure flags; run cancellation through `main()`.
- Expected stdout/stderr/exit: Stream `OSError` uses a structured server-error envelope and exits `6`; cancellation uses a structured timeout envelope and exits `5`; no audit bytes, traceback, or temporary path leak; download root contains no file; stream and response context close.
- Cleanup: Remove root and restore cancellation state.
- Evidence mapping: DESIGN-010 story AC 4 and 7; `test_content_failure_or_cancellation_cleans_partial_files_and_context`, `test_main_maps_async_cancellation_to_timeout`.

### AUD-TC-018 - Failed retry leaves only successful publication

- Type: resilience and atomicity.
- Behavior: Given the first content attempt writes partial bytes and fails with a retryable transport error, when the second attempt succeeds, then the first attempt leaves nothing and exactly one complete file is published.
- Command/function: `RetryHandler.execute(_download_content, ...)`.
- Prerequisites/fixtures: first stream emits `partial` then fails; second emits `complete`; retry delay disabled.
- Steps: Execute both attempts; inspect files, bytes, attempt count, and closure flags.
- Expected stdout/stderr/exit: One success JSON envelope and exit `0`; exactly one file contains `complete`; both contexts and streams close; no partial name or content appears in stdout/stderr.
- Cleanup: Remove the temporary root.
- Evidence mapping: DESIGN-010 retry and bounded-download rules, story AC 4 and 7; `test_content_retry_removes_failed_partial_before_publishing_success`.

### AUD-TC-019 - Unsafe output names are rejected before publication

- Type: negative and path security.
- Behavior: Given traversal, absolute, separator, NUL, dot, or dot-dot filenames, when content validates the name, then it rejects the request without creating the download root or an outside file.
- Command/function: `log-file content --output-filename` and `_download_content()`.
- Prerequisites/fixtures: unsafe-name table and monitored parent directory.
- Steps: Try every unsafe name; inspect root, parent, response context, stdout, and stderr.
- Expected stdout/stderr/exit: Structured user-input envelope on stdout and exit `1`; no traceback or audit content on stderr; no root or escaped file; response context exits.
- Cleanup: Remove monitored temporary parent.
- Evidence mapping: DESIGN-010 bounded path and error contracts, story AC 4 and 7; `test_content_rejects_unsafe_filename_without_creating_download_root`.

### AUD-TC-020 - List output format and stream separation

- Type: positive, output, confidentiality.
- Behavior: Given empty, uniform, and non-uniform list records, when format is `json`, `toon`, or `auto`, then success data is written once to stdout and only pagination metadata goes to stderr.
- Command/function: `log-file list` with format options and `--pretty`.
- Prerequisites/fixtures: empty list, uniform ID list, non-uniform list, remaining cursor, secret cursor sentinel.
- Steps: Run each shape and format; parse stdout and pagination metadata independently.
- Expected stdout/stderr/exit: Exit `0`; JSON is used for empty/non-uniform auto output; TOON is used only for uniform non-empty auto output; stderr contains the separator and exact pagination fields once; audit records never appear in stderr and cursor tokens never appear in NDJSON logs.
- Cleanup: Clear captures and secret sentinels.
- Evidence mapping: DESIGN-010 pagination/output contract and story AC 1 and 2; `test_main_list_outputs_data_then_pagination_metadata_on_stderr` plus shared `OutputFormatter` coverage.

### AUD-TC-021 - Content always returns JSON metadata without content leakage

- Type: positive, output, confidentiality.
- Behavior: Given `--format json`, `toon`, or `auto`, when content succeeds, then every selection returns the standard JSON download envelope and never emits audit bytes.
- Command/function: `log-file content` with all format choices and `--pretty`.
- Prerequisites/fixtures: safe bounded stream containing the audit-body secret sentinel.
- Steps: Invoke each format; parse stdout as JSON; scan stdout, stderr, and captured logs for payload bytes, token, IDs beyond allowed metadata, and request/response bodies.
- Expected stdout/stderr/exit: Exit `0`; stdout contains one JSON metadata envelope only; stderr is empty or safe NDJSON; no raw content, token, traceback, request body, or response body appears.
- Cleanup: Remove downloaded files and clear sentinels.
- Evidence mapping: DESIGN-010 output/log contract and story AC 4 and 7; `test_main_content_forces_json_and_orders_acl_scope_client_retry` plus bounded stream tests.

### AUD-TC-022 - Structured ADR-001 parser and runtime errors

- Type: negative and error taxonomy.
- Behavior: Given each supported failure class, when the CLI exits, then it writes one JSON error envelope to stdout with the exact ADR-001 code and keeps diagnostics separate.
- Command/function: both commands through `main()`.
- Prerequisites/fixtures: user input, HTTP 401/403/404/429/503, timeout, cancellation, ACL denial, configuration failure, filesystem failure, and unexpected exception fakes.
- Steps: Inject each failure after the correct lifecycle point; parse stdout and stderr; verify skipped downstream work where applicable.
- Expected stdout/stderr/exit: Codes are user input `1`, authentication `2`, permission `3`, not found `4`, timeout/cancellation `5`, server `6`, exhausted 429 `7`, ACL `8`, and configuration `9`; error envelope is JSON on stdout; NDJSON diagnostics, if any, are on stderr; no raw traceback, token, body, content, or temporary path appears.
- Cleanup: Clear injected exceptions, secrets, and temporary roots.
- Evidence mapping: ADR-001, DESIGN-010 error contract and story AC 3, 5, and 7; `test_argparse_failures_are_json_user_input_errors_on_stdout`, `test_main_serializes_exact_adr_exit_codes`, `test_main_maps_async_cancellation_to_timeout`.

### AUD-TC-023 - B3 enabled at outbound transport

- Type: positive tracing and transport integration.
- Behavior: Given tracing is enabled, when the client is created and an SDK request is prepared, then outbound transport carries one valid B3 multi-header context.
- Command/function: `AsyncClientFactory.invocation_scope(cfg)`, SDK request preparation, list request.
- Prerequisites/fixtures: enabled tracing config, clean SDK context, transport header capture.
- Steps: Enter the real tracing scope through `main()`; capture headers at client creation and request preparation.
- Expected stdout/stderr/exit: Success result and exit `0`; every capture has lowercase-hex `X-B3-TraceId` of 32 characters, `X-B3-SpanId` of 16 characters, and `X-B3-Sampled` equal to `0` or `1`; no W3C header appears.
- Cleanup: Reset all SDK context tokens and environment variables.
- Evidence mapping: DESIGN-005 B3 contract, DESIGN-010 story AC 6; enabled parameter of `test_b3_transport_headers_enabled_disabled_retry_stable_and_restored`.

### AUD-TC-024 - B3 disabled, retry stability, and context restoration

- Type: negative, resilience, isolation.
- Behavior: Given disabled tracing, retries, prior context, or a later formatter failure, when execution leaves the invocation, then disabled calls add no B3 headers, retry attempts share one enabled context, and prior values are restored on every exit path.
- Command/function: `main()` with real `TracingProvider` scope and captured SDK transport headers.
- Prerequisites/fixtures: enabled and disabled configs; first attempt transport failure followed by success; preset prior trace/span/sampled values; formatter, SDK, timeout, and cancellation failures.
- Steps: Run disabled flow; run enabled retry flow; run each failure with prior values; inspect every outbound header set and context after exit.
- Expected stdout/stderr/exit: Disabled flow has no `X-B3-*`; enabled retry captures identical B3 values for client creation and every attempt; no `traceparent` or `tracestate`; success exits `0`; failures use their ADR code; prior context is exact after all runs with no cross-test leakage.
- Cleanup: Reset context tokens in `finally`, clear trace environment variables, and clear captures.
- Evidence mapping: DESIGN-005 isolation contract, DESIGN-010 story AC 6 and 7; `test_b3_transport_headers_enabled_disabled_retry_stable_and_restored`, `test_b3_scope_restores_prior_values_after_formatter_failure`, `test_source_never_uses_eager_content_private_sdk_fields_or_w3c`.

### AUD-TC-025 - Import, console boundary, help, and thin launcher

- Type: packaging and side-effect regression.
- Behavior: Given the package and Claude launcher, when imported or asked for help, then they load without configuration, network, or filesystem side effects and use one event-loop boundary.
- Command/function: package import, launcher import, module `--help`, launcher `--help`, `console_main()`.
- Prerequisites/fixtures: empty arbitrary directory; guarded config/network/filesystem constructors; `asyncio.run` spy.
- Steps: Import all Audit modules and launcher; invoke root and operation help; call `console_main()` with fake `main()`; inspect launcher source.
- Expected stdout/stderr/exit: Imports produce no output or files; help exits `0` and names exactly both operations; `console_main()` calls `asyncio.run()` once and propagates the result; launcher delegates to packaged interfaces and contains no copied catalog, streaming, or ACL logic.
- Cleanup: Remove subprocess directory and restore the event-loop spy.
- Evidence mapping: DESIGN-010 packaging contract and story AC 8; `test_console_main_uses_one_asyncio_run_boundary`, `test_claude_launcher_is_thin_and_reexports_packaged_interfaces`, `test_imports_create_no_download_directory_or_network_side_effect`, help tests.

### AUD-TC-026 - Wheel, editable install, entry-point preservation, and regression

- Type: installation and regression.
- Behavior: Given local wheel and editable installs, when commands run from an arbitrary directory without `PYTHONPATH`, then `foundry-audit` and the Claude launcher work while existing console scripts and repository gates remain intact.
- Command/function: local wheel build; wheel and editable install; installed `foundry-audit --help`; Claude launcher help; full test, Ruff, mypy, and package checks.
- Prerequisites/fixtures: isolated virtual environments for Python 3.11 and 3.12; `PIP_NO_INDEX=1`; local build dependencies; snapshot of existing `[project.scripts]` entries.
- Steps: Build without live dependency resolution; inspect wheel for the Audit policy; install wheel then editable form with `--no-deps`; run help and packaged ACL probe from arbitrary CWD; compare every pre-existing entry point; run focused Audit tests and full regression with branch coverage.
- Expected stdout/stderr/exit: Every help and package check exits `0`; wheel contains `foundry_cli/audit/metadata-allow-list.md`; both operations are listed; all prior console scripts remain; focused and full suites pass on both Python versions; Ruff and mypy pass; repository branch coverage is at least 80%; no command makes a live Foundry request.
- Cleanup: Delete isolated builds and environments; retain command output in TESTEXEC evidence only.
- Evidence mapping: DESIGN-010 packaging and regression contract, story AC 8; all `tests/test_audit_console_wrapper.py` cases and the configured `pyproject.toml` gates.

## Traceability matrix

| Requirement area | Story/design criteria | Cases |
|---|---|---|
| Two operations, catalog, parser, nested routing | Story AC 1, 4, 8; operation catalog | AUD-TC-001, 002 |
| Dates, cursor, timeout 1-3600 | Story AC 1, 3, 7; date and invocation contracts | AUD-TC-003, 004, 005 |
| Raw exact-page pagination, counts, cap, reset | Story AC 1, 2 | AUD-TC-006 through 009 |
| ACL policy, precedence, ordering, packaged policy | Story AC 5 | AUD-TC-010 through 012 |
| Unknown-length bound, probe, atomic cleanup, cancellation, paths | Story AC 4, 7 | AUD-TC-013 through 019 |
| JSON/TOON, stdout/stderr, NDJSON, confidentiality | Story AC 1, 2, 4, 7 | AUD-TC-020 through 022 |
| B3 enabled/disabled/retry/restore; no W3C | Story AC 6 | AUD-TC-011, 023, 024 |
| Imports, console, launcher, wheel/editable installs, arbitrary CWD | Story AC 8 | AUD-TC-012, 025, 026 |
| Positive, negative, boundary, security, cancellation, regression | Complete design strategy | AUD-TC-001 through 026 |

All eight story acceptance criteria have at least one positive case and, where meaningful, a negative, boundary, security, or failure-path case.

## Execution and approval criteria

TESTEXEC-010 may begin only after DEV, UNITTEST, CODEREVIEW, and TESTCASE-010 reach their required completed states and the approved commit is available. Execute all 26 cases with no live network access.

For every case, record PASS, FAIL, or BLOCKED with the exact command, environment, expected result, actual result, stdout, stderr, exit code, cleanup result, and linked evidence. Any failure requires a BUG-SUB before TESTEXEC-010 can close. Final QA sign-off also requires all linked defects to be terminal, all eight story acceptance criteria to have passing evidence, supported Python checks to pass, and repository branch coverage to remain at least 80%.
