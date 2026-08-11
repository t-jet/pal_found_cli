---
id: QUESTION-043
type: question
title: 'SDK schema drift: installed foundry-platform-sdk 1.102.0 exposes only 8 widgets ops,
  DESIGN-022 requires 12 (DevModeSettings missing disable/get/pause/set_widget_set)'
status: Closed
addressed_to: tech-lead
created: 2026-08-10
updated: 2026-08-11
priority: High
assignee: tech-lead
reporter: python-developer
---

# QUESTION-043: SDK schema drift: installed foundry-platform-sdk 1.102.0 exposes only 8 widgets ops, DESIGN-022 requires 12 (DevModeSettings missing disable/get/pause/set_widget_set)

## Description

## Context

DEV-022 implements the foundry-widgets CLI per DESIGN-022 (12 operations). DESIGN-022 was validated against the vendored customer-input SDK docs (`foundry_sdk/v2/widgets/dev_mode_settings.py`, 6 DevModeSettings ops: disable/enable/get/pause/set_widget_set/set_widget_set_by_id).

## Verified discrepancy (inspect.signature probes on installed SDK)

The installed runtime SDK `foundry-platform-sdk 1.102.0` (latest on PyPI, in `.venv`, resolved via `from foundry_sdk.v2.widgets...`) exposes only **8** widgets operations:

- `widgets.DevModeSettings` (installed `dev_mode_settings.py`): only `enable`, `set_widget_set_by_id` — **missing `disable`, `get`, `pause`, `set_widget_set`**.
- `widgets.DevModeSettingsV2` (installed `dev_mode_settings_v2.py`, not in vendored snapshot): `enable`, `set_widget_set_manifest` (paths `/v2/widgets/devModeSettingsV2/...`).
- `WidgetSet.Release`: delete/get/list (present).
- `Repository`: get/publish (present).
- `WidgetSet`: get (present).

File-size evidence: installed `dev_mode_settings.py` = 12,828 B vs vendored = 29,458 B; installed `_client.py` = 3,849 B vs vendored = 3,316 B. Vendored `models.py` has `SetWidgetSetDevModeSettingsRequest`; installed does not. Vendored errors include `DisableDevModeSettingsPermissionDenied`/`GetDevModeSettingsPermissionDenied`/`PauseDevModeSettingsPermissionDenied`/`SetWidgetSetDevModeSettingsPermissionDenied`; installed errors do not.

Vendored customer-input repo is at tag 1.80.0 (older). Installed is 1.102.0 (newer, divergent: DevModeSettings API changed shape — 6 ops replaced by 2 + a new DevModeSettingsV2 resource).

## Options for tech-lead decision

1. **Implement 12-op CLI as-designed** against installed SDK surface anyway: `dev-mode-settings disable/get/pause/set-widget-set` commands would fail at runtime (AttributeError on missing SDK method). Unit tests would mock missing methods. Not runtime-safe.
2. **Implement installed-surface 8-op CLI** (`enable`, `set_widget_set_by_id`, `set_widget_set_manifest`? no — manifest is on DevModeSettingsV2 not in design; release 3, repository 2, widget_set 1) and amend DESIGN-022 + canonical env-var reference + metadata allow-list.
3. **Pin/upgrade SDK** to a version whose widgets surface matches the design (vendored 1.80.0 has the 6-op surface; but 1.102.0 is latest — need to check whether any version >= the design baseline retains the 6-op DevModeSettings).
4. Other per tech-lead judgment.

## Request

Decision required: which widgets operation surface should DEV-022 implement, and whether the canonical env-var reference, metadata allow-list, and DESIGN-022 need amendment. Also confirm whether `DevModeSettingsV2` (enable/set_widget_set_manifest) is in scope or out of scope.

DEV-021 (third-party-applications) is NOT affected: installed tpa surface matches vendored exactly (9 ops, only cosmetic TypeAlias diff in models).

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
