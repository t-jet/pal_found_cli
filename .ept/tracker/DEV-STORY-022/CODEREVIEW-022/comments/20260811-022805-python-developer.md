Subject: Review request — DEV-022 (foundry-widgets CLI, 8-op corrected catalog, commit 1b15565)
Created: 2026-08-11T02:28:05
Updated: 2026-08-11T02:28:05
---
## Review request — DEV-022 (foundry-widgets CLI)

DEV-022 is Resolved and blocks on CODEREVIEW-022 (LINK-00675/00676). Implementation commit **1b15565** on branch workflow_tuning_checkpoint-01.

### Scope reviewed
- `src/foundry_cli/widgets/` — 8-op CLI per QUESTION-043 corrected catalog (dev_mode_settings enable/set_widget_set_by_id, release delete/get/list, repository get/publish, widget-set get).
- `.claude/skills/foundry-widgets/` — SKILL.md + thin launcher.
- `src/foundry_cli/common/access_control_guard.py` — added `enable`, `set_widget_set` write verbs.
- `pyproject.toml` — console entry point, package-data, ruff E402.
- Tests: `tests/test_foundry_widgets_cli.py` (38), `tests/test_widgets_console_wrapper.py` (3), `tests/test_access_control_guard.py` (widgets regression).
- Docs: DESIGN-022 / canonical env-var reference / metadata allow-list / SAD-001 / document_index amended to 8-op surface.

### Verification summary (from DEV-022 evidence comment 20260811-022129-python-developer)
- compileall src exit 0; ruff clean; mypy 0 errors.
- Focused 41 passed; namespace branch coverage 89%; full suite 1362 passed at 86.55% branch.
- ACL runtime probe: 4 reads permitted / 4 writes blocked under METADATA_ONLY (exit 8 before client).
- SDK surface verified via inspect.signature on installed foundry-platform-sdk 1.102.0.

All files physically exist and compile — pre-review verification gate is satisfied. Reviewer: tech-lead (already assigned).
