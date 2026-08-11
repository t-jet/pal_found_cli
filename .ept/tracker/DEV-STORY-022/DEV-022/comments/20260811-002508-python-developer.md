Subject: Blocked by QUESTION-043 — SDK schema drift (widgets operation surface)
Created: 2026-08-11T00:25:08
Updated: 2026-08-11T00:25:08
---
## Blocker documented

**Blocker ID:** QUESTION-043 (Blocks link LINK-00677)
**Prior status:** New (development type has no New → Blocked transition; block recorded via link + this comment)

## Why

During environment verification for DEV-022 I discovered a critical SDK discrepancy:

- DESIGN-022 (approved) specifies a **12-operation** widgets catalog, validated against the vendored customer-input SDK snapshot.
- The **installed runtime SDK** `foundry-platform-sdk 1.102.0` (latest on PyPI, what tests and runtime use) exposes only **8** widgets operations: `widgets.DevModeSettings` has only `enable` + `set_widget_set_by_id` — **`disable`, `get`, `pause`, `set_widget_set` do not exist** on the installed SDK. A separate `DevModeSettingsV2` resource (`enable`/`set_widget_set_manifest`) exists that is not in DESIGN-022.

Implementing the 12-op CLI per DESIGN-022 would produce `dev-mode-settings disable/get/pause/set-widget-set` commands that fail at runtime (AttributeError on missing SDK method).

QUESTION-043 (addressed_to tech-lead) asks for a decision on which operation surface to implement. DEV-021 (third-party-applications) is NOT affected: installed SDK surface matches DESIGN-021 exactly (9 ops).

## Plan (contingent on decision)

1. Implement widgets CLI per the approved decision (12-op as-designed, or installed-surface 8-op + DevModeSettingsV2, per tech-lead).
2. Update DESIGN-022 / canonical env-var reference / metadata allow-list if the surface changes.
3. Add `disable`, `enable`, `pause`, `set_widget_set`, `set_widget_set_by_id`, `publish` write verbs to AccessControlGuard `_WRITE_VERBS` (only `publish`/`delete` currently present).
4. Tests mirroring the third-party-applications pattern.

Awaiting tech-lead decision on QUESTION-043 before proceeding.
