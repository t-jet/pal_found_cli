# TESTCASE-014 - Foundry Orchestration CLI QA test cases

## Scope

These cases cover DEV-STORY-014 and the complete approved surface of `foundry-orchestration`: 20 `foundry_sdk.v2.orchestration` operations across the Build, Job, Schedule, ScheduleVersion, and ScheduleRun client paths. They verify the exact catalog and parser, nested SDK routing and dispatch, JSON argument validation, cursor pagination, batch single-call behavior, access control precedence and the 8-operation write set, the packaged 12-permitted/8-blocked metadata-only policy, attribution suppression, B3 tracing, retry and error behavior, output and log contracts, privacy, packaging, and regression gates.

Routine acceptance uses mocked async SDK transport and real installed SDK exception classes. Live credentials and live Foundry access are not required. An approved non-production smoke is optional and cannot replace the mandatory mocked evidence.

## Source baseline

- [DESIGN-014](../architecture/DESIGN-014-orchestration-cli.md), completed and closed for DEV-STORY-014.
- [DESIGN-005](../architecture/DESIGN-005-common-components.md), covering bounded streaming, atomic persistence, and SDK-native B3 tracing.
- [DESIGN-010](../architecture/DESIGN-010-audit-cli.md), [DESIGN-011](../architecture/DESIGN-011-aip-agents-cli.md), [DESIGN-012](../architecture/DESIGN-012-language-models-cli.md), [DESIGN-013](../architecture/DESIGN-013-models-cli.md) — the sibling namespace patterns this story mirrors (nested dispatch, exact-page pagination, metadata-only policy).
- [ADR-001](../architecture/adr/ADR-001-exit-code-taxonomy.md), [ADR-002](../architecture/adr/ADR-002-call-timeout-defaults.md), [ADR-004](../architecture/adr/ADR-004-format-auto-algorithm.md), [ADR-005](../architecture/adr/ADR-005-log-format.md), [ADR-006](../architecture/adr/ADR-006-env-file-search-path.md), [ADR-007](../architecture/adr/ADR-007-operation-level-readonly.md).
- The canonical environment-variable reference and metadata allow-list (namespace `orchestration`, 20 rows; 12 PERMITTED / 8 BLOCKED in tier 3).
- Vendored SDK sources under `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/orchestration/` — the real nested client routes (Build, Job, Schedule, ScheduleVersion; ScheduleRun has no public methods).
- DEV-STORY-014 ticket body and technical scope comment `20260809-200456-architect` (authoritative 20-operation catalog cross-validated from three sources).
- Implementation expected under `src/foundry_cli/orchestration/`, `.claude/skills/foundry-orchestration/`, and `pyproject.toml`.

## Preconditions and shared fixtures

- Python 3.11 and 3.12 environments contain the project, development dependencies, and pinned `foundry-sdk`.
- Use a nested async SDK fake rooted at `client.orchestration` with the four public sub-clients (Build, Job, Schedule, ScheduleVersion). A wrong, flattened, raw, or streaming route must fail the fixture. The ScheduleRun sub-client must not be reachable from any catalog dispatch.
- Paged calls use `with_raw_response` fakes whose decoded models expose `data` and `next_page_token`. Batch and search responses are single-call objects and must not page.
- Use real installed SDK model validators for nested invalid-input checks and real `foundry_sdk._errors` classes for error taxonomy checks. Mock network transport; no service call or billable schedule/build run is permitted.
- Set retry delay to zero, disable jitter, and use two retries unless a case states otherwise. Capture attempt number, timeout, attribution, and B3 values.
- Capture stdout, stderr, logs, SDK arguments, context variables, client/network constructors, and filesystem changes independently. Do not retain credential, token, JSON-body, or response sentinel values.
- No binary downloads exist in this namespace; no download root or `BinaryDownloadHandler` is required by any case.
- Packaging cases build a clean local archive with dependency resolution disabled, install with `--no-deps`, and run from an arbitrary empty working directory without `PYTHONPATH`.
- Any optional live smoke uses an approved non-production Foundry tenant, synthetic records, least-privilege credentials, and a cleanup plan. Credentials must never enter retained evidence.
- TESTEXEC records the commit, OS, Python and SDK versions, environment type, exact command, expected and actual stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, evidence reference, and PASS/FAIL/BLOCKED status for every case.

## Test data

| Name | Fixture |
| --- | --- |
| Build RID | `ri.orchestration.main.build.test` |
| Job RID | `ri.orchestration.main.job.test` |
| Schedule RID | `ri.orchestration.main.schedule.test` |
| Schedule version RID | `ri.orchestration.main.schedule-version.test` |
| Target JSON | `{"type":"upstream","datasetRids":["ri.foundry.main.dataset.test"]}` |
| Fallback branches JSON | `["master"]` |
| Action JSON | `{"type":"build","buildTargets":["ri.foundry.main.dataset.test"]}` |
| Trigger JSON | `{"type":"manual"}` |
| Scope mode JSON | `{"type":"projectScope","projectRids":["ri.compass.main.project.test"]}` |
| Build-rids JSON | `["ri.orchestration.main.build.test","ri.orchestration.main.build.test-2"]` |
| Job-rids JSON | `["ri.orchestration.main.job.test","ri.orchestration.main.job.test-2"]` |
| Schedule-rids JSON | `["ri.orchestration.main.schedule.test","ri.orchestration.main.schedule.test-2"]` |
| Where JSON | `{"type":"eq","field":"status","value":"RUNNING"}` |
| Pagination | page size `2`, initial token `cursor-001`, batch sizes `1`, `2`, `40`, `41` |
| Timeout boundaries | `1`, `3600`; invalid `0`, `3601`, non-integer text |
| Secret sentinels | `sentinel-token-secret`, `sentinel-body-secret`, `sentinel-response-secret`, `sentinel-attribution-rid` |

## Command and route inventory

Every inventory row is exercised by ORC-TC-001 through ORC-TC-008. Unless a case states otherwise, success writes one formatted result to stdout, writes no application data to stderr, exits `0`, and leaves no command-specific file.

| CLI command | Exact public SDK route and method | Required input | Optional input |
| --- | --- | --- | --- |
| `build cancel RID` | `client.orchestration.Build.cancel` | `build_rid` | shared options |
| `build create --target-json ... --fallback-branches-json ...` | `client.orchestration.Build.create` | `--target-json`, `--fallback-branches-json` | `--force-build`, `--retry-count`, `--retry-backoff-duration`, `--abort-on-failure`, `--notifications-enabled`, `--branch-name`, shared options |
| `build get RID` | `client.orchestration.Build.get` | `build_rid` | shared options |
| `build get-batch --build-rids-json ...` | `client.orchestration.Build.get_batch` | `--build-rids-json` | shared options |
| `build jobs RID` | `client.orchestration.Build.with_raw_response.jobs` | `build_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages`, shared options |
| `build search` | `client.orchestration.Build.with_raw_response.search` | — | `--where-json`, `--order-by-json`, `--page-size`, `--page-token`, `--all`, `--max-pages`, shared options |
| `job get RID` | `client.orchestration.Job.get` | `job_rid` | shared options |
| `job get-batch --job-rids-json ...` | `client.orchestration.Job.get_batch` | `--job-rids-json` | shared options |
| `schedule create --action-json ... --trigger-json ... --scope-mode-json ...` | `client.orchestration.Schedule.create` | `--action-json`, `--trigger-json`, `--scope-mode-json` | `--display-name`, `--description`, shared options |
| `schedule delete RID` | `client.orchestration.Schedule.delete` | `schedule_rid` | shared options |
| `schedule get RID` | `client.orchestration.Schedule.get` | `schedule_rid` | shared options |
| `schedule get-affected-resources RID` | `client.orchestration.Schedule.get_affected_resources` | `schedule_rid` | shared options |
| `schedule get-batch --schedule-rids-json ...` | `client.orchestration.Schedule.get_batch` | `--schedule-rids-json` | shared options |
| `schedule pause RID` | `client.orchestration.Schedule.pause` | `schedule_rid` | shared options |
| `schedule replace RID --action-json ... --trigger-json ... --scope-mode-json ...` | `client.orchestration.Schedule.replace` | `schedule_rid`, `--action-json`, `--trigger-json`, `--scope-mode-json` | `--display-name`, `--description`, shared options |
| `schedule run RID` | `client.orchestration.Schedule.run` | `schedule_rid` | shared options |
| `schedule runs RID` | `client.orchestration.Schedule.with_raw_response.runs` | `schedule_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages`, shared options |
| `schedule unpause RID` | `client.orchestration.Schedule.unpause` | `schedule_rid` | shared options |
| `schedule-version get RID` | `client.orchestration.ScheduleVersion.get` | `schedule_version_rid` | shared options |
| `schedule-version schedule RID` | `client.orchestration.ScheduleVersion.schedule` | `schedule_version_rid` | shared options |

No command may receive `attribution`, `preview`, `_sdk_internal`, an absent optional set to `None`, or any unsupported paging, stream, raw-response, or file flag. The ScheduleRun sub-client must not appear in `OP_SPECS`.

## Test cases

### ORC-TC-001 - Catalog, parser, help, and exact 20 surface

- Type: positive, structural, negative parser.
- Given the installed module and launcher, when the catalog and parser are inspected, then exactly 20 unique SDK specifications exist, every inventory command parses, and ScheduleRun is absent from `OP_SPECS`.
- Command/function: `OP_SPECS`, `build_parser()`, `_spec_for()`, `_get_client()`, root/resource/operation `--help`, `main()` with missing resource/operation, unknown flags, missing required positionals/options, invalid choices/types.
- Prerequisites/fixtures: guarded config, client, network, and filesystem constructors.
- Steps: count `OP_SPECS`; assert no `schedule_run` key; parse all 20 inventory commands; run all help surfaces; run every incomplete or malformed form.
- Expected stdout/stderr/exit: help on stdout and exit `0`; catalog count exactly `20`; parser errors as one JSON envelope on stdout with `exit_code: 1`, empty diagnostic stderr, no traceback, no config/client/network/filesystem call.
- Cleanup: restore `sys.argv` and capture streams.
- Evidence mapping: DESIGN-014 catalog; story scope comment; `test_catalog_contains_exact_20_operations`, `test_parser_accepts_every_declared_argument`, `test_help_exits_zero_and_names_operations`.

### ORC-TC-002 - Nested SDK routing across the four client paths

- Type: positive, structural, route identity.
- Given distinct fakes for `Build`, `Job`, `Schedule`, and `ScheduleVersion`, when every inventory command runs, then each resolves the exact nested object and never a flattened or sibling route, and no command reaches ScheduleRun.
- Command/function: `_get_client()` and each dispatch path.
- Prerequisites/fixtures: fakes whose sibling routes fail on access.
- Steps: run one command per client path; assert the resolved resource object identity; assert no ScheduleRun access.
- Expected stdout/stderr/exit: success results on stdout once, exit `0`, no unexpected stderr; no flattened `orchestration.*` method call.
- Cleanup: reset fakes and captures.
- Evidence mapping: DESIGN-014 nested dispatch; `test_get_client_uses_exact_nested_routes`, dispatch tests.

### ORC-TC-003 - Required inputs forwarded and absent optionals omitted

- Type: positive, structural.
- Given each inventory command, when dispatch runs, then required positionals/options reach the SDK call and every absent optional is omitted (never `None`).
- Command/function: all 20 dispatches.
- Prerequisites/fixtures: recording SDK fakes.
- Steps: run each command with only required inputs; run `build create` with each optional present and absent; run `schedule create` with and without `--display-name`/`--description`; run `schedule replace` full form.
- Expected stdout/stderr/exit: SDK call arguments contain exactly the documented keys; success exits `0`; absent optionals absent from kwargs.
- Cleanup: clear fake call records.
- Evidence mapping: DESIGN-014 operation catalog; `test_dispatch_omits_absent_optional_arguments`.

### ORC-TC-004 - JSON argument validation before client creation

- Type: positive, negative, boundary.
- Given every structured flag (`--target-json`, `--fallback-branches-json`, `--action-json`, `--trigger-json`, `--scope-mode-json`, `--where-json`, `--order-by-json`, `--build-rids-json`, `--job-rids-json`, `--schedule-rids-json`), when validation runs, then valid JSON with the documented top-level shape reaches the SDK and invalid or mis-shaped JSON exits `1` before client or network work.
- Command/function: JSON validators, `main()`.
- Prerequisites/fixtures: guarded factory/network constructors; real SDK validators for nested checks.
- Steps: supply valid payloads; supply malformed JSON text; supply valid JSON with the wrong top-level type; supply JSON whose nested fields violate SDK validators.
- Expected stdout/stderr/exit: valid inputs call the SDK and exit `0`; invalid inputs write one JSON user-input envelope to stdout, exit `1`, no traceback, and never echo the input payload into stdout/stderr/logs.
- Cleanup: clear captured sentinels.
- Evidence mapping: DESIGN-014 JSON validation contract; `test_json_arguments_decode_before_dispatch`, `test_invalid_json_stops_before_client`.

### ORC-TC-005 - Exactly three cursor-paged commands

- Type: positive, boundary, structural.
- Given cursor-bearing fakes, when pagination candidates are inspected, then exactly `build.jobs`, `build.search`, and `schedule.runs` expose pagination flags and enter `PaginationHelper`; every other command rejects pagination flags.
- Command/function: `OP_SPECS` pagination metadata, `build_parser()`, `PaginationHelper` integration.
- Prerequisites/fixtures: catalog assertions; parser probes on non-paged commands.
- Steps: assert the three-command pagination set; parse paging flags on those three; attempt paging flags on the other 17.
- Expected stdout/stderr/exit: catalog marks exactly three paged operations; paging flags parse only on the three; unsupported flags produce a structured user-input error and exit `1`; paged runs fetch at most 40 actual pages in batch mode.
- Cleanup: clear parser state.
- Evidence mapping: DESIGN-014 paging contract; `test_catalog_marks_exactly_three_paged_operations`.

### ORC-TC-006 - Exact-page batch, EOF, and 40-page cap

- Type: positive, boundary.
- Given deterministic cursor chains, when `--all`/`--max-pages` runs on a paged command, then it counts actual server pages, stops at EOF, and never fetches page 41.
- Command/function: `PaginationHelper`-driven paged commands.
- Prerequisites/fixtures: chains of 1, 2, 40, 41, and 45 pages; one item per page.
- Steps: request `--max-pages 2`; request a batch where EOF occurs early; request a 45-page chain.
- Expected stdout/stderr/exit: aggregated records appear once on stdout; exit `0`; metadata reports exact pages and items; the capped case makes exactly 40 calls and returns the page-41 cursor without fetching it.
- Cleanup: clear page chains and metadata.
- Evidence mapping: DESIGN-014 paging rules; `test_batch_stops_at_eof`, `test_hard_caps_batch_at_40_actual_pages`.

### ORC-TC-007 - Pagination retry resets cursor-local state

- Type: resilience, regression.
- Given a transient failure on a later page, when the complete pagination attempt retries, then a fresh helper restarts from the original cursor and publishes only successful counters and records.
- Command/function: `RetryHandler.execute(<paged command>, ...)`.
- Prerequisites/fixtures: page one succeeds, page two fails once, then both succeed; delay and jitter disabled.
- Steps: execute two-page pagination; record cursors and helper counters across attempts.
- Expected stdout/stderr/exit: call order is initial, second, initial, second; final records contain no duplicates; metadata reports two pages and two items once; exit `0`; failed-attempt output is absent.
- Cleanup: reset retry fake and captures.
- Evidence mapping: DESIGN-014 paging retry rule; `test_pagination_retry_restarts_helper_without_duplicate_counts`.

### ORC-TC-008 - Batch and search responses are single-call

- Type: positive, structural, boundary.
- Given `get_batch` and `SearchBuildsResponse` fakes, when `build get-batch`, `job get-batch`, `schedule get-batch`, and `build search` run, then each performs exactly one SDK call, forwards the full rids JSON, and never routes through `PaginationHelper`.
- Command/function: the four single-call commands; `PaginationHelper` integration probe.
- Prerequisites/fixtures: recording fakes; pagination-helper spy that fails if invoked.
- Steps: run all four commands; assert SDK call counts and kwargs; assert no pagination metadata is emitted.
- Expected stdout/stderr/exit: one SDK call per command with the decoded rids/where arguments; no page metadata on stderr; exit `0`.
- Cleanup: clear fake call records.
- Evidence mapping: DESIGN-014 batch single-call contract; `test_batch_commands_make_single_call`, `test_search_response_never_paginates`.

### ORC-TC-009 - ACL precedence: global, namespace, and operation scopes

- Type: security, positive, negative.
- Given metadata-only and operation-level overrides, when ACL evaluates `ORCHESTRATION`, then permissive settings allow, blocking settings deny, and an operation override wins over the namespace setting.
- Command/function: `AccessControlGuard(cfg, "ORCHESTRATION").check()` for representative operations.
- Prerequisites/fixtures: packaged Orchestration allow-list and isolated environment variables.
- Steps: enable global metadata-only; check permitted and blocked operations; disable Orchestration metadata-only at namespace level; disable one operation explicitly; combine namespace read-only with an operation override.
- Expected stdout/stderr/exit: permitted checks return silently; blocked CLI calls write a structured ACL envelope to stdout, exit `8`, and do not create a client; the denying rule appears on stderr diagnostics; no secret appears.
- Cleanup: remove every ACL environment variable.
- Evidence mapping: DESIGN-014 access-control table; `test_acl_precedence_global_namespace_operation`.

### ORC-TC-010 - Read-only mode blocks the 8-operation write set

- Type: security, positive, negative.
- Given read-only mode enabled, when each write command runs, then `build.cancel`, `build.create`, `schedule.create`, `schedule.delete`, `schedule.pause`, `schedule.replace`, `schedule.run`, and `schedule.unpause` exit `8` before client or filesystem effects.
- Command/function: `AccessControlGuard` + `main()` for each write command.
- Prerequisites/fixtures: read-only environment; guarded factory/transport.
- Steps: run all 8 write commands under read-only; inspect event order.
- Expected stdout/stderr/exit: each blocked write emits one ACL envelope and exit `8` with the denying rule on stderr; no SDK call occurs.
- Cleanup: clear read-only variables and captures.
- Evidence mapping: DESIGN-014 read-only policy; `test_readonly_blocks_write_set`.

### ORC-TC-011 - Semantic reads despite POST

- Type: security, positive, regression.
- Given read-only and metadata-only modes, when `build search` and `schedule get-affected-resources` run, then they remain executable as semantic reads despite using POST.
- Command/function: `AccessControlGuard` classification plus `main()` for both commands under read-only and metadata-only modes.
- Prerequisites/fixtures: guarded config; both modes; recording fakes.
- Steps: run both commands under read-only mode; run both under metadata-only mode; assert permitted checks and SDK calls.
- Expected stdout/stderr/exit: both commands succeed and exit `0` under both modes; no ACL envelope; SDK receives the expected POST-backed arguments.
- Cleanup: clear mode variables and fake records.
- Evidence mapping: DESIGN-014 semantic-read classification; `test_search_and_get_affected_resources_are_semantic_reads`.

### ORC-TC-012 - Metadata-only tier: exact 12 permitted / 8 blocked

- Type: security, positive, negative.
- Given metadata-only mode, when every operation is checked, then exactly the 12 documented reads are permitted and the other 8 operations are blocked.
- Command/function: `AccessControlGuard` metadata-only evaluation over the full 20-op catalog.
- Prerequisites/fixtures: packaged Orchestration allow-list; the full catalog.
- Steps: assert the permitted set equals `build get/get_batch/jobs/search`, `job get/get_batch`, `schedule get/get_affected_resources/get_batch/runs`, `schedule_version get/schedule`; assert every mutation is blocked.
- Expected stdout/stderr/exit: 12 permitted checks return silently; each of the 8 blocked CLI calls writes an ACL envelope and exits `8` with the denying rule on stderr; no client or file effect.
- Cleanup: clear metadata-only variables.
- Evidence mapping: DESIGN-014 metadata policy; `test_metadata_only_permits_exactly_12`, `test_metadata_only_blocks_remaining_8`.

### ORC-TC-013 - Packaged metadata-only policy is fail closed and CWD independent

- Type: security, packaging, negative.
- Given the installed package with a missing or malformed packaged allow-list, when ACL runs, then it fails closed (no operation permitted) and the packaged policy resolves from an arbitrary working directory.
- Command/function: `_METADATA_ALLOWLIST_PATH`, `AccessControlGuard` from an installed wheel/editable launch.
- Prerequisites/fixtures: malformed/missing policy fixtures in an isolated environment; empty arbitrary CWD, no `PYTHONPATH`.
- Steps: probe policy path from the installed package; run a permitted-class check with malformed policy; run checks from the arbitrary CWD.
- Expected stdout/stderr/exit: malformed/missing policy blocks even previously-permitted operations (fail closed, exit `8`); packaged policy path resolves inside the installed package; valid packaged policy applies the 12/8 rule from any CWD.
- Cleanup: delete isolated environments and fixtures.
- Evidence mapping: DESIGN-014 fail-closed rule; `test_metadata_policy_fails_closed`, `test_packaged_metadata_policy_is_cwd_independent`.

### ORC-TC-014 - include_attribution=False on client and invocation scope

- Type: positive, privacy, structural.
- Given a real factory and `invocation_scope`, when any command executes, then client creation and scope use `include_attribution=False`, no attribution environment handling is added, and surrounding attribution state is unchanged after success and failure.
- Command/function: `FoundryClientFactory`, `AsyncClientFactory.invocation_scope(cfg)`, `main()`.
- Prerequisites/fixtures: factory/scope spies; preset outer attribution RID and environment.
- Steps: execute a read and a failed command; capture `include_attribution` on client and scope; capture attribution state before and after.
- Expected stdout/stderr/exit: both capture points pass `include_attribution=False`; no attribution variable is read or written; outer attribution state and env are identical after success and failure; no W3C `traceparent`/`tracestate`.
- Cleanup: reset context tokens and env.
- Evidence mapping: DESIGN-014 attribution rule; `test_client_and_scope_use_include_attribution_false`.

### ORC-TC-015 - B3 enabled at outbound transport

- Type: positive, tracing, transport integration.
- Given tracing enabled, when the client is created and an SDK request is prepared, then outbound transport carries one valid B3 multi-header context.
- Command/function: `AsyncClientFactory.invocation_scope(cfg)`, SDK request preparation, a representative read.
- Prerequisites/fixtures: enabled tracing config, clean SDK context, transport header capture.
- Steps: enter the real tracing scope through `main()`; capture headers at client creation and request preparation.
- Expected stdout/stderr/exit: success result and exit `0`; every capture has lowercase-hex `X-B3-TraceId` of 32 characters, `X-B3-SpanId` of 16 characters, and `X-B3-Sampled` `0` or `1`; no W3C header appears.
- Cleanup: reset SDK context tokens and environment variables.
- Evidence mapping: DESIGN-005 B3 contract; enabled parameter of the B3 transport test.

### ORC-TC-016 - B3 disabled, retry stability, and context restoration

- Type: negative, resilience, isolation.
- Given disabled tracing, retries, prior context, or a later formatter failure, when execution leaves the invocation, then disabled calls add no B3 headers, retry attempts share one enabled context, and prior values are restored on every exit path.
- Command/function: `main()` with real `TracingProvider` scope and captured SDK transport headers.
- Prerequisites/fixtures: enabled and disabled configs; first-attempt transport failure followed by success; preset prior trace/span/sampled values; formatter, SDK, timeout, and cancellation failures.
- Steps: run the disabled flow; run the enabled retry flow; run each failure with prior values; inspect every outbound header set and context after exit.
- Expected stdout/stderr/exit: disabled flow has no `X-B3-*`; enabled retry captures identical B3 values for client creation and every attempt; no `traceparent`/`tracestate`; success exits `0`; failures use their ADR code; prior context is exact after all runs with no cross-test leakage.
- Cleanup: reset context tokens in `finally`, clear trace env vars, clear captures.
- Evidence mapping: DESIGN-005 isolation contract; B3 enabled/disabled/retry/restore tests.

### ORC-TC-017 - Retry behavior and at-least-once disclosure

- Type: resilience, negative, boundary.
- Given retryable and non-retryable failures, when `RetryHandler` wraps a command, then transient conditions (503, exhausted 429, configured transport exceptions) are retried per ADR-002, and validation, authorization, and permanent errors are never retried.
- Command/function: `RetryHandler` around representative read and mutating commands.
- Prerequisites/fixtures: HTTP 503-then-success; repeated 429; 400/401/403/404; delay and jitter disabled; attempt counters.
- Steps: run each sequence and count attempts; verify cursor-local state for paged reads; verify the at-least-once disclosure is documented for create, replace, run, cancel, pause, unpause, and delete.
- Expected stdout/stderr/exit: recovered 503 has one success result and exit `0`; exhausted 429 exits `7`; validation/auth/permanent errors exit once with codes `1`/`2`/`3`/`4`; no duplicate result or content leak; disclosure text present where applicable.
- Cleanup: clear retry state and sentinels.
- Evidence mapping: ADR-001/002, DESIGN-014 retry contract; `test_retry_transient_only`, `test_permanent_errors_not_retried`.

### ORC-TC-018 - ADR-001 error taxonomy and structured envelopes

- Type: negative, error taxonomy.
- Given each supported failure class, when the CLI exits, then it writes one JSON error envelope to stdout with the exact ADR-001 code and keeps diagnostics separate on stderr.
- Command/function: representative commands through `main()`.
- Prerequisites/fixtures: user input, HTTP 401/403/404/429/503, timeout, cancellation, ACL denial, configuration failure, and unexpected exception fakes.
- Steps: inject each failure after the correct lifecycle point; parse stdout and stderr; verify skipped downstream work where applicable.
- Expected stdout/stderr/exit: codes are user input `1`, authentication `2`, permission `3`, not found `4`, timeout/cancellation `5`, server `6`, exhausted 429 `7`, ACL `8`, and configuration `9`; error envelope is JSON on stdout; NDJSON diagnostics, if any, are on stderr; no raw traceback, token, body, or response payload appears.
- Cleanup: clear injected exceptions, secrets, and temporary roots.
- Evidence mapping: ADR-001, DESIGN-014 error contract; `test_main_serializes_exact_adr_exit_codes`.

### ORC-TC-019 - Timeout boundaries and forwarding

- Type: positive, boundary, negative.
- Given CLI or configured timeouts, when execution starts, then values from 1 through 3600 seconds are accepted and the selected value reaches both retry handling and the SDK request; invalid values are rejected before ACL, scope, client, or filesystem work.
- Command/function: `_validate_timeout()`, representative commands with `--timeout`.
- Prerequisites/fixtures: values `1`, `30`, `3600`, CLI override `17`, configured default `42`, invalid `0`, `3601`, negative, and non-integer text.
- Steps: validate boundaries; execute with and without a CLI override; inspect retry construction and `request_timeout`; invoke each invalid value.
- Expected stdout/stderr/exit: valid requests produce one success result and exit `0`; retry and SDK receive the same chosen integer; invalid values write one JSON user-input envelope on stdout and exit `1` with no ACL/client/network call.
- Cleanup: restore config defaults and call records.
- Evidence mapping: ADR-002, DESIGN-014 invocation contract; `test_timeout_accepts_adr_002_bounds`, `test_invalid_timeout_stops_before_acl_or_client`.

### ORC-TC-020 - Output formats: JSON, TOON, auto, and pretty

- Type: positive, output, boundary.
- Given success results of each shape, when `--format json|toon|auto` and `--pretty` run, then single models, `None`, optional `schedule` results, lists, and structured errors follow the ADR-004 rules.
- Command/function: `OutputFormatter` via representative commands.
- Prerequisites/fixtures: a single `Build`, a `None` result (`schedule-version schedule` empty), a uniform ID list, a non-uniform list, an empty list, structured error.
- Steps: run each shape under each format; validate stdout parses as JSON where required; verify pretty indentation when enabled.
- Expected stdout/stderr/exit: exit `0`; auto selects TOON only for uniform non-empty arrays, otherwise JSON; empty/non-uniform output is JSON; `schedule-version schedule` with no result serializes `null`/empty consistently; error output remains the structured JSON envelope.
- Cleanup: clear captures and models.
- Evidence mapping: ADR-004, DESIGN-014 output contract; shared `OutputFormatter` coverage plus namespace assertions.

### ORC-TC-021 - NDJSON stderr, stream separation, and confidentiality

- Type: positive, output, confidentiality.
- Given successful list, paged, and batch runs, when logs and results flow, then success data appears once on stdout, diagnostics are NDJSON on stderr, and credential/body/response sentinels never appear anywhere.
- Command/function: representative list, paged, and batch commands.
- Prerequisites/fixtures: secret sentinels embedded in request/response fixtures; captured logs.
- Steps: run each command; scan stdout, stderr, and captured logs for sentinel values, raw response payloads, and request bodies.
- Expected stdout/stderr/exit: exit `0`; stdout carries results/metadata envelopes only; stderr carries NDJSON diagnostics only (empty or safe); none of the sentinels, payloads, or bodies appear in any stream or log.
- Cleanup: clear sentinels and temporary files.
- Evidence mapping: ADR-005, DESIGN-014 log contract; `test_ndjson_stderr_separation`, `test_no_secrets_in_logs_errors_or_tracebacks`.

### ORC-TC-022 - Import, console boundary, help, and thin launcher

- Type: packaging, side-effect regression.
- Given the package and Claude launcher, when imported or asked for help, then they load without configuration, network, or filesystem side effects and use one event-loop boundary.
- Command/function: package import, launcher import, module `--help`, launcher `--help`, `console_main()`.
- Prerequisites/fixtures: empty arbitrary directory; guarded config/network/filesystem constructors; `asyncio.run` spy.
- Steps: import all Orchestration modules and launcher; invoke root and operation help; call `console_main()` with fake `main()`; inspect launcher source.
- Expected stdout/stderr/exit: imports produce no output or files; help exits `0` and names the 20 operations; `console_main()` calls `asyncio.run()` once and propagates the result; launcher delegates to packaged interfaces and contains no copied catalog or ACL logic.
- Cleanup: remove subprocess directory and restore the event-loop spy.
- Evidence mapping: DESIGN-014 packaging contract; `test_console_main_uses_one_asyncio_run_boundary`, `test_claude_launcher_is_thin_and_reexports_packaged_interfaces`, `test_imports_create_no_side_effect`.

### ORC-TC-023 - Wheel, editable install, entry-point preservation, and regression

- Type: installation, regression.
- Given local wheel and editable installs, when commands run from an arbitrary directory without `PYTHONPATH`, then `foundry-orchestration` and the Claude launcher work while existing console scripts and repository gates remain intact.
- Command/function: local wheel build; wheel and editable install; installed `foundry-orchestration --help`; Claude launcher help; full test, Ruff, mypy, and package checks.
- Prerequisites/fixtures: isolated virtual environments for Python 3.11 and 3.12; `PIP_NO_INDEX=1`; local build dependencies; snapshot of existing `[project.scripts]` entries.
- Steps: build without live dependency resolution; inspect wheel for the Orchestration policy; install wheel then editable form with `--no-deps`; run help and packaged ACL probe from arbitrary CWD; compare every pre-existing entry point; run focused Orchestration tests and full regression with branch coverage.
- Expected stdout/stderr/exit: every help and package check exits `0`; wheel contains `foundry_cli/orchestration/metadata-allow-list.md`; all 20 operations are listed; all prior console scripts remain; focused and full suites pass on both Python versions; Ruff and mypy pass; repository branch coverage is at least 80%; no command makes a live Foundry request.
- Cleanup: delete isolated builds and environments; retain command output in TESTEXEC evidence only.
- Evidence mapping: DESIGN-014 packaging and regression contract; all `tests/test_foundry_orchestration_*` cases and the configured `pyproject.toml` gates.

## Traceability matrix

| Requirement area | Story/design criteria | Cases |
| --- | --- | --- |
| Exact 20 catalog, ScheduleRun absent, parser, help, nested routing | DESIGN-014 catalog; scope comment | ORC-TC-001 through 003 |
| JSON argument validation, pre-client rejection | Scope AC; DESIGN-014 contract | ORC-TC-004 |
| Exactly three cursor-paged commands, 40-page cap, cursor-local retry | Scope AC; DESIGN-014 | ORC-TC-005 through 007 |
| Batch and search single-call, no invented pagination | Scope AC; DESIGN-014 | ORC-TC-008 |
| ACL precedence, read-only 8-op write set, semantic reads, fail-closed policy | Scope AC | ORC-TC-009 through 013 |
| include_attribution=False and B3 only | Scope AC | ORC-TC-014 through 016 |
| Retry, error taxonomy, timeouts | Scope AC | ORC-TC-017 through 019 |
| Output formats, NDJSON, confidentiality | Scope AC | ORC-TC-020, 021 |
| Imports, console, launcher, wheel/editable, regression gates | Scope AC | ORC-TC-022, 023 |
| Positive, negative, boundary, security, resilience, structural, packaging | Complete design strategy | ORC-TC-001 through 023 |

Every story acceptance criterion and the ticket's explicit coverage list (build 6, job 2, schedule 10, schedule_version 2, schedule_run 0) has at least one positive case and, where meaningful, a negative, boundary, security, or failure-path case.

## Execution and approval criteria

TESTEXEC-014 may begin only after DEV, UNITTEST, CODEREVIEW, and TESTCASE-014 reach their required completed states and the approved commit is available. Execute all 23 cases with no live network access unless an approved non-production smoke is explicitly authorized.

For every case, record PASS, FAIL, or BLOCKED with the exact command, environment, expected result, actual result, stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, and linked evidence. Any failure requires a BUG-SUB before TESTEXEC-014 can close. Final QA sign-off also requires all linked defects to be terminal, every story acceptance criterion to have passing evidence, supported Python checks to pass, and repository branch coverage to remain at least 80%.
