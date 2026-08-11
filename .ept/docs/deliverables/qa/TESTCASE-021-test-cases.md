# TESTCASE-021 - Foundry Third-Party Applications CLI QA test cases

## Scope

These cases cover DEV-STORY-021 and the complete approved surface of `foundry-third-party-applications`: the 9 public `foundry_sdk.v2.third_party_applications` operations across the `ThirdPartyApplication` client (get), the `Website` client (deploy, get, undeploy), and the nested `Website.Version` client (delete, get, list, upload, upload_snapshot). They verify the exact catalog and parser, nested SDK routing through `client.third_party_applications.ThirdPartyApplication`, `Website`, and `Website.Version`, the cursor-paged `version list` command through `PaginationHelper` (`--page-size`, `--page-token`, `--all`, `--max-pages`), the two bounded zip uploads (`version upload`, `version upload-snapshot`) with the 16 MiB cap read after the access-control decision and before client construction, the 5-operation write set (deploy, undeploy, delete, upload, upload_snapshot) with the shared write-verb classification, the packaged 4-permitted/5-blocked metadata-only policy, `include_attribution=False`, B3 tracing, retry and at-least-once disclosure (duplicate-version caveat for `upload`), output and log contracts, privacy, packaging, and regression gates.

> **Acceptance criteria note:** The DEV-STORY-021 ticket body's Acceptance Criteria field still carries the grooming template placeholder; the authoritative acceptance criteria for this story are the DESIGN-021 contract sections (operation catalog, paging contract, binary upload contract, access and runtime policy), the story scope comment, and the populated `release_notes` field ("adds foundry-third-party-applications CLI (9 operations: third-party-application get; website deploy/get/undeploy; version delete/get/list/upload/upload-snapshot) with shared access control, pagination for version list, bounded zip uploads, B3 tracing, retry, output formatting, and packaged metadata-only policy").
>
> **Operation count note:** The story title and SAD-001 reference "9 operations". The vendored and installed SDK (v1.102.0) both expose exactly **9** public operations (`ThirdPartyApplication` 1: get; `Website` 3: deploy, get, undeploy; `Version` 5: delete, get, list, upload, upload_snapshot). The canonical environment-variable reference and the metadata allow-list are concordant at 9 rows each. The count is confirmed accurate; no correction is required.

Routine acceptance uses mocked async SDK transport and real installed SDK exception classes. Live credentials and live Foundry access are not required. An approved non-production smoke is optional and cannot replace the mandatory mocked evidence.

## Source baseline

- [DESIGN-021](../architecture/DESIGN-021-third-party-applications-cli.md), completed and closed for DEV-STORY-021.
- [DESIGN-005](../architecture/DESIGN-005-common-components.md), covering SDK-native B3 tracing and retry integration contracts.
- [DESIGN-011](../architecture/DESIGN-011-aip-agents-cli.md), [DESIGN-012](../architecture/DESIGN-012-language-models-cli.md), [DESIGN-013](../architecture/DESIGN-013-orchestration-cli.md), [DESIGN-017](../architecture/DESIGN-017-connectivity-cli.md), [DESIGN-018](../architecture/DESIGN-018-media-sets-cli.md) — the sibling namespace patterns this story mirrors (immutable operation catalog, exact nested SDK dispatch, packaged policy, cursor pagination via `PaginationHelper`, bounded binary uploads).
- [ADR-001](../architecture/adr/ADR-001-exit-code-taxonomy.md), [ADR-002](../architecture/adr/ADR-002-call-timeout-defaults.md), [ADR-004](../architecture/adr/ADR-004-format-auto-algorithm.md), [ADR-005](../architecture/adr/ADR-005-log-format.md), [ADR-006](../architecture/adr/ADR-006-env-file-search-path.md), [ADR-007](../architecture/adr/ADR-007-operation-level-readonly.md).
- The canonical environment-variable reference and metadata allow-list (namespace `third_party_applications`, 9 rows; `third_party_application.get`, `website.get`, `version.get`, `version.list` PERMITTED, the other 5 BLOCKED in tier 3).
- Vendored and installed SDK sources under `foundry_sdk/v2/third_party_applications/` — the real `ThirdPartyApplication`, `Website`, and `Version` client methods, request paths, and result types (verified via `inspect.signature` on installed SDK 1.102.0: `get(rid)`, `deploy(rid, *, version)`, `delete/get(rid, version_version)`, `list(rid, *, page_size, page_token)`, `upload/upload_snapshot(rid, body: bytes, *, version[, snapshot_identifier])`).
- DEV-STORY-021 ticket body, `release_notes`, and technical scope comment (authoritative 9-operation catalog).
- Implementation verified at commit `74094bc` ("feat(third_party_applications): add foundry-third-party-applications CLI (DEV-021)"): `src/foundry_cli/third_party_applications/` (scripts/`foundry_third_party_applications_cli.py`, `metadata-allow-list.md`), `pyproject.toml` entry point `foundry-third-party-applications` (L44), package data for the metadata allow-list, `.claude/skills/foundry-third-party-applications/` (SKILL.md + thin launcher).

## Preconditions and shared fixtures

- Python 3.11 and 3.12 environments contain the project, development dependencies, and pinned `foundry-sdk`.
- Use a nested async SDK fake rooted at `client.third_party_applications` with exactly three public accessor paths: `ThirdPartyApplication` (get), `Website` (deploy, get, undeploy), and the nested `Website.Version` (delete, get, list, upload, upload_snapshot). A wrong, flattened, raw, or streaming route must fail the fixture. No other sub-client may be reachable from any catalog dispatch.
- The `version` commands dispatch through the nested `Website.Version` accessor (`client.third_party_applications.Website.Version.<method>`).
- Exactly one operation returns a `ResourceIterator` or a server cursor: `version list`. Only `version list` exposes `--page-size`, `--page-token`, `--all`, and `--max-pages`; no other command may register pagination flags, and the `PaginationHelper` must never be invoked for a non-paged command.
- `version upload` and `version upload-snapshot` dispatch `body` positionally (the bounded-read file bytes) with `version` as the SDK keyword; the `--file` flag is consumed by the CLI and never forwarded; `upload-snapshot` forwards `--snapshot-identifier` only when provided. Use file fixtures at 0 B, small zip bytes, exactly 16 MiB, and over 16 MiB.
- Use real installed SDK model validators for nested invalid-input checks and real `foundry_sdk._errors` classes for error taxonomy checks. Mock network transport; no service call is permitted.
- Set retry delay to zero, disable jitter, and use the configured attempt count (default 4) unless a case states otherwise. Capture attempt number, timeout, attribution, and B3 values.
- Capture stdout, stderr, logs, SDK arguments, context variables, client/network constructors, and filesystem changes independently. Do not retain credential, token, JSON-body, or response sentinel values.
- Packaging cases build a clean local archive with dependency resolution disabled, install with `--no-deps`, and run from an arbitrary empty working directory without `PYTHONPATH`.
- Any optional live smoke uses an approved non-production Foundry tenant, synthetic applications/websites/versions, least-privilege credentials, and a cleanup plan. Credentials must never enter retained evidence.
- TESTEXEC records the commit, OS, Python and SDK versions, environment type, exact command, expected and actual stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, evidence reference, and PASS/FAIL/BLOCKED status for every case.

## Test data

| Name | Fixture |
| --- | --- |
| Third-party application RID | `ri.third-party-applications.main.application.qa-001` (valid 5-segment RID matching the SDK pattern) |
| Version string | `qa-website-version-1` (SDK `version` query parameter; also the `version_version` positional) |
| Snapshot identifier | `qa-snapshot-20260811` (optional) |
| Page size / token | `25`; resume token `tok-qa-021` |
| Zip fixtures | `upload-0b.zip` (0 B); `upload-small.zip` (valid zip bytes, 4 KiB); `upload-16mib.zip` (exactly 16 MiB); `upload-17mib.zip` (16 MiB + 1 B); directory path; missing path |
| Timeout variants | `1`, `30` (default), `3600`, CLI override `17`, configured default `42`, invalid `0`, `3601`, `-1`, non-integer text |
| Secret sentinels | `sentinel-secret-021`, `sentinel-token-secret`, `sentinel-body-secret`, `sentinel-response-secret`, `sentinel-attribution-rid` |

## Command and route inventory

Every inventory row is exercised by TPA-TC-001 through TPA-TC-003. Unless a case states otherwise, success writes one formatted result to stdout, writes no application data to stderr, exits `0`, and leaves no command-specific file.

| CLI command | Exact public SDK route and method | Required input | Optional input |
| --- | --- | --- | --- |
| `third-party-application get TPA_RID` | `client.third_party_applications.ThirdPartyApplication.get` | `third_party_application_rid` | shared options |
| `website deploy TPA_RID --version VERSION` | `client.third_party_applications.Website.deploy` | `third_party_application_rid`, `--version` | shared options |
| `website get TPA_RID` | `client.third_party_applications.Website.get` | `third_party_application_rid` | shared options |
| `website undeploy TPA_RID` | `client.third_party_applications.Website.undeploy` | `third_party_application_rid` | shared options |
| `version delete TPA_RID VERSION` | `client.third_party_applications.Website.Version.delete` | `third_party_application_rid`, `version_version` | shared options |
| `version get TPA_RID VERSION` | `client.third_party_applications.Website.Version.get` | `third_party_application_rid`, `version_version` | shared options |
| `version list TPA_RID` | `client.third_party_applications.Website.Version.list` | `third_party_application_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages`, shared options |
| `version upload TPA_RID --version VERSION --file PATH` | `client.third_party_applications.Website.Version.upload` | `third_party_application_rid`, `--version`, `--file` | shared options |
| `version upload-snapshot TPA_RID --version VERSION --file PATH` | `client.third_party_applications.Website.Version.upload_snapshot` | `third_party_application_rid`, `--version`, `--file` | `--snapshot-identifier`, shared options |

No command may receive `attribution`, `preview`, `_sdk_internal`, an absent optional set to `None`, or any unsupported paging, stream, raw-response, or file flag. Only `version list` may expose `--page-size`, `--page-token`, `--all`, `--max-pages`.

## Test cases

### TPA-TC-001 - Catalog, parser, help, and exact 9 surface

- Type: positive, structural, negative parser.
- Given the installed module and launcher, when the catalog and parser are inspected, then exactly 9 unique SDK specifications exist (third-party-application 1, website 3, version 5), every inventory command parses, and pagination flags exist only on `version list`.
- Command/function: `OP_SPECS`, `build_parser()`, `_spec_for()`, `_get_client()`, root/resource/operation `--help`, `main()` with missing resource/operation, unknown flags, missing required positionals/options, invalid choices/types.
- Prerequisites/fixtures: guarded config, client, network, and filesystem constructors.
- Steps: count `OP_SPECS`; assert the resource split `third_party_application` 1 / `website` 3 / `version` 5 and client paths `("ThirdPartyApplication",)`, `("Website",)`, and `("Website", "Version")`; assert `--page-size`/`--page-token`/`--all`/`--max-pages` exist only under `version list`; parse all 9 inventory commands; run all help surfaces; run every incomplete or malformed form.
- Expected stdout/stderr/exit: help on stdout and exit `0`; catalog count exactly `9`; parser errors as one JSON envelope on stdout with `exit_code: 1`, empty diagnostic stderr, no traceback, no config/client/network/filesystem call.
- Cleanup: restore `sys.argv` and capture streams.
- Evidence mapping: DESIGN-021 catalog (9 ops confirmed against installed SDK 1.102.0); story scope comment and release_notes; `test_catalog_contains_exact_9_operations`, `test_parser_accepts_every_declared_argument`, `test_parser_rejects_unknown_operation`, `test_non_paginated_commands_reject_pagination_flags` (tests/test_foundry_third_party_applications_cli.py); verified live at HEAD `74094bc`.

### TPA-TC-002 - Nested SDK routing through ThirdPartyApplication, Website, and Website.Version

- Type: positive, structural, route identity.
- Given distinct fakes for `ThirdPartyApplication`, `Website`, and `Website.Version`, when every inventory command runs, then each resolves the exact nested object and never a flattened or sibling route.
- Command/function: `_get_client()` (roots at `root_client.third_party_applications`, then walks the spec `client_path`) and each dispatch path.
- Prerequisites/fixtures: fakes whose sibling routes fail on access.
- Steps: run one command per client path; assert the resolved resource object identity; assert no flattened `third_party_applications.*` method call.
- Expected stdout/stderr/exit: success results on stdout once, exit `0`, no unexpected stderr; no flattened `third_party_applications.*` method call.
- Cleanup: reset fakes and captures.
- Evidence mapping: DESIGN-021 nested dispatch; story AC 1; `test_catalog_contains_exact_9_operations` (all nine resolve through the three nested client paths) plus the dispatch tests `test_third_party_application_get_dispatches_exact_arguments`, `test_website_deploy_dispatches_version`, `test_version_get_dispatches_positionals`.

### TPA-TC-003 - Required inputs forwarded and absent optionals omitted

- Type: positive, structural.
- Given each inventory command, when dispatch runs, then required positionals/options reach the SDK call and every absent optional is omitted (never `None`).
- Command/function: all 9 dispatches; `_build_kwargs()`.
- Prerequisites/fixtures: recording SDK fakes.
- Steps: run each command with only required inputs; run `version upload-snapshot` with and without `--snapshot-identifier`; run `version upload` with and without the bounded read; inspect the SDK call arguments.
- Expected stdout/stderr/exit: `third_party_application.get` receives the RID positionally; `website.deploy` receives the RID positionally plus `version`; `version.delete`/`version.get` receive both positionals (`third_party_application_rid`, `version_version`); `version.upload`/`version.upload_snapshot` receive the RID positionally, `body` bytes positionally, and `version` as keyword; `snapshot_identifier` present only when provided; absent optionals absent from kwargs; success exits `0`.
- Cleanup: clear fake call records.
- Evidence mapping: DESIGN-021 operation catalog; story AC 1; `test_third_party_application_get_dispatches_exact_arguments`, `test_version_upload_omits_absent_snapshot_identifier`, `test_website_deploy_dispatches_version` (tests/test_foundry_third_party_applications_cli.py).

### TPA-TC-004 - Version upload bounded file read after ACL and before client

- Type: positive, boundary, negative, security.
- Given the upload commands and guarded lifecycle, when `version upload` reads `--file`, then the bounded read (16 MiB cap) happens after the access-control decision and before any client construction, valid zips dispatch, oversized and missing files exit `1` as user input before client/network work, and the file bytes never echo into stdout/stderr/logs.
- Command/function: `main()` with `AccessControlGuard`/`AsyncClientFactory` spies; `_read_file_bounded()`.
- Prerequisites/fixtures: file fixtures 0 B, 4 KiB, exactly 16 MiB, 16 MiB + 1 B; directory path; missing path; client/factory constructors that record call order.
- Steps: run `version upload` with each fixture; run `version upload-snapshot` with the small fixture and `--snapshot-identifier`; assert event order (ACL check, then file read, then factory/client); attempt the oversized file; attempt the directory and missing path.
- Expected stdout/stderr/exit: valid fixtures call `Version.upload`/`upload_snapshot` with `body` bytes and exit `0`; the 16 MiB + 1 B file, directory, and missing path write one JSON user-input envelope on stdout and exit `1` before client construction; the raw zip bytes appear nowhere.
- Cleanup: delete fixture files, clear captures.
- Evidence mapping: DESIGN-021 binary upload contract (bounded read after ACL decision, before client); story AC 2; `test_version_upload_reads_file_bounded`, `test_version_upload_rejects_missing_file`, `test_version_upload_rejects_oversized_file`, `test_version_upload_snapshot_reads_file_bounded` (tests/test_foundry_third_party_applications_cli.py).

### TPA-TC-005 - Version lifecycle dispatch: list, get, delete, and upload effects

- Type: positive, structural, stateful.
- Given recording SDK fakes, when the CLI drives `version list`, `version get`, `version delete`, and `version upload`, then each resolves through `Website.Version`, the paged list aggregates items, get/delete forward both positionals, delete returns no content, and upload surfaces the created `Version`.
- Command/function: `version list`, `version get`, `version delete`, `version upload` dispatch.
- Prerequisites/fixtures: recording SDK fakes; `ListVersionsResponse` with `data` + `next_page_token`; `None` result fake for delete; `Version` response fakes.
- Steps: run `version list` with `--page-size 25` and capture pages; run `version get` on a returned version; run `version delete` on a version; run `version upload` with a small zip; inspect the SDK call arguments on each.
- Expected stdout/stderr/exit: each step exits `0`; `list` forwards `page_size` and aggregates into one array; `get`/`delete` forward both positionals; `delete` prints a serialized `null`/empty result consistently; no CLI-level state persists between invocations.
- Cleanup: clear fakes and captures.
- Evidence mapping: DESIGN-021 operation catalog; story AC 1, 3; `test_version_list_uses_raw_response_and_helper`, `test_version_get_dispatches_positionals`, `test_version_delete_dispatches_positionals`, `test_version_upload_reads_file_bounded` (tests/test_foundry_third_party_applications_cli.py).

### TPA-TC-006 - Pagination contract: page bounds, resume token, and degenerate values

- Type: positive, boundary, negative.
- Given the `version list` pagination surface, when `--page-size`/`--page-token`/`--all`/`--max-pages` run, then the effective page batch respects `FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES` (hard cap 40, `--all` selects the cap) and degenerate values (`--max-pages 0`, non-positive `--page-size`) are rejected as user input before ACL/client/network work.
- Command/function: `version list` dispatch; `PaginationHelper` bound validation.
- Prerequisites/fixtures: multi-page fakes; env `FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES` set to `3` and unset.
- Steps: run with `--page-size 25`; run with `--page-token` resume; run `--max-pages 3`; run `--all` with env cap `3`; run `--max-pages 0`; run `--page-size 0`.
- Expected stdout/stderr/exit: valid bounds fetch the documented page count and exit `0` with one aggregated array; `--max-pages 0` and `--page-size 0` write one JSON user-input envelope on stdout and exit `1` before ACL/client/network work; metadata emitted to stderr.
- Cleanup: restore env and call records.
- Evidence mapping: DESIGN-021 paging contract; story AC 3; `test_version_list_uses_raw_response_and_helper`, `test_version_list_defaults_to_single_page`, `test_catalog_marks_exactly_one_paginated_operation` (tests/test_foundry_third_party_applications_cli.py), shared `PaginationHelper` tests in tests/test_pagination_helper.py.

### TPA-TC-007 - Website lifecycle dispatch: deploy, get, undeploy

- Type: positive, structural, stateful.
- Given recording SDK fakes, when the CLI drives `website deploy`, `website get`, and `website undeploy`, then each resolves through `Website`, deploy forwards the RID positionally plus `version`, get and undeploy forward the RID, and undeploy surfaces the resulting `Website` state.
- Command/function: `website deploy`, `website get`, `website undeploy` dispatch.
- Prerequisites/fixtures: recording SDK fakes; `Website` response fakes.
- Steps: run `deploy` with a version and capture the website; run `get` on the RID; run `undeploy` on the RID; inspect the SDK call arguments on each.
- Expected stdout/stderr/exit: each step exits `0`; `deploy` receives `version` as keyword; `get`/`undeploy` receive the RID positionally; results surface once on stdout; no CLI-level state persists.
- Cleanup: clear fakes and captures.
- Evidence mapping: DESIGN-021 operation catalog; story AC 1, 3; `test_website_deploy_dispatches_version`, `test_website_get_dispatches_and_omits_absent_optional`, `test_website_undeploy_dispatches` (tests/test_foundry_third_party_applications_cli.py).

### TPA-TC-008 - Timeout boundaries and forwarding

- Type: positive, boundary, negative.
- Given CLI or configured timeouts, when execution starts, then values from 1 through 3600 seconds are accepted and the selected value reaches both retry handling and the SDK request; invalid values are rejected before ACL, scope, client, or filesystem work.
- Command/function: `_validate_timeout()`, representative commands with `--timeout`.
- Prerequisites/fixtures: values `1`, `30` (default), `3600`, CLI override `17`, configured default `42`, invalid `0`, `3601`, negative, and non-integer text.
- Steps: validate boundaries; execute with and without a CLI override; inspect retry construction and `request_timeout`; invoke each invalid value.
- Expected stdout/stderr/exit: valid requests produce one success result and exit `0`; retry and SDK receive the same chosen integer; invalid values write one JSON user-input envelope on stdout and exit `1` with no ACL/client/network call.
- Cleanup: restore config defaults and call records.
- Evidence mapping: ADR-002, DESIGN-021 invocation contract; story AC 12; `test_timeout_accepts_adr_002_bounds`, `test_invalid_timeout_returns_user_input_error` (tests/test_foundry_third_party_applications_cli.py).

### TPA-TC-009 - ACL precedence: global, namespace, and operation scopes

- Type: security, positive, negative.
- Given metadata-only and operation-level overrides, when ACL evaluates `THIRD_PARTY_APPLICATIONS`, then permissive settings allow, blocking settings deny, and an operation override wins over the namespace setting.
- Command/function: `AccessControlGuard(cfg, "THIRD_PARTY_APPLICATIONS").check()` for the 9 catalog operations.
- Prerequisites/fixtures: packaged Third-Party Applications allow-list and isolated environment variables.
- Steps: enable global metadata-only; check all 9 operations; disable the namespace metadata-only at namespace level; disable one operation explicitly; combine namespace read-only with an operation override.
- Expected stdout/stderr/exit: permitted checks return silently; blocked CLI calls write a structured ACL envelope to stdout, exit `8`, and do not create a client; the denying rule appears on stderr diagnostics; no secret appears.
- Cleanup: remove every ACL environment variable.
- Evidence mapping: DESIGN-021 access-control table; story AC 7; `test_acl_write_classification_matches_design`, `test_metadata_only_permits_exactly_4_blocks_5` (precedence exercised through the namespace runtime checks).

### TPA-TC-010 - Read-only mode blocks the 5-operation write set; semantic reads stay permitted

- Type: security, positive, negative.
- Given read-only mode enabled, when each write command runs, then `website deploy`, `website undeploy`, `version delete`, `version upload`, and `version upload-snapshot` exit `8` before client or filesystem effects, while `third-party-application get`, `website get`, `version get`, and `version list` remain executable as semantic reads.
- Command/function: `AccessControlGuard` + `main()` for each write command and the four reads.
- Prerequisites/fixtures: read-only environment; guarded factory/transport; response fakes.
- Steps: run all 5 write commands under read-only; run all 4 reads under read-only; inspect event order (no file read on blocked uploads).
- Expected stdout/stderr/exit: each blocked write emits one ACL envelope and exit `8` with the denying rule on stderr; no SDK call or file read occurs; the four reads succeed and exit `0`.
- Cleanup: clear read-only variables, captures, and records.
- Evidence mapping: DESIGN-021 read-only policy (write set = deploy, undeploy, delete, upload, upload_snapshot); story AC 7; `test_readonly_blocks_five_write_operations`, `test_reads_permitted_under_readonly` (tests/test_foundry_third_party_applications_cli.py).

### TPA-TC-011 - Metadata-only tier: exact 4 permitted / 5 blocked

- Type: security, positive, negative.
- Given metadata-only mode, when every operation is checked, then exactly the 4 documented reads (`third_party_application.get`, `website.get`, `version.get`, `version.list`) are permitted and the 5 writes (`website.deploy`, `website.undeploy`, `version.delete`, `version.upload`, `version.upload_snapshot`) are blocked.
- Command/function: `AccessControlGuard` + `main()` under metadata-only for all 9 operations.
- Prerequisites/fixtures: packaged allow-list; guarded factory/transport.
- Steps: run each of the 4 permitted commands; run each of the 5 blocked commands; inspect the parsed allow-list rows.
- Expected stdout/stderr/exit: the 4 reads exit `0`; the 5 writes exit `8` with one ACL envelope each, no client construction; the packaged allow-list parses to exactly 4 PERMITTED and 5 BLOCKED rows.
- Cleanup: clear captures and records.
- Evidence mapping: DESIGN-021 metadata-only policy; story AC 8; `test_metadata_only_permits_exactly_4_blocks_5`, `test_metadata_only_permits_four_and_blocks_five` (tests/test_foundry_third_party_applications_cli.py).

### TPA-TC-012 - Packaged metadata-only policy is fail closed and CWD independent

- Type: security, packaging, negative.
- Given the installed package with a missing or malformed packaged allow-list, when ACL runs, then it fails closed (no operation permitted) and the packaged policy resolves from an arbitrary working directory.
- Command/function: `_METADATA_ALLOWLIST_PATH`, `AccessControlGuard` from an installed wheel/editable launch.
- Prerequisites/fixtures: malformed/missing policy fixtures in an isolated environment; empty arbitrary CWD, no `PYTHONPATH`.
- Steps: probe policy path from the installed package; run a permitted-class check with malformed policy; run checks from the arbitrary CWD.
- Expected stdout/stderr/exit: malformed/missing policy blocks even previously-permitted operations (fail closed, exit `8`); packaged policy path resolves inside the installed package; valid packaged policy applies the 4/5 rule from any CWD.
- Cleanup: delete isolated environments and fixtures.
- Evidence mapping: DESIGN-021 fail-closed rule; story AC 8, 14; `test_metadata_only_permits_exactly_4_blocks_5` (parsed from the packaged allow-list); packaged-policy CWD independence follows the same pattern as `test_packaged_metadata_policy_is_cwd_independent` (tests/test_foundry_audit_cli.py) and is verified by the TESTEXEC-021 wheel/editable probe.

### TPA-TC-013 - include_attribution=False on client and invocation scope

- Type: positive, privacy, structural.
- Given a real factory and `invocation_scope`, when any command executes, then client creation and scope use `include_attribution=False`, no attribution environment handling is added, and surrounding attribution state is unchanged after success and failure.
- Command/function: `AsyncClientFactory.invocation_scope(cfg)`, `factory.create(cfg)`, `main()`.
- Prerequisites/fixtures: factory/scope spies; preset outer attribution RID and environment.
- Steps: execute a read and a failed command; capture `include_attribution` on client and scope; capture attribution state before and after.
- Expected stdout/stderr/exit: both capture points pass `include_attribution=False`; no attribution variable is read or written; outer attribution state and env are identical after success and failure; no W3C `traceparent`/`tracestate`.
- Cleanup: reset context tokens and env.
- Evidence mapping: DESIGN-021 attribution rule (namespace outside FR-ATTR-4); story AC 9; `test_invocation_uses_include_attribution_false` (tests/test_foundry_third_party_applications_cli.py).

### TPA-TC-014 - B3 enabled at outbound transport

- Type: positive, tracing, transport integration.
- Given tracing enabled, when the client is created and an SDK request is prepared, then outbound transport carries one valid B3 multi-header context.
- Command/function: `AsyncClientFactory.invocation_scope(cfg)`, SDK request preparation, a representative read.
- Prerequisites/fixtures: enabled tracing config, clean SDK context, transport header capture.
- Steps: enter the real tracing scope through `main()`; capture headers at client creation and request preparation.
- Expected stdout/stderr/exit: success result and exit `0`; every capture has lowercase-hex `X-B3-TraceId` of 32 characters, `X-B3-SpanId` of 16 characters, and `X-B3-Sampled` `0` or `1`; no W3C header appears.
- Cleanup: reset SDK context tokens and environment variables.
- Evidence mapping: DESIGN-005 B3 contract; story AC 10; `test_b3_transport_headers_enabled_disabled_retry_stable_and_restored` (tests/test_foundry_audit_cli.py) and `test_generated_context_has_valid_nonzero_b3_values_and_resets` (tests/test_tracing_provider.py); the namespace outbound-header probe is recorded in TESTEXEC-021 evidence.

### TPA-TC-015 - B3 disabled, retry stability, and context restoration

- Type: negative, resilience, isolation.
- Given disabled tracing, retries, prior context, or a later formatter failure, when execution leaves the invocation, then disabled calls add no B3 headers, retry attempts share one enabled context, and prior values are restored on every exit path.
- Command/function: `main()` with real `TracingProvider` scope and captured SDK transport headers.
- Prerequisites/fixtures: enabled and disabled configs; first-attempt transport failure followed by success; preset prior trace/span/sampled values; formatter, SDK, timeout, and cancellation failures.
- Steps: run the disabled flow; run the enabled retry flow; run each failure with prior values; inspect every outbound header set and context after exit.
- Expected stdout/stderr/exit: disabled flow has no `X-B3-*`; enabled retry captures identical B3 values for client creation and every attempt; no `traceparent`/`tracestate`; success exits `0`; failures use their ADR code; prior context is exact after all runs with no cross-test leakage.
- Cleanup: reset context tokens in `finally`, clear trace env vars, clear captures.
- Evidence mapping: DESIGN-005 isolation contract; story AC 10, 11; `test_b3_scope_restores_prior_values_after_formatter_failure` (tests/test_foundry_audit_cli.py) and `test_execute_traced_carries_same_b3_context_across_attempts_and_restores` (tests/test_tracing_provider.py).

### TPA-TC-016 - Retry behavior and at-least-once disclosure

- Type: resilience, negative, boundary.
- Given retryable and non-retryable failures, when `RetryHandler` wraps a command, then transient conditions (503, exhausted 429, configured transport exceptions) are retried per ADR-002, and validation, authorization, and permanent errors are never retried; the at-least-once disclosure is documented because retrying `version upload` can create a duplicate version record while retrying `website deploy`/`website undeploy` re-applies the same target state.
- Command/function: `RetryHandler` around representative read, deploy, delete, and upload commands.
- Prerequisites/fixtures: HTTP 503-then-success; repeated 429; 400/401/403/404; delay and jitter disabled; attempt counters.
- Steps: run each sequence and count attempts; verify the at-least-once disclosure is documented for upload (duplicate-version caveat) and deploy/undeploy (idempotent target state); verify reads and delete are retried per the ADR policy.
- Expected stdout/stderr/exit: recovered 503 has one success result and exit `0`; exhausted 429 exits `7`; validation/auth/permanent errors exit once with codes `1`/`2`/`3`/`4`; no duplicate result or content leak; disclosure text present where applicable.
- Cleanup: clear retry state and sentinels.
- Evidence mapping: ADR-001/002, DESIGN-021 retry contract; story AC 11; retry tests in tests/unit_test_retry_error_output_log.py (`test_http_429_and_503_are_retryable`, `test_http_non_429_503_does_not_retry`, `test_success_after_one_retry`, `test_retry_exhaustion_raises`); at-least-once disclosure is a design-documented property captured in TESTEXEC-021 evidence.

### TPA-TC-017 - ADR-001 error taxonomy and structured envelopes

- Type: negative, error taxonomy.
- Given each supported failure class, when the CLI exits, then it writes one JSON error envelope to stdout with the exact ADR-001 code and keeps diagnostics separate on stderr.
- Command/function: representative commands through `main()` and `_serialize_error()`.
- Prerequisites/fixtures: user input, HTTP 401/403/404/429/503, timeout, cancellation, ACL denial, configuration failure, and unexpected exception fakes.
- Steps: inject each failure after the correct lifecycle point; parse stdout and stderr; verify skipped downstream work where applicable.
- Expected stdout/stderr/exit: codes are user input `1`, authentication `2`, permission `3`, not found `4`, timeout/cancellation `5`, server `6`, exhausted 429 `7`, ACL `8`, and configuration `9`; error envelope is JSON on stdout; NDJSON diagnostics, if any, are on stderr; no raw traceback, token, or body appears.
- Cleanup: clear injected exceptions, secrets, and temporary files.
- Evidence mapping: ADR-001, DESIGN-021 error contract; story AC 12, 13; `test_unknown_operation_returns_user_input_error`, `test_sdk_error_maps_to_server_error_exit_code`, `test_sdk_timeout_maps_to_timeout_exit_code` (tests/test_foundry_third_party_applications_cli.py) plus the shared error-taxonomy tests in tests/unit_test_retry_error_output_log.py (`test_auth_error_exit_code_2` through `test_http_503_returns_server_error_after_retry_exhaustion`).

### TPA-TC-018 - Output formats: JSON, TOON, auto, and pretty

- Type: positive, output, boundary.
- Given success results of each shape, when `--format json|toon|auto` and `--pretty` run, then single models, `None` results (delete), and paged arrays follow the ADR-004 rules.
- Command/function: `OutputFormatter` via representative commands.
- Prerequisites/fixtures: a single `ThirdPartyApplication`, a `None` result (`version delete`), a `Website`, a paged list with a uniform `Version` array, an empty list, structured error.
- Steps: run each shape under each format; validate stdout parses as JSON where required; verify pretty indentation when enabled.
- Expected stdout/stderr/exit: exit `0`; auto selects TOON only for uniform non-empty arrays, otherwise JSON; empty/non-uniform output is JSON; `None` results serialize `null`/empty consistently; error output remains the structured JSON envelope.
- Cleanup: clear captures and models.
- Evidence mapping: ADR-004, DESIGN-021 output contract; story AC 12; `test_toon_output_format` (tests/test_foundry_third_party_applications_cli.py) plus shared `OutputFormatter` coverage in tests/unit_test_retry_error_output_log.py.

### TPA-TC-019 - NDJSON stderr, stream separation, and confidentiality

- Type: positive, output, confidentiality.
- Given successful get, list, upload, and undeploy runs, when logs and results flow, then success data appears once on stdout, diagnostics are NDJSON on stderr, and credential/body/response sentinels never appear anywhere.
- Command/function: representative get, list, upload, and undeploy commands.
- Prerequisites/fixtures: secret sentinels embedded in request/response fixtures and in the zip file; captured logs.
- Steps: run each command; scan stdout, stderr, and captured logs for sentinel values, raw request bodies, zip bytes, and secret values.
- Expected stdout/stderr/exit: exit `0`; stdout carries results/metadata envelopes only; stderr carries NDJSON diagnostics only (empty or safe); none of the sentinels, payloads, zip bytes, or bodies appear in any stream or log.
- Cleanup: clear sentinels and temporary files.
- Evidence mapping: ADR-005, DESIGN-021 log contract; story AC 12, 13; `test_sensitive_values_not_echoed_in_errors` plus the NDJSON stderr/log-setup tests in tests/unit_test_retry_error_output_log.py (TestNdJsonFormatter and log-setup stderr tests).

### TPA-TC-020 - Import, console boundary, help, and thin launcher

- Type: packaging, side-effect regression.
- Given the package and console entry point, when imported or asked for help, then they load without configuration, network, or filesystem side effects and use one event-loop boundary.
- Command/function: package import, module `--help`, entry point help, `console_main()`; the Claude skill launcher.
- Prerequisites/fixtures: empty arbitrary directory; guarded config/network/filesystem constructors; `asyncio.run` spy.
- Steps: import all Third-Party Applications modules; invoke root and operation help; call `console_main()` with fake `main()`; inspect the launcher source.
- Expected stdout/stderr/exit: imports produce no output or files; help exits `0` and names the 9 operations; `console_main()` calls `asyncio.run()` once and propagates the result; the launcher delegates to packaged interfaces and contains no copied catalog or ACL logic.
- Cleanup: remove subprocess directory and restore the event-loop spy.
- Evidence mapping: DESIGN-021 packaging contract; story AC 14; `test_console_main_wraps_async_entry` (tests/test_foundry_third_party_applications_cli.py); the thin-launcher pattern follows `test_claude_launcher_is_thin_and_reexports_packaged_interfaces` (tests/test_audit_console_wrapper.py) and import side-effect-freedom is verified by the TESTEXEC-021 subprocess probe.

### TPA-TC-021 - Wheel, editable install, entry-point preservation, and regression

- Type: installation, regression.
- Given local wheel and editable installs, when commands run from an arbitrary directory without `PYTHONPATH`, then `foundry-third-party-applications` works while existing console scripts and repository gates remain intact.
- Command/function: local wheel build; wheel and editable install; installed `foundry-third-party-applications --help`; full test, Ruff, mypy, and package checks.
- Prerequisites/fixtures: isolated virtual environments for Python 3.11 and 3.12; `PIP_NO_INDEX=1`; local build dependencies; snapshot of existing `[project.scripts]` entries.
- Steps: build without live dependency resolution; inspect wheel for the Third-Party Applications policy; install wheel then editable form with `--no-deps`; run help and packaged ACL probe from arbitrary CWD; compare every pre-existing entry point; run focused Third-Party Applications tests and full regression with branch coverage.
- Expected stdout/stderr/exit: every help and package check exits `0`; wheel contains `foundry_cli/third_party_applications/metadata-allow-list.md`; all 9 operations are listed; all prior console scripts remain; focused and full suites pass on both Python versions; Ruff and mypy pass; repository branch coverage is at least 80%; no command makes a live Foundry request.
- Cleanup: delete isolated builds and environments; retain command output in TESTEXEC evidence only.
- Evidence mapping: DESIGN-021 packaging and regression contract; story AC 14, 15; all `tests/test_foundry_third_party_applications_cli.py` cases (37 tests) and the configured `pyproject.toml` gates; full-suite pass at the approved HEAD.

### TPA-TC-022 - Snapshot disclosure and upload-snapshot optional behavior

- Type: positive, boundary, documentation.
- Given `version upload-snapshot`, when it runs, then it forwards `--snapshot-identifier` only when provided, and the skill documentation discloses that snapshot versions are auto-deleted after two days.
- Command/function: `version upload-snapshot` dispatch; skill documentation.
- Prerequisites/fixtures: recording SDK fake; snapshot identifier present and absent.
- Steps: run with `--snapshot-identifier qa-snapshot-20260811`; run without it; inspect the SDK kwargs; grep the skill documentation for the two-day auto-delete disclosure.
- Expected stdout/stderr/exit: with identifier, `upload_snapshot` receives `snapshot_identifier`; without it, the kwarg is absent (never `None`); success exits `0`; the disclosure text is present in `.claude/skills/foundry-third-party-applications/SKILL.md`.
- Cleanup: clear call records.
- Evidence mapping: DESIGN-021 binary upload contract and skill disclosure; story AC 2; `test_version_upload_snapshot_reads_file_bounded`, `test_version_upload_omits_absent_snapshot_identifier` (tests/test_foundry_third_party_applications_cli.py).

### TPA-TC-023 - Empty and non-empty required-value validation before client

- Type: negative, boundary.
- Given missing or empty required inputs, when each command runs, then whitespace-only or missing required positionals/options exit `1` as user input before ACL/client/network work, and no value is echoed.
- Command/function: `_validate_inputs()`, `_required_text()`, `main()`.
- Prerequisites/fixtures: guarded config/client/network constructors; empty-string and whitespace-only values.
- Steps: run `third-party-application get ""`; run `version get RID ""`; run `website deploy RID --version "  "`; run `version upload RID --version V --file ""`.
- Expected stdout/stderr/exit: each writes one JSON user-input envelope on stdout with `exit_code: 1`, empty diagnostic stderr, no traceback, and never echoes the input value.
- Cleanup: clear captures.
- Evidence mapping: DESIGN-021 validation contract; story AC 1; `test_empty_required_value_rejected_before_client` (tests/test_foundry_third_party_applications_cli.py).

### TPA-TC-024 - No attribution, preview, or internal parameter leakage

- Type: security, negative, structural.
- Given the full catalog, when dispatch runs, then no SDK call ever receives `attribution`, `preview`, or `_sdk_internal`, and absent optionals are never `None`.
- Command/function: all 9 dispatches; `_build_kwargs()`.
- Prerequisites/fixtures: recording SDK fakes.
- Steps: run every command; inspect every recorded SDK call for forbidden keys.
- Expected stdout/stderr/exit: success exits `0`; no call contains `attribution`, `preview`, or `_sdk_internal`; no `None`-valued optional is forwarded.
- Cleanup: clear call records.
- Evidence mapping: DESIGN-021 technical summary (preview/internal excluded, attribution suppressed); story AC 1, 9; `test_catalog_contains_exact_9_operations` plus the dispatch tests that assert exact argument sets.

## Traceability matrix

| Requirement area | Story/design criteria | Cases |
| --- | --- | --- |
| Exact 9 catalog, pagination only on version list, parser, help, nested routing, input omission | Story AC 1; scope comment and release_notes; operation catalog | TPA-TC-001 through 003, 023, 024 |
| Bounded zip uploads (16 MiB) after ACL before client; snapshot identifier optional | Story AC 2 | TPA-TC-004, 022 |
| Version lifecycle list/get/delete/upload; cursor pagination | Story AC 1, 3 | TPA-TC-005, 006 |
| Website lifecycle deploy/get/undeploy | Story AC 1, 3 | TPA-TC-007 |
| Timeout boundaries and forwarding | Story AC 12 | TPA-TC-008 |
| ACL precedence, read-only 5-op write set, semantic reads, fail-closed policy | Story AC 7, 8 | TPA-TC-009 through 012 |
| include_attribution=False and B3 only | Story AC 9, 10 | TPA-TC-013 through 015 |
| Retry (at-least-once disclosure for upload/deploy/undeploy), error taxonomy | Story AC 11, 13 | TPA-TC-016, 017 |
| Output formats, NDJSON, confidentiality | Story AC 12, 13 | TPA-TC-018, 019 |
| Imports, console, launcher, wheel/editable, regression gates | Story AC 14, 15 | TPA-TC-020, 021 |
| Positive, negative, boundary, security, resilience, structural, packaging | Complete design strategy | TPA-TC-001 through 024 |

All story acceptance criteria have at least one positive case and, where meaningful, a negative, boundary, security, or failure-path case. The 9-operation catalog is fully covered: `third-party-application get` via TPA-TC-001 through 003, 009, 010, 023; `website deploy`/`website undeploy` via TPA-TC-001 through 003, 007, 009, 010, 016, 019; `website get` via TPA-TC-001 through 003, 007, 009, 010; `version delete`/`version get` via TPA-TC-001 through 003, 005, 009, 010; `version list` via TPA-TC-001, 002, 005, 006, 009, 010, 018; `version upload`/`version upload-snapshot` via TPA-TC-001 through 005, 009, 010, 016, 019, 022, 023, 024; all 9 via the ACL, attribution, tracing, output, and packaging cases.

## Execution and approval criteria

TESTEXEC-021 may begin only after DEV, UNITTEST, CODEREVIEW, and TESTCASE-021 reach their required completed states and the approved commit is available. Execute all 24 cases with no live network access unless an approved non-production smoke is explicitly authorized.

For every case, record PASS, FAIL, or BLOCKED with the exact command, environment, expected result, actual result, stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, and linked evidence. Any failure requires a BUG-SUB before TESTEXEC-021 can close. Final QA sign-off also requires all linked defects to be terminal, every story acceptance criterion to have passing evidence, supported Python checks to pass, and repository branch coverage to remain at least 80%.
