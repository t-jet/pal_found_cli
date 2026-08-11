Subject: Implementation plan — foundry-widgets CLI (8-op corrected catalog, QUESTION-043)
Created: 2026-08-11T02:09:12
Updated: 2026-08-11T02:09:12
---
## Implementation plan (DEV-022)

### Corrected catalog — 8 ops (QUESTION-043 decision, tech-lead comment 20260811-005030)

Installed runtime SDK foundry-platform-sdk 1.102.0 exposes exactly 8 widgets operations (verified via inspect.signature on AsyncDevModeSettingsClient/AsyncRepositoryClient/AsyncWidgetSetClient/AsyncReleaseClient). The 4 missing DevModeSettings ops (disable/get/pause/set_widget_set) and DevModeSettingsV2 are OUT of scope per tech-lead decision.

| # | CLI command | SDK dispatch | Required input | Optional | Write |
| ---: | --- | --- | --- | --- | --- |
| 1 | dev-mode-settings enable | widgets.DevModeSettings.enable | — | — | yes |
| 2 | dev-mode-settings set-widget-set-by-id | widgets.DevModeSettings.set_widget_set_by_id | --widget-set-rid, --settings-json | — | yes |
| 3 | release delete | widgets.WidgetSet.Release.delete | widget_set_rid, release_version | — | yes |
| 4 | release get | widgets.WidgetSet.Release.get | widget_set_rid, release_version | — | no |
| 5 | release list | widgets.WidgetSet.Release.list | widget_set_rid | --page-size/--page-token/--all/--max-pages | no |
| 6 | repository get | widgets.Repository.get | repository_rid | — | no |
| 7 | repository publish | widgets.Repository.publish | repository_rid, --repository-version, --file | — | yes |
| 8 | widget-set get | widgets.WidgetSet.get | widget_set_rid | — | no |

### Deliverables
1. src/foundry_cli/widgets/__init__.py — package export (build_parser, console_main, main).
2. src/foundry_cli/widgets/scripts/__init__.py — scripts package.
3. src/foundry_cli/widgets/scripts/foundry_widgets_cli.py — 8-op CLI per corrected catalog.
4. src/foundry_cli/widgets/metadata-allow-list.md — packaged 5 PERMITTED / 3 BLOCKED (release.get/list, repository.get, widget_set.get, dev_mode_settings.enable? no — enable BLOCKED; see allow-list below).
5. .claude/skills/foundry-widgets/SKILL.md + scripts/foundry_widgets_cli.py thin launcher.
6. pyproject.toml — console entry point foundry-widgets, package-data, ruff E402 per-file-ignore.
7. src/foundry_cli/common/access_control_guard.py — add write verbs needed by final write set.
8. Canonical docs updates: DESIGN-022 (8-op note), canonical-env-var-reference.md widgets section (drop 4 stale ops), metadata-allow-list.md widgets section (8 rows), document_index.md.

### Metadata-only policy (5 PERMITTED / 3 BLOCKED)
- PERMITTED: widgets.release.get, widgets.release.list, widgets.repository.get, widgets.widget_set.get + widgets.dev_mode_settings.enable is a POST but token-scoped dev-mode toggle — per DESIGN-022 write set it is BLOCKED. So PERMITTED = release.get, release.list, repository.get, widget_set.get (4) and BLOCKED = dev_mode_settings.enable, dev_mode_settings.set_widget_set_by_id, release.delete, repository.publish (4)? Verify against canonical allow-list rows: canonical lists dev_mode_settings.get PERMITTED (not in catalog), dev_mode_settings.enable BLOCKED, set_widget_set_by_id BLOCKED, release.delete BLOCKED, release.get PERMITTED, release.list PERMITTED, repository.get PERMITTED, repository.publish BLOCKED, widget_set.get PERMITTED. => 4 PERMITTED / 4 BLOCKED for the 8 implemented ops.

### Implementation decisions
- PAGINATED_OPS = {("release","list")} via with_raw_response + PaginationHelper (--page-size/--page-token/--all/--max-pages).
- _UPLOAD_OPS = {"repository.publish"}: SDK positional body bytes; CLI reads --file bounded 16 MiB AFTER ACL decision, BEFORE client construction; --file consumed, --repository-version passed as SDK query kwarg repository_version.
- set_widget_set_by_id --settings-json parsed to dict (WidgetSetDevModeSettingsById union payload); --widget-set-rid required.
- client paths: DevModeSettings = ("DevModeSettings",); Repository = ("Repository",); WidgetSet = ("WidgetSet",); Release nested = ("WidgetSet","Release").
- include_attribution=False (outside FR-ATTR-4); B3 via invocation_scope; retry via RetryHandler; error serialization per ADR-001.
- Write verbs: enable, set_widget_set_by_id, delete, publish already partly in _WRITE_VERBS (delete/publish present); add enable + set_widget_set_by_id.

### Acceptance criteria (derived from corrected catalog + DESIGN-022)
- AC1: exactly 8 OP_SPECS entries, keys snake_case.
- AC2: all 8 commands parse (--help exit 0); dispatch resolves client_path.
- AC3: release list paginated; result + metadata emitted.
- AC4: repository publish bounded zip read 16 MiB after ACL, before client; --file never forwarded.
- AC5: write set (enable, set_widget_set_by_id, release.delete, repository.publish) blocked in READONLY/METADATA_ONLY; 4 reads permitted per allow-list.
- AC6: include_attribution=False; no preview params; optional args omitted when absent.
- AC7: all external connections timeout-configurable (--timeout, default cfg.timeout_s).
- AC8: OWASP self-review documented; no secrets; no network on import.

### Related docs
- DESIGN-022 (.ept/docs/deliverables/architecture/DESIGN-022-widgets-cli.md — still 12-op; will note 8-op correction in comment + canonical docs).
- Pattern refs: third-party-applications CLI (9-op with bounded upload + pagination), data_health CLI (json_args), common library.

### Verification plan
compileall, ruff, mypy, focused pytest, full regression, ACL runtime probes (metadata-only/readonly), --help smoke.
