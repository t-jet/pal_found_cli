# TESTCASE-020 - Foundry Data Health CLI QA test cases

## Scope

These cases cover DEV-STORY-020 and the complete approved surface of `foundry-data-health`: the 6 public `foundry_sdk.v2.data_health` operations across the `Check` client (create, delete, get, replace) and its nested `Check.CheckReport` client (get, get_latest). They verify the exact catalog and parser, nested SDK routing through `client.data_health.Check` and `client.data_health.Check.CheckReport`, JSON argument validation (`--config-json`), the `CheckConfig` discriminated-union dispatch, the `--intent` optional, the bounded non-cursor `--limit` on `check-report get-latest`, the 3-operation write set with `replace`-class classification, the packaged 3-permitted/3-blocked metadata-only policy, `include_attribution=False`, B3 tracing, retry and error behavior, output and log contracts, privacy, packaging, and regression gates.

> **Acceptance criteria note:** The DEV-STORY-020 ticket body's Acceptance Criteria field still carries the grooming template placeholder; the authoritative acceptance criteria for this story are the DESIGN-020 contract sections (operation catalog, paging contract, access and runtime policy), the story scope comment, and the populated `release_notes` field ("adds foundry-data-health CLI (6 operations corrected from stale 4: check create, check delete, check get, check replace, check-report get, check-report get-latest) with shared access control, write-set classification, B3 tracing, retry, output formatting, and packaged metadata-only policy (3 permitted / 3 blocked)").
>
> **Operation count note:** The story title and SAD-001 reference "4 operations". The vendored SDK (v1.102.0) exposes exactly **6** public operations (`Check` 4: create, delete, get, replace; `CheckReport` 2: get, get_latest). The canonical environment-variable reference and the metadata allow-list are concordant at 6 rows each. This suite designs cases for the actual 6-operation surface (same precedent as DEV-STORY-016 streams 17 to 15 and DEV-STORY-017 connectivity 15 to 20).

Routine acceptance uses mocked async SDK transport and real installed SDK exception classes. Live credentials and live Foundry access are not required. An approved non-production smoke is optional and cannot replace the mandatory mocked evidence.

## Source baseline

- [DESIGN-020](../architecture/DESIGN-020-data-health-cli.md), completed and closed for DEV-STORY-020.
- [DESIGN-005](../architecture/DESIGN-005-common-components.md), covering SDK-native B3 tracing and retry integration contracts.
- [DESIGN-011](../architecture/DESIGN-011-aip-agents-cli.md), [DESIGN-012](../architecture/DESIGN-012-language-models-cli.md), [DESIGN-017](../architecture/DESIGN-017-connectivity-cli.md) — the sibling namespace patterns this story mirrors (immutable operation catalog, exact nested SDK dispatch, packaged policy, `replace`-class write classification).
- [ADR-001](../architecture/adr/ADR-001-exit-code-taxonomy.md), [ADR-002](../architecture/adr/ADR-002-call-timeout-defaults.md), [ADR-004](../architecture/adr/ADR-004-format-auto-algorithm.md), [ADR-005](../architecture/adr/ADR-005-log-format.md), [ADR-006](../architecture/adr/ADR-006-env-file-search-path.md), [ADR-007](../architecture/adr/ADR-007-operation-level-readonly.md).
- The canonical environment-variable reference and metadata allow-list (namespace `data_health`, 6 rows; `data_health.check.get`, `data_health.check_report.get`, `data_health.check_report.get_latest` PERMITTED, the other 3 BLOCKED in tier 3).
- Vendored SDK sources under `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/data_health/` — the real `Check` and `CheckReport` client methods, request paths, result types, and the `CheckConfig` discriminated union.
- DEV-STORY-020 ticket body, `release_notes`, and technical scope comment (authoritative 6-operation catalog, corrected from the stale 4).
- Implementation verified at commit `b0df380`: `src/foundry_cli/data_health/` (scripts/`foundry_data_health_cli.py`, `metadata-allow-list.md`), `pyproject.toml` entry point `foundry-data-health` (L43), package data for the metadata allow-list (L59), Ruff E402 scope (L91). The `.claude/skills/foundry-data-health/` skill and launcher are under the CODEREVIEW-020 P1 correction (in flight); the launcher-related verification steps in DHT-TC-020/021 are conditioned on that correction landing and on the packaged console entry point, which exists.

## Preconditions and shared fixtures

- Python 3.11 and 3.12 environments contain the project, development dependencies, and pinned `foundry-sdk`.
- Use a nested async SDK fake rooted at `client.data_health` with exactly two public sub-clients: `Check` (create, delete, get, replace) and the nested `Check.CheckReport` (get, get_latest). A wrong, flattened, raw, or streaming route must fail the fixture. No other sub-client may be reachable from any catalog dispatch.
- The `check_report` commands dispatch through the nested `Check.CheckReport` accessor (`client.data_health.Check.CheckReport.<method>`).
- No operation returns a `ResourceIterator` or a server cursor; no `PaginationHelper` may be invoked for any command. `check_report get_latest` takes an integer `--limit` (default 10, maximum 100) that bounds a single response.
- `--config-json` fakes accept the decoded `CheckConfig` discriminated-union dict (`type` discriminator across all check config kinds) and record it; `replace` reuses the same validation path.
- Use real installed SDK model validators for nested invalid-input checks and real `foundry_sdk._errors` classes for error taxonomy checks. Mock network transport; no service call is permitted.
- Set retry delay to zero, disable jitter, and use two retries unless a case states otherwise. Capture attempt number, timeout, attribution, and B3 values.
- Capture stdout, stderr, logs, SDK arguments, context variables, client/network constructors, and filesystem changes independently. Do not retain credential, token, JSON-body, or response sentinel values.
- Packaging cases build a clean local archive with dependency resolution disabled, install with `--no-deps`, and run from an arbitrary empty working directory without `PYTHONPATH`.
- Any optional live smoke uses an approved non-production Foundry tenant, synthetic checks and check reports, least-privilege credentials, and a cleanup plan. Credentials must never enter retained evidence.
- TESTEXEC records the commit, OS, Python and SDK versions, environment type, exact command, expected and actual stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, evidence reference, and PASS/FAIL/BLOCKED status for every case.

## Test data

| Name | Fixture |
| --- | --- |
| Check RID | `ri.data-health.main.check.qa-001` (valid 5-segment RID) |
| Check report RID | `ri.data-health.main.check-report.qa-001` (valid 5-segment RID) |
| Check config JSON | `{"type": "stringSet", "target": "users"}` (discriminated union, object required) |
| Config shape variants | `[]` (array), `"text"` (scalar), `null`, malformed JSON text, missing `type` discriminator, unknown `type`, nested fields violating SDK validators |
| Intent | `qa-intent-note` (optional string); absent form |
| Limit variants | absent (default 10); `1`; `100`; `101`; `0`; `-1`; non-integer text |
| Secret sentinels | `sentinel-secret-020`, `sentinel-token-secret`, `sentinel-body-secret`, `sentinel-response-secret`, `sentinel-attribution-rid` |

## Command and route inventory

Every inventory row is exercised by DHT-TC-001 through DHT-TC-003. Unless a case states otherwise, success writes one formatted result to stdout, writes no application data to stderr, exits `0`, and leaves no command-specific file.

| CLI command | Exact public SDK route and method | Required input | Optional input |
| --- | --- | --- | --- |
| `check create --config-json ...` | `client.data_health.Check.create` | `--config-json` | `--intent`, shared options |
| `check delete CHECK_RID` | `client.data_health.Check.delete` | `check_rid` | shared options |
| `check get CHECK_RID` | `client.data_health.Check.get` | `check_rid` | shared options |
| `check replace CHECK_RID --config-json ...` | `client.data_health.Check.replace` | `check_rid`, `--config-json` | `--intent`, shared options |
| `check-report get CHECK_RID CHECK_REPORT_RID` | `client.data_health.Check.CheckReport.get` | `check_rid`, `check_report_rid` | shared options |
| `check-report get-latest CHECK_RID` | `client.data_health.Check.CheckReport.get_latest` | `check_rid` | `--limit`, shared options |

No command may receive `attribution`, `preview`, `_sdk_internal`, an absent optional set to `None`, or any unsupported paging, stream, raw-response, or file flag. No pagination flags (`--page-size`, `--page-token`, `--all`, `--max-pages`) may exist in `OP_SPECS` or the parser. `--limit` is an integer flag on `check-report get-latest` only.

## Test cases

### DHT-TC-001 - Catalog, parser, help, and exact 6 surface

- Type: positive, structural, negative parser.
- Given the installed module and launcher, when the catalog and parser are inspected, then exactly 6 unique SDK specifications exist (check 4, check-report 2), every inventory command parses, and no pagination flag exists anywhere in the surface.
- Command/function: `OP_SPECS`, `build_parser()`, `_spec_for()`, `_get_client()`, root/resource/operation `--help`, `main()` with missing resource/operation, unknown flags, missing required positionals/options, invalid choices/types.
- Prerequisites/fixtures: guarded config, client, network, and filesystem constructors.
- Steps: count `OP_SPECS`; assert the resource split `check` 4 / `check_report` 2 and client paths `("Check",)` and `("Check", "CheckReport")`; assert no `--page-size`/`--page-token`/`--all`/`--max-pages` flag in any parser; parse all 6 inventory commands; run all help surfaces; run every incomplete or malformed form.
- Expected stdout/stderr/exit: help on stdout and exit `0`; catalog count exactly `6`; parser errors as one JSON envelope on stdout with `exit_code: 1`, empty diagnostic stderr, no traceback, no config/client/network/filesystem call.
- Cleanup: restore `sys.argv` and capture streams.
- Evidence mapping: DESIGN-020 catalog (corrected from stale 4); story scope comment and release_notes; `test_catalog_contains_exact_6_operations`, `test_parser_accepts_every_declared_argument`, `test_parser_rejects_unknown_operation`, `test_no_pagination_flags_anywhere` (tests/test_foundry_data_health_cli.py); verified live at HEAD `b0df380` (probe: `DATA_HEALTH_OP_SPECS: 6`, `{'check': 4, 'check_report': 2}`, client paths `('Check',)` and `('Check', 'CheckReport')`).

### DHT-TC-002 - Nested SDK routing through Check and Check.CheckReport

- Type: positive, structural, route identity.
- Given distinct fakes for `Check` and `Check.CheckReport`, when every inventory command runs, then each resolves the exact nested object and never a flattened or sibling route.
- Command/function: `_get_client()` (roots at `root_client.data_health`, then walks the spec `client_path`) and each dispatch path.
- Prerequisites/fixtures: fakes whose sibling routes fail on access.
- Steps: run one command per client path; assert the resolved resource object identity; assert no flattened `data_health.*` method call.
- Expected stdout/stderr/exit: success results on stdout once, exit `0`, no unexpected stderr; no flattened `data_health.*` method call.
- Cleanup: reset fakes and captures.
- Evidence mapping: DESIGN-020 nested dispatch; story AC 1; `test_catalog_contains_exact_6_operations` (all six resolve through the two nested client paths) plus the dispatch tests `test_check_create_dispatches_config_and_intent`, `test_check_report_get_dispatches_through_nested_client`, `test_check_report_get_latest_forwards_limit`.

### DHT-TC-003 - Required inputs forwarded and absent optionals omitted

- Type: positive, structural.
- Given each inventory command, when dispatch runs, then required positionals/options reach the SDK call and every absent optional is omitted (never `None`).
- Command/function: all 6 dispatches; `_build_kwargs()`.
- Prerequisites/fixtures: recording SDK fakes.
- Steps: run each command with only required inputs; run `check create` and `check replace` with and without `--intent`; run `check-report get-latest` with and without `--limit`; inspect the SDK call arguments.
- Expected stdout/stderr/exit: `check.create` receives the decoded `config` dict and (when provided) `intent`; `check.replace` receives `check_rid` positionally plus `config`/`intent`; `check_report.get` receives both RIDs positionally; `check_report.get_latest` receives `check_rid` positionally and `limit` only when provided; absent optionals absent from kwargs; success exits `0`.
- Cleanup: clear fake call records.
- Evidence mapping: DESIGN-020 operation catalog; story AC 1; `test_check_create_omits_absent_intent`, `test_check_report_get_latest_omits_absent_limit`, `test_check_create_dispatches_config_and_intent`, `test_check_replace_dispatches_with_config` (tests/test_foundry_data_health_cli.py).

### DHT-TC-004 - JSON argument validation before client creation

- Type: positive, negative, boundary.
- Given the structured flag `--config-json`, when validation runs, then valid JSON with the documented top-level shape (a `CheckConfig` discriminated-union object) reaches the SDK and invalid or mis-shaped JSON exits `1` before client or network work.
- Command/function: `_parse_json_object()`, `_validate_inputs()`, `main()`.
- Prerequisites/fixtures: guarded factory/network constructors; real SDK validators for nested checks.
- Steps: supply a valid config object; supply malformed JSON text; supply valid JSON with the wrong top-level type (array, scalar, null); supply JSON whose nested fields violate SDK validators (missing `type` discriminator, unknown `type`, wrong fields for the kind); run `check create` without `--config-json`.
- Expected stdout/stderr/exit: valid inputs call the SDK and exit `0`; invalid inputs write one JSON user-input envelope to stdout, exit `1`, no traceback, and never echo the input payload into stdout/stderr/logs; a missing required `--config-json` is a parser error with exit `1` before client creation.
- Cleanup: clear captured sentinels.
- Evidence mapping: DESIGN-020 JSON validation contract (CheckConfig discriminated union); story AC 2; `test_invalid_config_json_rejected_before_client`, `test_config_json_must_be_object`, `test_config_json_required_for_create` (tests/test_foundry_data_health_cli.py).

### DHT-TC-005 - Check lifecycle dispatch: create, get, delete, replace

- Type: positive, structural, stateful.
- Given recording SDK fakes, when the CLI drives `check create`, `check get`, `check replace`, and `check delete`, then each resolves through `Check`, the created/updated `Check` is surfaced, `replace` reuses the `CheckConfig` validation path with the same discriminated-union contract as `create`, and `delete` returns no content.
- Command/function: `check create`, `check get`, `check replace`, `check delete` dispatch.
- Prerequisites/fixtures: recording SDK fakes; `Check` response fakes; `delete` `None` result fake.
- Steps: run `create` with a config and capture the returned check; run `get` on the returned RID; run `replace` with a new config (and optionally `--intent`); run `delete` on the RID; inspect the SDK call arguments on each.
- Expected stdout/stderr/exit: each step exits `0`; `create`/`replace` forward the decoded config dict and `intent` (when provided); `get`/`delete` forward the positional `check_rid`; `delete` prints a serialized `null`/empty result consistently; no CLI-level state persists between invocations.
- Cleanup: clear fakes and captures.
- Evidence mapping: DESIGN-020 operation catalog and replace-class write classification; story AC 1, 3; `test_check_create_dispatches_config_and_intent`, `test_check_get_dispatches_to_check_get`, `test_check_replace_dispatches_with_config`, `test_check_delete_dispatches_to_check_delete` (tests/test_foundry_data_health_cli.py).

### DHT-TC-006 - Nested check-report dispatch: get and get-latest

- Type: positive, structural, boundary.
- Given fakes for the nested `Check.CheckReport` accessor, when `check-report get` and `check-report get-latest` run, then both resolve through `Check.CheckReport` (never a flattened `check_report.*` route), `get` forwards both RIDs, and `get-latest` bounds its single response with the integer `--limit` (default 10, maximum 100).
- Command/function: `check-report get` and `check-report get-latest` dispatch; `_get_client()` with `("Check", "CheckReport")`.
- Prerequisites/fixtures: recording nested SDK fakes; `CheckReport` and `GetLatestCheckReportsResponse` response fakes; limit variants absent, `1`, `100`, `101`, `0`, `-1`, non-integer text.
- Steps: run `get` with both RIDs; run `get-latest` without `--limit`, with `--limit 1`, with `--limit 100`; assert the nested route identity; attempt `--limit 101`, `--limit 0`, `--limit -1`, and non-integer `--limit`.
- Expected stdout/stderr/exit: valid runs exit `0` and call `Check.CheckReport.get`/`get_latest` with the exact RIDs and (when provided) `limit`; `get-latest` without `--limit` forwards no limit kwarg (SDK default 10 applies server-side); invalid limit values are rejected before client/network work with one JSON user-input envelope and exit `1`.
- Cleanup: clear fake call records and captures.
- Evidence mapping: DESIGN-020 nested dispatch and `--limit` contract (default 10, maximum 100, no cursor); story AC 1, 3; `test_check_report_get_dispatches_through_nested_client`, `test_check_report_get_latest_forwards_limit`, `test_check_report_get_latest_omits_absent_limit` (tests/test_foundry_data_health_cli.py); the server-enforced bound for 101 is documented in CODEREVIEW-020 (installed SDK `CheckReportLimit` is a plain `int` alias; the server rejects out-of-range with a 400 mapped to exit `1`).

### DHT-TC-007 - Timeout boundaries and forwarding

- Type: positive, boundary, negative.
- Given CLI or configured timeouts, when execution starts, then values from 1 through 3600 seconds are accepted and the selected value reaches both retry handling and the SDK request; invalid values are rejected before ACL, scope, client, or filesystem work.
- Command/function: `_validate_timeout()`, representative commands with `--timeout`.
- Prerequisites/fixtures: values `1`, `30` (default), `3600`, CLI override `17`, configured default `42`, invalid `0`, `3601`, negative, and non-integer text.
- Steps: validate boundaries; execute with and without a CLI override; inspect retry construction and `request_timeout`; invoke each invalid value.
- Expected stdout/stderr/exit: valid requests produce one success result and exit `0`; retry and SDK receive the same chosen integer; invalid values write one JSON user-input envelope on stdout and exit `1` with no ACL/client/network call.
- Cleanup: restore config defaults and call records.
- Evidence mapping: ADR-002, DESIGN-020 invocation contract; story AC 12; `test_timeout_accepts_adr_002_bounds`, `test_invalid_timeout_stops_before_acl_or_client` (tests/test_foundry_data_health_cli.py).

### DHT-TC-008 - ACL precedence: global, namespace, and operation scopes

- Type: security, positive, negative.
- Given metadata-only and operation-level overrides, when ACL evaluates `DATA_HEALTH`, then permissive settings allow, blocking settings deny, and an operation override wins over the namespace setting.
- Command/function: `AccessControlGuard(cfg, "DATA_HEALTH").check()` for representative operations.
- Prerequisites/fixtures: packaged Data Health allow-list and isolated environment variables.
- Steps: enable global metadata-only; check permitted and blocked operations; disable Data Health metadata-only at namespace level; disable one operation explicitly; combine namespace read-only with an operation override.
- Expected stdout/stderr/exit: permitted checks return silently; blocked CLI calls write a structured ACL envelope to stdout, exit `8`, and do not create a client; the denying rule appears on stderr diagnostics; no secret appears.
- Cleanup: remove every ACL environment variable.
- Evidence mapping: DESIGN-020 access-control table; story AC 7; `test_metadata_only_permits_exactly_3_blocks_3`, `test_metadata_only_runtime_permits_three_and_blocks_three` (precedence exercised through the namespace runtime checks).

### DHT-TC-009 - Read-only mode blocks the 3-operation write set; semantic reads stay permitted

- Type: security, positive, negative.
- Given read-only mode enabled, when each write command runs, then `check create`, `check delete`, and `check replace` exit `8` before client or filesystem effects, while `check get`, `check-report get`, and `check-report get-latest` remain executable as semantic reads.
- Command/function: `AccessControlGuard` + `main()` for each write command and the three reads.
- Prerequisites/fixtures: read-only environment; guarded factory/transport; response fakes.
- Steps: run all 3 write commands under read-only; run all 3 reads under read-only; inspect event order.
- Expected stdout/stderr/exit: each blocked write emits one ACL envelope and exit `8` with the denying rule on stderr; no SDK call occurs; the three reads succeed and exit `0`.
- Cleanup: clear read-only variables, captures, and records.
- Evidence mapping: DESIGN-020 read-only policy (write set = create/delete/replace, replace-class); story AC 7; `test_readonly_blocks_three_write_operations`, `test_semantic_reads_permitted_under_readonly` (tests/test_foundry_data_health_cli.py).

### DHT-TC-010 - Metadata-only tier: exact 3 permitted / 3 blocked

- Type: security, positive, negative.
- Given metadata-only mode, when every operation is checked, then exactly the 3 documented reads (`check.get`, `check_report.get`, `check_report.get_latest`) are permitted and the other 3 operations (`check.create`, `check.delete`, `check.replace`) are blocked.
- Command/function: `AccessControlGuard` metadata-only evaluation over the full 6-op catalog.
- Prerequisites/fixtures: packaged Data Health allow-list; the full catalog.
- Steps: assert the permitted set equals the 3 documented reads; assert every mutation (including `replace`) is blocked.
- Expected stdout/stderr/exit: 3 permitted checks return silently; each of the 3 blocked CLI calls writes an ACL envelope and exits `8` with the denying rule on stderr; no client or file effect.
- Cleanup: clear metadata-only variables.
- Evidence mapping: DESIGN-020 metadata policy; story AC 8; `test_metadata_only_permits_exactly_3_blocks_3` and `test_metadata_only_runtime_permits_three_and_blocks_three`; verified live at HEAD `b0df380` (packaged allow-list: check.get/check_report.get/check_report.get_latest PERMITTED, create/delete/replace BLOCKED).

### DHT-TC-011 - Packaged metadata-only policy is fail closed and CWD independent

- Type: security, packaging, negative.
- Given the installed package with a missing or malformed packaged allow-list, when ACL runs, then it fails closed (no operation permitted) and the packaged policy resolves from an arbitrary working directory.
- Command/function: `_METADATA_ALLOWLIST_PATH`, `AccessControlGuard` from an installed wheel/editable launch.
- Prerequisites/fixtures: malformed/missing policy fixtures in an isolated environment; empty arbitrary CWD, no `PYTHONPATH`.
- Steps: probe policy path from the installed package; run a permitted-class check with malformed policy; run checks from the arbitrary CWD.
- Expected stdout/stderr/exit: malformed/missing policy blocks even previously-permitted operations (fail closed, exit `8`); packaged policy path resolves inside the installed package; valid packaged policy applies the 3/3 rule from any CWD.
- Cleanup: delete isolated environments and fixtures.
- Evidence mapping: DESIGN-020 fail-closed rule; story AC 8, 14; `test_metadata_only_permits_exactly_3_blocks_3` (parsed from the packaged allow-list); packaged-policy CWD independence follows the same pattern as `test_packaged_metadata_policy_is_cwd_independent` (tests/test_foundry_audit_cli.py) and is verified by the TESTEXEC-020 wheel/editable probe.

### DHT-TC-012 - include_attribution=False on client and invocation scope

- Type: positive, privacy, structural.
- Given a real factory and `invocation_scope`, when any command executes, then client creation and scope use `include_attribution=False`, no attribution environment handling is added, and surrounding attribution state is unchanged after success and failure.
- Command/function: `AsyncClientFactory.invocation_scope(cfg)`, `factory.create(cfg)`, `main()`.
- Prerequisites/fixtures: factory/scope spies; preset outer attribution RID and environment.
- Steps: execute a read and a failed command; capture `include_attribution` on client and scope; capture attribution state before and after.
- Expected stdout/stderr/exit: both capture points pass `include_attribution=False`; no attribution variable is read or written; outer attribution state and env are identical after success and failure; no W3C `traceparent`/`tracestate`.
- Cleanup: reset context tokens and env.
- Evidence mapping: DESIGN-020 attribution rule (namespace outside FR-ATTR-4); story AC 9; `test_invocation_uses_include_attribution_false` (tests/test_foundry_data_health_cli.py).

### DHT-TC-013 - B3 enabled at outbound transport

- Type: positive, tracing, transport integration.
- Given tracing enabled, when the client is created and an SDK request is prepared, then outbound transport carries one valid B3 multi-header context.
- Command/function: `AsyncClientFactory.invocation_scope(cfg)`, SDK request preparation, a representative read.
- Prerequisites/fixtures: enabled tracing config, clean SDK context, transport header capture.
- Steps: enter the real tracing scope through `main()`; capture headers at client creation and request preparation.
- Expected stdout/stderr/exit: success result and exit `0`; every capture has lowercase-hex `X-B3-TraceId` of 32 characters, `X-B3-SpanId` of 16 characters, and `X-B3-Sampled` `0` or `1`; no W3C header appears.
- Cleanup: reset SDK context tokens and environment variables.
- Evidence mapping: DESIGN-005 B3 contract; story AC 10; `test_b3_transport_headers_enabled_disabled_retry_stable_and_restored` (tests/test_foundry_audit_cli.py) and `test_generated_context_has_valid_nonzero_b3_values_and_resets` (tests/test_tracing_provider.py); the namespace outbound-header probe is recorded in TESTEXEC-020 evidence.

### DHT-TC-014 - B3 disabled, retry stability, and context restoration

- Type: negative, resilience, isolation.
- Given disabled tracing, retries, prior context, or a later formatter failure, when execution leaves the invocation, then disabled calls add no B3 headers, retry attempts share one enabled context, and prior values are restored on every exit path.
- Command/function: `main()` with real `TracingProvider` scope and captured SDK transport headers.
- Prerequisites/fixtures: enabled and disabled configs; first-attempt transport failure followed by success; preset prior trace/span/sampled values; formatter, SDK, timeout, and cancellation failures.
- Steps: run the disabled flow; run the enabled retry flow; run each failure with prior values; inspect every outbound header set and context after exit.
- Expected stdout/stderr/exit: disabled flow has no `X-B3-*`; enabled retry captures identical B3 values for client creation and every attempt; no `traceparent`/`tracestate`; success exits `0`; failures use their ADR code; prior context is exact after all runs with no cross-test leakage.
- Cleanup: reset context tokens in `finally`, clear trace env vars, clear captures.
- Evidence mapping: DESIGN-005 isolation contract; story AC 10, 11; `test_b3_scope_restores_prior_values_after_formatter_failure` (tests/test_foundry_audit_cli.py) and `test_execute_traced_carries_same_b3_context_across_attempts_and_restores` (tests/test_tracing_provider.py).

### DHT-TC-015 - Retry behavior and at-least-once disclosure

- Type: resilience, negative, boundary.
- Given retryable and non-retryable failures, when `RetryHandler` wraps a command, then transient conditions (503, exhausted 429, configured transport exceptions) are retried per ADR-002, and validation, authorization, and permanent errors are never retried; the at-least-once disclosure is documented because retrying `check create` or `check replace` can duplicate checks or re-run validation.
- Command/function: `RetryHandler` around representative read, create, replace, and delete commands.
- Prerequisites/fixtures: HTTP 503-then-success; repeated 429; 400/401/403/404; delay and jitter disabled; attempt counters.
- Steps: run each sequence and count attempts; verify the at-least-once disclosure is documented for create and replace (retrying can duplicate checks or re-run validation); verify reads and delete are retried per the ADR policy.
- Expected stdout/stderr/exit: recovered 503 has one success result and exit `0`; exhausted 429 exits `7`; validation/auth/permanent errors exit once with codes `1`/`2`/`3`/`4`; no duplicate result or content leak; disclosure text present where applicable.
- Cleanup: clear retry state and sentinels.
- Evidence mapping: ADR-001/002, DESIGN-020 retry contract; story AC 11; retry tests in tests/unit_test_retry_error_output_log.py (`test_http_429_and_503_are_retryable`, `test_http_non_429_503_does_not_retry`, `test_success_after_one_retry`, `test_retry_exhaustion_raises`); at-least-once disclosure is a design-documented property captured in TESTEXEC-020 evidence.

### DHT-TC-016 - ADR-001 error taxonomy and structured envelopes

- Type: negative, error taxonomy.
- Given each supported failure class, when the CLI exits, then it writes one JSON error envelope to stdout with the exact ADR-001 code and keeps diagnostics separate on stderr.
- Command/function: representative commands through `main()` and `_serialize_error()`.
- Prerequisites/fixtures: user input, HTTP 401/403/404/429/503, timeout, cancellation, ACL denial, configuration failure, and unexpected exception fakes.
- Steps: inject each failure after the correct lifecycle point; parse stdout and stderr; verify skipped downstream work where applicable.
- Expected stdout/stderr/exit: codes are user input `1`, authentication `2`, permission `3`, not found `4`, timeout/cancellation `5`, server `6`, exhausted 429 `7`, ACL `8`, and configuration `9`; error envelope is JSON on stdout; NDJSON diagnostics, if any, are on stderr; no raw traceback, token, or body appears.
- Cleanup: clear injected exceptions, secrets, and temporary files.
- Evidence mapping: ADR-001, DESIGN-020 error contract; story AC 12, 13; `test_unknown_operation_returns_user_input_error`, `test_sdk_error_maps_to_exit_code` (tests/test_foundry_data_health_cli.py) plus the shared error-taxonomy tests in tests/unit_test_retry_error_output_log.py (`test_auth_error_exit_code_2` through `test_http_503_returns_server_error_after_retry_exhaustion`).

### DHT-TC-017 - Output formats: JSON, TOON, auto, and pretty

- Type: positive, output, boundary.
- Given success results of each shape, when `--format json|toon|auto` and `--pretty` run, then single models, `None` results, and `GetLatestCheckReportsResponse` results follow the ADR-004 rules.
- Command/function: `OutputFormatter` via representative commands.
- Prerequisites/fixtures: a single `Check`, a `None` result (`check delete`), a `CheckReport`, a `GetLatestCheckReportsResponse` with a uniform list, an empty list, structured error.
- Steps: run each shape under each format; validate stdout parses as JSON where required; verify pretty indentation when enabled.
- Expected stdout/stderr/exit: exit `0`; auto selects TOON only for uniform non-empty arrays, otherwise JSON; empty/non-uniform output is JSON; `None` results serialize `null`/empty consistently; error output remains the structured JSON envelope.
- Cleanup: clear captures and models.
- Evidence mapping: ADR-004, DESIGN-020 output contract; story AC 12; `test_output_toon_and_json_formats` (tests/test_foundry_data_health_cli.py) plus shared `OutputFormatter` coverage in tests/unit_test_retry_error_output_log.py.

### DHT-TC-018 - NDJSON stderr, stream separation, and confidentiality

- Type: positive, output, confidentiality.
- Given successful create, replace, get, and get-latest runs, when logs and results flow, then success data appears once on stdout, diagnostics are NDJSON on stderr, and credential/body/response sentinels never appear anywhere.
- Command/function: representative create, replace, get, and get-latest commands.
- Prerequisites/fixtures: secret sentinels embedded in request/response fixtures; captured logs.
- Steps: run each command; scan stdout, stderr, and captured logs for sentinel values, raw request bodies, and secret values.
- Expected stdout/stderr/exit: exit `0`; stdout carries results/metadata envelopes only; stderr carries NDJSON diagnostics only (empty or safe); none of the sentinels, payloads, or bodies appear in any stream or log.
- Cleanup: clear sentinels and temporary files.
- Evidence mapping: ADR-005, DESIGN-020 log contract; story AC 12, 13; `test_sensitive_values_not_echoed_in_errors` plus the NDJSON stderr/log-setup tests in tests/unit_test_retry_error_output_log.py (TestNdJsonFormatter and log-setup stderr tests).

### DHT-TC-019 - Import, console boundary, help, and thin launcher

- Type: packaging, side-effect regression.
- Given the package and console entry point, when imported or asked for help, then they load without configuration, network, or filesystem side effects and use one event-loop boundary.
- Command/function: package import, module `--help`, entry point help, `console_main()`; the Claude skill launcher once the CODEREVIEW-020 P1 correction (`.claude/skills/foundry-data-health/`) lands.
- Prerequisites/fixtures: empty arbitrary directory; guarded config/network/filesystem constructors; `asyncio.run` spy.
- Steps: import all Data Health modules; invoke root and operation help; call `console_main()` with fake `main()`; inspect the launcher source when available.
- Expected stdout/stderr/exit: imports produce no output or files; help exits `0` and names the 6 operations; `console_main()` calls `asyncio.run()` once and propagates the result; the launcher (when landed) delegates to packaged interfaces and contains no copied catalog or ACL logic.
- Cleanup: remove subprocess directory and restore the event-loop spy.
- Evidence mapping: DESIGN-020 packaging contract; story AC 14; `test_console_main_uses_one_asyncio_run_boundary` (tests/test_foundry_data_health_cli.py); the thin-launcher pattern follows `test_claude_launcher_is_thin_and_reexports_packaged_interfaces` (tests/test_audit_console_wrapper.py) and import side-effect-freedom is verified by the TESTEXEC-020 subprocess probe.

### DHT-TC-020 - Wheel, editable install, entry-point preservation, and regression

- Type: installation, regression.
- Given local wheel and editable installs, when commands run from an arbitrary directory without `PYTHONPATH`, then `foundry-data-health` works while existing console scripts and repository gates remain intact.
- Command/function: local wheel build; wheel and editable install; installed `foundry-data-health --help`; full test, Ruff, mypy, and package checks.
- Prerequisites/fixtures: isolated virtual environments for Python 3.11 and 3.12; `PIP_NO_INDEX=1`; local build dependencies; snapshot of existing `[project.scripts]` entries.
- Steps: build without live dependency resolution; inspect wheel for the Data Health policy; install wheel then editable form with `--no-deps`; run help and packaged ACL probe from arbitrary CWD; compare every pre-existing entry point; run focused Data Health tests and full regression with branch coverage.
- Expected stdout/stderr/exit: every help and package check exits `0`; wheel contains `foundry_cli/data_health/metadata-allow-list.md`; all 6 operations are listed; all prior console scripts remain; focused and full suites pass on both Python versions; Ruff and mypy pass; repository branch coverage is at least 80%; no command makes a live Foundry request.
- Cleanup: delete isolated builds and environments; retain command output in TESTEXEC evidence only.
- Evidence mapping: DESIGN-020 packaging and regression contract; story AC 14, 15; all `tests/test_foundry_data_health_cli.py` cases (27 tests) and the configured `pyproject.toml` gates; full-suite pass at HEAD `b0df380` (1267 tests, of which the checkpoints/data_health focused suites are 52).

## Traceability matrix

| Requirement area | Story/design criteria | Cases |
| --- | --- | --- |
| Exact 6 catalog (corrected from stale 4), no pagination, parser, help, nested routing, input omission | Story AC 1; scope comment and release_notes; operation catalog | DHT-TC-001 through 003 |
| JSON argument validation, pre-client rejection, CheckConfig discriminated union | Story AC 2 | DHT-TC-004 |
| Check lifecycle: create/get/replace/delete; replace-class write classification | Story AC 1, 3 | DHT-TC-005 |
| Nested CheckReport dispatch and bounded --limit | Story AC 1, 3 | DHT-TC-006 |
| ACL precedence, read-only 3-op write set, semantic reads, fail-closed policy | Story AC 7, 8 | DHT-TC-008 through 011 |
| include_attribution=False and B3 only | Story AC 9, 10 | DHT-TC-012 through 014 |
| Retry (at-least-once disclosure for create/replace), error taxonomy | Story AC 11, 13 | DHT-TC-015, 016 |
| Output formats, NDJSON, confidentiality | Story AC 12, 13 | DHT-TC-017, 018 |
| Imports, console, launcher, wheel/editable, regression gates | Story AC 14, 15 | DHT-TC-019, 020 |
| Positive, negative, boundary, security, resilience, structural, packaging | Complete design strategy | DHT-TC-001 through 020 |

All story acceptance criteria have at least one positive case and, where meaningful, a negative, boundary, security, or failure-path case. The 6-operation catalog is fully covered: `check create`/`check replace` via DHT-TC-001 through 005, 009, 015; `check get`/`check delete` via DHT-TC-001 through 003, 005, 009; `check-report get`/`check-report get-latest` via DHT-TC-001 through 003, 006, 009; all 6 via the ACL, attribution, tracing, output, and packaging cases.

## Execution and approval criteria

TESTEXEC-020 may begin only after DEV, UNITTEST, CODEREVIEW, and TESTCASE-020 reach their required completed states and the approved commit is available. Execute all 20 cases with no live network access unless an approved non-production smoke is explicitly authorized.

For every case, record PASS, FAIL, or BLOCKED with the exact command, environment, expected result, actual result, stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, and linked evidence. Any failure requires a BUG-SUB before TESTEXEC-020 can close. Final QA sign-off also requires all linked defects to be terminal, every story acceptance criterion to have passing evidence, supported Python checks to pass, and repository branch coverage to remain at least 80%.
