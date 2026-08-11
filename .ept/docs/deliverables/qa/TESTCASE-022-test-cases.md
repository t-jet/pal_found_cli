# TESTCASE-022 - Foundry Widgets CLI QA test cases

## Scope

These cases cover DEV-STORY-022 and the corrected **8-operation** surface of `foundry-widgets` per QUESTION-043: the 8 public `foundry_sdk.v2.widgets` operations across the `DevModeSettings` client (enable, set_widget_set_by_id), the `Repository` client (get, publish), the `WidgetSet` client (get), and the nested `WidgetSet.Release` client (delete, get, list). They verify the exact catalog and parser, nested SDK routing through `client.widgets.DevModeSettings`, `Repository`, `WidgetSet`, and `WidgetSet.Release`, JSON argument validation (`--settings-json` for the `WidgetSetDevModeSettingsById` body on `set-widget-set-by-id`), the cursor-paged `release list` command through `PaginationHelper` (`--page-size`, `--page-token`, `--all`, `--max-pages`), the bounded zip publish (`repository publish`) with the 16 MiB cap read after the access-control decision and before client construction, the 4-operation write set (enable, set_widget_set_by_id, release delete, repository publish), the packaged 4-permitted/4-blocked metadata-only policy, `include_attribution=False`, B3 tracing, retry and at-least-once disclosure (duplicate-release caveat for `publish`), output and log contracts, privacy, packaging, and regression gates.

> **Acceptance criteria note:** The DEV-STORY-022 ticket body's Acceptance Criteria field still carries the grooming template placeholder; the authoritative acceptance criteria for this story are the DEV-022 scope, the QUESTION-043 tech-lead decision, and the DESIGN-022 contract sections as corrected to the 8-operation surface (operation catalog, paging contract, binary upload contract, access and runtime policy).
>
> **Operation count note:** The story title and SAD-001 reference "12 operations", and DESIGN-022's stale catalog still lists 12. Per QUESTION-043 (Closed 2026-08-11, tech-lead answer comment `20260811-004954`), the installed runtime SDK `foundry-platform-sdk 1.102.0` exposes exactly **8** in-scope public operations (`DevModeSettings` 2: enable, set_widget_set_by_id; `Repository` 2: get, publish; `WidgetSet` 1: get; `WidgetSet.Release` 3: delete, get, list). The 4 DESIGN-022 DevModeSettings ops `disable`, `get`, `pause`, `set_widget_set` do not exist on the installed SDK (would raise `AttributeError` at runtime) and `DevModeSettingsV2` (enable, set_widget_set_manifest) is explicitly out of scope. This suite designs cases for the actual installed-surface 8-operation catalog (same precedent as streams 17→15, connectivity 15→20, data-health 4→6). The design amendment and the canonical env-var reference / metadata allow-list updates to 8 rows are implementer actions pending DEV-022.
>
> **Implementation gate note:** At the time of authoring (2026-08-11) DEV-022 is still in Development; `src/foundry_cli/widgets/` does not yet exist. Cases below are conditioned on the implementation landing with the corrected 8-op surface; they reference the verified installed SDK contracts (via `inspect.signature` on SDK 1.102.0) so they are implementable as soon as the CLI lands.

Routine acceptance uses mocked async SDK transport and real installed SDK exception classes. Live credentials and live Foundry access are not required. An approved non-production smoke is optional and cannot replace the mandatory mocked evidence.

## Source baseline

- [DESIGN-022](../architecture/DESIGN-022-widgets-cli.md), completed for DEV-STORY-022 but with a stale 12-op catalog; the corrected 8-op surface comes from the closed QUESTION-043 (tech-lead decision, 2026-08-11).
- [DESIGN-005](../architecture/DESIGN-005-common-components.md), covering SDK-native B3 tracing and retry integration contracts.
- [DESIGN-011](../architecture/DESIGN-011-aip-agents-cli.md), [DESIGN-012](../architecture/DESIGN-012-language-models-cli.md), [DESIGN-013](../architecture/DESIGN-013-orchestration-cli.md), [DESIGN-017](../architecture/DESIGN-017-connectivity-cli.md), [DESIGN-018](../architecture/DESIGN-018-media-sets-cli.md) — the sibling namespace patterns this story mirrors (immutable operation catalog, exact nested SDK dispatch, packaged policy, cursor pagination via `PaginationHelper`, bounded binary uploads).
- [ADR-001](../architecture/adr/ADR-001-exit-code-taxonomy.md), [ADR-002](../architecture/adr/ADR-002-call-timeout-defaults.md), [ADR-004](../architecture/adr/ADR-004-format-auto-algorithm.md), [ADR-005](../architecture/adr/ADR-005-log-format.md), [ADR-006](../architecture/adr/ADR-006-env-file-search-path.md), [ADR-007](../architecture/adr/ADR-007-operation-level-readonly.md).
- The canonical environment-variable reference and metadata allow-list (namespace `widgets`; the tech-lead answer directs an amendment to 8 rows).
- Installed SDK sources under `.venv/Lib/site-packages/foundry_sdk/v2/widgets/` — verified via `inspect.signature` on `foundry-platform-sdk 1.102.0` (the authoritative runtime surface): `AsyncDevModeSettingsClient.enable(*, preview)`, `set_widget_set_by_id(*, settings: WidgetSetDevModeSettingsById, widget_set_rid)`, `AsyncRepositoryClient.get(repository_rid)`, `publish(repository_rid, body: bytes, *, repository_version)`, `AsyncWidgetSetClient.get(widget_set_rid)`, `AsyncReleaseClient.delete/get(widget_set_rid, release_version)`, `list(widget_set_rid, *, page_size, page_token)` returning `AsyncResourceIterator[Release]`.
- `WidgetSetDevModeSettingsById` model requires `base_href: str` and `widget_settings: Dict[str, WidgetDevModeSettings]`; `DevModeSettings` returns `status: DevModeStatus` plus `widget_set_settings`.
- DEV-STORY-022 ticket body, `release_notes`, and technical scope comment; QUESTION-043 (Closed) with the tech-lead decision answer.
- Implementation: to land in `src/foundry_cli/widgets/` (scripts/`foundry_widgets_cli.py`, `metadata-allow-list.md`), `pyproject.toml` entry point `foundry-widgets`, and `.claude/skills/foundry-widgets/`. Gate status: **not yet present** at authoring time; TESTCASE-022 remains in Open until runnable code lands.

## Preconditions and shared fixtures

- Python 3.11 and 3.12 environments contain the project, development dependencies, and pinned `foundry-sdk` (1.102.0).
- Use a nested async SDK fake rooted at `client.widgets` with exactly four public accessor paths: `DevModeSettings` (enable, set_widget_set_by_id), `Repository` (get, publish), `WidgetSet` (get), and the nested `WidgetSet.Release` (delete, get, list). A wrong, flattened, raw, or streaming route must fail the fixture. No other sub-client may be reachable from any catalog dispatch.
- The `release` commands dispatch through the nested `WidgetSet.Release` accessor (`client.widgets.WidgetSet.Release.<method>`); `dev-mode-settings` and `repository` commands dispatch through `client.widgets.DevModeSettings`/`Repository`; `widget-set` through `client.widgets.WidgetSet`.
- Exactly one operation returns a `ResourceIterator` or a server cursor: `release list`. Only `release list` exposes `--page-size`, `--page-token`, `--all`, and `--max-pages`; no other command may register pagination flags, and the `PaginationHelper` must never be invoked for a non-paged command.
- `set-widget-set-by-id` takes `--settings-json` parsed as a JSON object that must decode into the `WidgetSetDevModeSettingsById` body (`base_href` and `widget_settings`); the decoded dict is forwarded as the SDK `settings` keyword together with `widget_set_rid`. `repository publish` dispatches `body` positionally (the bounded-read file bytes) with `repository_version` as the SDK keyword; the `--file` flag is consumed by the CLI and never forwarded. Use file fixtures at 0 B, small zip bytes, exactly 16 MiB, and over 16 MiB.
- Use real installed SDK model validators for nested invalid-input checks and real `foundry_sdk._errors` classes for error taxonomy checks. Mock network transport; no service call is permitted.
- Set retry delay to zero, disable jitter, and use the configured attempt count (default 4) unless a case states otherwise. Capture attempt number, timeout, attribution, and B3 values.
- Capture stdout, stderr, logs, SDK arguments, context variables, client/network constructors, and filesystem changes independently. Do not retain credential, token, JSON-body, or response sentinel values.
- Packaging cases build a clean local archive with dependency resolution disabled, install with `--no-deps`, and run from an arbitrary empty working directory without `PYTHONPATH`.
- Any optional live smoke uses an approved non-production Foundry tenant, synthetic widget repositories/widget sets/releases, least-privilege credentials, and a cleanup plan. Credentials must never enter retained evidence.
- TESTEXEC records the commit, OS, Python and SDK versions, environment type, exact command, expected and actual stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, evidence reference, and PASS/FAIL/BLOCKED status for every case.

## Test data

| Name | Fixture |
| --- | --- |
| Widget-set RID | `ri.widgets.main.widget-set.qa-001` (valid 5-segment RID matching the SDK pattern) |
| Repository RID | `ri.widgets.main.repository.qa-001` (valid 5-segment RID) |
| Release version | `qa-release-1` (SDK `release_version` positional) |
| Repository version | `qa-repo-version-1` (SDK `repository_version` keyword) |
| Settings JSON | `{"base_href": "https://qa.example.com", "widget_settings": {"w1": {"status": "enabled"}}}` (valid `WidgetSetDevModeSettingsById` body) |
| Settings shape variants | `[]` (array), `"text"` (scalar), `null`, malformed JSON text, missing `base_href`, missing `widget_settings`, unknown nested fields violating SDK validators |
| Page size / token | `25`; resume token `tok-qa-022` |
| Zip fixtures | `publish-0b.zip` (0 B); `publish-small.zip` (valid zip bytes, 4 KiB); `publish-16mib.zip` (exactly 16 MiB); `publish-17mib.zip` (16 MiB + 1 B); directory path; missing path |
| Timeout variants | `1`, `30` (default), `3600`, CLI override `17`, configured default `42`, invalid `0`, `3601`, `-1`, non-integer text |
| Secret sentinels | `sentinel-secret-022`, `sentinel-token-secret`, `sentinel-body-secret`, `sentinel-response-secret`, `sentinel-attribution-rid` |

## Command and route inventory

Every inventory row is exercised by WGT-TC-001 through WGT-TC-003. Unless a case states otherwise, success writes one formatted result to stdout, writes no application data to stderr, exits `0`, and leaves no command-specific file.

| CLI command | Exact public SDK route and method | Required input | Optional input |
| --- | --- | --- | --- |
| `dev-mode-settings enable` | `client.widgets.DevModeSettings.enable` | — | shared options |
| `dev-mode-settings set-widget-set-by-id WIDGET_SET_RID --settings-json JSON` | `client.widgets.DevModeSettings.set_widget_set_by_id` | `widget_set_rid`, `--settings-json` | shared options |
| `repository get REPO_RID` | `client.widgets.Repository.get` | `repository_rid` | shared options |
| `repository publish REPO_RID --repository-version VER --file PATH` | `client.widgets.Repository.publish` | `repository_rid`, `--repository-version`, `--file` | shared options |
| `widget-set get WIDGET_SET_RID` | `client.widgets.WidgetSet.get` | `widget_set_rid` | shared options |
| `release delete WIDGET_SET_RID RELEASE_VERSION` | `client.widgets.WidgetSet.Release.delete` | `widget_set_rid`, `release_version` | shared options |
| `release get WIDGET_SET_RID RELEASE_VERSION` | `client.widgets.WidgetSet.Release.get` | `widget_set_rid`, `release_version` | shared options |
| `release list WIDGET_SET_RID` | `client.widgets.WidgetSet.Release.list` | `widget_set_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages`, shared options |

No command may receive `attribution`, `preview`, `_sdk_internal`, an absent optional set to `None`, or any unsupported paging, stream, raw-response, or file flag. Only `release list` may expose `--page-size`, `--page-token`, `--all`, `--max-pages`. No `dev-mode-settings disable/get/pause/set-widget-set` command and no `dev-mode-settings-v2` resource may exist in the catalog (SDK 1.102.0 lacks those methods; QUESTION-043).

## Test cases

### WGT-TC-001 - Catalog, parser, help, and exact 8 surface

- Type: positive, structural, negative parser.
- Given the installed module and launcher, when the catalog and parser are inspected, then exactly 8 unique SDK specifications exist (dev-mode-settings 2, repository 2, widget-set 1, release 3), every inventory command parses, pagination flags exist only on `release list`, and the stale-12 operations (`disable`, `get`, `pause`, `set-widget-set`) plus any `dev-mode-settings-v2` resource are absent.
- Command/function: `OP_SPECS`, `build_parser()`, `_spec_for()`, `_get_client()`, root/resource/operation `--help`, `main()` with missing resource/operation, unknown flags, missing required positionals/options, invalid choices/types.
- Prerequisites/fixtures: guarded config, client, network, and filesystem constructors.
- Steps: count `OP_SPECS`; assert the resource split `dev_mode_settings` 2 / `repository` 2 / `widget_set` 1 / `release` 3 and client paths `("DevModeSettings",)`, `("Repository",)`, `("WidgetSet",)`, and `("WidgetSet", "Release")`; assert `--page-size`/`--page-token`/`--all`/`--max-pages` exist only under `release list`; assert no `disable`/`pause`/`get`/`set-widget-set` subcommand and no `dev-mode-settings-v2` resource; parse all 8 inventory commands; run all help surfaces; run every incomplete or malformed form.
- Expected stdout/stderr/exit: help on stdout and exit `0`; catalog count exactly `8`; parser errors as one JSON envelope on stdout with `exit_code: 1`, empty diagnostic stderr, no traceback, no config/client/network/filesystem call.
- Cleanup: restore `sys.argv` and capture streams.
- Evidence mapping: QUESTION-043 tech-lead decision (8-op installed surface); DESIGN-022 catalog as amended; `test_catalog_contains_exact_8_operations`, `test_parser_accepts_every_declared_argument`, `test_parser_rejects_unknown_operation`, `test_no_stale_12_operations_in_catalog` (tests/test_foundry_widgets_cli.py).

### WGT-TC-002 - Nested SDK routing through DevModeSettings, Repository, WidgetSet, and WidgetSet.Release

- Type: positive, structural, route identity.
- Given distinct fakes for `DevModeSettings`, `Repository`, `WidgetSet`, and `WidgetSet.Release`, when every inventory command runs, then each resolves the exact nested object and never a flattened or sibling route.
- Command/function: `_get_client()` (roots at `root_client.widgets`, then walks the spec `client_path`) and each dispatch path.
- Prerequisites/fixtures: fakes whose sibling routes fail on access.
- Steps: run one command per client path; assert the resolved resource object identity; assert no flattened `widgets.*` method call.
- Expected stdout/stderr/exit: success results on stdout once, exit `0`, no unexpected stderr; no flattened `widgets.*` method call.
- Cleanup: reset fakes and captures.
- Evidence mapping: QUESTION-043 decision and DESIGN-022 nested dispatch; story AC 1; `test_catalog_contains_exact_8_operations` (all eight resolve through the four nested client paths) plus the dispatch tests `test_dev_mode_settings_enable_dispatches`, `test_release_get_dispatches_through_nested_client`, `test_repository_publish_dispatches_body_positionally`.

### WGT-TC-003 - Required inputs forwarded and absent optionals omitted

- Type: positive, structural.
- Given each inventory command, when dispatch runs, then required positionals/options reach the SDK call and every absent optional is omitted (never `None`).
- Command/function: all 8 dispatches; `_build_kwargs()`.
- Prerequisites/fixtures: recording SDK fakes.
- Steps: run each command with only required inputs; run `set-widget-set-by-id` with and without the settings body; run `repository publish` with the bounded read; inspect the SDK call arguments.
- Expected stdout/stderr/exit: `dev_mode_settings.enable` receives no required args; `set_widget_set_by_id` receives `widget_set_rid` plus the decoded `settings` dict (with `base_href` and `widget_settings`); `repository.get` receives the RID positionally; `repository.publish` receives the RID positionally, `body` bytes positionally, and `repository_version` as keyword; `widget_set.get` receives the RID positionally; `release.delete`/`release.get` receive both positionals; absent optionals absent from kwargs; success exits `0`.
- Cleanup: clear fake call records.
- Evidence mapping: QUESTION-043 decision and DESIGN-022 operation catalog; story AC 1; `test_dev_mode_settings_set_widget_set_by_id_dispatches_settings`, `test_release_get_dispatches_positionals`, `test_repository_publish_forwards_repository_version` (tests/test_foundry_widgets_cli.py).

### WGT-TC-004 - JSON argument validation before client creation

- Type: positive, negative, boundary.
- Given the structured flag `--settings-json`, when validation runs, then valid JSON with the documented top-level shape (a `WidgetSetDevModeSettingsById` object with `base_href` and `widget_settings`) reaches the SDK and invalid or mis-shaped JSON exits `1` before client or network work.
- Command/function: `_parse_json_object()`, `_validate_inputs()`, `main()`.
- Prerequisites/fixtures: guarded factory/network constructors; real SDK validators for nested checks.
- Steps: supply a valid settings object; supply malformed JSON text; supply valid JSON with the wrong top-level type (array, scalar, null); supply JSON whose nested fields violate SDK validators (missing `base_href`, missing `widget_settings`, unknown widget settings fields); run `set-widget-set-by-id` without `--settings-json`.
- Expected stdout/stderr/exit: valid inputs call the SDK and exit `0`; invalid inputs write one JSON user-input envelope to stdout, exit `1`, no traceback, and never echo the input payload into stdout/stderr/logs; a missing required `--settings-json` is a parser error with exit `1` before client creation.
- Cleanup: clear captured sentinels.
- Evidence mapping: DESIGN-022 JSON validation contract (WidgetSetDevModeSettingsById); story AC 2; `test_invalid_settings_json_rejected_before_client`, `test_settings_json_must_be_object`, `test_settings_json_required_for_set_widget_set_by_id` (tests/test_foundry_widgets_cli.py).

### WGT-TC-005 - Repository publish bounded file read after ACL and before client

- Type: positive, boundary, negative, security.
- Given the publish command and guarded lifecycle, when `repository publish` reads `--file`, then the bounded read (16 MiB cap) happens after the access-control decision and before any client construction, valid zips dispatch, oversized and missing files exit `1` as user input before client/network work, and the file bytes never echo into stdout/stderr/logs.
- Command/function: `main()` with `AccessControlGuard`/`AsyncClientFactory` spies; `_read_file_bounded()`.
- Prerequisites/fixtures: file fixtures 0 B, 4 KiB, exactly 16 MiB, 16 MiB + 1 B; directory path; missing path; client/factory constructors that record call order.
- Steps: run `repository publish` with each fixture; assert event order (ACL check, then file read, then factory/client); attempt the oversized file; attempt the directory and missing path.
- Expected stdout/stderr/exit: valid fixtures call `Repository.publish` with `body` bytes and exit `0`; the 16 MiB + 1 B file, directory, and missing path write one JSON user-input envelope on stdout and exit `1` before client construction; the raw zip bytes appear nowhere.
- Cleanup: delete fixture files, clear captures.
- Evidence mapping: DESIGN-022 binary upload contract (bounded read after ACL decision, before client); story AC 2; `test_repository_publish_reads_file_bounded`, `test_repository_publish_rejects_missing_file`, `test_repository_publish_rejects_oversized_file` (tests/test_foundry_widgets_cli.py).

### WGT-TC-006 - Release lifecycle dispatch: list, get, delete

- Type: positive, structural, stateful.
- Given recording SDK fakes, when the CLI drives `release list`, `release get`, and `release delete`, then each resolves through `WidgetSet.Release`, the paged list aggregates items, get forwards both positionals, and delete returns no content.
- Command/function: `release list`, `release get`, `release delete` dispatch.
- Prerequisites/fixtures: recording SDK fakes; `ListReleasesResponse` with `data` + `next_page_token`; `None` result fake for delete; `Release` response fakes.
- Steps: run `release list` with `--page-size 25` and capture pages; run `release get` on a returned release; run `release delete` on a release; inspect the SDK call arguments on each.
- Expected stdout/stderr/exit: each step exits `0`; `list` forwards `page_size` and aggregates into one array; `get`/`delete` forward both positionals; `delete` prints a serialized `null`/empty result consistently; no CLI-level state persists between invocations.
- Cleanup: clear fakes and captures.
- Evidence mapping: DESIGN-022 operation catalog; story AC 1, 3; `test_release_list_uses_raw_response_and_helper`, `test_release_get_dispatches_positionals`, `test_release_delete_dispatches_positionals` (tests/test_foundry_widgets_cli.py).

### WGT-TC-007 - Pagination contract: page bounds, resume token, and degenerate values

- Type: positive, boundary, negative.
- Given the `release list` pagination surface, when `--page-size`/`--page-token`/`--all`/`--max-pages` run, then the effective page batch respects `FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES` (hard cap 40, `--all` selects the cap) and degenerate values (`--max-pages 0`, non-positive `--page-size`) are rejected as user input before ACL/client/network work.
- Command/function: `release list` dispatch; `PaginationHelper` bound validation.
- Prerequisites/fixtures: multi-page fakes; env `FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES` set to `3` and unset.
- Steps: run with `--page-size 25`; run with `--page-token` resume; run `--max-pages 3`; run `--all` with env cap `3`; run `--max-pages 0`; run `--page-size 0`.
- Expected stdout/stderr/exit: valid bounds fetch the documented page count and exit `0` with one aggregated array; `--max-pages 0` and `--page-size 0` write one JSON user-input envelope on stdout and exit `1` before ACL/client/network work; metadata emitted to stderr.
- Cleanup: restore env and call records.
- Evidence mapping: DESIGN-022 paging contract; story AC 3; `test_release_list_uses_raw_response_and_helper`, `test_release_list_defaults_to_single_page`, `test_catalog_marks_exactly_one_paginated_operation` (tests/test_foundry_widgets_cli.py), shared `PaginationHelper` tests in tests/test_pagination_helper.py.

### WGT-TC-008 - DevModeSettings lifecycle: enable and set-widget-set-by-id

- Type: positive, structural, stateful.
- Given recording SDK fakes, when the CLI drives `dev-mode-settings enable` and `dev-mode-settings set-widget-set-by-id`, then each resolves through `DevModeSettings`, enable takes no required inputs, and set-widget-set-by-id forwards the decoded settings body plus the widget-set RID.
- Command/function: `dev-mode-settings enable`, `dev-mode-settings set-widget-set-by-id` dispatch.
- Prerequisites/fixtures: recording SDK fakes; `DevModeSettings` response fakes.
- Steps: run `enable` and capture the returned settings; run `set-widget-set-by-id` with a valid settings body and inspect the SDK call; run `set-widget-set-by-id` with each invalid settings shape.
- Expected stdout/stderr/exit: `enable` calls `DevModeSettings.enable` with no required args and exits `0`; `set_widget_set_by_id` receives `widget_set_rid` plus `settings` decoded dict and exits `0`; invalid shapes exit `1` before client creation.
- Cleanup: clear fakes and captures.
- Evidence mapping: QUESTION-043 decision (only enable + set_widget_set_by_id in scope); DESIGN-022 dev-mode-settings contract; story AC 1, 3; `test_dev_mode_settings_enable_dispatches`, `test_dev_mode_settings_set_widget_set_by_id_dispatches_settings` (tests/test_foundry_widgets_cli.py).

### WGT-TC-009 - Timeout boundaries and forwarding

- Type: positive, boundary, negative.
- Given CLI or configured timeouts, when execution starts, then values from 1 through 3600 seconds are accepted and the selected value reaches both retry handling and the SDK request; invalid values are rejected before ACL, scope, client, or filesystem work.
- Command/function: `_validate_timeout()`, representative commands with `--timeout`.
- Prerequisites/fixtures: values `1`, `30` (default), `3600`, CLI override `17`, configured default `42`, invalid `0`, `3601`, negative, and non-integer text.
- Steps: validate boundaries; execute with and without a CLI override; inspect retry construction and `request_timeout`; invoke each invalid value.
- Expected stdout/stderr/exit: valid requests produce one success result and exit `0`; retry and SDK receive the same chosen integer; invalid values write one JSON user-input envelope on stdout and exit `1` with no ACL/client/network call.
- Cleanup: restore config defaults and call records.
- Evidence mapping: ADR-002, DESIGN-022 invocation contract; story AC 12; `test_timeout_accepts_adr_002_bounds`, `test_invalid_timeout_returns_user_input_error` (tests/test_foundry_widgets_cli.py).

### WGT-TC-010 - ACL precedence: global, namespace, and operation scopes

- Type: security, positive, negative.
- Given metadata-only and operation-level overrides, when ACL evaluates `WIDGETS`, then permissive settings allow, blocking settings deny, and an operation override wins over the namespace setting.
- Command/function: `AccessControlGuard(cfg, "WIDGETS").check()` for the 8 catalog operations.
- Prerequisites/fixtures: packaged Widgets allow-list and isolated environment variables.
- Steps: enable global metadata-only; check all 8 operations; disable the namespace metadata-only at namespace level; disable one operation explicitly; combine namespace read-only with an operation override.
- Expected stdout/stderr/exit: permitted checks return silently; blocked CLI calls write a structured ACL envelope to stdout, exit `8`, and do not create a client; the denying rule appears on stderr diagnostics; no secret appears.
- Cleanup: remove every ACL environment variable.
- Evidence mapping: DESIGN-022 access-control table (corrected to the 8-op write set); story AC 7; `test_acl_write_classification_matches_design`, `test_metadata_only_permits_exactly_4_blocks_4` (precedence exercised through the namespace runtime checks).

### WGT-TC-011 - Read-only mode blocks the 4-operation write set; semantic reads stay permitted

- Type: security, positive, negative.
- Given read-only mode enabled, when each write command runs, then `dev-mode-settings enable`, `dev-mode-settings set-widget-set-by-id`, `release delete`, and `repository publish` exit `8` before client or filesystem effects, while `repository get`, `widget-set get`, `release get`, and `release list` remain executable as semantic reads.
- Command/function: `AccessControlGuard` + `main()` for each write command and the four reads.
- Prerequisites/fixtures: read-only environment; guarded factory/transport; response fakes.
- Steps: run all 4 write commands under read-only; run all 4 reads under read-only; inspect event order (no file read on blocked publish).
- Expected stdout/stderr/exit: each blocked write emits one ACL envelope and exit `8` with the denying rule on stderr; no SDK call or file read occurs; the four reads succeed and exit `0`.
- Cleanup: clear read-only variables, captures, and records.
- Evidence mapping: DESIGN-022 read-only policy (write set = enable, set_widget_set_by_id, delete, publish); story AC 7; `test_readonly_blocks_four_write_operations`, `test_reads_permitted_under_readonly` (tests/test_foundry_widgets_cli.py).

### WGT-TC-012 - Metadata-only tier: exact 4 permitted / 4 blocked

- Type: security, positive, negative.
- Given metadata-only mode, when every operation is checked, then exactly the 4 documented reads (`repository.get`, `widget_set.get`, `release.get`, `release.list`) are permitted and the 4 writes (`dev_mode_settings.enable`, `dev_mode_settings.set_widget_set_by_id`, `release.delete`, `repository.publish`) are blocked.
- Command/function: `AccessControlGuard` + `main()` under metadata-only for all 8 operations.
- Prerequisites/fixtures: packaged allow-list; guarded factory/transport.
- Steps: run each of the 4 permitted commands; run each of the 4 blocked commands; inspect the parsed allow-list rows.
- Expected stdout/stderr/exit: the 4 reads exit `0`; the 4 writes exit `8` with one ACL envelope each, no client construction; the packaged allow-list parses to exactly 4 PERMITTED and 4 BLOCKED rows.
- Cleanup: clear captures and records.
- Evidence mapping: DESIGN-022 metadata-only policy (corrected to the 8-op catalog); story AC 8; `test_metadata_only_permits_exactly_4_blocks_4`, `test_metadata_only_permits_four_and_blocks_four` (tests/test_foundry_widgets_cli.py).

### WGT-TC-013 - Packaged metadata-only policy is fail closed and CWD independent

- Type: security, packaging, negative.
- Given the installed package with a missing or malformed packaged allow-list, when ACL runs, then it fails closed (no operation permitted) and the packaged policy resolves from an arbitrary working directory.
- Command/function: `_METADATA_ALLOWLIST_PATH`, `AccessControlGuard` from an installed wheel/editable launch.
- Prerequisites/fixtures: malformed/missing policy fixtures in an isolated environment; empty arbitrary CWD, no `PYTHONPATH`.
- Steps: probe policy path from the installed package; run a permitted-class check with malformed policy; run checks from the arbitrary CWD.
- Expected stdout/stderr/exit: malformed/missing policy blocks even previously-permitted operations (fail closed, exit `8`); packaged policy path resolves inside the installed package; valid packaged policy applies the 4/4 rule from any CWD.
- Cleanup: delete isolated environments and fixtures.
- Evidence mapping: DESIGN-022 fail-closed rule; story AC 8, 14; `test_metadata_only_permits_exactly_4_blocks_4` (parsed from the packaged allow-list); packaged-policy CWD independence follows the same pattern as `test_packaged_metadata_policy_is_cwd_independent` (tests/test_foundry_audit_cli.py) and is verified by the TESTEXEC-022 wheel/editable probe.

### WGT-TC-014 - include_attribution=False on client and invocation scope

- Type: positive, privacy, structural.
- Given a real factory and `invocation_scope`, when any command executes, then client creation and scope use `include_attribution=False`, no attribution environment handling is added, and surrounding attribution state is unchanged after success and failure.
- Command/function: `AsyncClientFactory.invocation_scope(cfg)`, `factory.create(cfg)`, `main()`.
- Prerequisites/fixtures: factory/scope spies; preset outer attribution RID and environment.
- Steps: execute a read and a failed command; capture `include_attribution` on client and scope; capture attribution state before and after.
- Expected stdout/stderr/exit: both capture points pass `include_attribution=False`; no attribution variable is read or written; outer attribution state and env are identical after success and failure; no W3C `traceparent`/`tracestate`.
- Cleanup: reset context tokens and env.
- Evidence mapping: DESIGN-022 attribution rule (namespace outside FR-ATTR-4); story AC 9; `test_invocation_uses_include_attribution_false` (tests/test_foundry_widgets_cli.py).

### WGT-TC-015 - B3 enabled at outbound transport

- Type: positive, tracing, transport integration.
- Given tracing enabled, when the client is created and an SDK request is prepared, then outbound transport carries one valid B3 multi-header context.
- Command/function: `AsyncClientFactory.invocation_scope(cfg)`, SDK request preparation, a representative read.
- Prerequisites/fixtures: enabled tracing config, clean SDK context, transport header capture.
- Steps: enter the real tracing scope through `main()`; capture headers at client creation and request preparation.
- Expected stdout/stderr/exit: success result and exit `0`; every capture has lowercase-hex `X-B3-TraceId` of 32 characters, `X-B3-SpanId` of 16 characters, and `X-B3-Sampled` `0` or `1`; no W3C header appears.
- Cleanup: reset SDK context tokens and environment variables.
- Evidence mapping: DESIGN-005 B3 contract; story AC 10; `test_b3_transport_headers_enabled_disabled_retry_stable_and_restored` (tests/test_foundry_audit_cli.py) and `test_generated_context_has_valid_nonzero_b3_values_and_resets` (tests/test_tracing_provider.py); the namespace outbound-header probe is recorded in TESTEXEC-022 evidence.

### WGT-TC-016 - B3 disabled, retry stability, and context restoration

- Type: negative, resilience, isolation.
- Given disabled tracing, retries, prior context, or a later formatter failure, when execution leaves the invocation, then disabled calls add no B3 headers, retry attempts share one enabled context, and prior values are restored on every exit path.
- Command/function: `main()` with real `TracingProvider` scope and captured SDK transport headers.
- Prerequisites/fixtures: enabled and disabled configs; first-attempt transport failure followed by success; preset prior trace/span/sampled values; formatter, SDK, timeout, and cancellation failures.
- Steps: run the disabled flow; run the enabled retry flow; run each failure with prior values; inspect every outbound header set and context after exit.
- Expected stdout/stderr/exit: disabled flow has no `X-B3-*`; enabled retry captures identical B3 values for client creation and every attempt; no `traceparent`/`tracestate`; success exits `0`; failures use their ADR code; prior context is exact after all runs with no cross-test leakage.
- Cleanup: reset context tokens in `finally`, clear trace env vars, clear captures.
- Evidence mapping: DESIGN-005 isolation contract; story AC 10, 11; `test_b3_scope_restores_prior_values_after_formatter_failure` (tests/test_foundry_audit_cli.py) and `test_execute_traced_carries_same_b3_context_across_attempts_and_restores` (tests/test_tracing_provider.py).

### WGT-TC-017 - Retry behavior and at-least-once disclosure

- Type: resilience, negative, boundary.
- Given retryable and non-retryable failures, when `RetryHandler` wraps a command, then transient conditions (503, exhausted 429, configured transport exceptions) are retried per ADR-002, and validation, authorization, and permanent errors are never retried; the at-least-once disclosure is documented because retrying `repository publish` can create a duplicate release while retrying dev-mode toggles re-applies the same target state.
- Command/function: `RetryHandler` around representative read, enable, delete, and publish commands.
- Prerequisites/fixtures: HTTP 503-then-success; repeated 429; 400/401/403/404; delay and jitter disabled; attempt counters.
- Steps: run each sequence and count attempts; verify the at-least-once disclosure is documented for publish (duplicate-release caveat) and dev-mode toggles (idempotent target state); verify reads and delete are retried per the ADR policy.
- Expected stdout/stderr/exit: recovered 503 has one success result and exit `0`; exhausted 429 exits `7`; validation/auth/permanent errors exit once with codes `1`/`2`/`3`/`4`; no duplicate result or content leak; disclosure text present where applicable.
- Cleanup: clear retry state and sentinels.
- Evidence mapping: ADR-001/002, DESIGN-022 retry contract; story AC 11; retry tests in tests/unit_test_retry_error_output_log.py (`test_http_429_and_503_are_retryable`, `test_http_non_429_503_does_not_retry`, `test_success_after_one_retry`, `test_retry_exhaustion_raises`); at-least-once disclosure is a design-documented property captured in TESTEXEC-022 evidence.

### WGT-TC-018 - ADR-001 error taxonomy and structured envelopes

- Type: negative, error taxonomy.
- Given each supported failure class, when the CLI exits, then it writes one JSON error envelope to stdout with the exact ADR-001 code and keeps diagnostics separate on stderr.
- Command/function: representative commands through `main()` and `_serialize_error()`.
- Prerequisites/fixtures: user input, HTTP 401/403/404/429/503, timeout, cancellation, ACL denial, configuration failure, and unexpected exception fakes.
- Steps: inject each failure after the correct lifecycle point; parse stdout and stderr; verify skipped downstream work where applicable.
- Expected stdout/stderr/exit: codes are user input `1`, authentication `2`, permission `3`, not found `4`, timeout/cancellation `5`, server `6`, exhausted 429 `7`, ACL `8`, and configuration `9`; error envelope is JSON on stdout; NDJSON diagnostics, if any, are on stderr; no raw traceback, token, or body appears.
- Cleanup: clear injected exceptions, secrets, and temporary files.
- Evidence mapping: ADR-001, DESIGN-022 error contract; story AC 12, 13; `test_unknown_operation_returns_user_input_error`, `test_sdk_error_maps_to_server_error_exit_code`, `test_sdk_timeout_maps_to_timeout_exit_code` (tests/test_foundry_widgets_cli.py) plus the shared error-taxonomy tests in tests/unit_test_retry_error_output_log.py (`test_auth_error_exit_code_2` through `test_http_503_returns_server_error_after_retry_exhaustion`).

### WGT-TC-019 - Output formats: JSON, TOON, auto, and pretty

- Type: positive, output, boundary.
- Given success results of each shape, when `--format json|toon|auto` and `--pretty` run, then single models, `None` results (delete), and paged arrays follow the ADR-004 rules.
- Command/function: `OutputFormatter` via representative commands.
- Prerequisites/fixtures: a single `Repository`, a `None` result (`release delete`), a `DevModeSettings`, a paged list with a uniform `Release` array, an empty list, structured error.
- Steps: run each shape under each format; validate stdout parses as JSON where required; verify pretty indentation when enabled.
- Expected stdout/stderr/exit: exit `0`; auto selects TOON only for uniform non-empty arrays, otherwise JSON; empty/non-uniform output is JSON; `None` results serialize `null`/empty consistently; error output remains the structured JSON envelope.
- Cleanup: clear captures and models.
- Evidence mapping: ADR-004, DESIGN-022 output contract; story AC 12; `test_toon_output_format` (tests/test_foundry_widgets_cli.py) plus shared `OutputFormatter` coverage in tests/unit_test_retry_error_output_log.py.

### WGT-TC-020 - NDJSON stderr, stream separation, and confidentiality

- Type: positive, output, confidentiality.
- Given successful publish, list, get, and enable runs, when logs and results flow, then success data appears once on stdout, diagnostics are NDJSON on stderr, and credential/body/response sentinels never appear anywhere.
- Command/function: representative publish, list, get, and enable commands.
- Prerequisites/fixtures: secret sentinels embedded in request/response fixtures and in the zip file; captured logs.
- Steps: run each command; scan stdout, stderr, and captured logs for sentinel values, raw request bodies, zip bytes, settings bodies, and secret values.
- Expected stdout/stderr/exit: exit `0`; stdout carries results/metadata envelopes only; stderr carries NDJSON diagnostics only (empty or safe); none of the sentinels, payloads, zip bytes, settings bodies, or request bodies appear in any stream or log.
- Cleanup: clear sentinels and temporary files.
- Evidence mapping: ADR-005, DESIGN-022 log contract; story AC 12, 13; `test_sensitive_values_not_echoed_in_errors` plus the NDJSON stderr/log-setup tests in tests/unit_test_retry_error_output_log.py (TestNdJsonFormatter and log-setup stderr tests).

### WGT-TC-021 - Import, console boundary, help, and thin launcher

- Type: packaging, side-effect regression.
- Given the package and console entry point, when imported or asked for help, then they load without configuration, network, or filesystem side effects and use one event-loop boundary.
- Command/function: package import, module `--help`, entry point help, `console_main()`; the Claude skill launcher.
- Prerequisites/fixtures: empty arbitrary directory; guarded config/network/filesystem constructors; `asyncio.run` spy.
- Steps: import all Widgets modules; invoke root and operation help; call `console_main()` with fake `main()`; inspect the launcher source.
- Expected stdout/stderr/exit: imports produce no output or files; help exits `0` and names the 8 operations; `console_main()` calls `asyncio.run()` once and propagates the result; the launcher delegates to packaged interfaces and contains no copied catalog or ACL logic.
- Cleanup: remove subprocess directory and restore the event-loop spy.
- Evidence mapping: DESIGN-022 packaging contract; story AC 14; `test_console_main_wraps_async_entry` (tests/test_foundry_widgets_cli.py); the thin-launcher pattern follows `test_claude_launcher_is_thin_and_reexports_packaged_interfaces` (tests/test_audit_console_wrapper.py) and import side-effect-freedom is verified by the TESTEXEC-022 subprocess probe.

### WGT-TC-022 - Wheel, editable install, entry-point preservation, and regression

- Type: installation, regression.
- Given local wheel and editable installs, when commands run from an arbitrary directory without `PYTHONPATH`, then `foundry-widgets` works while existing console scripts and repository gates remain intact.
- Command/function: local wheel build; wheel and editable install; installed `foundry-widgets --help`; full test, Ruff, mypy, and package checks.
- Prerequisites/fixtures: isolated virtual environments for Python 3.11 and 3.12; `PIP_NO_INDEX=1`; local build dependencies; snapshot of existing `[project.scripts]` entries.
- Steps: build without live dependency resolution; inspect wheel for the Widgets policy; install wheel then editable form with `--no-deps`; run help and packaged ACL probe from arbitrary CWD; compare every pre-existing entry point; run focused Widgets tests and full regression with branch coverage.
- Expected stdout/stderr/exit: every help and package check exits `0`; wheel contains `foundry_cli/widgets/metadata-allow-list.md`; all 8 operations are listed; all prior console scripts remain; focused and full suites pass on both Python versions; Ruff and mypy pass; repository branch coverage is at least 80%; no command makes a live Foundry request.
- Cleanup: delete isolated builds and environments; retain command output in TESTEXEC evidence only.
- Evidence mapping: DESIGN-022 packaging and regression contract; story AC 14, 15; all `tests/test_foundry_widgets_cli.py` cases and the configured `pyproject.toml` gates; full-suite pass at the approved HEAD.

### WGT-TC-023 - Empty and non-empty required-value validation before client

- Type: negative, boundary.
- Given missing or empty required inputs, when each command runs, then whitespace-only or missing required positionals/options exit `1` as user input before ACL/client/network work, and no value is echoed.
- Command/function: `_validate_inputs()`, `_required_text()`, `main()`.
- Prerequisites/fixtures: guarded config/client/network constructors; empty-string and whitespace-only values.
- Steps: run `repository get ""`; run `release get RID ""`; run `repository publish RID --repository-version "  " --file F`; run `set-widget-set-by-id "" --settings-json '{"base_href":"x","widget_settings":{}}'`.
- Expected stdout/stderr/exit: each writes one JSON user-input envelope on stdout with `exit_code: 1`, empty diagnostic stderr, no traceback, and never echoes the input value.
- Cleanup: clear captures.
- Evidence mapping: DESIGN-022 validation contract; story AC 1; `test_empty_required_value_rejected_before_client` (tests/test_foundry_widgets_cli.py).

### WGT-TC-024 - No attribution, preview, or internal parameter leakage

- Type: security, negative, structural.
- Given the full catalog, when dispatch runs, then no SDK call ever receives `attribution`, `preview`, or `_sdk_internal`, and absent optionals are never `None`.
- Command/function: all 8 dispatches; `_build_kwargs()`.
- Prerequisites/fixtures: recording SDK fakes.
- Steps: run every command; inspect every recorded SDK call for forbidden keys.
- Expected stdout/stderr/exit: success exits `0`; no call contains `attribution`, `preview`, or `_sdk_internal`; no `None`-valued optional is forwarded.
- Cleanup: clear call records.
- Evidence mapping: DESIGN-022 technical summary (preview/internal excluded, attribution suppressed); story AC 1, 9; `test_catalog_contains_exact_8_operations` plus the dispatch tests that assert exact argument sets.

## Traceability matrix

| Requirement area | Story/design criteria | Cases |
| --- | --- | --- |
| Exact 8 catalog (corrected from stale 12 per QUESTION-043), pagination only on release list, parser, help, nested routing, input omission | Story AC 1; QUESTION-043 decision; corrected operation catalog | WGT-TC-001 through 003, 023, 024 |
| JSON argument validation, pre-client rejection, WidgetSetDevModeSettingsById body | Story AC 2 | WGT-TC-004 |
| Bounded zip publish (16 MiB) after ACL before client | Story AC 2 | WGT-TC-005 |
| Release lifecycle list/get/delete; cursor pagination | Story AC 1, 3 | WGT-TC-006, 007 |
| DevModeSettings lifecycle enable and set-widget-set-by-id | Story AC 1, 3 | WGT-TC-008 |
| Timeout boundaries and forwarding | Story AC 12 | WGT-TC-009 |
| ACL precedence, read-only 4-op write set, semantic reads, fail-closed policy | Story AC 7, 8 | WGT-TC-010 through 013 |
| include_attribution=False and B3 only | Story AC 9, 10 | WGT-TC-014 through 016 |
| Retry (at-least-once disclosure for publish/dev-mode toggles), error taxonomy | Story AC 11, 13 | WGT-TC-017, 018 |
| Output formats, NDJSON, confidentiality | Story AC 12, 13 | WGT-TC-019, 020 |
| Imports, console, launcher, wheel/editable, regression gates | Story AC 14, 15 | WGT-TC-021, 022 |
| Positive, negative, boundary, security, resilience, structural, packaging | Complete design strategy | WGT-TC-001 through 024 |

All story acceptance criteria have at least one positive case and, where meaningful, a negative, boundary, security, or failure-path case. The 8-operation catalog is fully covered: `dev-mode-settings enable` via WGT-TC-001 through 003, 008, 010, 011, 020; `dev-mode-settings set-widget-set-by-id` via WGT-TC-001 through 004, 008, 010, 011, 023; `repository get` via WGT-TC-001 through 003, 010, 011, 023; `repository publish` via WGT-TC-001 through 003, 005, 010, 011, 017, 020, 023, 024; `widget-set get` via WGT-TC-001 through 003, 010, 011; `release delete`/`release get` via WGT-TC-001 through 003, 006, 010, 011; `release list` via WGT-TC-001, 002, 006, 007, 010, 011, 019; all 8 via the ACL, attribution, tracing, output, and packaging cases.

## Execution and approval criteria

TESTEXEC-022 may begin only after DEV, UNITTEST, CODEREVIEW, and TESTCASE-022 reach their required completed states and the approved commit is available, and only after the implementation lands with the corrected 8-op surface (see the implementation gate note). Execute all 24 cases with no live network access unless an approved non-production smoke is explicitly authorized.

For every case, record PASS, FAIL, or BLOCKED with the exact command, environment, expected result, actual result, stdout, stderr, exit code, SDK calls, filesystem result, cleanup result, and linked evidence. Any failure requires a BUG-SUB before TESTEXEC-022 can close. Final QA sign-off also requires all linked defects to be terminal, every story acceptance criterion to have passing evidence, supported Python checks to pass, and repository branch coverage to remain at least 80%.
