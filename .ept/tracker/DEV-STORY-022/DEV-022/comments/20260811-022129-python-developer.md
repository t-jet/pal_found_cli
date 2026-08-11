Subject: Implementation complete — 8-op widgets CLI, files, verification, OWASP self-review (commit 1b15565)
Created: 2026-08-11T02:21:29
Updated: 2026-08-11T02:21:29
---
## Files created/modified (commit 1b15565)

### Created
1. `src/foundry_cli/widgets/__init__.py` — package export (build_parser, console_main, main).
2. `src/foundry_cli/widgets/scripts/__init__.py` — scripts package.
3. `src/foundry_cli/widgets/scripts/foundry_widgets_cli.py` — 8-op CLI per corrected catalog.
4. `src/foundry_cli/widgets/metadata-allow-list.md` — packaged 4/8 policy (4 PERMITTED / 4 BLOCKED).
5. `.claude/skills/foundry-widgets/SKILL.md` — Claude skill doc.
6. `.claude/skills/foundry-widgets/scripts/foundry_widgets_cli.py` — thin launcher.
7. `tests/test_foundry_widgets_cli.py` — 38 unit/integration tests.
8. `tests/test_widgets_console_wrapper.py` — 3 console/launcher tests.

### Modified
9. `src/foundry_cli/common/access_control_guard.py` — added `enable`, `set_widget_set` to `_WRITE_VERBS` (prefix match covers set_widget_set_by_id; delete/publish already present).
10. `tests/test_access_control_guard.py` — regression test `test_widgets_verbs_are_writes`.
11. `pyproject.toml` — entry point `foundry-widgets`, package-data, ruff E402 ignore.
12. `.ept/docs/deliverables/architecture/DESIGN-022-widgets-cli.md` — corrected to 8-op surface (QUESTION-043), operation table, write set 4, policy 4/8.
13. `.ept/docs/deliverables/architecture/canonical-env-var-reference.md` — widgets section: 4 stale rows marked not implemented.
14. `.ept/docs/deliverables/architecture/metadata-allow-list.md` — widgets section: 4 stale rows marked not implemented.
15. `.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md` — DEV-STORY-022 row updated to 8 ops.
16. `.ept/docs/document_index.md` — DESIGN-022 row corrected + Implementation Change note.

## Verification (all green)

- compileall src exit 0; launcher --help exit 0 (foundry-widgets, all 4 resources listed).
- ruff clean on all new/modified files; mypy 0 errors (source + guard).
- Focused new tests: 41 passed (38 CLI + 3 wrapper); namespace branch coverage 89% (threshold 80%).
- ACL guard suite incl. new write-verb regression: 122 passed in combined run.
- Full suite: 1362 passed, 0 failed, repo branch coverage 86.55%.
- Runtime ACL probe (METADATA_ONLY=true): 4 reads (release get/list, repository get, widget-set get) pass ACL and reach client construction; 4 writes (dev-mode-settings enable, set-widget-set-by-id, release delete, repository publish) exit 8 before client.
- SDK surface verified via inspect.signature on installed foundry-platform-sdk 1.102.0: exactly 8 ops; set_widget_set_by_id(settings, widget_set_rid) kw-only; publish(repository_rid, body, *, repository_version) positional bytes.

## Decisions

- PAGINATED_OPS = {("release","list")} via with_raw_response + PaginationHelper.
- repository publish: bounded 16 MiB file read AFTER ACL decision, BEFORE client construction; --file consumed, --repository-version forwarded as SDK kwarg repository_version.
- set_widget_set_by_id --settings-json parsed to dict (WidgetSetDevModeSettingsById payload), --widget-set-rid required kwarg.
- include_attribution=False on factory + invocation_scope (outside FR-ATTR-4).
- Duplicate-release caveat under at-least-once retries documented in SKILL.md.
- OP_SPECS ordered alphabetically by resource (dev_mode_settings, release, repository, widget_set).

## OWASP Top-10 self-review

- A01 Broken Access Control: AccessControlGuard runs before client creation and file effects; 4-op write set blocked in READONLY/METADATA_ONLY; packaged policy fail-closed 4/8.
- A02 Cryptographic Failures: no crypto; tokens only via env/.env, never echoed.
- A03 Injection: argparse/JSON parsing local; no shell interpolation; inputs validated non-empty.
- A05 Security Misconfiguration: no hardcoded secrets; privacy-safe error envelopes (generic message for SDK errors).
- A07/A09/A10: no auth/identity changes; no sensitive logging; all external calls timeout-configurable.
- A06/A08: no vulnerable deps; no insecure deserialization (json.loads only).

No findings requiring escalation. Ready for code review (CODEREVIEW-022).
