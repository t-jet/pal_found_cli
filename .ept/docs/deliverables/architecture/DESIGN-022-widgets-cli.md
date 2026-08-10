# DESIGN-022 - Foundry Widgets CLI

| Field | Value |
| --- | --- |
| Story | DEV-STORY-022 |
| Status | Completed; ready for implementation |
| Date | 2026-08-10 |
| Scope | `foundry-widgets` CLI and Claude skill, 8 Widgets API v2 operations (corrected from 12, QUESTION-043) |

> **Operation count correction (QUESTION-043, 2026-08-11):** The original design was
> validated against the vendored customer-input SDK snapshot (v1.102.0) at 12 operations.
> The **installed runtime SDK** `foundry-platform-sdk 1.102.0` (what tests and runtime
> actually use) exposes exactly **8** public operations. `DevModeSettings` has only
> `enable` and `set_widget_set_by_id` — `disable`, `get`, `pause`, `set_widget_set`
> do NOT exist and a separate `DevModeSettingsV2` resource (`enable`/`set_widget_set_manifest`)
> is present but **out of scope** per the tech-lead decision (comment 20260811-005030
> on DEV-022, 20260811-005035 on UNITTEST-022). Implementing the 12-op catalog would
> raise `AttributeError` at runtime for the 4 missing operations. This document and the
> canonical env-var reference / metadata allow-list are amended to the 8-op surface.

## Technical summary

Add a Widgets namespace CLI exposing exactly 8 public `foundry_sdk.v2.widgets` operations across the `DevModeSettings`, `Repository`, `WidgetSet`, and nested `WidgetSet.Release` client paths. The CLI uses the SDK's public nested clients and excludes preview and internal parameters.

Every command supports the shared `--timeout`, `--format`, and `--pretty` options. JSON-shaped inputs are parsed and validated locally before the client is created. Optional SDK arguments are omitted when the user does not provide them. The client factory and `invocation_scope` use `include_attribution=False`; this namespace is outside FR-ATTR-4 scope and must not add attribution configuration.

> **Operation count note:** The story title and SAD-001 reference "12 operations", but
> the **installed runtime SDK** (foundry-platform-sdk 1.102.0) exposes exactly **8**
> public operations (`DevModeSettings` 2: enable, set_widget_set_by_id; `Release` 3:
> delete, get, list; `Repository` 2: get, publish; `WidgetSet` 1: get). The four
> `DevModeSettings` operations `disable`/`get`/`pause`/`set_widget_set` are absent from
> the installed SDK and `DevModeSettingsV2` is out of scope (QUESTION-043 decision).
> The canonical environment-variable reference and the metadata allow-list are amended
> to 8 rows each (the 4 removed rows are retained in the canonical docs but marked as
> not implemented). This count supersedes the original 12-op design.

## Evidence and governing references

This design follows:

- SRS-001 FR-ACL, FR-PAG, FR-TRACE, FR-ASYNC, FR-OUT, FR-ERR, and the privacy requirements;
- SAD-001 namespace packaging and stateless CLI structure (EPIC-007, DEV-STORY-022 entry);
- DESIGN-005 tracing, retry, and common-component integration contracts;
- DESIGN-011 patterns for an immutable operation catalog, exact nested SDK dispatch, packaged policy, and SDK-native error handling;
- DESIGN-012 patterns for JSON argument validation and output contracts;
- DESIGN-013 patterns for cursor pagination via `PaginationHelper`;
- DESIGN-017/018 patterns for bounded binary uploads (bounded file read after the access-control decision, before client construction);
- ADR-001 exit codes, ADR-002 timeouts, ADR-004 format selection, ADR-005 logging, ADR-006 configuration search, and ADR-007 read-only precedence;
- the canonical environment-variable reference, which defines operation enablement and read-only overrides (namespace `widgets`, 8 implemented rows + 4 marked not-implemented);
- the canonical metadata allow-list, which blocks 4 of the 8 implemented operations in tier 3;
- vendored SDK sources under `foundry_sdk/v2/widgets/` (`_client.py`, `dev_mode_settings.py`, `release.py`, `repository.py`, `widget_set.py`) and the installed runtime SDK 1.102.0 signatures verified via `inspect`.

## Operation catalog

CLI names use kebab-case. Catalog keys and ACL paths use snake_case. `OP_SPECS` contains exactly 8 unique entries.

| # | CLI command | SDK dispatch | Required input | Optional input | HTTP and result |
| ---: | --- | --- | --- | --- | --- |
| 1 | `dev-mode-settings enable` | `client.widgets.DevModeSettings.enable` | — | — | `POST /v2/widgets/devModeSettings/enable`; `DevModeSettings` |
| 2 | `dev-mode-settings set-widget-set-by-id` | `client.widgets.DevModeSettings.set_widget_set_by_id` | `--widget-set-rid`, `--settings-json` | — | `POST /v2/widgets/devModeSettings/setWidgetSetById`; `DevModeSettings` |
| 3 | `release delete` | `client.widgets.WidgetSet.Release.delete` | `widget_set_rid`, `release_version` | — | `DELETE /v2/widgets/widgetSets/{rid}/releases/{version}`; None |
| 4 | `release get` | `client.widgets.WidgetSet.Release.get` | `widget_set_rid`, `release_version` | — | `GET /v2/widgets/widgetSets/{rid}/releases/{version}`; `Release` |
| 5 | `release list` | `client.widgets.WidgetSet.Release.list` | `widget_set_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages` | `GET /v2/widgets/widgetSets/{rid}/releases`; `ResourceIterator[Release]` |
| 6 | `repository get` | `client.widgets.Repository.get` | `repository_rid` | — | `GET /v2/widgets/repositories/{rid}`; `Repository` |
| 7 | `repository publish` | `client.widgets.Repository.publish` | `repository_rid`, `--repository-version`, `--file` | — | `POST /v2/widgets/repositories/{rid}/publish`; `Release` |
| 8 | `widget-set get` | `client.widgets.WidgetSet.get` | `widget_set_rid` | — | `GET /v2/widgets/widgetSets/{rid}`; `WidgetSet` |

> **Not implemented (absent from installed SDK 1.102.0):** `dev-mode-settings disable`,
> `dev-mode-settings get`, `dev-mode-settings pause`, `dev-mode-settings set-widget-set`.
> `DevModeSettingsV2` (`enable`/`set_widget_set_manifest`) is a separate resource
> outside this design's scope. See the correction note at the top.

The Widgets namespace routes through `client.widgets` with four client paths: `DevModeSettings`, `Release` (nested under `WidgetSet.Release`), `Repository`, and `WidgetSet`. `preview` parameters are excluded. The `release list` response (`ListReleasesResponse`) carries `data` plus a `nextPageToken` cursor.

### Paging contract

`release list` is the only paged operation; it returns a `ResourceIterator` with a server cursor. It uses `PaginationHelper` and accepts `--page-size`, `--page-token`, `--all`, and `--max-pages`. No other operation exposes pagination flags.

### Binary upload contract

`repository publish` accepts the widget-set build as a zip file that must include a valid manifest at `.palantir/widgets.config.json`. The SDK signature is `publish(repository_rid, body: bytes, *, repository_version, preview, ...)` with `body` as a positional bytes argument. The CLI reads `--file` with a bounded read (16 MiB) AFTER the access-control decision and BEFORE the client is constructed. The `--file` flag is consumed by the CLI and never forwarded; `--repository-version` is passed as the SDK `repository_version` query parameter.

### Access and runtime policy

The write set is `dev_mode_settings.enable`, `dev_mode_settings.set_widget_set_by_id`, `release.delete`, and `repository.publish` (4 operations). `release.delete` is a DELETE classified by the shared write-verb set. The two mutating POSTs (`enable`, `set_widget_set_by_id`) require write classification: add the operation-specific verbs to the shared `AccessControlGuard` write set (`enable`, `set_widget_set`; precedent: `launch`, `promote_version`, `upload`, `calculate` from the models/media-sets batches). The four remaining operations (`release.get`, `release.list`, `repository.get`, `widget_set.get`) are semantic reads. Read-only mode blocks the complete write set unless a canonical override permits it.

Metadata-only policy is fail closed. It permits exactly 4 operations (`release.get`, `release.list`, `repository.get`, `widget_set.get`) and blocks the remaining 4 (`dev_mode_settings.enable`, `dev_mode_settings.set_widget_set_by_id`, `release.delete`, `repository.publish`), matching the amended canonical allow-list. Namespace and exact-operation controls are evaluated before the client is constructed.

Use SDK-native B3 tracing through `invocation_scope` and restore context after success and failure. Retry only the ADR-approved transient conditions and disclose at-least-once behavior: retrying `repository.publish` can create a duplicate release, and retrying dev-mode toggles re-applies the same target state; both caveats are documented in skill documentation.

## Component breakdown

- `src/foundry_cli/widgets/` — command catalog, parser, dispatch, JSON validator for `--settings-json` (the `WidgetSetDevModeSettingsById` payload), bounded file-read for publish, pagination integration, packaged metadata-only policy.
- Claude skill and launcher for `foundry-widgets`.
- Focused unit and integration test modules.
- `pyproject.toml` console entry point, package data, and quality-tool scope.

## Estimates and sprint fit

| Sub-task | Assignee | Estimated hours |
| --- | --- | --- |
| DESIGN-022 | tech-lead | 6 |
| DEV-022 | python-developer | 16 |
| UNITTEST-022 | python-developer | 12 |
| CODEREVIEW-022 | tech-lead | 6 |
| TESTCASE-022 | qa-engineer | 8 |
| TESTEXEC-022 | qa-engineer | 8 |
| DEVOPS-022 | devops-engineer | 3 |
| **Total** | | **59** |

The story fits within one sprint (8 operations across four client paths, one paged command, one bounded upload). No split into additional stories is required.

## Risks

SDK schema drift on the `DevModeSettings`/`Release`/`Repository`/`WidgetSet` models; duplicate release effects under at-least-once retries for `publish`; dev-mode settings JSON payload shape (widget-id-based vs rid-based settings unions) validated locally; packaged-policy drift; shared ACL write-verb classification changes; and zip file size/manifest validation for publish.
