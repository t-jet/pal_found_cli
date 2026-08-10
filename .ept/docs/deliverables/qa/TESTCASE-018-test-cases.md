# TESTCASE-018 - Foundry Media Sets CLI QA test cases

## Scope

These cases cover DEV-STORY-018 and the complete approved surface of `foundry-media-sets`: 19 `foundry_sdk.v2.media_sets` operations across the single `MediaSet` client path. They verify the exact catalog and parser, nested SDK routing and dispatch, JSON argument validation, the transaction lifecycle (create/commit/abort/clear), the four bounded binary downloads (`get_result`, `read`, `read_original`, `retrieve`) streamed through `with_streaming_response` and persisted by `BinaryDownloadHandler` with the FR-DL JSON envelope, the two bounded binary uploads (`upload`, `upload_media`), the 9-operation write set, the packaged 5-permitted/14-blocked metadata-only policy, `include_attribution=True` per FR-ATTR-4, B3 tracing, retry and error behavior, output and log contracts, privacy, packaging, and regression gates.

Routine acceptance uses mocked async SDK transport and real installed SDK exception classes. Live credentials and live Foundry access are not required. An approved non-production smoke is optional and cannot replace the mandatory mocked evidence.

## Source baseline

- [DESIGN-018](../architecture/DESIGN-018-media-sets-cli.md), completed and closed for DEV-STORY-018.
- [DESIGN-005](../architecture/DESIGN-005-common-components.md), covering bounded streaming via `BinaryDownloadHandler` and SDK-native B3 tracing.
- [DESIGN-015](../architecture/DESIGN-015-sql-queries-cli.md), covering the bounded binary download pattern this story extends to four operations.
- [DESIGN-011](../architecture/DESIGN-011-aip-agents-cli.md), [DESIGN-012](../architecture/DESIGN-012-language-models-cli.md), [DESIGN-013](../architecture/DESIGN-013-models-cli.md), [DESIGN-014](../architecture/DESIGN-014-orchestration-cli.md) — the sibling namespace patterns this story mirrors (nested dispatch, metadata-only policy).
- [ADR-001](../architecture/adr/ADR-001-exit-code-taxonomy.md), [ADR-002](../architecture/adr/ADR-002-call-timeout-defaults.md), [ADR-004](../architecture/adr/ADR-004-format-auto-algorithm.md), [ADR-005](../architecture/adr/ADR-005-log-format.md), [ADR-006](../architecture/adr/ADR-006-env-file-search-path.md), [ADR-007](../architecture/adr/ADR-007-operation-level-readonly.md).
- The canonical environment-variable reference and metadata allow-list (namespace `media_sets`, 19 rows; `media_set.get`, `media_set.get_rid_by_path`, `media_set.get_status`, `media_set.info`, `media_set.metadata` PERMITTED, the other 14 BLOCKED in tier 3; `FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS` per FR-ATTR-4).
- Vendored SDK sources under `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/media_sets/` — the real `MediaSetClient` methods, request paths, and result types.
- DEV-STORY-018 ticket body, `release_notes`, and technical scope comment (authoritative 19-operation catalog).
- Implementation verified at HEAD `62c269f`: `src/foundry_cli/media_sets/`, `.claude/skills/foundry-media-sets/`, and `pyproject.toml` (entry point `foundry-media-sets`).

## Preconditions and shared fixtures

- Python 3.11 and 3.12 environments contain the project, development dependencies, and pinned `foundry-sdk`.
- Use a nested async SDK fake rooted at `client.media_sets` with exactly one public sub-client: `MediaSet` (abort, calculate, clear, commit, create, get, get_result, get_rid_by_path, get_status, info, metadata, read, read_original, reference, register, retrieve, transform, upload, upload_media). A wrong, flattened, raw, or streaming route must fail the fixture. No other sub-client may be reachable from any catalog dispatch.
- The four download commands use `client.media_sets.MediaSet.with_streaming_response.<method>` returning a streaming context with `aiter_bytes`; the stream is bounded by `BinaryDownloadHandler` (`FOUNDRY_AGENTIC_CLI_MAX_DOWNLOAD_BYTES`, default 1,572,864 bytes) and persisted atomically under the download root (default `.foundry-data/downloads`, per-download UUID directory, temp file `os.replace`, cleanup on failure). The FR-DL JSON envelope (`file_path`, `file_size`, `checksum_md5`, `checksum_sha256`, `mime_type`, `truncated`, nullable `source_size`, nullable `source_size_at_least`) is emitted to stdout. `--output` selects the target file name.
- The two upload commands (`upload`, `upload_media`) read `--file` bounded (`_read_file_bounded`, 16 MiB cap) after the ACL decision and before client construction. `upload_media` requires both `--file` and `--filename`.
- No operation returns a `ResourceIterator`; no `PaginationHelper` may be invoked for any command.
- Use real installed SDK model validators for nested invalid-input checks and real `foundry_sdk._errors` classes for error taxonomy checks. Mock network transport; no service call or billable media transfer is permitted.
- Set retry delay to zero, disable jitter, and use two retries unless a case states otherwise. Capture attempt number, timeout, attribution, and B3 values.
- Capture stdout, stderr, logs, SDK arguments, context variables, client/network constructors, and filesystem changes independently. Do not retain credential, token, body, or response sentinel values.
- Packaging cases build a clean local archive with dependency resolution disabled, install with `--no-deps`, and run from an arbitrary empty working directory without `PYTHONPATH`.
- Any optional live smoke uses an approved non-production Foundry tenant, synthetic media items, least-privilege credentials, and a cleanup plan. Credentials must never enter retained evidence.
- TESTEXEC records the commit, OS, Python and SDK versions, environment type, exact command, expected and actual stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, evidence reference, and PASS/FAIL/BLOCKED status for every case.

## Test data

| Name | Fixture |
| --- | --- |
| Media set RID | `ri.mediasets.main.media-set.test` |
| Media item RID | `ri.mediasets.main.media-item.test` |
| Transaction ID | `qa-transaction-001` |
| Transformation job ID | `qa-job-001` |
| Media item path | `folder/item.bin` |
| Physical item name | `qa-physical-item-001` |
| Branch name | `master` |
| Branch RID | `ri.compass.main.branch.test` |
| View RID | `ri.views.main.view.test` |
| Read token | `qa-read-token` |
| Transformation JSON | `{"type": "imagery:thumbnail"}` |
| Download output file | `item.bin`; unsafe variants `../escape`, `..\\escape`, `/absolute`, `.` |
| Download stream fixtures | empty stream; `b"media-bytes"`; a stream above the configured bound (e.g. `b"x" * 200` with a 100-byte bound) |
| Upload file payloads | empty file; `b"media-bytes"`; a file above the 16 MiB upload cap; missing path |
| Filename variants | `item.bin` (valid), `temp.bin` (upload-media) |
| Timeout boundaries | `1`, `30` (default), `3600`; invalid `0`, `3601`, non-integer text |
| Secret sentinels | `sentinel-secret-018`, `sentinel-token-secret`, `sentinel-body-secret`, `sentinel-response-secret`, `sentinel-attribution-rid` |

## Command and route inventory

Every inventory row is exercised by MDT-TC-001 through MDT-TC-003. Unless a case states otherwise, success writes one formatted result to stdout, writes no application data to stderr, exits `0`, and leaves no command-specific file outside the download root for download cases.

| CLI command | Exact public SDK route and method | Required input | Optional input |
| --- | --- | --- | --- |
| `media-set abort MEDIA_SET_RID TRANSACTION_ID` | `client.media_sets.MediaSet.abort` | `media_set_rid`, `transaction_id` | `--preview`, shared options |
| `media-set calculate MEDIA_SET_RID MEDIA_ITEM_RID` | `client.media_sets.MediaSet.calculate` | `media_set_rid`, `media_item_rid` | `--preview`, `--read-token`, shared options |
| `media-set clear MEDIA_SET_RID --media-item-path ...` | `client.media_sets.MediaSet.clear` | `media_set_rid`, `--media-item-path` | `--branch-name`, `--branch-rid`, `--preview`, `--transaction-id`, `--view-rid`, shared options |
| `media-set commit MEDIA_SET_RID TRANSACTION_ID` | `client.media_sets.MediaSet.commit` | `media_set_rid`, `transaction_id` | `--preview`, shared options |
| `media-set create MEDIA_SET_RID` | `client.media_sets.MediaSet.create` | `media_set_rid` | `--branch-name`, `--preview`, shared options |
| `media-set get MEDIA_SET_RID` | `client.media_sets.MediaSet.get` | `media_set_rid` | `--preview`, shared options |
| `media-set get-result MEDIA_SET_RID MEDIA_ITEM_RID TRANSFORMATION_JOB_ID --output ...` | `client.media_sets.MediaSet.get_result` | `media_set_rid`, `media_item_rid`, `transformation_job_id`, `--output` | `--preview`, `--token`, shared options |
| `media-set get-rid-by-path MEDIA_SET_RID --media-item-path ...` | `client.media_sets.MediaSet.get_rid_by_path` | `media_set_rid`, `--media-item-path` | `--branch-name`, `--branch-rid`, `--preview`, `--view-rid`, shared options |
| `media-set get-status MEDIA_SET_RID MEDIA_ITEM_RID TRANSFORMATION_JOB_ID` | `client.media_sets.MediaSet.get_status` | `media_set_rid`, `media_item_rid`, `transformation_job_id` | `--preview`, `--token`, shared options |
| `media-set info MEDIA_SET_RID MEDIA_ITEM_RID` | `client.media_sets.MediaSet.info` | `media_set_rid`, `media_item_rid` | `--preview`, `--read-token`, shared options |
| `media-set metadata MEDIA_SET_RID MEDIA_ITEM_RID` | `client.media_sets.MediaSet.metadata` | `media_set_rid`, `media_item_rid` | `--preview`, `--read-token`, shared options |
| `media-set read MEDIA_SET_RID MEDIA_ITEM_RID --output ...` | `client.media_sets.MediaSet.read` | `media_set_rid`, `media_item_rid`, `--output` | `--preview`, `--read-token`, shared options |
| `media-set read-original MEDIA_SET_RID MEDIA_ITEM_RID --output ...` | `client.media_sets.MediaSet.read_original` | `media_set_rid`, `media_item_rid`, `--output` | `--preview`, `--read-token`, shared options |
| `media-set reference MEDIA_SET_RID MEDIA_ITEM_RID` | `client.media_sets.MediaSet.reference` | `media_set_rid`, `media_item_rid` | `--preview`, `--read-token`, shared options |
| `media-set register MEDIA_SET_RID --physical-item-name ...` | `client.media_sets.MediaSet.register` | `media_set_rid`, `--physical-item-name` | `--branch-name`, `--media-item-path`, `--preview`, `--transaction-id`, `--view-rid`, shared options |
| `media-set retrieve MEDIA_SET_RID MEDIA_ITEM_RID --output ...` | `client.media_sets.MediaSet.retrieve` | `media_set_rid`, `media_item_rid`, `--output` | `--preview`, `--read-token`, shared options |
| `media-set transform MEDIA_SET_RID MEDIA_ITEM_RID --transformation-json ...` | `client.media_sets.MediaSet.transform` | `media_set_rid`, `media_item_rid`, `--transformation-json` | `--preview`, `--token`, shared options |
| `media-set upload MEDIA_SET_RID --file ...` | `client.media_sets.MediaSet.upload` | `media_set_rid`, `--file` | `--branch-name`, `--branch-rid`, `--media-item-path`, `--media-item-rid`, `--preview`, `--transaction-id`, `--view-rid`, shared options |
| `media-set upload-media --file ... --filename ...` | `client.media_sets.MediaSet.upload_media` | `--file`, `--filename` | `--media-item-rid`, `--preview`, shared options |

No command may receive `attribution`, `_sdk_internal`, an absent optional set to `None`, or any unsupported paging, stream, raw-response, or file flag. No pagination flags may exist in `OP_SPECS` or the parser.

## Test cases

### MDT-TC-001 - Catalog, parser, help, and exact 19 surface

- Type: positive, structural, negative parser.
- Given the installed module and launcher, when the catalog and parser are inspected, then exactly 19 unique SDK specifications exist (all on the single `media_set` resource), every inventory command parses, and no pagination flag exists anywhere in the surface.
- Command/function: `OP_SPECS`, `build_parser()`, `_spec_for()`, `_get_client()`, root/resource/operation `--help`, `main()` with missing resource/operation, unknown flags, missing required positionals/options, invalid choices/types.
- Prerequisites/fixtures: guarded config, client, network, and filesystem constructors.
- Steps: count `OP_SPECS`; assert no `--page-size`/`--page-token`/`--all`/`--max-pages` flag in any parser; parse all 19 inventory commands; run all help surfaces; run every incomplete or malformed form.
- Expected stdout/stderr/exit: help on stdout and exit `0`; catalog count exactly `19`; parser errors as one JSON envelope on stdout with `exit_code: 1`, empty diagnostic stderr, no traceback, no config/client/network/filesystem call.
- Cleanup: restore `sys.argv` and capture streams.
- Evidence mapping: DESIGN-018 catalog; story scope comment; `test_catalog_contains_exact_19_operations`, `test_parser_accepts_every_declared_argument`, `test_parser_rejects_unknown_operation` (tests/test_foundry_media_sets_cli.py); absence of pagination flags and `--help` behavior are verified by those catalog/parser tests plus the module `--help` probe recorded in TESTEXEC-018 evidence.

### MDT-TC-002 - Nested SDK routing across the single client path

- Type: positive, structural, route identity.
- Given a fake for `MediaSet`, when every inventory command runs, then each resolves the exact `client.media_sets.MediaSet` object and never a flattened or sibling route.
- Command/function: `_get_client()` and each dispatch path.
- Prerequisites/fixtures: fakes whose sibling routes fail on access.
- Steps: run one command per operation group (metadata, transaction, content, transformation); assert the resolved resource object identity; assert no flattened `media_sets.*` method call.
- Expected stdout/stderr/exit: success results on stdout once, exit `0`, no unexpected stderr; no flattened `media_sets.*` method call.
- Cleanup: reset fakes and captures.
- Evidence mapping: DESIGN-018 nested dispatch; story AC 1; `test_catalog_contains_exact_19_operations` (all nineteen resolve through the single `MediaSet` client path) plus the dispatch tests `test_media_set_get_dispatches_exact_arguments`, `test_transform_dispatches_with_json_transformation`.

### MDT-TC-003 - Required inputs forwarded and absent optionals omitted

- Type: positive, structural.
- Given each inventory command, when dispatch runs, then required positionals/options reach the SDK call and every absent optional is omitted (never `None`).
- Command/function: all 19 dispatches.
- Prerequisites/fixtures: recording SDK fakes.
- Steps: run each command with only required inputs; run `media-set create` with and without `--branch-name`; run `media-set clear`/`register` with and without `--transaction-id`/`--branch-name`/`--view-rid`; run `media-set upload` with and without `--transaction-id`; run `media-set transform` with and without `--token`; run `media-set calculate` with and without `--read-token`.
- Expected stdout/stderr/exit: SDK call arguments contain exactly the documented keys; success exits `0`; absent optionals absent from kwargs; `--preview` maps to a boolean flag value.
- Cleanup: clear fake call records.
- Evidence mapping: DESIGN-018 operation catalog; story AC 1; `test_media_set_get_dispatches_exact_arguments`, `test_transform_dispatches_with_json_transformation`, `test_transaction_lifecycle_dispatch` (absent optionals omitted).

### MDT-TC-004 - JSON argument validation before client creation

- Type: positive, negative, boundary.
- Given the structured flag `--transformation-json`, when validation runs, then valid JSON with the documented top-level shape reaches the SDK and invalid or mis-shaped JSON exits `1` before client or network work.
- Command/function: JSON validators, `main()`.
- Prerequisites/fixtures: guarded factory/network constructors; real SDK validators for nested checks.
- Steps: supply a valid transformation payload; supply malformed JSON text; supply valid JSON with the wrong top-level type; supply JSON whose nested fields violate SDK validators.
- Expected stdout/stderr/exit: valid input calls the SDK and exits `0`; invalid inputs write one JSON user-input envelope to stdout, exit `1`, no traceback, and never echo the input payload into stdout/stderr/logs.
- Cleanup: clear captured sentinels.
- Evidence mapping: DESIGN-018 JSON validation contract; story AC 2; `test_invalid_transformation_json_rejected_before_client` (valid decode and rejection before client creation).

### MDT-TC-005 - Transaction lifecycle: create, commit, abort, clear

- Type: positive, structural, stateful.
- Given a transactional media set, when the CLI drives `media-set create`, `media-set upload --transaction-id`, `media-set commit`, `media-set abort`, and `media-set clear --transaction-id`, then the returned `TransactionId` is surfaced, `commit` makes items visible, `abort` deletes them, and `clear` requires an explicit `--transaction-id` (the CLI does not auto-manage transactions).
- Command/function: `media-set create`, `commit`, `abort`, `clear`, `upload` dispatch.
- Prerequisites/fixtures: recording SDK fakes; `TransactionId` response fake; `commit`/`abort`/`clear` `None` result fakes.
- Steps: run `create` and capture the transaction id; run `upload --transaction-id`; run `commit`; run `abort` on a separate created transaction; run `clear --transaction-id`.
- Expected stdout/stderr/exit: each step exits `0`; `create` prints the transaction id on stdout; `upload` forwards `transaction_id`; `commit`/`abort`/`clear` call the SDK with the transaction id; no CLI-level state persists between invocations.
- Cleanup: clear fakes and captures.
- Evidence mapping: DESIGN-018 transaction contract; story AC 3, 5; `test_transaction_lifecycle_dispatch` (tests/test_foundry_media_sets_cli.py).

### MDT-TC-006 - Bounded binary upload: upload reads file before client creation

- Type: positive, boundary, negative.
- Given a local file, when `media-set upload --file` runs, then the file content is read in a bounded and validated way after the ACL decision and passed as `bytes` to the SDK, with files above the 16 MiB upload cap and missing paths rejected before client construction.
- Command/function: `media-set upload` dispatch; `_read_file_bounded()`.
- Prerequisites/fixtures: empty file; `b"media-bytes"` file; a file above the 16 MiB cap; missing path; guarded factory/transport.
- Steps: upload each file; assert the SDK body bytes; attempt the oversized file and a missing path; inspect event order.
- Expected stdout/stderr/exit: valid files reach the SDK as the exact byte content and exit `0`; oversized or missing files write one JSON user-input envelope on stdout and exit `1` with no client or network call.
- Cleanup: remove temporary files.
- Evidence mapping: DESIGN-018 binary upload contract; story AC 5; `test_upload_reads_file_bounded`, `test_upload_rejects_missing_file` (tests/test_foundry_media_sets_cli.py); the oversized-file rejection is verified by the `_read_file_bounded` 16 MiB bound probe recorded in TESTEXEC-018 evidence.

### MDT-TC-007 - Bounded binary upload: upload-media requires filename

- Type: positive, boundary, negative.
- Given a local file and `--filename`, when `media-set upload-media` runs, then the file content is read bounded and passed as `bytes` with the `filename` kwarg, and a missing `--filename` is rejected by the parser before client construction.
- Command/function: `media-set upload-media` dispatch; parser required-option validation.
- Prerequisites/fixtures: recording SDK fake; empty and populated files; missing `--filename` form.
- Steps: run with `--file` and `--filename`; run with `--file` only; run with a missing path; assert the SDK body bytes and `filename` kwarg.
- Expected stdout/stderr/exit: valid run exits `0` and calls the SDK with the exact bytes and `filename`; missing `--filename` or missing file writes one JSON user-input envelope on stdout and exits `1` before client/network work.
- Cleanup: remove temporary files and captures.
- Evidence mapping: DESIGN-018 upload-media contract; story AC 5; `test_upload_media_dispatches_with_filename`, `test_parser_accepts_every_declared_argument` (upload-media with `--file` and `--filename`), `test_upload_rejects_missing_file`.

### MDT-TC-008 - Binary download: read persists atomically and reports FR-DL envelope

- Type: positive, structural, filesystem.
- Given a streamed content response, when `media-set read --output` runs, then the stream is read bounded through `with_streaming_response`, the file is persisted atomically under the download root (temp file then `os.replace`, no partial file on failure), and the FR-DL envelope (`file_path`, `file_size`, `checksum_md5`, `checksum_sha256`, `mime_type`, `truncated`, `source_size`, `source_size_at_least`) is emitted to stdout.
- Command/function: `media-set read` dispatch; `_download_operation()`; `BinaryDownloadHandler.save()`.
- Prerequisites/fixtures: `_StreamingMediaSet` fake with `aiter_bytes`; temp download root; known payload `b"media-bytes"`; a stream failure fake.
- Steps: run with `--output item.bin`; verify the final file bytes, checksums against the payload, envelope fields, and directory structure; inject a stream failure mid-way and verify the partial and temp files are removed and no final file remains.
- Expected stdout/stderr/exit: exit `0`; file written at the envelope `file_path` with exact bytes and matching md5/sha256; `truncated` false and `source_size` equal to the payload size; failure path exits with the mapped error code and leaves no partial or temp artifact.
- Cleanup: remove the download root and captures.
- Evidence mapping: DESIGN-018 binary download contract; story AC 4; `test_read_download_writes_atomically_and_reports_envelope` (tests/test_foundry_media_sets_cli.py) plus the shared `BinaryDownloadHandler` atomicity tests in tests/test_binary_download.py (`test_stream_failure_removes_partial_and_temporary_files`, `test_concurrent_same_name_downloads_never_overwrite`).

### MDT-TC-009 - Binary downloads: read-original, retrieve, get-result envelope equivalence

- Type: positive, structural.
- Given streamed responses for the three remaining download operations, when `media-set read-original`, `media-set retrieve`, and `media-set get-result` run, then each writes its file atomically and emits the same FR-DL envelope shape with operation-correct routing.
- Command/function: `media-set read_original`, `retrieve`, `get_result` dispatch; `_download_operation()`.
- Prerequisites/fixtures: `_StreamingMediaSet` fake exposing all three methods; temp download root; `--output` for each; token/read-token optional flags.
- Steps: run each command with `--output`; verify routing to the correct streaming method, the persisted file, and the envelope; run without `--output` to exercise the operation-derived default filename.
- Expected stdout/stderr/exit: exit `0` for each; each file persisted with exact bytes and valid checksums; envelope `truncated` false; without `--output` the filename derives from the operation with a `.bin` fallback extension; no partial artifacts.
- Cleanup: remove the download root and captures.
- Evidence mapping: DESIGN-018 binary download contract; story AC 4; `test_read_original_retrieve_get_result_download_envelopes` (tests/test_foundry_media_sets_cli.py).

### MDT-TC-010 - Binary download truncation when stream exceeds the bound

- Type: boundary, negative, filesystem.
- Given a stream whose source length exceeds the configured download bound, when a download command runs, then `BinaryDownloadHandler` stores only the bounded prefix, sets `truncated` true with `source_size_at_least`, emits a warning to stderr, and leaves a valid prefix file with correct checksums.
- Command/function: `_download_operation()`; `BinaryDownloadHandler.save()` with `FOUNDRY_AGENTIC_CLI_MAX_DOWNLOAD_BYTES` (default 1,572,864).
- Prerequisites/fixtures: a stream of 200 bytes with a 100-byte bound; temp download root.
- Steps: run `media-set read` against the oversized stream; inspect the stored file size, `truncated`, `file_size`, `source_size_at_least`, and stderr warning.
- Expected stdout/stderr/exit: exit `0`; stored file has exactly `limit` bytes; envelope `truncated` true, `file_size` equal to the bound, `source_size_at_least` equal to `limit + 1`; stderr carries one warning NDJSON line; checksums match the stored prefix.
- Cleanup: remove the download root and captures.
- Evidence mapping: DESIGN-005 FR-DL bound; story AC 4; `test_download_truncates_when_stream_exceeds_limit` (tests/test_foundry_media_sets_cli.py) plus shared tests in tests/test_binary_download.py (`test_unknown_length_reads_only_limit_plus_one_and_hashes_stored_prefix`, `test_known_oversize_stops_after_prefix_and_keeps_declared_size`).

### MDT-TC-011 - Binary download filename safety and path confinement

- Type: security, negative.
- Given unsafe `--output` values, when a download command runs, then the CLI rejects separators, absolute paths, and dot-path escapes before any file is created, and the final file is confined under the download root.
- Command/function: `BinaryDownloadHandler._safe_filename()`; `_download_operation()`.
- Prerequisites/fixtures: unsafe names `../escape`, `..\\escape`, `/absolute`, `.`, `.`; empty name; temp download root; guarded stream fakes.
- Steps: run `media-set read --output <unsafe>` for each variant; run with an empty name; verify no file is created outside the root.
- Expected stdout/stderr/exit: each unsafe or empty name writes one JSON user-input envelope on stdout and exits `1` with no file created; valid names stay under the download root and exit `0`.
- Cleanup: remove the download root.
- Evidence mapping: DESIGN-005 filename safety; story AC 4, 13; `test_download_rejects_unsafe_filename` (tests/test_foundry_media_sets_cli.py) plus shared `test_unsafe_filename_is_rejected_before_root_creation` and `test_download_dir_permissions_are_umask_independent_on_posix` (tests/test_binary_download.py).

### MDT-TC-012 - Timeout boundaries and forwarding

- Type: positive, boundary, negative.
- Given CLI or configured timeouts, when execution starts, then values from 1 through 3600 seconds are accepted and the selected value reaches both retry handling and the SDK request; invalid values are rejected before ACL, scope, client, or filesystem work.
- Command/function: `_validate_timeout()`, representative commands with `--timeout`.
- Prerequisites/fixtures: values `1`, `30` (default), `3600`, CLI override `17`, configured default `42`, invalid `0`, `3601`, negative, and non-integer text.
- Steps: validate boundaries; execute with and without a CLI override; inspect retry construction and `request_timeout`; invoke each invalid value.
- Expected stdout/stderr/exit: valid requests produce one success result and exit `0`; retry and SDK receive the same chosen integer; invalid values write one JSON user-input envelope on stdout and exit `1` with no ACL/client/network call.
- Cleanup: restore config defaults and call records.
- Evidence mapping: ADR-002, DESIGN-018 invocation contract; story AC 12; `test_timeout_accepts_adr_002_bounds`, `test_invalid_timeout_returns_user_input_error` (tests/test_foundry_media_sets_cli.py).

### MDT-TC-013 - ACL precedence: global, namespace, and operation scopes

- Type: security, positive, negative.
- Given metadata-only and operation-level overrides, when ACL evaluates `MEDIA_SETS`, then permissive settings allow, blocking settings deny, and an operation override wins over the namespace setting.
- Command/function: `AccessControlGuard(cfg, "MEDIA_SETS").check()` for representative operations.
- Prerequisites/fixtures: packaged Media Sets allow-list and isolated environment variables.
- Steps: enable global metadata-only; check permitted and blocked operations; disable Media Sets metadata-only at namespace level; disable one operation explicitly; combine namespace read-only with an operation override.
- Expected stdout/stderr/exit: permitted checks return silently; blocked CLI calls write a structured ACL envelope to stdout, exit `8`, and do not create a client; the denying rule appears on stderr diagnostics; no secret appears.
- Cleanup: remove every ACL environment variable.
- Evidence mapping: DESIGN-018 access-control table; story AC 7; `test_acl_write_classification_matches_design`, `test_metadata_only_allowlist_parses_exactly` (precedence exercised through the namespace runtime checks).

### MDT-TC-014 - Read-only mode blocks the 9-operation write set; content reads stay semantic reads

- Type: security, positive, negative.
- Given read-only mode enabled, when each write command runs, then `media-set abort`, `media-set calculate`, `media-set clear`, `media-set commit`, `media-set create`, `media-set register`, `media-set transform`, `media-set upload`, and `media-set upload-media` exit `8` before client or filesystem effects, while `media-set read`, `media-set read-original`, `media-set retrieve`, and `media-set get-result` remain executable as semantic reads despite exposing content.
- Command/function: `AccessControlGuard` + `main()` for each write command and the four content reads.
- Prerequisites/fixtures: read-only environment; guarded factory/transport; stream and response fakes.
- Steps: run all 9 write commands under read-only; run the four content reads under read-only; inspect event order.
- Expected stdout/stderr/exit: each blocked write emits one ACL envelope and exit `8` with the denying rule on stderr; no SDK call occurs; the four content reads succeed and exit `0`.
- Cleanup: clear read-only variables, captures, and records.
- Evidence mapping: DESIGN-018 read-only policy; story AC 7; `test_readonly_blocks_nine_write_operations` (tests/test_foundry_media_sets_cli.py).

### MDT-TC-015 - Metadata-only tier: exact 5 permitted / 14 blocked

- Type: security, positive, negative.
- Given metadata-only mode, when every operation is checked, then exactly the 5 documented reads (`media_set.get`, `media_set.get_rid_by_path`, `media_set.get_status`, `media_set.info`, `media_set.metadata`) are permitted and the other 14 operations (all mutations and all content reads/downloads) are blocked.
- Command/function: `AccessControlGuard` metadata-only evaluation over the full 19-op catalog.
- Prerequisites/fixtures: packaged Media Sets allow-list; the full catalog.
- Steps: assert the permitted set equals the 5 documented reads; assert every mutation and content read (including `read`, `read_original`, `retrieve`, `get_result`) is blocked.
- Expected stdout/stderr/exit: 5 permitted checks return silently; each of the 14 blocked CLI calls writes an ACL envelope and exits `8` with the denying rule on stderr; no client or file effect.
- Cleanup: clear metadata-only variables.
- Evidence mapping: DESIGN-018 metadata policy; story AC 8; `test_metadata_only_allowlist_parses_exactly`, `test_metadata_only_permits_five_and_blocks_fourteen` (tests/test_foundry_media_sets_cli.py); verified live at HEAD `62c269f` (probe: `MEDIA_PERMITTED: 5` matching the allow-list exactly, `MEDIA_BLOCKED: 14`).

### MDT-TC-016 - Packaged metadata-only policy is fail closed and CWD independent

- Type: security, packaging, negative.
- Given the installed package with a missing or malformed packaged allow-list, when ACL runs, then it fails closed (no operation permitted) and the packaged policy resolves from an arbitrary working directory.
- Command/function: `_METADATA_ALLOWLIST_PATH`, `AccessControlGuard` from an installed wheel/editable launch.
- Prerequisites/fixtures: malformed/missing policy fixtures in an isolated environment; empty arbitrary CWD, no `PYTHONPATH`.
- Steps: probe policy path from the installed package; run a permitted-class check with malformed policy; run checks from the arbitrary CWD.
- Expected stdout/stderr/exit: malformed/missing policy blocks even previously-permitted operations (fail closed, exit `8`); packaged policy path resolves inside the installed package; valid packaged policy applies the 5/14 rule from any CWD.
- Cleanup: delete isolated environments and fixtures.
- Evidence mapping: DESIGN-018 fail-closed rule; story AC 8, 14; `test_metadata_only_allowlist_parses_exactly` (parsed from the packaged allow-list); packaged-policy CWD independence follows the same pattern as `test_packaged_metadata_policy_is_cwd_independent` (tests/test_foundry_audit_cli.py) and is verified by the TESTEXEC-018 wheel/editable probe.

### MDT-TC-017 - include_attribution=True on client, scope, and SDK calls

- Type: positive, privacy, structural.
- Given FR-ATTR-4 attribution enabled, when a command executes, then client creation and scope use `include_attribution=True`, the attribution RID is passed to `transform` and `upload_media` when enabled, and surrounding attribution state is unchanged after success and failure.
- Command/function: `FoundryClientFactory`, `AsyncClientFactory.invocation_scope(cfg)`, `main()`; SDK attribution kwargs on `transform`/`upload_media`.
- Prerequisites/fixtures: factory/scope spies; preset `FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION=true` and `FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS` with a sentinel RID; recording SDK fakes.
- Steps: execute a metadata read and a `transform` with attribution enabled; capture `include_attribution` on client and scope; capture the SDK kwargs; run a failed command; capture attribution state before and after.
- Expected stdout/stderr/exit: both capture points pass `include_attribution=True`; `transform` and `upload_media` receive the attribution RID when enabled; outer attribution state and env are identical after success and failure; no W3C `traceparent`/`tracestate`.
- Cleanup: reset context tokens and env.
- Evidence mapping: DESIGN-018 attribution rule (FR-ATTR-4); story AC 9; `test_invocation_uses_include_attribution_true`, `test_real_factory_restores_attribution_state_after_success`, `test_real_factory_restores_attribution_state_after_failure` (tests/test_foundry_media_sets_cli.py).

### MDT-TC-018 - B3 enabled at outbound transport

- Type: positive, tracing, transport integration.
- Given tracing enabled, when the client is created and an SDK request is prepared, then outbound transport carries one valid B3 multi-header context.
- Command/function: `AsyncClientFactory.invocation_scope(cfg)`, SDK request preparation, a representative metadata read.
- Prerequisites/fixtures: enabled tracing config, clean SDK context, transport header capture.
- Steps: enter the real tracing scope through `main()`; capture headers at client creation and request preparation.
- Expected stdout/stderr/exit: success result and exit `0`; every capture has lowercase-hex `X-B3-TraceId` of 32 characters, `X-B3-SpanId` of 16 characters, and `X-B3-Sampled` `0` or `1`; no W3C header appears.
- Cleanup: reset SDK context tokens and environment variables.
- Evidence mapping: DESIGN-005 B3 contract; story AC 10; `test_b3_transport_headers_enabled_disabled_retry_stable_and_restored` (tests/test_foundry_audit_cli.py) and `test_generated_context_has_valid_nonzero_b3_values_and_resets` (tests/test_tracing_provider.py); the namespace outbound-header probe is recorded in TESTEXEC-018 evidence.

### MDT-TC-019 - B3 disabled, retry stability, and context restoration

- Type: negative, resilience, isolation.
- Given disabled tracing, retries, prior context, or a later formatter failure, when execution leaves the invocation, then disabled calls add no B3 headers, retry attempts share one enabled context, and prior values are restored on every exit path.
- Command/function: `main()` with real `TracingProvider` scope and captured SDK transport headers.
- Prerequisites/fixtures: enabled and disabled configs; first-attempt transport failure followed by success; preset prior trace/span/sampled values; formatter, SDK, timeout, and cancellation failures.
- Steps: run the disabled flow; run the enabled retry flow; run each failure with prior values; inspect every outbound header set and context after exit.
- Expected stdout/stderr/exit: disabled flow has no `X-B3-*`; enabled retry captures identical B3 values for client creation and every attempt; no `traceparent`/`tracestate`; success exits `0`; failures use their ADR code; prior context is exact after all runs with no cross-test leakage.
- Cleanup: reset context tokens in `finally`, clear trace env vars, clear captures.
- Evidence mapping: DESIGN-005 isolation contract; story AC 10, 11; `test_b3_scope_restores_prior_values_after_formatter_failure` (tests/test_foundry_audit_cli.py) and `test_execute_traced_carries_same_b3_context_across_attempts_and_restores` (tests/test_tracing_provider.py).

### MDT-TC-020 - Retry behavior and at-least-once disclosure

- Type: resilience, negative, boundary.
- Given retryable and non-retryable failures, when `RetryHandler` wraps a command, then transient conditions (503, exhausted 429, configured transport exceptions) are retried per ADR-002, and validation, authorization, and permanent errors are never retried.
- Command/function: `RetryHandler` around representative read, create, commit, abort, upload, register, and transform commands.
- Prerequisites/fixtures: HTTP 503-then-success; repeated 429; 400/401/403/404; delay and jitter disabled; attempt counters.
- Steps: run each sequence and count attempts; verify the at-least-once disclosure is documented for create, commit, abort, upload, register, and transform (retrying can duplicate items, re-run transformations, or cost); verify metadata and content reads are safe to retry.
- Expected stdout/stderr/exit: recovered 503 has one success result and exit `0`; exhausted 429 exits `7`; validation/auth/permanent errors exit once with codes `1`/`2`/`3`/`4`; no duplicate result or content leak; disclosure text present where applicable.
- Cleanup: clear retry state and sentinels.
- Evidence mapping: ADR-001/002, DESIGN-018 retry contract; story AC 11; retry tests in tests/unit_test_retry_error_output_log.py (`test_http_429_and_503_are_retryable`, `test_http_non_429_503_does_not_retry`, `test_success_after_one_retry`, `test_retry_exhaustion_raises`); at-least-once disclosure is a design-documented property captured in TESTEXEC-018 evidence.

### MDT-TC-021 - ADR-001 error taxonomy and structured envelopes

- Type: negative, error taxonomy.
- Given each supported failure class, when the CLI exits, then it writes one JSON error envelope to stdout with the exact ADR-001 code and keeps diagnostics separate on stderr.
- Command/function: representative commands through `main()`.
- Prerequisites/fixtures: user input, HTTP 401/403/404/429/503, timeout, cancellation, ACL denial, configuration failure, and unexpected exception fakes.
- Steps: inject each failure after the correct lifecycle point; parse stdout and stderr; verify skipped downstream work where applicable.
- Expected stdout/stderr/exit: codes are user input `1`, authentication `2`, permission `3`, not found `4`, timeout/cancellation `5`, server `6`, exhausted 429 `7`, ACL `8`, and configuration `9`; error envelope is JSON on stdout; NDJSON diagnostics, if any, are on stderr; no raw traceback, token, or body appears.
- Cleanup: clear injected exceptions, secrets, and temporary files.
- Evidence mapping: ADR-001, DESIGN-018 error contract; story AC 12, 13; `test_sdk_error_maps_to_server_error_exit_code`, `test_sdk_timeout_maps_to_timeout_exit_code` (tests/test_foundry_media_sets_cli.py) plus the shared error-taxonomy tests in tests/unit_test_retry_error_output_log.py (`test_auth_error_exit_code_2` through `test_http_503_returns_server_error_after_retry_exhaustion`).

### MDT-TC-022 - Output formats: JSON, TOON, auto, and pretty

- Type: positive, output, boundary.
- Given success results of each shape, when `--format json|toon|auto` and `--pretty` run, then single models, `None` results, download envelopes, and structured errors follow the ADR-004 rules.
- Command/function: `OutputFormatter` via representative commands.
- Prerequisites/fixtures: a single `GetMediaSetResponse`, `None` results (`abort`, `commit`, `clear`), a `TransactionId`, a download envelope dict, a uniform non-empty array response, structured error.
- Steps: run each shape under each format; validate stdout parses as JSON where required; verify pretty indentation when enabled.
- Expected stdout/stderr/exit: exit `0`; auto selects TOON only for uniform non-empty arrays, otherwise JSON; empty/non-uniform output is JSON; `None` results serialize `null`/empty consistently; download output remains the JSON envelope; error output remains the structured JSON envelope.
- Cleanup: clear captures and models.
- Evidence mapping: ADR-004, DESIGN-018 output contract; story AC 12; `test_toon_output_format` (tests/test_foundry_media_sets_cli.py) plus shared `OutputFormatter` coverage in tests/unit_test_retry_error_output_log.py.

### MDT-TC-023 - NDJSON stderr, stream separation, and confidentiality

- Type: positive, output, confidentiality.
- Given successful create, upload, download, and transformation runs, when logs and results flow, then success data appears once on stdout, diagnostics are NDJSON on stderr, and credential/body/response sentinels never appear anywhere.
- Command/function: representative create, upload, download, and transform commands.
- Prerequisites/fixtures: secret sentinels embedded in request/response fixtures; captured logs.
- Steps: run each command; scan stdout, stderr, and captured logs for sentinel values, raw content bytes, and request bodies.
- Expected stdout/stderr/exit: exit `0`; stdout carries results/envelope/diagnostics only; stderr carries NDJSON diagnostics only (empty or safe); none of the sentinels, payloads, or bodies appear in any stream or log.
- Cleanup: clear sentinels and temporary files.
- Evidence mapping: ADR-005, DESIGN-018 log contract; story AC 12, 13; the NDJSON stderr/log-setup tests in tests/unit_test_retry_error_output_log.py (TestNdJsonFormatter and log-setup stderr tests); download content bytes are never emitted to stdout (the FR-DL envelope only), verified by `test_read_download_writes_atomically_and_reports_envelope`.

### MDT-TC-024 - Import, console boundary, help, and thin launcher

- Type: packaging, side-effect regression.
- Given the package and Claude launcher, when imported or asked for help, then they load without configuration, network, or filesystem side effects and use one event-loop boundary.
- Command/function: package import, launcher import, module `--help`, launcher `--help`, `console_main()`.
- Prerequisites/fixtures: empty arbitrary directory; guarded config/network/filesystem constructors; `asyncio.run` spy.
- Steps: import all Media Sets modules and launcher; invoke root and operation help; call `console_main()` with fake `main()`; inspect launcher source.
- Expected stdout/stderr/exit: imports produce no output or files; help exits `0` and names the 19 operations; `console_main()` calls `asyncio.run()` once and propagates the result; launcher delegates to packaged interfaces and contains no copied catalog, download, upload, or ACL logic.
- Cleanup: remove subprocess directory and restore the event-loop spy.
- Evidence mapping: DESIGN-018 packaging contract; story AC 14; `test_console_main_wraps_async_entry` (tests/test_foundry_media_sets_cli.py); the thin-launcher pattern follows `test_claude_launcher_is_thin_and_reexports_packaged_interfaces` (tests/test_audit_console_wrapper.py) and import side-effect-freedom is verified by the TESTEXEC-018 subprocess probe.

### MDT-TC-025 - Wheel, editable install, entry-point preservation, and regression

- Type: installation, regression.
- Given local wheel and editable installs, when commands run from an arbitrary directory without `PYTHONPATH`, then `foundry-media-sets` and the Claude launcher work while existing console scripts and repository gates remain intact.
- Command/function: local wheel build; wheel and editable install; installed `foundry-media-sets --help`; Claude launcher help; full test, Ruff, mypy, and package checks.
- Prerequisites/fixtures: isolated virtual environments for Python 3.11 and 3.12; `PIP_NO_INDEX=1`; local build dependencies; snapshot of existing `[project.scripts]` entries.
- Steps: build without live dependency resolution; inspect wheel for the Media Sets policy; install wheel then editable form with `--no-deps`; run help and packaged ACL probe from arbitrary CWD; compare every pre-existing entry point; run focused Media Sets tests and full regression with branch coverage.
- Expected stdout/stderr/exit: every help and package check exits `0`; wheel contains `foundry_cli/media_sets/metadata-allow-list.md`; all 19 operations are listed; all prior console scripts remain; focused and full suites pass on both Python versions; Ruff and mypy pass; repository branch coverage is at least 80%; no command makes a live Foundry request.
- Cleanup: delete isolated builds and environments; retain command output in TESTEXEC evidence only.
- Evidence mapping: DESIGN-018 packaging and regression contract; story AC 14, 15; all `tests/test_foundry_media_sets_cli.py` cases (31 tests) and the configured `pyproject.toml` gates; full-suite pass at HEAD `62c269f` (64 focused connectivity+media_sets tests green).

## Traceability matrix

| Requirement area | Story/design criteria | Cases |
| --- | --- | --- |
| Exact 19 catalog, no pagination, parser, help, nested routing, input omission | Story AC 1; scope comment; operation catalog | MDT-TC-001 through 003 |
| JSON argument validation, pre-client rejection | Story AC 2 | MDT-TC-004 |
| Transaction lifecycle: create/commit/abort/clear | Story AC 3, 5 | MDT-TC-005 |
| Bounded binary uploads: upload and upload-media | Story AC 5 | MDT-TC-006, 007 |
| Binary downloads: read, read-original, retrieve, get-result, atomicity, truncation, filename safety | Story AC 4 | MDT-TC-008 through 011 |
| ACL precedence, read-only 9-op write set, semantic content reads, fail-closed policy | Story AC 7, 8 | MDT-TC-013 through 016 |
| include_attribution=True and B3 only | Story AC 9, 10 | MDT-TC-017 through 019 |
| Retry, error taxonomy | Story AC 11, 13 | MDT-TC-020, 021 |
| Output formats, NDJSON, confidentiality | Story AC 12, 13 | MDT-TC-022, 023 |
| Imports, console, launcher, wheel/editable, regression gates | Story AC 14, 15 | MDT-TC-024, 025 |
| Positive, negative, boundary, security, resilience, structural, packaging | Complete design strategy | MDT-TC-001 through 025 |

All story acceptance criteria have at least one positive case and, where meaningful, a negative, boundary, security, or failure-path case. The 19-operation catalog is fully covered: the single `MediaSet` path is exercised by MDT-TC-001 through 011 plus ACL cases; the transaction lifecycle by MDT-TC-005; all four download operations by MDT-TC-008 through 011; both upload operations by MDT-TC-006, 007.

## Execution and approval criteria

TESTEXEC-018 may begin only after DEV, UNITTEST, CODEREVIEW, and TESTCASE-018 reach their required completed states and the approved commit is available. Execute all 25 cases with no live network access unless an approved non-production smoke is explicitly authorized.

For every case, record PASS, FAIL, or BLOCKED with the exact command, environment, expected result, actual result, stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, and linked evidence. Any failure requires a BUG-SUB before TESTEXEC-018 can close. Final QA sign-off also requires all linked defects to be terminal, every story acceptance criterion to have passing evidence, supported Python checks to pass, and repository branch coverage to remain at least 80%.
