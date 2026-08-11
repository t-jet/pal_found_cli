---
id: QUESTION-042
type: question
title: 'QUESTION-XXX - SDK/design mismatch: installed DevModeSettings exposes 2 ops, not
  6 (widgets)'
status: Duplicated
addressed_to: tech-lead
created: 2026-08-10
updated: 2026-08-11
priority: High
reporter: python-developer
---

# QUESTION-042: QUESTION-XXX - SDK/design mismatch: installed DevModeSettings exposes 2 ops, not 6 (widgets)

## Description

# SDK/design mismatch: installed DevModeSettings exposes 2 ops, not 6

## Context

DEV-022 implements the foundry-widgets CLI per DESIGN-022 (12 operations, of which DevModeSettings = 6: disable, enable, get, pause, set_widget_set, set_widget_set_by_id). The design was cross-validated against the vendored SDK source under `.ept/docs/customer_input/foundry-platform-python/` (which contains all 6 methods) and the canonical env-var reference + metadata allow-list (12 rows each).

## Verified evidence from the INSTALLED SDK (foundry-platform-sdk 1.102.0, in .venv)

- `foundry_sdk.v2.widgets.dev_mode_settings.DevModeSettingsClient` exposes exactly **2** public methods: `enable`, `set_widget_set_by_id`. Methods `disable`, `get`, `pause`, `set_widget_set` are **absent** from the installed source file.
- The installed `foundry_sdk/v2/widgets/_client.py` additionally exposes a **new** `DevModeSettingsV2` client (methods: `enable`, `set_widget_set_manifest`) that does not exist in the vendored customer-input snapshot.
- Installed SDK generated CLI (`v2/cli.py`) registers only `DevModeSettings.enable` and `DevModeSettings.set_widget_set_by_id` for dev_mode_settings.
- Direct comparison: `dev_mode_settings.py` DIFFERS between customer-input and installed; the 4 removed methods (disable/get/pause/set_widget_set) were dropped in the installed snapshot.
- All other widgets modules (release.py, repository.py, widget_set.py) are IDENTICAL to customer-input. TPA (third_party_applications) files are identical — DEV-021 (9 ops) is NOT affected.

## Question

How should DEV-022 proceed given the installed SDK 1.102.0 exposes only 2 of the 6 designed DevModeSettings operations?

Options for the tech-lead to rule on:
1. **Implement exactly what the installed SDK exposes**: 8 ops total (DevModeSettings 2: enable, set_widget_set_by_id; Release 3; Repository 2; WidgetSet 1), correcting the story count from 12 → 8 and updating env-ref/allow-list/DESIGN-022 accordingly.
2. **Implement the 12-op catalog from the vendored customer-input snapshot** (which has all 6 DevModeSettings methods) — accepting that 4 CLI commands (disable/get/pause/set_widget_set) would raise AttributeError at dispatch time against the installed SDK, since the methods do not exist at runtime.
3. **Pin/upgrade the SDK** to a version matching the vendored snapshot and implement all 12 ops.
4. **Other** — please specify.

Also requested: authoritative ruling on which SDK snapshot is canonical for implementation (installed .venv vs vendored customer-input), and whether the env-var reference / metadata allow-list / DESIGN-022 should be corrected if option 1 is chosen.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
