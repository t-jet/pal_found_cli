# TESTCASE-016 - Foundry Streams CLI QA test cases

## Scope

These cases cover DEV-STORY-016 and the complete approved surface of `foundry-streams`: 15 `foundry_sdk.v2.streams` operations across the Dataset (1), Stream (8), and Subscriber (6) client paths. They verify the exact catalog and parser, nested SDK routing and dispatch, JSON argument validation, the ADR-003 batch-response pattern for record reads with bounded `--max-records` caps, access control precedence and the 10-operation write set (including the `reset` write-verb classification), the packaged 3-permitted/12-blocked metadata-only policy, the namespace stream timeout, attribution suppression, B3 tracing, retry and error behavior, output and log contracts, privacy, packaging, and regression gates.

> **Operation count note:** The story title and ADR-003/SAD-001 reference "17 operations". The vendored SDK (v1.102.0) exposes exactly **15** public operations (Dataset 1, Stream 8, Subscriber 6), and DESIGN-016, the canonical environment-variable reference, and the metadata allow-list are concordant at 15. This suite designs cases for the actual 15-operation surface.

Routine acceptance uses mocked async SDK transport and real installed SDK exception classes. Live credentials and live Foundry access are not required. An approved non-production smoke is optional and cannot replace the mandatory mocked evidence.

## Source baseline

- [DESIGN-016](../architecture/DESIGN-016-streams-cli.md), completed and closed for DEV-STORY-016.
- [ADR-003](../architecture/adr/ADR-003-streams-batch-strategy.md) — the batch-response strategy for record reads (aggregated emission on exit; no progressive streaming).
- [DESIGN-005](../architecture/DESIGN-005-common-components.md), covering bounded streaming and SDK-native B3 tracing.
- [DESIGN-011](../architecture/DESIGN-011-aip-agents-cli.md), [DESIGN-012](../architecture/DESIGN-012-language-models-cli.md), [DESIGN-013](../architecture/DESIGN-013-models-cli.md), [DESIGN-014](../architecture/DESIGN-014-orchestration-cli.md) — the sibling namespace patterns this story mirrors (nested dispatch, metadata-only policy, single-call batches).
- [ADR-001](../architecture/adr/ADR-001-exit-code-taxonomy.md), [ADR-002](../architecture/adr/ADR-002-call-timeout-defaults.md), [ADR-004](../architecture/adr/ADR-004-format-auto-algorithm.md), [ADR-005](../architecture/adr/ADR-005-log-format.md), [ADR-006](../architecture/adr/ADR-006-env-file-search-path.md), [ADR-007](../architecture/adr/ADR-007-operation-level-readonly.md).
- The canonical environment-variable reference and metadata allow-list (namespace `streams`, 15 rows; `stream.get`, `stream.get_end_offsets`, `subscriber.get_read_position` PERMITTED, the other 12 BLOCKED in tier 3; `FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S` default 120).
- Vendored SDK sources under `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/streams/` — the real `DatasetClient`, `StreamClient`, and `SubscriberClient` methods, request paths, and result types.
- DEV-STORY-016 ticket body and technical scope comment `20260810-014623-architect` (authoritative 15-operation catalog).
- Implementation expected under `src/foundry_cli/streams/`, `.claude/skills/foundry-streams/`, and `pyproject.toml`.

## Preconditions and shared fixtures

- Python 3.11 and 3.12 environments contain the project, development dependencies, and pinned `foundry-sdk`.
- Use a nested async SDK fake rooted at `client.streams` with exactly three public sub-clients: `Dataset` (create), `Dataset.Stream` (create, get, get_end_offsets, get_records, publish_binary_record, publish_record, publish_records, reset), and `Dataset.Stream.Subscriber` (commit_offsets, create, delete, get_read_position, read_records, reset_offsets). A wrong, flattened, raw, or streaming route must fail the fixture. No other sub-client may be reachable from any catalog dispatch.
- Batch-read fakes return single-call response models (`GetRecordsResponse`, `ReadSubscriberRecordsResponse`) with no cursor; no `PaginationHelper` may be invoked for any command.
- `publish_binary_record` fakes accept `bytes` and record the exact body; file reads for the binary publish are bounded and validated before client construction.
- Use real installed SDK model validators for nested invalid-input checks and real `foundry_sdk._errors` classes for error taxonomy checks. Mock network transport; no service call or billable stream publish is permitted.
- Set retry delay to zero, disable jitter, and use two retries unless a case states otherwise. Capture attempt number, timeout, attribution, and B3 values.
- Capture stdout, stderr, logs, SDK arguments, context variables, client/network constructors, and filesystem changes independently. Do not retain credential, token, JSON-body, record, or response sentinel values.
- No operation returns a streamed file download; no download root or `BinaryDownloadHandler` is required by any case.
- Packaging cases build a clean local archive with dependency resolution disabled, install with `--no-deps`, and run from an arbitrary empty working directory without `PYTHONPATH`.
- Any optional live smoke uses an approved non-production Foundry tenant, synthetic records, least-privilege credentials, and a cleanup plan. Credentials must never enter retained evidence.
- TESTEXEC records the commit, OS, Python and SDK versions, environment type, exact command, expected and actual stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, evidence reference, and PASS/FAIL/BLOCKED status for every case.

## Test data

| Name | Fixture |
| --- | --- |
| Dataset RID | `ri.foundry.main.dataset.stream-test` |
| Parent folder RID | `ri.compass.main.folder.test` |
| Branch name | `master` |
| Stream schema JSON | `{"fieldSchemaTypes": {"value": "STRING"}}` |
| Compressed flag | `--compressed` |
| Partitions count | `3` |
| Stream type | `HIGH_THROUGHPUT` |
| Partition ID | `0` |
| Start offset | `42` |
| View RID | `ri.streams.main.view.test` |
| Record JSON | `{"value": "qa-record-001"}` |
| Records JSON | `[{"value": "qa-record-001"}, {"value": "qa-record-002"}]` |
| Binary file payloads | empty file; `abc`; a file above the 16 MiB publish cap (`_read_file_bounded` bound) |
| Subscriber ID | `qa-subscriber-001` |
| Read position JSON | `{"type": "earliest"}` |
| Position JSON (reset) | `{"type": "specific", "partitions": {"0": 5}}` |
| Offsets JSON | `{"0": 5, "1": 3}` |
| Partition IDs JSON | `["0", "1"]` |
| Max-records boundaries | `1`, `100` (default), `1000` (read-records server max), `10000` (get-records max); invalid `0`, `10001`, non-integer text |
| Timeout boundaries | `1`, `120` (streams default), `3600`; invalid `0`, `3601`, non-integer text |
| Secret sentinels | `sentinel-token-secret`, `sentinel-body-secret`, `sentinel-record-secret`, `sentinel-response-secret`, `sentinel-attribution-rid` |

## Command and route inventory

Every inventory row is exercised by STR-TC-001 through STR-TC-004. Unless a case states otherwise, success writes one formatted result to stdout, writes no application data to stderr, exits `0`, and leaves no command-specific file.

| CLI command | Exact public SDK route and method | Required input | Optional input |
| --- | --- | --- | --- |
| `dataset create --name ... --parent-folder-rid ... --schema-json ...` | `client.streams.Dataset.create` | `--name`, `--parent-folder-rid`, `--schema-json` | `--branch-name`, `--compressed`, `--partitions-count`, `--stream-type`, shared options |
| `stream create DATASET_RID --branch-name ... --schema-json ...` | `client.streams.Dataset.Stream.create` | `dataset_rid`, `--branch-name`, `--schema-json` | `--compressed`, `--partitions-count`, `--stream-type`, shared options |
| `stream get DATASET_RID BRANCH` | `client.streams.Dataset.Stream.get` | `dataset_rid`, `stream_branch_name` | shared options |
| `stream get-end-offsets DATASET_RID BRANCH` | `client.streams.Dataset.Stream.get_end_offsets` | `dataset_rid`, `stream_branch_name` | `--view-rid`, shared options |
| `stream get-records DATASET_RID BRANCH --partition-id ... [--max-records ...]` | `client.streams.Dataset.Stream.get_records` | `dataset_rid`, `stream_branch_name`, `--partition-id` (SDK-required `limit` exposed as `--max-records`, default 100) | `--start-offset`, `--view-rid`, `--max-records`, shared options |
| `stream publish-binary-record DATASET_RID BRANCH --file ...` | `client.streams.Dataset.Stream.publish_binary_record` | `dataset_rid`, `stream_branch_name`, `--file` | `--view-rid`, shared options |
| `stream publish-record DATASET_RID BRANCH --record-json ...` | `client.streams.Dataset.Stream.publish_record` | `dataset_rid`, `stream_branch_name`, `--record-json` | `--view-rid`, shared options |
| `stream publish-records DATASET_RID BRANCH --records-json ...` | `client.streams.Dataset.Stream.publish_records` | `dataset_rid`, `stream_branch_name`, `--records-json` | `--view-rid`, shared options |
| `stream reset DATASET_RID BRANCH` | `client.streams.Dataset.Stream.reset` | `dataset_rid`, `stream_branch_name` | `--schema-json`, `--compressed`, `--partitions-count`, `--stream-type`, shared options |
| `subscriber create DATASET_RID BRANCH --subscriber-id ...` | `client.streams.Dataset.Stream.Subscriber.create` | `dataset_rid`, `stream_branch_name`, `--subscriber-id` | `--read-position-json`, shared options |
| `subscriber commit-offsets DATASET_RID BRANCH SUBSCRIBER_ID --offsets-json ...` | `client.streams.Dataset.Stream.Subscriber.commit_offsets` | `dataset_rid`, `stream_branch_name`, `subscriber_subscriber_id`, `--offsets-json` | `--view-rid`, shared options |
| `subscriber delete DATASET_RID BRANCH SUBSCRIBER_ID` | `client.streams.Dataset.Stream.Subscriber.delete` | `dataset_rid`, `stream_branch_name`, `subscriber_subscriber_id` | shared options |
| `subscriber get-read-position DATASET_RID BRANCH SUBSCRIBER_ID` | `client.streams.Dataset.Stream.Subscriber.get_read_position` | `dataset_rid`, `stream_branch_name`, `subscriber_subscriber_id` | `--view-rid`, shared options |
| `subscriber read-records DATASET_RID BRANCH SUBSCRIBER_ID` | `client.streams.Dataset.Stream.Subscriber.read_records` | `dataset_rid`, `stream_branch_name`, `subscriber_subscriber_id` | `--auto-commit`, `--max-records`, `--partition-ids-json`, `--view-rid`, shared options |
| `subscriber reset-offsets DATASET_RID BRANCH SUBSCRIBER_ID --position-json ...` | `client.streams.Dataset.Stream.Subscriber.reset_offsets` | `dataset_rid`, `stream_branch_name`, `subscriber_subscriber_id`, `--position-json` | shared options |

No command may receive `attribution`, `preview`, `_sdk_internal`, an absent optional set to `None`, or any unsupported paging, stream, raw-response, or file flag. No pagination flags may exist in `OP_SPECS` or the parser; batch reads are bounded by `--max-records` only.

## Test cases

### STR-TC-001 - Catalog, parser, help, and exact 15 surface

- Type: positive, structural, negative parser.
- Given the installed module and launcher, when the catalog and parser are inspected, then exactly 15 unique SDK specifications exist (Dataset 1, Stream 8, Subscriber 6), every inventory command parses, and no pagination flag exists anywhere in the surface.
- Command/function: `OP_SPECS`, `build_parser()`, `_spec_for()`, `_get_client()`, root/resource/operation `--help`, `main()` with missing resource/operation, unknown flags, missing required positionals/options, invalid choices/types.
- Prerequisites/fixtures: guarded config, client, network, and filesystem constructors.
- Steps: count `OP_SPECS`; assert no `--page-size`/`--page-token`/`--all`/`--max-pages` flag in any parser; parse all 15 inventory commands; run all help surfaces; run every incomplete or malformed form.
- Expected stdout/stderr/exit: help on stdout and exit `0`; catalog count exactly `15`; parser errors as one JSON envelope on stdout with `exit_code: 1`, empty diagnostic stderr, no traceback, no config/client/network/filesystem call.
- Cleanup: restore `sys.argv` and capture streams.
- Evidence mapping: DESIGN-016 catalog; story scope comment; `test_catalog_contains_exact_15_operations`, `test_catalog_marks_exactly_two_batch_read_operations`, `test_parser_accepts_every_declared_argument`, `test_parser_rejects_unknown_operation`; absence of pagination flags and `--help` behavior are verified by those catalog/parser tests plus the module `--help` probe recorded in TESTEXEC-016 evidence.

### STR-TC-002 - Nested SDK routing across the three client paths

- Type: positive, structural, route identity.
- Given distinct fakes for `Dataset`, `Dataset.Stream`, and `Dataset.Stream.Subscriber`, when every inventory command runs, then each resolves the exact nested object and never a flattened or sibling route.
- Command/function: `_get_client()` and each dispatch path.
- Prerequisites/fixtures: fakes whose sibling routes fail on access.
- Steps: run one command per client path; assert the resolved resource object identity; assert no flattened `streams.*` method call.
- Expected stdout/stderr/exit: success results on stdout once, exit `0`, no unexpected stderr; no flattened `streams.*` method call.
- Cleanup: reset fakes and captures.
- Evidence mapping: DESIGN-016 nested dispatch; story AC 1; `test_catalog_contains_exact_15_operations` (all fifteen resolve through the three nested client paths) plus the dispatch tests `test_dataset_create_dispatches_with_json_schema`, `test_stream_get_dispatches`, `test_get_records_batch_read_maps_max_records_to_limit`, `test_subscriber_read_records_aggregates_batch`.

### STR-TC-003 - Required inputs forwarded and absent optionals omitted

- Type: positive, structural.
- Given each inventory command, when dispatch runs, then required positionals/options reach the SDK call and every absent optional is omitted (never `None`).
- Command/function: all 15 dispatches.
- Prerequisites/fixtures: recording SDK fakes.
- Steps: run each command with only required inputs; run `dataset create` and `stream create` with each optional present and absent; run `stream reset` with and without `--schema-json`; run `subscriber create` with and without `--read-position-json`; run `subscriber read-records` with and without `--auto-commit`/`--max-records`/`--partition-ids-json`; run `subscriber commit-offsets` with and without `--view-rid`.
- Expected stdout/stderr/exit: SDK call arguments contain exactly the documented keys; success exits `0`; absent optionals absent from kwargs; `--max-records` maps to the SDK `limit` argument.
- Cleanup: clear fake call records.
- Evidence mapping: DESIGN-016 operation catalog; story AC 1; `test_get_records_batch_read_maps_max_records_to_limit` and `test_subscriber_read_records_aggregates_batch` (absent optionals omitted, `--max-records` mapped to SDK `limit`).

### STR-TC-004 - JSON argument validation before client creation

- Type: positive, negative, boundary.
- Given every structured flag (`--schema-json`, `--record-json`, `--records-json`, `--read-position-json`, `--offsets-json`, `--position-json`, `--partition-ids-json`), when validation runs, then valid JSON with the documented top-level shape reaches the SDK and invalid or mis-shaped JSON exits `1` before client or network work.
- Command/function: JSON validators, `main()`.
- Prerequisites/fixtures: guarded factory/network constructors; real SDK validators for nested checks.
- Steps: supply valid payloads; supply malformed JSON text; supply valid JSON with the wrong top-level type (object vs array vs scalar); supply JSON whose nested fields violate SDK validators.
- Expected stdout/stderr/exit: valid inputs call the SDK and exit `0`; invalid inputs write one JSON user-input envelope to stdout, exit `1`, no traceback, and never echo the input payload into stdout/stderr/logs.
- Cleanup: clear captured sentinels.
- Evidence mapping: DESIGN-016 JSON validation contract; story AC 2; `test_dataset_create_dispatches_with_json_schema`, `test_publish_record_with_json`, `test_subscriber_commit_offsets_json`, `test_subscriber_reset_offsets_position_json` (valid decode) and `test_invalid_*_json_rejected_before_client` patterns (invalid or mis-shaped JSON rejected before client creation).

### STR-TC-005 - ADR-003 batch contract: stream get-records aggregates and exits

- Type: positive, structural, boundary.
- Given a `GetRecordsResponse` fake with several partitions and records, when `stream get-records` runs, then `--max-records` (default 100, max 10000) is mapped to the SDK `limit` argument, the records are aggregated into one array (or TOON if uniform) emitted once on exit, and no record is emitted progressively.
- Command/function: `stream get-records` dispatch; batch aggregation.
- Prerequisites/fixtures: response fake with a known record set; stdout tap that fails on progressive writes.
- Steps: run with explicit `--max-records 25`; run without it (default 100); assert the SDK `limit` value and single aggregated stdout emission.
- Expected stdout/stderr/exit: SDK receives `limit=25` (or `100` by default); one aggregated result on stdout; exit `0`; no partial record array, streaming, or pagination metadata anywhere.
- Cleanup: clear response fakes and captures.
- Evidence mapping: DESIGN-016 batch-response contract; story AC 3, 4; `test_get_records_batch_read_maps_max_records_to_limit`, `test_catalog_marks_exactly_two_batch_read_operations`, and `test_parser_rejects_max_records_above_bound`.

### STR-TC-006 - ADR-003 batch contract: subscriber read-records offsets semantics

- Type: positive, security, structural.
- Given a `ReadSubscriberRecordsResponse` fake, when `subscriber read-records` runs, then offsets are mutated only when `--auto-commit` is passed; without it the SDK receives `auto_commit=False` (default) and the caller commits explicitly via `subscriber commit-offsets`.
- Command/function: `subscriber read-records` dispatch; `subscriber commit-offsets` follow-up.
- Prerequisites/fixtures: recording fakes; `--max-records` default `100` and server max `1000`.
- Steps: run without `--auto-commit`; run with `--auto-commit`; assert the SDK `auto_commit` kwarg and `limit` mapping; verify explicit commit path with `--offsets-json`.
- Expected stdout/stderr/exit: without `--auto-commit` the SDK call carries `auto_commit=False` (or the argument is omitted); with it `auto_commit=True`; `limit` default `100`, capped at `1000`; records aggregated once on stdout; exit `0`.
- Cleanup: clear fake call records.
- Evidence mapping: DESIGN-016 subscriber offset contract; story AC 3, 5; `test_subscriber_read_records_aggregates_batch` (auto-commit off semantics) and `test_subscriber_commit_offsets_json` (explicit commit path).

### STR-TC-007 - Batch-read volume boundaries: caps and no progressive streaming

- Type: boundary, negative.
- Given `--max-records` boundary values, when batch reads run, then `1` through the namespace cap are accepted, the default is `100`, values above the cap are rejected or clamped per the documented server limit, and no progressive stdout emission ever occurs.
- Command/function: `stream get-records`, `subscriber read-records` dispatch and validation.
- Prerequisites/fixtures: response fakes; stdout tap that fails on progressive writes.
- Steps: run with `1`, `100`, `1000`, and `10000` (get-records) / `1000` (read-records); run invalid `0`, `10001` (get-records), `1001` (read-records), and non-integer text.
- Expected stdout/stderr/exit: valid values reach the SDK `limit` and exit `0` with one aggregated emission; invalid values write one JSON user-input envelope on stdout and exit `1` before ACL/client/network work (or clamp per the documented server limit where the design states clamping); no progressive or partial output.
- Cleanup: clear response fakes and captures.
- Evidence mapping: DESIGN-016 batch caps; story AC 3, 4; `test_parser_rejects_max_records_above_bound` and `test_catalog_marks_exactly_two_batch_read_operations` (caps 10,000/1,000, default 100); invalid-value rejection recorded in TESTEXEC-016 evidence.

### STR-TC-008 - Publish binary record: bounded file read before client creation

- Type: positive, boundary, negative.
- Given a local file, when `stream publish-binary-record --file` runs, then the file content is read in a bounded and validated way and passed as `bytes` to the SDK, with files above the 16 MiB publish cap rejected before client construction.
- Command/function: `stream publish-binary-record` dispatch; `_read_file_bounded` file-read validation.
- Prerequisites/fixtures: empty file; `abc` file; a file above the 16 MiB cap; missing path; guarded factory/transport.
- Steps: publish each file; assert the SDK body bytes; attempt a file over the 16 MiB bound and a missing path; inspect event order.
- Expected stdout/stderr/exit: valid files reach the SDK as the exact byte content and exit `0`; oversized or missing files write one JSON user-input envelope on stdout and exit `1` with no client or network call.
- Cleanup: remove temporary files.
- Evidence mapping: DESIGN-016 binary publish contract; story AC 5; `test_publish_binary_record_reads_file`, `test_publish_binary_record_missing_file_rejected_before_client`; the oversized-file rejection is verified by the `_read_file_bounded` 16 MiB bound probe recorded in TESTEXEC-016 evidence.

### STR-TC-009 - Streams namespace timeout override

- Type: positive, boundary, negative.
- Given `FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S`, when any streams command runs, then the namespace timeout (default 120s per ADR-002/ADR-003) overrides the shared default and reaches retry handling and the SDK request; invalid values are rejected before ACL, scope, client, or filesystem work.
- Command/function: `_validate_timeout()`, representative streams commands under the namespace default and an explicit override.
- Prerequisites/fixtures: default env; explicit `120` and `17`; invalid `0`, `3601`, negative, non-integer text.
- Steps: run with no env set (expect 120); run with the override; inspect retry construction and `request_timeout`; invoke each invalid value.
- Expected stdout/stderr/exit: valid requests produce one success result and exit `0`; retry and SDK receive the selected integer (120 default, override value when set); invalid values write one JSON user-input envelope on stdout and exit `1` with no ACL/client/network call.
- Cleanup: restore env defaults and call records.
- Evidence mapping: ADR-002/003, DESIGN-016 invocation contract; story AC 6; `test_streams_default_timeout_used_when_env_absent`, `test_streams_timeout_env_overrides_default`, `test_invalid_timeout_stops_before_acl_or_client`.

### STR-TC-010 - ACL precedence: global, namespace, and operation scopes

- Type: security, positive, negative.
- Given metadata-only and operation-level overrides, when ACL evaluates `STREAMS`, then permissive settings allow, blocking settings deny, and an operation override wins over the namespace setting.
- Command/function: `AccessControlGuard(cfg, "STREAMS").check()` for representative operations.
- Prerequisites/fixtures: packaged Streams allow-list and isolated environment variables.
- Steps: enable global metadata-only; check permitted and blocked operations; disable Streams metadata-only at namespace level; disable one operation explicitly; combine namespace read-only with an operation override.
- Expected stdout/stderr/exit: permitted checks return silently; blocked CLI calls write a structured ACL envelope to stdout, exit `8`, and do not create a client; the denying rule appears on stderr diagnostics; no secret appears.
- Cleanup: remove every ACL environment variable.
- Evidence mapping: DESIGN-016 access-control table; story AC 7; `test_readonly_blocks_ten_write_operations`, `test_semantic_reads_permitted_under_readonly`, and `test_metadata_only_runtime_blocks_blocked_ops_and_permits_three` (precedence exercised through the namespace runtime checks).

### STR-TC-011 - Read-only mode blocks the 10-operation write set; record reads stay semantic reads

- Type: security, positive, negative.
- Given read-only mode enabled, when each write command runs, then `dataset.create`, `stream.create`, `stream.publish_binary_record`, `stream.publish_record`, `stream.publish_records`, `stream.reset`, `subscriber.create`, `subscriber.commit_offsets`, `subscriber.delete`, and `subscriber.reset_offsets` exit `8` before client or filesystem effects, while `stream.get_records` and `subscriber.read_records` remain executable as semantic reads despite using GET/POST with byte or record payloads.
- Command/function: `AccessControlGuard` + `main()` for each write command and the two record reads.
- Prerequisites/fixtures: read-only environment; guarded factory/transport; record fakes.
- Steps: run all 10 write commands under read-only; run `stream get_records` and `subscriber read_records` under read-only; inspect event order.
- Expected stdout/stderr/exit: each blocked write emits one ACL envelope and exit `8` with the denying rule on stderr; no SDK call occurs; both record reads succeed and exit `0` (read_records with `auto_commit` defaulting off so no offset mutation).
- Cleanup: clear read-only variables, captures, and records.
- Evidence mapping: DESIGN-016 read-only policy; story AC 7; `test_readonly_blocks_ten_write_operations`, `test_semantic_reads_permitted_under_readonly`.

### STR-TC-012 - Reset verb keeps write classification

- Type: security, regression.
- Given the shared `AccessControlGuard` write classification, when `stream.reset` and `subscriber.reset_offsets` are classified, then they remain writes even under narrower operation overrides that could otherwise downgrade them to reads.
- Command/function: `AccessControlGuard` write-set classification and override resolution.
- Prerequisites/fixtures: override matrix combining namespace metadata-only, namespace read-only, and operation-level read-only settings for `stream.reset` and `subscriber.reset_offsets`.
- Steps: apply each override combination; assert the write classification holds and read-only still blocks.
- Expected stdout/stderr/exit: both operations classify as writes under every combination; read-only blocks both with exit `8`; no silent downgrade to read behavior.
- Cleanup: clear all override variables.
- Evidence mapping: DESIGN-016 ACL write-set correction (reset verb added to `_WRITE_VERBS`); story AC 7; `test_reset_verbs_stay_write_classified_under_narrow_overrides` and `test_readonly_blocks_stream_reset_before_client` (tests/test_foundry_streams_cli.py + tests/test_access_control_guard.py regression tests).

### STR-TC-013 - Metadata-only tier: exact 3 permitted / 12 blocked

- Type: security, positive, negative.
- Given metadata-only mode, when every operation is checked, then exactly the 3 documented reads (`stream.get`, `stream.get_end_offsets`, `subscriber.get_read_position`) are permitted and the other 12 operations are blocked.
- Command/function: `AccessControlGuard` metadata-only evaluation over the full 15-op catalog.
- Prerequisites/fixtures: packaged Streams allow-list; the full catalog.
- Steps: assert the permitted set equals `{stream.get, stream.get_end_offsets, subscriber.get_read_position}`; assert every mutation and record content read (including `stream.get_records` and `subscriber.read_records`) is blocked.
- Expected stdout/stderr/exit: 3 permitted checks return silently; each of the 12 blocked CLI calls writes an ACL envelope and exits `8` with the denying rule on stderr; no client or file effect.
- Cleanup: clear metadata-only variables.
- Evidence mapping: DESIGN-016 metadata policy; story AC 8; `test_metadata_only_permits_exactly_3_blocks_12` and `test_metadata_only_runtime_blocks_blocked_ops_and_permits_three`.

### STR-TC-014 - Packaged metadata-only policy is fail closed and CWD independent

- Type: security, packaging, negative.
- Given the installed package with a missing or malformed packaged allow-list, when ACL runs, then it fails closed (no operation permitted) and the packaged policy resolves from an arbitrary working directory.
- Command/function: `_METADATA_ALLOWLIST_PATH`, `AccessControlGuard` from an installed wheel/editable launch.
- Prerequisites/fixtures: malformed/missing policy fixtures in an isolated environment; empty arbitrary CWD, no `PYTHONPATH`.
- Steps: probe policy path from the installed package; run a permitted-class check with malformed policy; run checks from the arbitrary CWD.
- Expected stdout/stderr/exit: malformed/missing policy blocks even previously-permitted operations (fail closed, exit `8`); packaged policy path resolves inside the installed package; valid packaged policy applies the 3/12 rule from any CWD.
- Cleanup: delete isolated environments and fixtures.
- Evidence mapping: DESIGN-016 fail-closed rule; story AC 8, 14; `test_metadata_only_permits_exactly_3_blocks_12` (parsed from the packaged allow-list); packaged-policy CWD independence follows the same pattern as `test_packaged_metadata_policy_is_cwd_independent` (tests/test_foundry_audit_cli.py) and is verified by the TESTEXEC-016 wheel/editable probe.

### STR-TC-015 - include_attribution=False on client and invocation scope

- Type: positive, privacy, structural.
- Given a real factory and `invocation_scope`, when any command executes, then client creation and scope use `include_attribution=False`, no attribution environment handling is added, and surrounding attribution state is unchanged after success and failure.
- Command/function: `FoundryClientFactory`, `AsyncClientFactory.invocation_scope(cfg)`, `main()`.
- Prerequisites/fixtures: factory/scope spies; preset outer attribution RID and environment.
- Steps: execute a read and a failed command; capture `include_attribution` on client and scope; capture attribution state before and after.
- Expected stdout/stderr/exit: both capture points pass `include_attribution=False`; no attribution variable is read or written; outer attribution state and env are identical after success and failure; no W3C `traceparent`/`tracestate`.
- Cleanup: reset context tokens and env.
- Evidence mapping: DESIGN-016 attribution rule; story AC 9; `test_invocation_uses_include_attribution_false`.

### STR-TC-016 - B3 enabled at outbound transport

- Type: positive, tracing, transport integration.
- Given tracing enabled, when the client is created and an SDK request is prepared, then outbound transport carries one valid B3 multi-header context.
- Command/function: `AsyncClientFactory.invocation_scope(cfg)`, SDK request preparation, a representative read.
- Prerequisites/fixtures: enabled tracing config, clean SDK context, transport header capture.
- Steps: enter the real tracing scope through `main()`; capture headers at client creation and request preparation.
- Expected stdout/stderr/exit: success result and exit `0`; every capture has lowercase-hex `X-B3-TraceId` of 32 characters, `X-B3-SpanId` of 16 characters, and `X-B3-Sampled` `0` or `1`; no W3C header appears.
- Cleanup: reset SDK context tokens and environment variables.
- Evidence mapping: DESIGN-005 B3 contract; story AC 10; `test_b3_transport_headers_enabled_disabled_retry_stable_and_restored` (tests/test_foundry_audit_cli.py) and `test_generated_context_has_valid_nonzero_b3_values_and_resets` (tests/test_tracing_provider.py); the namespace outbound-header probe is recorded in TESTEXEC-016 evidence.

### STR-TC-017 - B3 disabled, retry stability, and context restoration

- Type: negative, resilience, isolation.
- Given disabled tracing, retries, prior context, or a later formatter failure, when execution leaves the invocation, then disabled calls add no B3 headers, retry attempts share one enabled context, and prior values are restored on every exit path.
- Command/function: `main()` with real `TracingProvider` scope and captured SDK transport headers.
- Prerequisites/fixtures: enabled and disabled configs; first-attempt transport failure followed by success; preset prior trace/span/sampled values; formatter, SDK, timeout, and cancellation failures.
- Steps: run the disabled flow; run the enabled retry flow; run each failure with prior values; inspect every outbound header set and context after exit.
- Expected stdout/stderr/exit: disabled flow has no `X-B3-*`; enabled retry captures identical B3 values for client creation and every attempt; no `traceparent`/`tracestate`; success exits `0`; failures use their ADR code; prior context is exact after all runs with no cross-test leakage.
- Cleanup: reset context tokens in `finally`, clear trace env vars, clear captures.
- Evidence mapping: DESIGN-005 isolation contract; story AC 10, 11; `test_b3_scope_restores_prior_values_after_formatter_failure` (tests/test_foundry_audit_cli.py) and `test_execute_traced_carries_same_b3_context_across_attempts_and_restores` (tests/test_tracing_provider.py).

### STR-TC-018 - Retry behavior and at-least-once disclosure

- Type: resilience, negative, boundary.
- Given retryable and non-retryable failures, when `RetryHandler` wraps a command, then transient conditions (503, exhausted 429, configured transport exceptions) are retried per ADR-002, and validation, authorization, and permanent errors are never retried.
- Command/function: `RetryHandler` around representative read, publish, create, reset, commit, and delete commands.
- Prerequisites/fixtures: HTTP 503-then-success; repeated 429; 400/401/403/404; delay and jitter disabled; attempt counters.
- Steps: run each sequence and count attempts; verify the at-least-once disclosure is documented for create, publish, reset, commit, and delete (retrying can duplicate records or cost); verify reads without auto-commit are safe to retry.
- Expected stdout/stderr/exit: recovered 503 has one success result and exit `0`; exhausted 429 exits `7`; validation/auth/permanent errors exit once with codes `1`/`2`/`3`/`4`; no duplicate record, result, or content leak; disclosure text present where applicable.
- Cleanup: clear retry state and sentinels.
- Evidence mapping: ADR-001/002, DESIGN-016 retry contract; story AC 11; retry tests in tests/unit_test_retry_error_output_log.py (`test_http_429_and_503_are_retryable`, `test_http_non_429_503_does_not_retry`, `test_success_after_one_retry`, `test_retry_exhaustion_raises`); at-least-once disclosure is a design-documented property captured in TESTEXEC-016 evidence.

### STR-TC-019 - ADR-001 error taxonomy and structured envelopes

- Type: negative, error taxonomy.
- Given each supported failure class, when the CLI exits, then it writes one JSON error envelope to stdout with the exact ADR-001 code and keeps diagnostics separate on stderr.
- Command/function: representative commands through `main()`.
- Prerequisites/fixtures: user input, HTTP 401/403/404/429/503, timeout, cancellation, ACL denial, configuration failure, and unexpected exception fakes.
- Steps: inject each failure after the correct lifecycle point; parse stdout and stderr; verify skipped downstream work where applicable.
- Expected stdout/stderr/exit: codes are user input `1`, authentication `2`, permission `3`, not found `4`, timeout/cancellation `5`, server `6`, exhausted 429 `7`, ACL `8`, and configuration `9`; error envelope is JSON on stdout; NDJSON diagnostics, if any, are on stderr; no raw traceback, token, body, or record payload appears.
- Cleanup: clear injected exceptions, secrets, and temporary files.
- Evidence mapping: ADR-001, DESIGN-016 error contract; story AC 12, 13; `test_sdk_error_maps_to_exit_code` (namespace) plus the shared error-taxonomy tests in tests/unit_test_retry_error_output_log.py (`test_auth_error_exit_code_2` through `test_http_503_returns_server_error_after_retry_exhaustion`).

### STR-TC-020 - Timeout boundaries and forwarding

- Type: positive, boundary, negative.
- Given CLI or configured timeouts, when execution starts, then values from 1 through 3600 seconds are accepted and the selected value reaches both retry handling and the SDK request; invalid values are rejected before ACL, scope, client, or filesystem work.
- Command/function: `_validate_timeout()`, representative commands with `--timeout`.
- Prerequisites/fixtures: values `1`, `30`, `3600`, CLI override `17`, configured default `42`, invalid `0`, `3601`, negative, and non-integer text.
- Steps: validate boundaries; execute with and without a CLI override; inspect retry construction and `request_timeout`; invoke each invalid value.
- Expected stdout/stderr/exit: valid requests produce one success result and exit `0`; retry and SDK receive the same chosen integer; invalid values write one JSON user-input envelope on stdout and exit `1` with no ACL/client/network call.
- Cleanup: restore config defaults and call records.
- Evidence mapping: ADR-002, DESIGN-016 invocation contract; story AC 12; `test_timeout_accepts_adr_002_bounds`, `test_invalid_timeout_stops_before_acl_or_client`.

### STR-TC-021 - Output formats: JSON, TOON, auto, and pretty

- Type: positive, output, boundary.
- Given success results of each shape, when `--format json|toon|auto` and `--pretty` run, then single models, `None` results, batch record arrays, and structured errors follow the ADR-004 rules.
- Command/function: `OutputFormatter` via representative commands.
- Prerequisites/fixtures: a single `Dataset`/`Stream`/`Subscriber`, `None` results (`publish-record`, `publish-records`, `publish-binary-record`, `subscriber delete`), `PartitionOffsets` (`commit-offsets`, `get-read-position`, `reset-offsets`), a uniform record array (`get-records`, `read-records`), an empty record array, structured error.
- Steps: run each shape under each format; validate stdout parses as JSON where required; verify pretty indentation when enabled.
- Expected stdout/stderr/exit: exit `0`; auto selects TOON only for uniform non-empty arrays, otherwise JSON; empty/non-uniform output is JSON; `None` results serialize `null`/empty consistently; batch arrays are emitted once per the ADR-003 contract; error output remains the structured JSON envelope.
- Cleanup: clear captures and models.
- Evidence mapping: ADR-004, DESIGN-016 output contract; story AC 12; `test_output_toon_and_json_formats` (namespace) plus shared `OutputFormatter` coverage in tests/unit_test_retry_error_output_log.py.

### STR-TC-022 - NDJSON stderr, stream separation, and confidentiality

- Type: positive, output, confidentiality.
- Given successful create, publish, and batch-read runs, when logs and results flow, then success data appears once on stdout, diagnostics are NDJSON on stderr, and credential/body/record/response sentinels never appear anywhere.
- Command/function: representative create, publish, and batch-read commands.
- Prerequisites/fixtures: secret sentinels embedded in request/response fixtures; captured logs.
- Steps: run each command; scan stdout, stderr, and captured logs for sentinel values, raw record payloads, and request bodies.
- Expected stdout/stderr/exit: exit `0`; stdout carries results/metadata envelopes only; stderr carries NDJSON diagnostics only (empty or safe); none of the sentinels, payloads, or bodies appear in any stream or log.
- Cleanup: clear sentinels and temporary files.
- Evidence mapping: ADR-005, DESIGN-016 log contract; story AC 12, 13; `test_sensitive_values_not_echoed_in_errors` (namespace) plus the NDJSON stderr/log-setup tests in tests/unit_test_retry_error_output_log.py (TestNdJsonFormatter and log-setup stderr tests).

### STR-TC-023 - Import, console boundary, help, and thin launcher

- Type: packaging, side-effect regression.
- Given the package and Claude launcher, when imported or asked for help, then they load without configuration, network, or filesystem side effects and use one event-loop boundary.
- Command/function: package import, launcher import, module `--help`, launcher `--help`, `console_main()`.
- Prerequisites/fixtures: empty arbitrary directory; guarded config/network/filesystem constructors; `asyncio.run` spy.
- Steps: import all Streams modules and launcher; invoke root and operation help; call `console_main()` with fake `main()`; inspect launcher source.
- Expected stdout/stderr/exit: imports produce no output or files; help exits `0` and names the 15 operations; `console_main()` calls `asyncio.run()` once and propagates the result; launcher delegates to packaged interfaces and contains no copied catalog, batch, or ACL logic.
- Cleanup: remove subprocess directory and restore the event-loop spy.
- Evidence mapping: DESIGN-016 packaging contract; story AC 14; `test_console_main_uses_one_asyncio_run_boundary` (namespace); the thin-launcher pattern follows `test_claude_launcher_is_thin_and_reexports_packaged_interfaces` (tests/test_audit_console_wrapper.py) and import side-effect-freedom is verified by the TESTEXEC-016 subprocess probe.

### STR-TC-024 - Wheel, editable install, entry-point preservation, and regression

- Type: installation, regression.
- Given local wheel and editable installs, when commands run from an arbitrary directory without `PYTHONPATH`, then `foundry-streams` and the Claude launcher work while existing console scripts and repository gates remain intact.
- Command/function: local wheel build; wheel and editable install; installed `foundry-streams --help`; Claude launcher help; full test, Ruff, mypy, and package checks.
- Prerequisites/fixtures: isolated virtual environments for Python 3.11 and 3.12; `PIP_NO_INDEX=1`; local build dependencies; snapshot of existing `[project.scripts]` entries.
- Steps: build without live dependency resolution; inspect wheel for the Streams policy; install wheel then editable form with `--no-deps`; run help and packaged ACL probe from arbitrary CWD; compare every pre-existing entry point; run focused Streams tests and full regression with branch coverage.
- Expected stdout/stderr/exit: every help and package check exits `0`; wheel contains `foundry_cli/streams/metadata-allow-list.md`; all 15 operations are listed; all prior console scripts remain; focused and full suites pass on both Python versions; Ruff and mypy pass; repository branch coverage is at least 80%; no command makes a live Foundry request.
- Cleanup: delete isolated builds and environments; retain command output in TESTEXEC evidence only.
- Evidence mapping: DESIGN-016 packaging and regression contract; story AC 14, 15; all `tests/test_foundry_streams_*` cases and the configured `pyproject.toml` gates.

## Traceability matrix

| Requirement area | Story/design criteria | Cases |
| --- | --- | --- |
| Exact 15 catalog, no pagination, parser, help, nested routing, input omission | Story AC 1; scope comment; operation catalog | STR-TC-001 through 003 |
| JSON argument validation, pre-client rejection | Story AC 2 | STR-TC-004 |
| ADR-003 batch reads: aggregation on exit, offset semantics, caps, bounded binary publish | Story AC 3, 4, 5 | STR-TC-005 through 008 |
| Streams timeout override and shared timeout bounds | Story AC 6, 12 | STR-TC-009, 020 |
| ACL precedence, read-only 10-op write set, semantic reads, reset classification, fail-closed policy | Story AC 7, 8 | STR-TC-010 through 014 |
| include_attribution=False and B3 only | Story AC 9, 10 | STR-TC-015 through 017 |
| Retry, error taxonomy | Story AC 11, 13 | STR-TC-018, 019 |
| Output formats, NDJSON, confidentiality | Story AC 12, 13 | STR-TC-021, 022 |
| Imports, console, launcher, wheel/editable, regression gates | Story AC 14, 15 | STR-TC-023, 024 |
| Positive, negative, boundary, security, resilience, structural, packaging | Complete design strategy | STR-TC-001 through 024 |

All story acceptance criteria have at least one positive case and, where meaningful, a negative, boundary, security, or failure-path case. The 15-operation catalog is fully covered: Dataset (1) via STR-TC-001 through 003 plus ACL cases; Stream (8) via STR-TC-001 through 008 plus ACL cases; Subscriber (6) via STR-TC-001 through 007 plus ACL cases.

## Execution and approval criteria

TESTEXEC-016 may begin only after DEV, UNITTEST, CODEREVIEW, and TESTCASE-016 reach their required completed states and the approved commit is available. Execute all 24 cases with no live network access unless an approved non-production smoke is explicitly authorized.

For every case, record PASS, FAIL, or BLOCKED with the exact command, environment, expected result, actual result, stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, and linked evidence. Any failure requires a BUG-SUB before TESTEXEC-016 can close. Final QA sign-off also requires all linked defects to be terminal, every story acceptance criterion to have passing evidence, supported Python checks to pass, and repository branch coverage to remain at least 80%.
