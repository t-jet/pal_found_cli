Subject: Blocked by QUESTION-043 — widgets SDK operation surface decision pending
Created: 2026-08-11T00:28:16
Updated: 2026-08-11T00:28:16
---
## Blocker documented

**Blocker ID:** QUESTION-043 (Blocks link LINK-00678)
**Prior status:** New (unittest type has no New → Blocked transition; block recorded via link + this comment)

## Why

UNITTEST-022 writes unit tests for the foundry-widgets CLI. The widgets operation surface is under dispute:

- DESIGN-022 specifies 12 widgets operations (DevModeSettings 6: disable/enable/get/pause/set_widget_set/set_widget_set_by_id).
- Installed runtime SDK `foundry-platform-sdk 1.102.0` exposes only 8 widgets operations; `DevModeSettings` lacks `disable`, `get`, `pause`, `set_widget_set`.

Tests must target the agreed operation surface (and Open → In Progress DoD requires DEV-022 to be ready for tests). Until tech-lead resolves QUESTION-043, test scope is undetermined.

## Test plan (contingent on decision)

1. Catalog integrity tests for the agreed operation set.
2. Parser surface + dispatch tests for each operation (incl. `--settings-json` for set_widget_set/set_widget_set_by_id).
3. Bounded zip upload tests for `repository publish` (16 MiB bound after ACL, before client).
4. Pagination tests for `release list` (with_raw_response + PaginationHelper).
5. ACL write-classification tests (6 dev-mode verbs + release.delete + repository.publish) and metadata-only 5/12 policy tests.
6. Attribution (include_attribution=False), error taxonomy, timeout, output format, console boundary tests.

Awaiting tech-lead decision on QUESTION-043 before proceeding.
