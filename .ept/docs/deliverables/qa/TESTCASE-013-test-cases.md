# TESTCASE-013 - Foundry Models CLI QA test cases

## Scope

These cases cover DEV-STORY-013 and the complete approved surface of `foundry-models`: 23 `foundry_sdk.v2.models` operations across live deployments, models, versions, experiments, experiment content, Model Studio, config versions, runs, and trainers. They verify the exact catalog and parser, nested SDK routing and dispatch, JSON argument validation, cursor pagination, service-side slicing, streamed downloads with atomic persistence, access control precedence and write classification, the packaged 12-permitted/11-blocked metadata-only policy, attribution suppression, B3 tracing, retry and error behavior, output and log contracts, privacy, packaging, and regression gates.

Routine acceptance uses mocked async SDK transport and real installed SDK exception classes. Live credentials and live Foundry access are not required. An approved non-production smoke is optional and cannot replace the mandatory mocked evidence.

## Source baseline

- [DESIGN-013](../architecture/DESIGN-013-models-cli.md), completed and closed for DEV-STORY-013.
- [DESIGN-005](../architecture/DESIGN-005-common-components.md), covering bounded binary streaming, atomic persistence, and SDK-native B3 tracing.
- [DESIGN-010](../architecture/DESIGN-010-audit-cli.md), [DESIGN-011](../architecture/DESIGN-011-aip-agents-cli.md), [DESIGN-012](../architecture/DESIGN-012-language-models-cli.md) — the sibling namespace patterns this story mirrors.
- [ADR-001](../architecture/adr/ADR-001-exit-code-taxonomy.md), [ADR-002](../architecture/adr/ADR-002-call-timeout-defaults.md), [ADR-004](../architecture/adr/ADR-004-format-auto-algorithm.md), [ADR-005](../architecture/adr/ADR-005-log-format.md), [ADR-006](../architecture/adr/ADR-006-env-file-search-path.md), [ADR-007](../architecture/adr/ADR-007-operation-level-readonly.md).
- The canonical environment-variable reference and metadata allow-list (namespace `models`, 23 rows; 12 PERMITTED / 11 BLOCKED in tier 3).
- Vendored SDK sources under `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/models/` — the real nested client routes (LiveDeployment, Model, Model.Version, Model.Experiment, Model.Experiment.Series, Model.Experiment.ArtifactTable, ModelStudio, ModelStudio.ConfigVersion, ModelStudio.Run, ModelStudio.Trainer).
- DEV-STORY-013 ticket body (authoritative 23-command catalog and 15 acceptance criteria).
- Implementation expected under `src/foundry_cli/models/`, `.claude/skills/foundry-models/`, and `pyproject.toml`.

## Preconditions and shared fixtures

- Python 3.11 and 3.12 environments contain the project, development dependencies, and pinned `foundry-sdk`.
- Use a nested async SDK fake rooted at `client.models` with the ten public sub-clients above. A wrong, flattened, raw, or streaming route must fail the fixture.
- Paged calls use `with_raw_response` fakes whose decoded models expose `data` and `next_page_token`. Streaming calls use public-only `with_streaming_response` fakes with `aiter_bytes()`; any private attribute access fails the case.
- Use real installed SDK model validators for nested invalid-input checks and real `foundry_sdk._errors` classes for error taxonomy checks. Mock network transport; no service call or billable inference is permitted.
- Set retry delay to zero, disable jitter, and use two retries unless a case states otherwise. Capture attempt number, timeout, attribution, and B3 values.
- Capture stdout, stderr, logs, SDK arguments, context variables, client/network constructors, and filesystem changes independently. Do not retain credential, token, prompt, input, content, or downloaded-byte sentinel values.
- Each download case uses a fresh temporary root and a small byte limit. Path cases monitor the parent directory for escapes.
- Packaging cases build a clean local archive with dependency resolution disabled, install with `--no-deps`, and run from an arbitrary empty working directory without `PYTHONPATH`.
- Any optional live smoke uses an approved non-production Foundry tenant, synthetic records, least-privilege credentials, and a cleanup plan. Credentials must never enter retained evidence.
- TESTEXEC records the commit, OS, Python and SDK versions, environment type, exact command, expected and actual stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, evidence reference, and PASS/FAIL/BLOCKED status for every case.

## Test data

| Name | Fixture |
| --- | --- |
| Model RID | `ri.models.main.model.test` |
| Model version RID | `ri.models.main.model-version.test-1` |
| Live deployment RID | `ri.models.main.live-deployment.test` |
| Experiment RID | `ri.models.main.experiment.test` |
| Experiment series name | `accuracy` |
| Artifact table name | `training-metrics` |
| Model Studio RID | `ri.models.main.model-studio.test` |
| Config version | `v1` |
| Trainer ID | `qa-trainer-001` |
| Parent folder RID | `ri.compass.main.folder.test` |
| Transform input JSON | `{"inputs": [{"feature": 1}]}` |
| Backing repositories JSON | `["ri.foundry.main.repository.test"]` |
| Resources JSON | `{"numCores": 4, "memory": "16GB"}` |
| Worker config JSON | `{"numWorkers": 1}` |
| Pagination | page size `2`, initial token `cursor-001`, batch sizes `1`, `2`, `40`, `41` |
| Slicing controls | `--offset 5`, `--page-size 3` |
| Download limit | `5` bytes |
| Byte payloads | empty; `abc`; `abcde`; `abcdefghi` followed by unread sentinel chunk |
| Output names | safe `model.bin`; unsafe `../escape`, `..\escape`, `/absolute`, `nul\0name`, `.`, `..` |
| Timeout boundaries | `1`, `3600`; invalid `0`, `3601`, non-integer text |
| Secret sentinels | `sentinel-token-secret`, `sentinel-input-secret`, `sentinel-content-secret`, `sentinel-bytes-secret`, `sentinel-attribution-rid` |

## Command and route inventory

Every inventory row is exercised by MDL-TC-001 through MDL-TC-008. Unless a case states otherwise, success writes one formatted result to stdout, writes no application data to stderr, exits `0`, and leaves only documented download effects.

| CLI command | Exact public SDK route and method | Required input | Optional input |
| --- | --- | --- | --- |
| `live-deployment transform-json RID --input-json ...` | `client.models.LiveDeployment.transform_json` | `live_deployment_rid`, `--input-json` | `--timeout`, `--format`, `--pretty` |
| `model create --name ... --parent-folder-rid ...` | `client.models.Model.create` | `--name`, `--parent-folder-rid` | shared options |
| `model get RID` | `client.models.Model.get` | `model_rid` | shared options |
| `model promote-version RID --source-model-version-rid ...` | `client.models.Model.promote_version` | `model_rid`, `--source-model-version-rid` | shared options |
| `model-version create RID --backing-repositories-json ... --conda-requirements-json ... --model-api-json ... --model-files-json ...` | `client.models.Model.Version.create` | `model_rid` + four JSON flags | shared options |
| `model-version get RID RID` | `client.models.Model.Version.get` | `model_rid`, `model_version_rid` | shared options |
| `model-version list RID` | `client.models.Model.Version.with_raw_response.list` | `model_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages`, shared options |
| `experiment get RID RID` | `client.models.Model.Experiment.get` | `model_rid`, `experiment_rid` | shared options |
| `experiment search RID` | `client.models.Model.Experiment.with_raw_response.search` | `model_rid` | `--order-by-json`, `--where-json`, `--page-size`, `--page-token`, `--all`, `--max-pages`, shared options |
| `experiment-series json RID RID NAME --offset --page-size` | `client.models.Model.Experiment.Series.json` | `model_rid`, `experiment_rid`, `experiment_series_name` | `--offset`, `--page-size`, shared options |
| `experiment-series parquet RID RID NAME --output ...` | `client.models.Model.Experiment.Series.with_streaming_response.parquet` | `model_rid`, `experiment_rid`, `experiment_series_name`, `--output` | shared options |
| `experiment-artifact-table json RID RID NAME --output ...` | `client.models.Model.Experiment.ArtifactTable.with_streaming_response.json` | `model_rid`, `experiment_rid`, `experiment_artifact_table_name`, `--output` | `--offset`, `--page-size`, shared options |
| `experiment-artifact-table parquet RID RID NAME --output ...` | `client.models.Model.Experiment.ArtifactTable.with_streaming_response.parquet` | `model_rid`, `experiment_rid`, `experiment_artifact_table_name`, `--output` | shared options |
| `model-studio create --name ... --parent-folder-rid ...` | `client.models.ModelStudio.create` | `--name`, `--parent-folder-rid` | shared options |
| `model-studio get RID` | `client.models.ModelStudio.get` | `model_studio_rid` | shared options |
| `model-studio launch RID` | `client.models.ModelStudio.launch` | `model_studio_rid` | shared options |
| `model-studio-config-version create RID --name ... --resources-json ... --trainer-id ... --worker-config-json ...` | `client.models.ModelStudio.ConfigVersion.create` | `model_studio_rid`, `--name`, `--resources-json`, `--trainer-id`, `--worker-config-json` | `--changelog`, shared options |
| `model-studio-config-version get RID VERSION` | `client.models.ModelStudio.ConfigVersion.get` | `model_studio_rid`, `model_studio_config_version_version` | shared options |
| `model-studio-config-version latest RID` | `client.models.ModelStudio.ConfigVersion.latest` | `model_studio_rid` | shared options |
| `model-studio-config-version list RID` | `client.models.ModelStudio.ConfigVersion.with_raw_response.list` | `model_studio_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages`, shared options |
| `model-studio-run list RID` | `client.models.ModelStudio.Run.with_raw_response.list` | `model_studio_rid` | `--config-version`, `--page-size`, `--page-token`, `--all`, `--max-pages`, shared options |
| `model-studio-trainer get ID --version` | `client.models.ModelStudio.Trainer.get` | `model_studio_trainer_trainer_id` | `--version`, shared options |
| `model-studio-trainer list` | `client.models.ModelStudio.Trainer.list` | none | shared options |

No command may receive `attribution`, `preview`, `_sdk_internal`, an absent optional set to `None`, or any unsupported paging, stream, raw-response, or file flag.

## Test cases

### MDL-TC-001 - Catalog, parser, help, and exact 23 surface

- Type: positive, structural, negative parser.
- Given the installed module and launcher, when the catalog and parser are inspected, then exactly 23 unique SDK specifications exist and every inventory command parses.
- Command/function: `OP_SPECS`, `build_parser()`, `_spec_for()`, `_get_client()`, root/resource/operation `--help`, `main()` with missing resource/operation, unknown flags, missing required positionals/options, invalid choices/types.
- Prerequisites/fixtures: guarded config, client, network, and filesystem constructors.
- Steps: count `OP_SPECS`; parse all 23 inventory commands; run all help surfaces; run every incomplete or malformed form.
- Expected stdout/stderr/exit: help on stdout and exit `0`; catalog count exactly `23`; parser errors as one JSON envelope on stdout with `exit_code: 1`, empty diagnostic stderr, no traceback, no config/client/network/filesystem call.
- Cleanup: restore `sys.argv` and capture streams.
- Evidence mapping: DESIGN-013 catalog; story AC 1, 14; `test_catalog_contains_exact_23_operations`, `test_parser_accepts_every_declared_argument`, `test_help_exits_zero_and_names_operations`.

### MDL-TC-002 - Nested SDK routing across the ten client paths

- Type: positive, structural, route identity.
- Given distinct fakes for `LiveDeployment`, `Model`, `Model.Version`, `Model.Experiment`, `Model.Experiment.Series`, `Model.Experiment.ArtifactTable`, `ModelStudio`, `ModelStudio.ConfigVersion`, `ModelStudio.Run`, and `ModelStudio.Trainer`, when every inventory command runs, then each resolves the exact nested object and never a flattened or sibling route.
- Command/function: `_get_client()` and each dispatch path.
- Prerequisites/fixtures: fakes whose sibling routes fail on access.
- Steps: run one command per client path; assert the resolved resource object identity.
- Expected stdout/stderr/exit: success results on stdout once, exit `0`, no unexpected stderr; no flattened `models.*` method call.
- Cleanup: reset fakes and captures.
- Evidence mapping: DESIGN-013 nested dispatch; story AC 1; `test_get_client_uses_exact_nested_routes`, dispatch tests.

### MDL-TC-003 - Required inputs forwarded and absent optionals omitted

- Type: positive, structural.
- Given each inventory command, when dispatch runs, then required positionals/options reach the SDK call and every absent optional is omitted (never `None`).
- Command/function: all 23 dispatches.
- Prerequisites/fixtures: recording SDK fakes.
- Steps: run each command with only required inputs; run `model-studio-config-version create` with and without `--changelog`; run `model-studio-trainer get` with and without `--version`; run `model-studio-run list` with and without `--config-version`.
- Expected stdout/stderr/exit: SDK call arguments contain exactly the documented keys; success exits `0`; absent optionals absent from kwargs.
- Cleanup: clear fake call records.
- Evidence mapping: DESIGN-013 operation catalog; story AC 1.

### MDL-TC-004 - JSON argument validation before client creation

- Type: positive, negative, boundary.
- Given every structured flag (`--input-json`, `--backing-repositories-json`, `--conda-requirements-json`, `--model-api-json`, `--model-files-json`, `--order-by-json`, `--where-json`, `--resources-json`, `--worker-config-json`), when validation runs, then valid JSON with the documented top-level shape reaches the SDK and invalid or mis-shaped JSON exits `1` before client or network work.
- Command/function: JSON validators, `main()`.
- Prerequisites/fixtures: guarded factory/network constructors; real SDK validators for nested checks.
- Steps: supply valid payloads; supply malformed JSON text; supply valid JSON with the wrong top-level type (object vs array vs scalar); supply JSON whose nested fields violate SDK validators.
- Expected stdout/stderr/exit: valid inputs call the SDK and exit `0`; invalid inputs write one JSON user-input envelope to stdout, exit `1`, no traceback, and never echo the input payload into stdout/stderr/logs.
- Cleanup: clear captured sentinels.
- Evidence mapping: DESIGN-013 JSON validation contract; story AC 2; `test_json_arguments_decode_before_dispatch`, `test_invalid_json_stops_before_client`.

### MDL-TC-005 - Exactly four cursor-paged commands

- Type: positive, boundary, structural.
- Given cursor-bearing fakes, when pagination candidates are inspected, then exactly `experiment search`, `model-version list`, `model-studio-config-version list`, and `model-studio-run list` expose pagination flags and enter `PaginationHelper`; every other command rejects pagination flags.
- Command/function: `OP_SPECS` pagination metadata, `build_parser()`, `PaginationHelper` integration.
- Prerequisites/fixtures: catalog assertions; parser probes on non-paged commands.
- Steps: assert the four-command pagination set; parse paging flags on those four; attempt paging flags on the other 19.
- Expected stdout/stderr/exit: catalog marks exactly four paged operations; paging flags parse only on the four; unsupported flags produce a structured user-input error and exit `1`; paged runs fetch at most 40 actual pages in batch mode.
- Cleanup: clear parser state.
- Evidence mapping: DESIGN-013 paging contract; story AC 3, 4; `test_catalog_marks_exactly_four_paged_operations`.

### MDL-TC-006 - Exact-page batch, EOF, and 40-page cap

- Type: positive, boundary.
- Given deterministic cursor chains, when `--all`/`--max-pages` runs on a paged command, then it counts actual server pages, stops at EOF, and never fetches page 41.
- Command/function: `PaginationHelper`-driven list/search commands.
- Prerequisites/fixtures: chains of 1, 2, 40, 41, and 45 pages; one item per page.
- Steps: request `--max-pages 2`; request a batch where EOF occurs early; request a 45-page chain.
- Expected stdout/stderr/exit: aggregated records appear once on stdout; exit `0`; metadata reports exact pages and items; the capped case makes exactly 40 calls and returns the page-41 cursor without fetching it.
- Cleanup: clear page chains and metadata.
- Evidence mapping: DESIGN-013 paging rules; story AC 3; `test_batch_stops_at_eof`, `test_hard_caps_batch_at_40_actual_pages`.

### MDL-TC-007 - Pagination retry resets cursor-local state

- Type: resilience, regression.
- Given a transient failure on a later page, when the complete pagination attempt retries, then a fresh helper restarts from the original cursor and publishes only successful counters and records.
- Command/function: `RetryHandler.execute(<paged command>, ...)`.
- Prerequisites/fixtures: page one succeeds, page two fails once, then both succeed; delay and jitter disabled.
- Steps: execute two-page pagination; record cursors and helper counters across attempts.
- Expected stdout/stderr/exit: call order is initial, second, initial, second; final records contain no duplicates; metadata reports two pages and two items once; exit `0`; failed-attempt output is absent.
- Cleanup: reset retry fake and captures.
- Evidence mapping: DESIGN-013 paging retry rule; story AC 3, 11; `test_pagination_retry_restarts_helper_without_duplicate_counts`.

### MDL-TC-008 - Service slicing never routes through PaginationHelper

- Type: positive, structural, boundary.
- Given `experiment-series json` and `experiment-artifact-table json`, when `--offset` and `--page-size` are supplied, then the values are forwarded exactly once as SDK slicing arguments and never interpreted as client pagination.
- Command/function: series/artifact JSON dispatches, `PaginationHelper` integration probe.
- Prerequisites/fixtures: recording fakes; pagination-helper spy that fails if invoked.
- Steps: run both commands with `--offset 5 --page-size 3`; assert SDK kwargs and helper usage.
- Expected stdout/stderr/exit: SDK receives `offset=5` and `page_size=3` once; no pagination metadata emitted; exit `0`.
- Cleanup: clear fake records.
- Evidence mapping: DESIGN-013 slicing contract; story AC 4; `test_series_json_forwards_slicing_once_not_pagination`.

### MDL-TC-009 - Trainer list exposes no pagination flags

- Type: structural, negative.
- Given the trainer list catalog row, when the parser and dispatch are inspected, then no pagination flags exist and no invented cursor handling runs.
- Command/function: `OP_SPECS` trainer list row, `build_parser()`.
- Prerequisites/fixtures: catalog assertion.
- Steps: assert no paging keys; attempt paging flags.
- Expected stdout/stderr/exit: trainer list has no pagination flags; paging flags produce a structured user-input error and exit `1`; the SDK call receives no paging kwargs.
- Cleanup: clear parser state.
- Evidence mapping: DESIGN-013 trainer note; story AC 4; `test_trainer_list_exposes_no_pagination`.

### MDL-TC-010 - Streamed download below the byte limit

- Type: positive, boundary.
- Given a public stream shorter than the byte limit, when a download command runs, then the full payload is atomically published and reported as non-truncated.
- Command/function: the three download commands through `BinaryDownloadHandler`.
- Prerequisites/fixtures: three-byte stream, five-byte limit, safe filename, public-only response fake.
- Steps: download; inspect SDK arguments, context closure, saved bytes, result envelope, and directory contents.
- Expected stdout/stderr/exit: JSON metadata envelope on stdout, no content on stdout/stderr, exit `0`; file contains `abc`; `file_size` and `source_size` are `3`; `truncated` false; one published file remains.
- Cleanup: remove the temporary download root.
- Evidence mapping: DESIGN-013 bounded download design; story AC 5; below-limit parameter of the streamed-download test.

### MDL-TC-011 - Streamed download above the limit uses one probe byte

- Type: boundary, security.
- Given content above the limit followed by a sentinel chunk, when download reaches the bound, then it stores only the allowed prefix and observes no more than one extra byte.
- Command/function: the three download commands through `BinaryDownloadHandler`.
- Prerequisites/fixtures: `abcdefghi`, unread sentinel chunk, five-byte limit, stream index counter.
- Steps: download and inspect stored bytes, source fields, iterator reads, and context cleanup.
- Expected stdout/stderr/exit: JSON envelope on stdout, exit `0`; file contains `abcde`; `file_size: 5`, `truncated: true`, `source_size: null`, `source_size_at_least: 6`; sentinel chunk is not read or logged.
- Cleanup: remove the temporary root and stream fake.
- Evidence mapping: DESIGN-013 bounded download design; story AC 5; above-limit parameter of the streamed-download test.

### MDL-TC-012 - Download failure and cancellation clean atomically

- Type: negative, cancellation, filesystem security.
- Given a stream failure or `asyncio.CancelledError` after partial bytes, when download aborts, then no partial or temporary file remains and all stream contexts close.
- Command/function: the three download commands, `main()` cancellation path.
- Prerequisites/fixtures: failing byte stream for `OSError` and cancellation; fresh root.
- Steps: run both failures after one chunk; inspect all descendants and closure flags; run cancellation through `main()`.
- Expected stdout/stderr/exit: stream `OSError` uses a structured server-error envelope and exits `6`; cancellation uses a structured timeout envelope and exits `5`; no content bytes, traceback, or temporary path leak; download root contains no file; stream and response context close.
- Cleanup: remove root and restore cancellation state.
- Evidence mapping: DESIGN-013 download atomicity; story AC 5, 13; `test_download_failure_cleans_partial_files`, `test_cancellation_maps_to_timeout`.

### MDL-TC-013 - Unsafe output names are rejected before publication

- Type: negative, path security.
- Given traversal, absolute, separator, NUL, dot, or dot-dot filenames, when download validates the name, then it rejects the request without creating the download root or an outside file.
- Command/function: the three download commands with `--output`.
- Prerequisites/fixtures: unsafe-name table and monitored parent directory.
- Steps: try every unsafe name; inspect root, parent, response context, stdout, and stderr.
- Expected stdout/stderr/exit: structured user-input envelope on stdout and exit `1`; no traceback or content on stderr; no root or escaped file; response context exits.
- Cleanup: remove monitored temporary parent.
- Evidence mapping: DESIGN-013 path and error contracts; story AC 5, 7; `test_download_rejects_unsafe_filename_without_creating_download_root`.

### MDL-TC-014 - ACL precedence: global, namespace, and operation scopes

- Type: security, positive, negative.
- Given metadata-only and operation-level overrides, when ACL evaluates `MODELS`, then permissive settings allow, blocking settings deny, and an operation override wins over the namespace setting.
- Command/function: `AccessControlGuard(cfg, "MODELS").check()` for representative operations.
- Prerequisites/fixtures: packaged Models allow-list and isolated environment variables.
- Steps: enable global metadata-only; check permitted and blocked operations; disable Models metadata-only at namespace level; disable one operation explicitly; combine namespace read-only with an operation override.
- Expected stdout/stderr/exit: permitted checks return silently; blocked CLI calls write a structured ACL envelope to stdout, exit `8`, and do not create a client or path; the denying rule appears on stderr diagnostics; no secret appears.
- Cleanup: remove every ACL environment variable.
- Evidence mapping: DESIGN-013 access-control table; story AC 6, 7; `test_acl_precedence_global_namespace_operation`.

### MDL-TC-015 - Read-only mode blocks the write set; experiment search stays a read

- Type: security, positive, negative.
- Given read-only mode enabled, when each write command runs, then `transform_json`, all creates, `promote_version`, and `launch` exit `8` before client or filesystem effects, while `experiment search` remains executable as a semantic read.
- Command/function: `AccessControlGuard` + `main()` for each write command and `experiment search`.
- Prerequisites/fixtures: read-only environment; guarded factory/transport; search fake.
- Steps: run all 7 write commands under read-only (`transform_json`, `model create`, `model-version create`, `model-studio create`, `model-studio-config-version create`, `model promote-version`, `model-studio launch`); run `experiment search` under read-only; inspect event order and filesystem.
- Expected stdout/stderr/exit: each blocked write emits one ACL envelope and exit `8` with the denying rule on stderr; no SDK call and no download file created; search succeeds and exits `0`.
- Cleanup: clear read-only variables, captures, and roots.
- Evidence mapping: DESIGN-013 read-only policy; story AC 6; `test_readonly_blocks_write_set`, `test_experiment_search_is_semantic_read`.

### MDL-TC-016 - Launch and promote keep write classification

- Type: security, regression.
- Given the shared `AccessControlGuard` write classification, when `model-studio launch` and `model promote-version` are classified, then they remain writes even under narrower operation overrides that could otherwise downgrade them to reads.
- Command/function: `AccessControlGuard` write-set classification and override resolution.
- Prerequisites/fixtures: override matrix combining namespace metadata-only, namespace read-only, and operation-level read-only settings for `launch` and `promote_version`.
- Steps: apply each override combination; assert the write classification holds and read-only still blocks.
- Expected stdout/stderr/exit: both operations classify as writes under every combination; read-only blocks both with exit `8`; no silent downgrade to read behavior.
- Cleanup: clear all override variables.
- Evidence mapping: DESIGN-013 ACL write-set correction; story AC 6, 7; `test_launch_and_promote_never_inherit_read_behavior`.

### MDL-TC-017 - Metadata-only tier: exact 12 permitted / 11 blocked

- Type: security, positive, negative.
- Given metadata-only mode, when every operation is checked, then exactly the 12 documented reads are permitted and the other 11 operations are blocked.
- Command/function: `AccessControlGuard` metadata-only evaluation over the full 23-op catalog.
- Prerequisites/fixtures: packaged Models allow-list; the full catalog.
- Steps: assert the permitted set equals `experiment get/search`, `model get`, `model-studio get`, `model-version get/list`, `model-studio-config-version get/latest/list`, `model-studio-run list`, `model-studio-trainer get/list`; assert every other operation is blocked.
- Expected stdout/stderr/exit: 12 permitted checks return silently; each of the 11 blocked CLI calls writes an ACL envelope and exits `8` with the denying rule on stderr; no client or file effect.
- Cleanup: clear metadata-only variables.
- Evidence mapping: DESIGN-013 metadata policy; story AC 8; `test_metadata_only_permits_exactly_12`, `test_metadata_only_blocks_remaining_11`.

### MDL-TC-018 - Packaged metadata-only policy is fail closed and CWD independent

- Type: security, packaging, negative.
- Given the installed package with a missing or malformed packaged allow-list, when ACL runs, then it fails closed (no operation permitted) and the packaged policy resolves from an arbitrary working directory.
- Command/function: `_METADATA_ALLOWLIST_PATH`, `AccessControlGuard` from an installed wheel/editable launch.
- Prerequisites/fixtures: malformed/missing policy fixtures in an isolated environment; empty arbitrary CWD, no `PYTHONPATH`.
- Steps: probe policy path from the installed package; run a permitted-class check with malformed policy; run checks from the arbitrary CWD.
- Expected stdout/stderr/exit: malformed/missing policy blocks even previously-permitted operations (fail closed, exit `8`); packaged policy path resolves inside the installed package; valid packaged policy applies the 12/11 rule from any CWD.
- Cleanup: delete isolated environments and fixtures.
- Evidence mapping: DESIGN-013 fail-closed rule; story AC 8, 14; `test_metadata_policy_fails_closed`, `test_packaged_metadata_policy_is_cwd_independent`.

### MDL-TC-019 - include_attribution=False on client and invocation scope

- Type: positive, privacy, structural.
- Given a real factory and `invocation_scope`, when any command executes, then client creation and scope use `include_attribution=False`, no attribution environment handling is added, and surrounding attribution state is unchanged after success and failure.
- Command/function: `FoundryClientFactory`, `AsyncClientFactory.invocation_scope(cfg)`, `main()`.
- Prerequisites/fixtures: factory/scope spies; preset outer attribution RID and environment.
- Steps: execute a read and a failed command; capture `include_attribution` on client and scope; capture attribution state before and after.
- Expected stdout/stderr/exit: both capture points pass `include_attribution=False`; no `FOUNDRY_*` attribution variable is read or written; outer attribution state and env are identical after success and failure; no W3C `traceparent`/`tracestate`.
- Cleanup: reset context tokens and env.
- Evidence mapping: DESIGN-013 attribution rule; story AC 9; `test_client_and_scope_use_include_attribution_false`.

### MDL-TC-020 - B3 enabled at outbound transport

- Type: positive, tracing, transport integration.
- Given tracing enabled, when the client is created and an SDK request is prepared, then outbound transport carries one valid B3 multi-header context.
- Command/function: `AsyncClientFactory.invocation_scope(cfg)`, SDK request preparation, a representative read.
- Prerequisites/fixtures: enabled tracing config, clean SDK context, transport header capture.
- Steps: enter the real tracing scope through `main()`; capture headers at client creation and request preparation.
- Expected stdout/stderr/exit: success result and exit `0`; every capture has lowercase-hex `X-B3-TraceId` of 32 characters, `X-B3-SpanId` of 16 characters, and `X-B3-Sampled` `0` or `1`; no W3C header appears.
- Cleanup: reset SDK context tokens and environment variables.
- Evidence mapping: DESIGN-005 B3 contract; story AC 10; enabled parameter of the B3 transport test.

### MDL-TC-021 - B3 disabled, retry stability, and context restoration

- Type: negative, resilience, isolation.
- Given disabled tracing, retries, prior context, or a later formatter failure, when execution leaves the invocation, then disabled calls add no B3 headers, retry attempts share one enabled context, and prior values are restored on every exit path.
- Command/function: `main()` with real `TracingProvider` scope and captured SDK transport headers.
- Prerequisites/fixtures: enabled and disabled configs; first-attempt transport failure followed by success; preset prior trace/span/sampled values; formatter, SDK, timeout, and cancellation failures.
- Steps: run the disabled flow; run the enabled retry flow; run each failure with prior values; inspect every outbound header set and context after exit.
- Expected stdout/stderr/exit: disabled flow has no `X-B3-*`; enabled retry captures identical B3 values for client creation and every attempt; no `traceparent`/`tracestate`; success exits `0`; failures use their ADR code; prior context is exact after all runs with no cross-test leakage.
- Cleanup: reset context tokens in `finally`, clear trace env vars, clear captures.
- Evidence mapping: DESIGN-005 isolation contract; story AC 10, 11; B3 enabled/disabled/retry/restore tests.

### MDL-TC-022 - Retry behavior and at-least-once disclosure

- Type: resilience, negative, boundary.
- Given retryable and non-retryable failures, when `RetryHandler` wraps a command, then transient conditions (503, exhausted 429, configured transport exceptions) are retried per ADR-002, and validation, authorization, and permanent errors are never retried.
- Command/function: `RetryHandler` around representative read, inference (`transform_json`), and mutating commands.
- Prerequisites/fixtures: HTTP 503-then-success; repeated 429; 400/401/403/404; delay and jitter disabled; attempt counters.
- Steps: run each sequence and count attempts; verify cursor-local state for paged reads; verify the at-least-once disclosure is documented for inference, creates, promotion, and launch.
- Expected stdout/stderr/exit: recovered 503 has one success result and exit `0`; exhausted 429 exits `7`; validation/auth/permanent errors exit once with codes `1`/`2`/`3`/`4`; no duplicate result or content leak; disclosure text present where applicable.
- Cleanup: clear retry state and sentinels.
- Evidence mapping: ADR-001/002, DESIGN-013 retry contract; story AC 11; `test_retry_transient_only`, `test_permanent_errors_not_retried`.

### MDL-TC-023 - ADR-001 error taxonomy and structured envelopes

- Type: negative, error taxonomy.
- Given each supported failure class, when the CLI exits, then it writes one JSON error envelope to stdout with the exact ADR-001 code and keeps diagnostics separate on stderr.
- Command/function: representative commands through `main()`.
- Prerequisites/fixtures: user input, HTTP 401/403/404/429/503, timeout, cancellation, ACL denial, configuration failure, filesystem failure, and unexpected exception fakes.
- Steps: inject each failure after the correct lifecycle point; parse stdout and stderr; verify skipped downstream work where applicable.
- Expected stdout/stderr/exit: codes are user input `1`, authentication `2`, permission `3`, not found `4`, timeout/cancellation `5`, server `6`, exhausted 429 `7`, ACL `8`, and configuration `9`; error envelope is JSON on stdout; NDJSON diagnostics, if any, are on stderr; no raw traceback, token, body, content, or temporary path appears.
- Cleanup: clear injected exceptions, secrets, and temporary roots.
- Evidence mapping: ADR-001, DESIGN-013 error contract; story AC 12, 13; `test_main_serializes_exact_adr_exit_codes`.

### MDL-TC-024 - Timeout boundaries and forwarding

- Type: positive, boundary, negative.
- Given CLI or configured timeouts, when execution starts, then values from 1 through 3600 seconds are accepted and the selected value reaches both retry handling and the SDK request; invalid values are rejected before ACL, scope, client, or filesystem work.
- Command/function: `_validate_timeout()`, representative commands with `--timeout`.
- Prerequisites/fixtures: values `1`, `30`, `3600`, CLI override `17`, configured default `42`, invalid `0`, `3601`, negative, and non-integer text.
- Steps: validate boundaries; execute with and without a CLI override; inspect retry construction and `request_timeout`; invoke each invalid value.
- Expected stdout/stderr/exit: valid requests produce one success result and exit `0`; retry and SDK receive the same chosen integer; invalid values write one JSON user-input envelope on stdout and exit `1` with no ACL/client/network/filesystem call.
- Cleanup: restore config defaults and call records.
- Evidence mapping: ADR-002, DESIGN-013 invocation contract; story AC 12; `test_timeout_accepts_adr_002_bounds`, `test_invalid_timeout_stops_before_acl_or_client`.

### MDL-TC-025 - Output formats: JSON, TOON, auto, and pretty

- Type: positive, output, boundary.
- Given success results of each shape, when `--format json|toon|auto` and `--pretty` run, then single models, `None`, optional `latest` results, lists, and structured errors follow the ADR-004 rules.
- Command/function: `OutputFormatter` via representative commands.
- Prerequisites/fixtures: a single `Model`, a `None` result (`config-version latest` empty), a uniform ID list, a non-uniform list, an empty list, structured error.
- Steps: run each shape under each format; validate stdout parses as JSON where required; verify pretty indentation when enabled.
- Expected stdout/stderr/exit: exit `0`; auto selects TOON only for uniform non-empty arrays, otherwise JSON; empty/non-uniform output is JSON; `latest` with no result serializes `null`/empty consistently; error output remains the structured JSON envelope.
- Cleanup: clear captures and models.
- Evidence mapping: ADR-004, DESIGN-013 output contract; story AC 12; shared `OutputFormatter` coverage plus namespace assertions.

### MDL-TC-026 - NDJSON stderr, stream separation, and confidentiality

- Type: positive, output, confidentiality.
- Given successful list, paged, and download runs, when logs and results flow, then success data appears once on stdout, diagnostics are NDJSON on stderr, and credential/body/input/content/byte sentinels never appear anywhere.
- Command/function: representative list, paged, and download commands.
- Prerequisites/fixtures: secret sentinels embedded in request/response fixtures; captured logs.
- Steps: run each command; scan stdout, stderr, and captured logs for sentinel values, raw content bytes, and request/response bodies.
- Expected stdout/stderr/exit: exit `0`; stdout carries results/metadata envelopes only; stderr carries NDJSON diagnostics only (empty or safe); none of the sentinels, payload bytes, tokens, or bodies appear in any stream or log.
- Cleanup: clear sentinels and temporary files.
- Evidence mapping: ADR-005, DESIGN-013 log contract; story AC 12, 13; `test_ndjson_stderr_separation`, `test_no_secrets_in_logs_errors_or_tracebacks`.

### MDL-TC-027 - Import, console boundary, help, and thin launcher

- Type: packaging, side-effect regression.
- Given the package and Claude launcher, when imported or asked for help, then they load without configuration, network, or filesystem side effects and use one event-loop boundary.
- Command/function: package import, launcher import, module `--help`, launcher `--help`, `console_main()`.
- Prerequisites/fixtures: empty arbitrary directory; guarded config/network/filesystem constructors; `asyncio.run` spy.
- Steps: import all Models modules and launcher; invoke root and operation help; call `console_main()` with fake `main()`; inspect launcher source.
- Expected stdout/stderr/exit: imports produce no output or files; help exits `0` and names the 23 operations; `console_main()` calls `asyncio.run()` once and propagates the result; launcher delegates to packaged interfaces and contains no copied catalog, download, or ACL logic.
- Cleanup: remove subprocess directory and restore the event-loop spy.
- Evidence mapping: DESIGN-013 packaging contract; story AC 14; `test_console_main_uses_one_asyncio_run_boundary`, `test_claude_launcher_is_thin_and_reexports_packaged_interfaces`, `test_imports_create_no_download_directory_or_network_side_effect`.

### MDL-TC-028 - Wheel, editable install, entry-point preservation, and regression

- Type: installation, regression.
- Given local wheel and editable installs, when commands run from an arbitrary directory without `PYTHONPATH`, then `foundry-models` and the Claude launcher work while existing console scripts and repository gates remain intact.
- Command/function: local wheel build; wheel and editable install; installed `foundry-models --help`; Claude launcher help; full test, Ruff, mypy, and package checks.
- Prerequisites/fixtures: isolated virtual environments for Python 3.11 and 3.12; `PIP_NO_INDEX=1`; local build dependencies; snapshot of existing `[project.scripts]` entries.
- Steps: build without live dependency resolution; inspect wheel for the Models policy; install wheel then editable form with `--no-deps`; run help and packaged ACL probe from arbitrary CWD; compare every pre-existing entry point; run focused Models tests and full regression with branch coverage.
- Expected stdout/stderr/exit: every help and package check exits `0`; wheel contains `foundry_cli/models/metadata-allow-list.md`; all 23 operations are listed; all prior console scripts remain; focused and full suites pass on both Python versions; Ruff and mypy pass; repository branch coverage is at least 80%; no command makes a live Foundry request.
- Cleanup: delete isolated builds and environments; retain command output in TESTEXEC evidence only.
- Evidence mapping: DESIGN-013 packaging and regression contract; story AC 14, 15; all `tests/test_models_*` cases and the configured `pyproject.toml` gates.

## Traceability matrix

| Requirement area | Story/design criteria | Cases |
| --- | --- | --- |
| Exact 23 catalog, parser, help, nested routing, input omission | Story AC 1, 14; operation catalog | MDL-TC-001 through 003 |
| JSON argument validation, pre-client rejection | Story AC 2 | MDL-TC-004 |
| Exactly four cursor-paged commands, 40-page cap, cursor-local retry | Story AC 3 | MDL-TC-005 through 007 |
| Service slicing vs pagination; trainer list no cursor | Story AC 4 | MDL-TC-008, 009 |
| Streamed downloads: bounded, atomic, closure, paths | Story AC 5, 13 | MDL-TC-010 through 013 |
| ACL precedence, read-only write set, semantic read, launch/promote classification | Story AC 6, 7 | MDL-TC-014 through 016 |
| Metadata-only 12/11, fail closed, packaged policy | Story AC 8, 14 | MDL-TC-017, 018 |
| include_attribution=False and B3 only | Story AC 9, 10 | MDL-TC-019 through 021 |
| Retry, error taxonomy, timeouts | Story AC 11, 12 | MDL-TC-022 through 024 |
| Output formats, NDJSON, confidentiality | Story AC 12, 13 | MDL-TC-025, 026 |
| Imports, console, launcher, wheel/editable, regression gates | Story AC 14, 15 | MDL-TC-027, 028 |
| Positive, negative, boundary, security, resilience, structural, packaging | Complete design strategy | MDL-TC-001 through 028 |

All 15 story acceptance criteria have at least one positive case and, where meaningful, a negative, boundary, security, or failure-path case.

## Execution and approval criteria

TESTEXEC-013 may begin only after DEV, UNITTEST, CODEREVIEW, and TESTCASE-013 reach their required completed states and the approved commit is available. Execute all 28 cases with no live network access unless an approved non-production smoke is explicitly authorized.

For every case, record PASS, FAIL, or BLOCKED with the exact command, environment, expected result, actual result, stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, and linked evidence. Any failure requires a BUG-SUB before TESTEXEC-013 can close. Final QA sign-off also requires all linked defects to be terminal, all 15 story acceptance criteria to have passing evidence, supported Python checks to pass, and repository branch coverage to remain at least 80%.
