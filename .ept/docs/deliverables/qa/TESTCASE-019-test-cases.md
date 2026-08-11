# TESTCASE-019 - Foundry Checkpoints CLI QA test cases

## Scope

These cases cover DEV-STORY-019 and the complete approved surface of `foundry-checkpoints`: the 3 public `foundry_sdk.v2.checkpoints` operations on the single `Record` client path (`record.get`, `record.get_batch`, `record.search`). They verify the exact catalog and parser, nested SDK routing through `client.checkpoints.Record`, JSON argument validation (`--where-json`, `--records-json`), the cursor-paginated `record search` command through `PaginationHelper`, the `get_batch` positional-body dispatch, the zero-write semantic-read ACL classification, the packaged 3-permitted/0-blocked metadata-only policy, `include_attribution=False`, B3 tracing, retry and error behavior, output and log contracts, privacy, packaging, and regression gates.

> **Acceptance criteria note:** The DEV-STORY-019 ticket body's Acceptance Criteria field still carries the grooming template placeholder; the authoritative acceptance criteria for this story are the DESIGN-019 contract sections (operation catalog, paging contract, access and runtime policy), the story scope comment, and the populated `release_notes` field ("adds foundry-checkpoints CLI (3 operations: record get, record get-batch, record search) with shared access control, pagination for record search, B3 tracing, retry, output formatting, and packaged metadata-only policy").
>
> **Operation count note:** The story title and SAD-001 reference "3 operations". The vendored SDK (v1.102.0) exposes exactly **3** public operations on `Record` (`get`, `get_batch`, `search`). The canonical environment-variable reference and the metadata allow-list are concordant at 3 rows each. The count is confirmed accurate; no correction is required.

Routine acceptance uses mocked async SDK transport and real installed SDK exception classes. Live credentials and live Foundry access are not required. An approved non-production smoke is optional and cannot replace the mandatory mocked evidence.

## Source baseline

- [DESIGN-019](../architecture/DESIGN-019-checkpoints-cli.md), completed and closed for DEV-STORY-019.
- [DESIGN-005](../architecture/DESIGN-005-common-components.md), covering SDK-native B3 tracing, retry, and pagination integration contracts.
- [DESIGN-011](../architecture/DESIGN-011-aip-agents-cli.md), [DESIGN-012](../architecture/DESIGN-012-language-models-cli.md), [DESIGN-013](../architecture/DESIGN-013-models-cli.md) — the sibling namespace patterns this story mirrors (immutable operation catalog, exact nested SDK dispatch, packaged policy, cursor pagination via `PaginationHelper`).
- [ADR-001](../architecture/adr/ADR-001-exit-code-taxonomy.md), [ADR-002](../architecture/adr/ADR-002-call-timeout-defaults.md), [ADR-004](../architecture/adr/ADR-004-format-auto-algorithm.md), [ADR-005](../architecture/adr/ADR-005-log-format.md), [ADR-006](../architecture/adr/ADR-006-env-file-search-path.md), [ADR-007](../architecture/adr/ADR-007-operation-level-readonly.md).
- The canonical environment-variable reference and metadata allow-list (namespace `checkpoints`, 3 rows; `checkpoints.record.get`, `checkpoints.record.get_batch`, `checkpoints.record.search` all PERMITTED in tier 3).
- Vendored SDK sources under `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/checkpoints/` — the real `Record` client methods, request paths, and result types (`Record`, `GetRecordsBatchResponse`, `SearchCheckpointRecordsResponse` with `data` + `next_page_token`).
- DEV-STORY-019 ticket body, `release_notes`, and technical scope comment (authoritative 3-operation catalog).
- Implementation verified at commit `b0df380`: `src/foundry_cli/checkpoints/` (scripts/`foundry_checkpoints_cli.py`, `metadata-allow-list.md`), `pyproject.toml` entry point `foundry-checkpoints` (L42), package data for the metadata allow-list (L58), Ruff E402 scope (L90). The `.claude/skills/foundry-checkpoints/` skill and launcher are under the CODEREVIEW-019 P1 correction (in flight); the launcher-related verification steps in CKP-TC-020/021 are conditioned on that correction landing and on the packaged console entry point, which exists.

## Preconditions and shared fixtures

- Python 3.11 and 3.12 environments contain the project, development dependencies, and pinned `foundry-sdk`.
- Use a nested async SDK fake rooted at `client.checkpoints` with exactly one public sub-client: `Record` (`get`, `get_batch`, `search`) and its `with_raw_response.search` accessor. A wrong, flattened, raw, or streaming route must fail the fixture. No other sub-client may be reachable from any catalog dispatch.
- `record search` uses `client.checkpoints.Record.with_raw_response.search` through `PaginationHelper`; page fakes return `SimpleNamespace(data=[...], next_page_token=...)` so empty pages decode safely. No `PaginationHelper` may be invoked for `record get` or `record get-batch`.
- `record get-batch` fakes record the positional body list; the decoded `--records-json` array is appended positionally and never forwarded as a keyword.
- Use real installed SDK model validators for nested invalid-input checks and real `foundry_sdk._errors` classes for error taxonomy checks. Mock network transport; no service call is permitted.
- Set retry delay to zero, disable jitter, and use two retries unless a case states otherwise. Capture attempt number, timeout, attribution, and B3 values.
- Capture stdout, stderr, logs, SDK arguments, context variables, client/network constructors, and filesystem changes independently. Do not retain credential, token, JSON-body, or response sentinel values.
- The one cursor-paged command emits pagination metadata (`pages_fetched`, `total_items`, `next_page_token`, `page_size`) as compact JSON to stderr via `PaginationHelper.emit_metadata()` per ADR-005. No download root or `BinaryDownloadHandler` is required by any case.
- Packaging cases build a clean local archive with dependency resolution disabled, install with `--no-deps`, and run from an arbitrary empty working directory without `PYTHONPATH`.
- Any optional live smoke uses an approved non-production Foundry tenant, synthetic checkpoint records, least-privilege credentials, and a cleanup plan. Credentials must never enter retained evidence.
- TESTEXEC records the commit, OS, Python and SDK versions, environment type, exact command, expected and actual stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, evidence reference, and PASS/FAIL/BLOCKED status for every case.

## Test data

| Name | Fixture |
| --- | --- |
| Record RID | `ri.checks.main.record.qa-001` (valid 5-segment RID) |
| Batch body JSON | `[{"recordRid": "ri.checks.main.record.qa-001"}, {"recordRid": "ri.checks.main.record.qa-002"}]` |
| Batch size variants | empty array `[]`; one element; the 100-element SDK bound; a 101-element array |
| Search where JSON | `{"type": "eq", "field": "status", "value": "ok"}` (object required) |
| Where shape variants | `[]` (array), `"text"` (scalar), `null`, malformed JSON text, nested field violating SDK validators |
| Sort direction | `ASC`, `DESC`, invalid `SIDEWAYS` |
| List page fakes | empty page; one page with `next_page_token`; two pages with `next_page_token`; exhausted page token |
| Pagination flags | `--page-size 50`, `--page-token <tok>`, `--all`, `--max-pages 3`, `--max-pages 0`, `--page-size 0` |
| Timeout boundaries | `1`, `30` (default), `3600`; invalid `0`, `3601`, non-integer text |
| Secret sentinels | `sentinel-secret-019`, `sentinel-token-secret`, `sentinel-body-secret`, `sentinel-response-secret`, `sentinel-attribution-rid` |

## Command and route inventory

Every inventory row is exercised by CKP-TC-001 through CKP-TC-003. Unless a case states otherwise, success writes one formatted result to stdout, writes no application data to stderr, exits `0`, and leaves no command-specific file.

| CLI command | Exact public SDK route and method | Required input | Optional input |
| --- | --- | --- | --- |
| `record get RECORD_RID` | `client.checkpoints.Record.get` | `record_rid` | shared options |
| `record get-batch --records-json ...` | `client.checkpoints.Record.get_batch` | `--records-json` (JSON array) | shared options |
| `record search --where-json ...` | `client.checkpoints.Record.search` | `--where-json` | `--page-size`, `--page-token`, `--all`, `--max-pages`, `--sort-direction`, shared options |

`record search` routes through `client.checkpoints.Record.with_raw_response.search`; `record get` and `record get-batch` route through the plain `Record` accessor. No command may receive `attribution`, `preview`, `_sdk_internal`, an absent optional set to `None`, or any unsupported paging, stream, raw-response, or file flag. Pagination flags (`--page-size`, `--page-token`, `--all`, `--max-pages`) may exist only on `record search`.

## Test cases

### CKP-TC-001 - Catalog, parser, help, and exact 3 surface

- Type: positive, structural, negative parser.
- Given the installed module and launcher, when the catalog and parser are inspected, then exactly 3 unique SDK specifications exist (all on the single `record` resource), every inventory command parses, and pagination flags exist only on `record search`.
- Command/function: `OP_SPECS`, `build_parser()`, `_spec_for()`, `_get_client()`, root/resource/operation `--help`, `main()` with missing resource/operation, unknown flags, missing required positionals/options, invalid choices/types.
- Prerequisites/fixtures: guarded config, client, network, and filesystem constructors.
- Steps: count `OP_SPECS`; assert `PAGINATED_OPS == {("record", "search")}`; assert `--page-size`/`--page-token`/`--all`/`--max-pages` exist on `record search` and on no other command; parse all 3 inventory commands; run all help surfaces; run every incomplete or malformed form (missing resource, missing operation, unknown operation, unknown flag, missing required positional/option, invalid `--format` choice).
- Expected stdout/stderr/exit: help on stdout and exit `0`; catalog count exactly `3`; parser errors as one JSON envelope on stdout with `exit_code: 1`, empty diagnostic stderr, no traceback, no config/client/network/filesystem call.
- Cleanup: restore `sys.argv` and capture streams.
- Evidence mapping: DESIGN-019 catalog; story scope comment and release_notes; `test_catalog_contains_exact_3_operations`, `test_catalog_marks_exactly_one_paginated_operation`, `test_parser_accepts_every_declared_argument`, `test_parser_rejects_unknown_operation`, `test_pagination_flags_only_on_record_search` (tests/test_foundry_checkpoints_cli.py); verified live at HEAD `b0df380` (probe: `CHECKPOINTS_OP_SPECS: 3`, `PAGINATED_OPS: [('record', 'search')]`).

### CKP-TC-002 - Nested SDK routing through the single Record client path

- Type: positive, structural, route identity.
- Given a fake for `client.checkpoints.Record`, when every inventory command runs, then each resolves the exact `Record` object and never a flattened or sibling route.
- Command/function: `_get_client()` (roots at `root_client.checkpoints`, then walks `("Record",)`) and each dispatch path.
- Prerequisites/fixtures: fakes whose sibling routes fail on access.
- Steps: run one command per operation; assert the resolved resource object identity; assert no flattened `checkpoints.*` method call.
- Expected stdout/stderr/exit: success results on stdout once, exit `0`, no unexpected stderr; no flattened `checkpoints.*` method call.
- Cleanup: reset fakes and captures.
- Evidence mapping: DESIGN-019 nested dispatch; story AC 1; `test_catalog_contains_exact_3_operations` (all three resolve through the single `Record` client path) plus the dispatch tests `test_get_dispatches_to_record_get`, `test_get_batch_dispatches_body_positionally`, `test_search_dispatches_where_and_optionals`.

### CKP-TC-003 - Required inputs forwarded and absent optionals omitted

- Type: positive, structural.
- Given each inventory command, when dispatch runs, then required positionals/options reach the SDK call and every absent optional is omitted (never `None`).
- Command/function: all 3 dispatches; `_build_kwargs()`.
- Prerequisites/fixtures: recording SDK fakes.
- Steps: run `record get` with only the RID; run `record get-batch` with only `--records-json`; run `record search` with only `--where-json`, then with `--sort-direction`, then with every optional set; inspect the SDK call arguments.
- Expected stdout/stderr/exit: `record.get` receives the positional `record_rid` plus `request_timeout`; `record.get_batch` receives the decoded body list positionally (never as a keyword) plus `request_timeout`; `record.search` receives the decoded `where` dict and `sort_direction` (when provided) and never `page_size`/`page_token` (they come from the pagination path); absent optionals absent from kwargs; success exits `0`.
- Cleanup: clear fake call records.
- Evidence mapping: DESIGN-019 operation catalog; story AC 1; `test_get_dispatches_to_record_get`, `test_get_batch_dispatches_body_positionally`, `test_search_dispatches_where_and_optionals`.

### CKP-TC-004 - JSON argument validation before client creation

- Type: positive, negative, boundary.
- Given the structured flags `--where-json` (object) and `--records-json` (array), when validation runs, then valid JSON with the documented top-level shape reaches the SDK and invalid or mis-shaped JSON exits `1` before client or network work.
- Command/function: `_parse_json_object()`, `_parse_json_list()`, `_validate_inputs()`, `main()`.
- Prerequisites/fixtures: guarded factory/network constructors; real SDK validators for nested checks.
- Steps: supply a valid where object and a valid records array; supply malformed JSON text; supply valid JSON with the wrong top-level type (where as array/scalar, records as object); supply JSON whose nested fields violate SDK validators (e.g. a batch element without `recordRid`).
- Expected stdout/stderr/exit: valid inputs call the SDK and exit `0`; invalid inputs write one JSON user-input envelope to stdout, exit `1`, no traceback, and never echo the input payload into stdout/stderr/logs.
- Cleanup: clear captured sentinels.
- Evidence mapping: DESIGN-019 JSON validation contract; story AC 2; `test_invalid_where_json_rejected_before_client`, `test_where_json_must_be_object`, `test_invalid_records_json_rejected_before_client` (tests/test_foundry_checkpoints_cli.py).

### CKP-TC-005 - Pagination contract: record search defaults to a single page and emits metadata

- Type: positive, boundary, structural.
- Given a `SearchCheckpointRecordsResponse`-shaped page fake, when `record search` runs without pagination flags, then one page is fetched with the default page size (100, `FOUNDRY_AGENTIC_CLI_DEFAULT_PAGE_SIZE`) and the aggregated items are printed on stdout while pagination metadata is emitted to stderr.
- Command/function: `record search` dispatch; `_fetch_raw_page()`, `_resolve_pagination_flags()`, `_paginate_operation()`, `PaginationHelper.paginate()` and `emit_metadata()`.
- Prerequisites/fixtures: a one-page fake with a `next_page_token`; a fake that returns an empty page; `HARD_MAX_BATCH_PAGES = 40`, `MAX_BATCH_PAGES` default 40, default page size 100.
- Steps: run with no pagination flags against a page that returns items plus a next token; run against an empty page; assert the default page size and single page fetch; inspect stderr metadata.
- Expected stdout/stderr/exit: success array on stdout and exit `0`; exactly one page fetched; stderr carries one metadata block per ADR-005 (`pages_fetched`, `total_items`, `next_page_token`, `page_size`); no metadata on `record get` or `record get-batch`.
- Cleanup: clear page fakes and captures.
- Evidence mapping: DESIGN-019 paging contract; story AC 3; `test_record_search_uses_raw_response_and_helper`, `test_record_search_defaults_to_single_page` (raw-response decode and `SimpleNamespace(data=...)` empty-page guard), plus shared `PaginationHelper` tests in tests/test_pagination_helper.py.

### CKP-TC-006 - Pagination contract: page bounds, resume token, and degenerate values

- Type: positive, boundary, negative.
- Given the same pagination surface, when `record search` runs with `--page-size`/`--page-token`/`--all`/`--max-pages`, then the effective page batch respects `FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES` (hard cap 40, `--all` selects the cap) and degenerate values (`--max-pages 0`, non-positive `--page-size`) are rejected as user input before ACL/client/network work.
- Command/function: `record search` dispatch; `PaginationHelper` bound validation.
- Prerequisites/fixtures: multi-page fakes; env `FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES` set to `3` and unset.
- Steps: run with `--page-size 50`; run with `--page-token` resume; run `--max-pages 3`; run `--all` with env cap `3`; run `--max-pages 0`; run `--page-size 0`.
- Expected stdout/stderr/exit: valid bounds fetch the documented page count and exit `0` with one aggregated array; `--max-pages 0` and `--page-size 0` write one JSON user-input envelope on stdout and exit `1` before ACL/client/network work; metadata emitted to stderr.
- Cleanup: restore env and call records.
- Evidence mapping: DESIGN-019 paging contract; story AC 3; `test_record_search_defaults_to_single_page`, `test_catalog_marks_exactly_one_paginated_operation`, shared `PaginationHelper` bound tests in tests/test_pagination_helper.py.

### CKP-TC-007 - get_batch positional body dispatch and 100-element SDK bound

- Type: positive, boundary, negative.
- Given a `--records-json` array, when `record get-batch` runs, then the decoded list is appended positionally to the SDK call (never a keyword) and the batch is bounded at 100 elements by the SDK contract, with a 101-element input surfacing as a user-input error through the SDK validator.
- Command/function: `record get-batch` dispatch; `_invoke()`; `_build_kwargs()`.
- Prerequisites/fixtures: recording SDK fake; batch fixtures `[]`, `[1]`, 100 elements, 101 elements.
- Steps: run each batch size; assert the positional body bytes/list on the SDK call; verify no `records` keyword is ever forwarded; attempt the 101-element batch.
- Expected stdout/stderr/exit: valid batches (0..100) call `Record.get_batch` with the exact decoded list and exit `0`; a 101-element batch writes one JSON user-input envelope on stdout and exits `1` (SDK `ValidationError` classified as user input) with no client retry or network call.
- Cleanup: clear fake call records and captures.
- Evidence mapping: DESIGN-019 batch contract (get_batch body bounded at 100 by SDK); story AC 2; `test_get_batch_dispatches_body_positionally` (tests/test_foundry_checkpoints_cli.py).

### CKP-TC-008 - Timeout boundaries and forwarding

- Type: positive, boundary, negative.
- Given CLI or configured timeouts, when execution starts, then values from 1 through 3600 seconds are accepted and the selected value reaches both retry handling and the SDK request; invalid values are rejected before ACL, scope, client, or filesystem work.
- Command/function: `_validate_timeout()`, representative commands with `--timeout`.
- Prerequisites/fixtures: values `1`, `30` (default), `3600`, CLI override `17`, configured default `42`, invalid `0`, `3601`, negative, and non-integer text.
- Steps: validate boundaries; execute with and without a CLI override; inspect retry construction and `request_timeout`; invoke each invalid value.
- Expected stdout/stderr/exit: valid requests produce one success result and exit `0`; retry and SDK receive the same chosen integer; invalid values write one JSON user-input envelope on stdout and exit `1` with no ACL/client/network call.
- Cleanup: restore config defaults and call records.
- Evidence mapping: ADR-002, DESIGN-019 invocation contract; story AC 12; `test_timeout_accepts_adr_002_bounds`, `test_invalid_timeout_stops_before_acl_or_client` (tests/test_foundry_checkpoints_cli.py).

### CKP-TC-009 - ACL precedence: global, namespace, and operation scopes

- Type: security, positive, negative.
- Given metadata-only and operation-level overrides, when ACL evaluates `CHECKPOINTS`, then permissive settings allow, blocking settings deny, and an operation override wins over the namespace setting.
- Command/function: `AccessControlGuard(cfg, "CHECKPOINTS").check()` for the 3 catalog operations.
- Prerequisites/fixtures: packaged Checkpoints allow-list and isolated environment variables.
- Steps: enable global metadata-only; check all 3 operations; disable Checkpoints metadata-only at namespace level; disable one operation explicitly; combine namespace read-only with an operation override.
- Expected stdout/stderr/exit: permitted checks return silently; blocked CLI calls write a structured ACL envelope to stdout, exit `8`, and do not create a client; the denying rule appears on stderr diagnostics; no secret appears.
- Cleanup: remove every ACL environment variable.
- Evidence mapping: DESIGN-019 access-control table; story AC 7; `test_readonly_permits_all_three_operations`, `test_metadata_only_permits_exactly_3_blocks_0`, `test_metadata_only_runtime_permits_all_three` (precedence exercised through the namespace runtime checks).

### CKP-TC-010 - Read-only mode permits all 3 semantic reads

- Type: security, positive.
- Given read-only mode enabled, when each command runs, then `record get`, `record get-batch`, and `record search` all succeed because the namespace has zero write operations, including the two POST-but-read operations (`get_batch`, `search`).
- Command/function: `AccessControlGuard` + `main()` for all 3 operations.
- Prerequisites/fixtures: read-only environment; guarded factory/transport; response fakes.
- Steps: run all 3 commands under read-only; inspect event order.
- Expected stdout/stderr/exit: each command exits `0` and reaches the SDK; no ACL envelope is emitted; no write classification exists in the catalog.
- Cleanup: clear read-only variables, captures, and records.
- Evidence mapping: DESIGN-019 read-only policy (zero-write namespace); story AC 7; `test_readonly_permits_all_three_operations` (tests/test_foundry_checkpoints_cli.py).

### CKP-TC-011 - Metadata-only tier: exact 3 permitted / 0 blocked

- Type: security, positive, negative.
- Given metadata-only mode, when every operation is checked, then exactly the 3 documented reads (`record.get`, `record.get_batch`, `record.search`) are permitted and nothing is blocked.
- Command/function: `AccessControlGuard` metadata-only evaluation over the full 3-op catalog.
- Prerequisites/fixtures: packaged Checkpoints allow-list; the full catalog.
- Steps: assert the permitted set equals the 3 documented reads; assert no operation in the catalog is blocked.
- Expected stdout/stderr/exit: 3 permitted checks return silently; no ACL envelope is ever emitted; no client or file effect.
- Cleanup: clear metadata-only variables.
- Evidence mapping: DESIGN-019 metadata policy; story AC 8; `test_metadata_only_permits_exactly_3_blocks_0` and `test_metadata_only_runtime_permits_all_three`; verified live at HEAD `b0df380` (packaged allow-list lists all 3 as PERMITTED).

### CKP-TC-012 - Packaged metadata-only policy is fail closed and CWD independent

- Type: security, packaging, negative.
- Given the installed package with a missing or malformed packaged allow-list, when ACL runs, then it fails closed (no operation permitted) and the packaged policy resolves from an arbitrary working directory.
- Command/function: `_METADATA_ALLOWLIST_PATH`, `AccessControlGuard` from an installed wheel/editable launch.
- Prerequisites/fixtures: malformed/missing policy fixtures in an isolated environment; empty arbitrary CWD, no `PYTHONPATH`.
- Steps: probe policy path from the installed package; run a permitted-class check with malformed policy; run checks from the arbitrary CWD.
- Expected stdout/stderr/exit: malformed/missing policy blocks even previously-permitted operations (fail closed, exit `8`); packaged policy path resolves inside the installed package; valid packaged policy applies the 3/0 rule from any CWD.
- Cleanup: delete isolated environments and fixtures.
- Evidence mapping: DESIGN-019 fail-closed rule; story AC 8, 14; `test_metadata_only_permits_exactly_3_blocks_0` (parsed from the packaged allow-list); packaged-policy CWD independence follows the same pattern as `test_packaged_metadata_policy_is_cwd_independent` (tests/test_foundry_audit_cli.py) and is verified by the TESTEXEC-019 wheel/editable probe.

### CKP-TC-013 - include_attribution=False on client and invocation scope

- Type: positive, privacy, structural.
- Given a real factory and `invocation_scope`, when any command executes, then client creation and scope use `include_attribution=False`, no attribution environment handling is added, and surrounding attribution state is unchanged after success and failure.
- Command/function: `AsyncClientFactory.invocation_scope(cfg)`, `factory.create(cfg)`, `main()`.
- Prerequisites/fixtures: factory/scope spies; preset outer attribution RID and environment.
- Steps: execute a read and a failed command; capture `include_attribution` on client and scope; capture attribution state before and after.
- Expected stdout/stderr/exit: both capture points pass `include_attribution=False`; no attribution variable is read or written; outer attribution state and env are identical after success and failure; no W3C `traceparent`/`tracestate`.
- Cleanup: reset context tokens and env.
- Evidence mapping: DESIGN-019 attribution rule (namespace outside FR-ATTR-4); story AC 9; `test_invocation_uses_include_attribution_false` (tests/test_foundry_checkpoints_cli.py).

### CKP-TC-014 - B3 enabled at outbound transport

- Type: positive, tracing, transport integration.
- Given tracing enabled, when the client is created and an SDK request is prepared, then outbound transport carries one valid B3 multi-header context.
- Command/function: `AsyncClientFactory.invocation_scope(cfg)`, SDK request preparation, a representative read.
- Prerequisites/fixtures: enabled tracing config, clean SDK context, transport header capture.
- Steps: enter the real tracing scope through `main()`; capture headers at client creation and request preparation.
- Expected stdout/stderr/exit: success result and exit `0`; every capture has lowercase-hex `X-B3-TraceId` of 32 characters, `X-B3-SpanId` of 16 characters, and `X-B3-Sampled` `0` or `1`; no W3C header appears.
- Cleanup: reset SDK context tokens and environment variables.
- Evidence mapping: DESIGN-005 B3 contract; story AC 10; `test_b3_transport_headers_enabled_disabled_retry_stable_and_restored` (tests/test_foundry_audit_cli.py) and `test_generated_context_has_valid_nonzero_b3_values_and_resets` (tests/test_tracing_provider.py); the namespace outbound-header probe is recorded in TESTEXEC-019 evidence.

### CKP-TC-015 - B3 disabled, retry stability, and context restoration

- Type: negative, resilience, isolation.
- Given disabled tracing, retries, prior context, or a later formatter failure, when execution leaves the invocation, then disabled calls add no B3 headers, retry attempts share one enabled context, and prior values are restored on every exit path.
- Command/function: `main()` with real `TracingProvider` scope and captured SDK transport headers.
- Prerequisites/fixtures: enabled and disabled configs; first-attempt transport failure followed by success; preset prior trace/span/sampled values; formatter, SDK, timeout, and cancellation failures.
- Steps: run the disabled flow; run the enabled retry flow; run each failure with prior values; inspect every outbound header set and context after exit.
- Expected stdout/stderr/exit: disabled flow has no `X-B3-*`; enabled retry captures identical B3 values for client creation and every attempt; no `traceparent`/`tracestate`; success exits `0`; failures use their ADR code; prior context is exact after all runs with no cross-test leakage.
- Cleanup: reset context tokens in `finally`, clear trace env vars, clear captures.
- Evidence mapping: DESIGN-005 isolation contract; story AC 10, 11; `test_b3_scope_restores_prior_values_after_formatter_failure` (tests/test_foundry_audit_cli.py) and `test_execute_traced_carries_same_b3_context_across_attempts_and_restores` (tests/test_tracing_provider.py).

### CKP-TC-016 - Retry behavior and cursor state preserved across page retries

- Type: resilience, negative, boundary.
- Given retryable and non-retryable failures, when `RetryHandler` wraps a command, then transient conditions (503, exhausted 429, configured transport exceptions) are retried per ADR-002 and validation, authorization, and permanent errors are never retried; because all 3 operations have no mutating or billable side effects, all are safe to retry and no at-least-once disclosure is required, and `record search` preserves its local cursor state across page retries.
- Command/function: `RetryHandler` around `record get`, `record get-batch`, and `record search` (including `_paginate_operation` page fetches).
- Prerequisites/fixtures: HTTP 503-then-success; repeated 429; 400/401/403/404; delay and jitter disabled; attempt counters; a page fetch that fails once mid-pagination then succeeds with the same token.
- Steps: run each sequence and count attempts; verify reads are retried safely and no disclosure text is produced; run the mid-pagination failure and verify the cursor token is re-sent and pages do not duplicate or skip.
- Expected stdout/stderr/exit: recovered 503 has one success result and exit `0`; exhausted 429 exits `7`; validation/auth/permanent errors exit once with codes `1`/`2`/`3`/`4`; no duplicate result or content leak; cursor state yields exactly the documented item set.
- Cleanup: clear retry state and sentinels.
- Evidence mapping: ADR-001/002, DESIGN-019 retry contract (all three safe, no disclosure); story AC 11; retry tests in tests/unit_test_retry_error_output_log.py (`test_http_429_and_503_are_retryable`, `test_http_non_429_503_does_not_retry`, `test_success_after_one_retry`, `test_retry_exhaustion_raises`); cursor preservation across page retries is verified by `test_record_search_uses_raw_response_and_helper` plus the `PaginationHelper` paginate tests in tests/test_pagination_helper.py.

### CKP-TC-017 - ADR-001 error taxonomy and structured envelopes

- Type: negative, error taxonomy.
- Given each supported failure class, when the CLI exits, then it writes one JSON error envelope to stdout with the exact ADR-001 code and keeps diagnostics separate on stderr.
- Command/function: representative commands through `main()` and `_serialize_error()`.
- Prerequisites/fixtures: user input, HTTP 401/403/404/429/503, timeout, cancellation, ACL denial, configuration failure, and unexpected exception fakes.
- Steps: inject each failure after the correct lifecycle point; parse stdout and stderr; verify skipped downstream work where applicable.
- Expected stdout/stderr/exit: codes are user input `1`, authentication `2`, permission `3`, not found `4`, timeout/cancellation `5`, server `6`, exhausted 429 `7`, ACL `8`, and configuration `9`; error envelope is JSON on stdout; NDJSON diagnostics, if any, are on stderr; no raw traceback, token, or body appears.
- Cleanup: clear injected exceptions, secrets, and temporary files.
- Evidence mapping: ADR-001, DESIGN-019 error contract; story AC 12, 13; `test_unknown_operation_returns_user_input_error`, `test_missing_operation_returns_user_input_error`, `test_sdk_error_maps_to_exit_code` (tests/test_foundry_checkpoints_cli.py) plus the shared error-taxonomy tests in tests/unit_test_retry_error_output_log.py (`test_auth_error_exit_code_2` through `test_http_503_returns_server_error_after_retry_exhaustion`).

### CKP-TC-018 - Output formats: JSON, TOON, auto, and pretty

- Type: positive, output, boundary.
- Given success results of each shape, when `--format json|toon|auto` and `--pretty` run, then single models, `GetRecordsBatchResponse` maps, and paginated arrays follow the ADR-004 rules.
- Command/function: `OutputFormatter` via representative commands.
- Prerequisites/fixtures: a single `Record`, a `GetRecordsBatchResponse` (record-batch map), a uniform list array from `record search`, an empty list array, structured error.
- Steps: run each shape under each format; validate stdout parses as JSON where required; verify pretty indentation when enabled.
- Expected stdout/stderr/exit: exit `0`; auto selects TOON only for uniform non-empty arrays, otherwise JSON; empty/non-uniform output is JSON; single models serialize as JSON; error output remains the structured JSON envelope.
- Cleanup: clear captures and models.
- Evidence mapping: ADR-004, DESIGN-019 output contract; story AC 12; `test_output_toon_and_json_formats` (tests/test_foundry_checkpoints_cli.py) plus shared `OutputFormatter` coverage in tests/unit_test_retry_error_output_log.py.

### CKP-TC-019 - NDJSON stderr, stream separation, and confidentiality

- Type: positive, output, confidentiality.
- Given successful get, get-batch, and search runs, when logs and results flow, then success data appears once on stdout, diagnostics are NDJSON on stderr, and credential/body/response sentinels never appear anywhere.
- Command/function: representative `record get`, `record get-batch`, and `record search` commands.
- Prerequisites/fixtures: secret sentinels embedded in request/response fixtures; captured logs.
- Steps: run each command; scan stdout, stderr, and captured logs for sentinel values, raw request bodies, and secret values.
- Expected stdout/stderr/exit: exit `0`; stdout carries results/metadata envelopes only; stderr carries NDJSON diagnostics only (empty or safe); none of the sentinels, payloads, or bodies appear in any stream or log.
- Cleanup: clear sentinels and temporary files.
- Evidence mapping: ADR-005, DESIGN-019 log contract; story AC 12, 13; `test_sensitive_values_not_echoed_in_errors` plus the NDJSON stderr/log-setup tests in tests/unit_test_retry_error_output_log.py (TestNdJsonFormatter and log-setup stderr tests).

### CKP-TC-020 - Import, console boundary, help, and thin launcher

- Type: packaging, side-effect regression.
- Given the package and console entry point, when imported or asked for help, then they load without configuration, network, or filesystem side effects and use one event-loop boundary.
- Command/function: package import, module `--help`, entry point help, `console_main()`; the Claude skill launcher once the CODEREVIEW-019 P1 correction (`.claude/skills/foundry-checkpoints/`) lands.
- Prerequisites/fixtures: empty arbitrary directory; guarded config/network/filesystem constructors; `asyncio.run` spy.
- Steps: import all Checkpoints modules; invoke root and operation help; call `console_main()` with fake `main()`; inspect the launcher source when available.
- Expected stdout/stderr/exit: imports produce no output or files; help exits `0` and names the 3 operations; `console_main()` calls `asyncio.run()` once and propagates the result; the launcher (when landed) delegates to packaged interfaces and contains no copied catalog, pagination, or ACL logic.
- Cleanup: remove subprocess directory and restore the event-loop spy.
- Evidence mapping: DESIGN-019 packaging contract; story AC 14; `test_console_main_uses_one_asyncio_run_boundary` (tests/test_foundry_checkpoints_cli.py); the thin-launcher pattern follows `test_claude_launcher_is_thin_and_reexports_packaged_interfaces` (tests/test_audit_console_wrapper.py) and import side-effect-freedom is verified by the TESTEXEC-019 subprocess probe.

### CKP-TC-021 - Wheel, editable install, entry-point preservation, and regression

- Type: installation, regression.
- Given local wheel and editable installs, when commands run from an arbitrary directory without `PYTHONPATH`, then `foundry-checkpoints` works while existing console scripts and repository gates remain intact.
- Command/function: local wheel build; wheel and editable install; installed `foundry-checkpoints --help`; full test, Ruff, mypy, and package checks.
- Prerequisites/fixtures: isolated virtual environments for Python 3.11 and 3.12; `PIP_NO_INDEX=1`; local build dependencies; snapshot of existing `[project.scripts]` entries.
- Steps: build without live dependency resolution; inspect wheel for the Checkpoints policy; install wheel then editable form with `--no-deps`; run help and packaged ACL probe from arbitrary CWD; compare every pre-existing entry point; run focused Checkpoints tests and full regression with branch coverage.
- Expected stdout/stderr/exit: every help and package check exits `0`; wheel contains `foundry_cli/checkpoints/metadata-allow-list.md`; all 3 operations are listed; all prior console scripts remain; focused and full suites pass on both Python versions; Ruff and mypy pass; repository branch coverage is at least 80%; no command makes a live Foundry request.
- Cleanup: delete isolated builds and environments; retain command output in TESTEXEC evidence only.
- Evidence mapping: DESIGN-019 packaging and regression contract; story AC 14, 15; all `tests/test_foundry_checkpoints_cli.py` cases (25 tests) and the configured `pyproject.toml` gates; full-suite pass at HEAD `b0df380` (1267 tests, of which the checkpoints/data_health focused suites are 52).

## Traceability matrix

| Requirement area | Story/design criteria | Cases |
| --- | --- | --- |
| Exact 3 catalog, pagination placement, parser, help, nested routing, input omission | Story AC 1; scope comment and release_notes; operation catalog | CKP-TC-001 through 003 |
| JSON argument validation, pre-client rejection, batch body bound | Story AC 2 | CKP-TC-004, 007 |
| Pagination contract: record search via PaginationHelper, bounds, resume, metadata | Story AC 3 | CKP-TC-005, 006 |
| ACL precedence, read-only semantic reads, zero-write catalog, fail-closed policy | Story AC 7, 8 | CKP-TC-009 through 012 |
| include_attribution=False and B3 only | Story AC 9, 10 | CKP-TC-013 through 015 |
| Retry (all safe, no disclosure), error taxonomy | Story AC 11, 13 | CKP-TC-016, 017 |
| Output formats, NDJSON, confidentiality | Story AC 12, 13 | CKP-TC-018, 019 |
| Imports, console, launcher, wheel/editable, regression gates | Story AC 14, 15 | CKP-TC-020, 021 |
| Positive, negative, boundary, security, resilience, structural, packaging | Complete design strategy | CKP-TC-001 through 021 |

All story acceptance criteria have at least one positive case and, where meaningful, a negative, boundary, security, or failure-path case. The 3-operation catalog is fully covered: `record get` via CKP-TC-001 through 003, 008, 010, 014 through 019; `record get-batch` via CKP-TC-001 through 004, 007, 010, 014 through 019; `record search` (the only paged command) via CKP-TC-001 through 006, 010, 016 through 019 plus ACL cases.

## Execution and approval criteria

TESTEXEC-019 may begin only after DEV, UNITTEST, CODEREVIEW, and TESTCASE-019 reach their required completed states and the approved commit is available. Execute all 21 cases with no live network access unless an approved non-production smoke is explicitly authorized.

For every case, record PASS, FAIL, or BLOCKED with the exact command, environment, expected result, actual result, stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, and linked evidence. Any failure requires a BUG-SUB before TESTEXEC-019 can close. Final QA sign-off also requires all linked defects to be terminal, every story acceptance criterion to have passing evidence, supported Python checks to pass, and repository branch coverage to remain at least 80%.
