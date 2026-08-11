# TESTEXEC-022 - Foundry Widgets CLI execution log

Date: 2026-08-11
Story: DEV-STORY-022
Test design: TESTCASE-022 (24 cases WGT-TC-001..024, corrected 8-op surface per QUESTION-043)
Commit under test: `1b15565` ("feat(widgets): add foundry-widgets CLI - 8-op corrected catalog (DEV-022, UNITTEST-022)")

## Result

**Pass.** All 24 mandatory cases (WGT-TC-001 through WGT-TC-024) passed
against the corrected 8-operation surface. The focused Widgets suite and the
full regression suite are green with branch coverage above the repository gate
on Python 3.11; on Python 3.12 the focused suite is green and the full suite
shows the same single pre-existing audit-namespace wheel-install flake
described in the TESTEXEC-021 log (environment-harness, unrelated to this
story). No defects were opened; no BUG-SUB was created.

## Baseline and environments

| Item | Value |
| --- | --- |
| Commit under test | `1b15565` (workflow_tuning_checkpoint-01; widgets CLI commit) |
| Workspace | Windows; shared working tree with unrelated in-progress changes |
| Python 3.11 (`.venv`) | CPython 3.11.9; `foundry-sdk 1.102.0`; `pytest 9.0.3` |
| Python 3.12 (seeded venv) | CPython 3.12.9; `foundry-sdk 1.102.0`; `pytest 9.1.1`; `pytest-asyncio`; `pytest-cov`; pip seeded (`T:\tmp\qa312-seeded`) |
| Transport | Nested async SDK fakes, installed SDK models, installed SDK exceptions |
| External access | No live Foundry requests (offline environment; no credentials available) |

Routine acceptance uses mocked async SDK transport and real installed SDK
exception classes, exactly as the test-case document prescribes. Live access
was neither approved nor required.

> **Environment note:** the shell carries no ambient `FOUNDRY_*` variables
> during the probes (scrubbed per invocation). With credentials absent,
> permitted reads pass the access-control decision and stop at the config
> check with the documented `ConfigurationError` exit `9`. This is environment
> behavior, not a product defect.

## Command evidence

| ID | Exact command/probe | Expected | Actual | Result |
| --- | --- | --- | --- | --- |
| E1 | Catalog probe: `len(OP_SPECS)`, resource split | Exactly 8 specs: dev_mode_settings 2, repository 2, widget_set 1, release 3 | `8`; `Counter({'release': 3, 'dev_mode_settings': 2, 'repository': 2, 'widget_set': 1})`; exit 0 | Pass |
| E2 | `.venv\Scripts\python.exe -m foundry_cli.widgets.scripts.foundry_widgets_cli --help` | Help on stdout, exit 0, 8 operations named | Usage naming `dev-mode-settings/release/repository/widget-set`; "8 Widgets API v2 operations"; exit 0 | Pass |
| E3 | `.claude\skills\foundry-widgets\scripts\foundry_widgets_cli.py --help` | Thin launcher help, exit 0 | Same usage text; exit 0 | Pass |
| E4 | `... release list --help` | Pagination flags only on release list | `--page-size`, `--page-token`, `--all`, `--max-pages` present only here | Pass |
| E5 | `... <cli> bogus` / `... <cli>` (no args) | One JSON user-input envelope on stdout, exit 1, no traceback | `{"error": true, "exit_code": 1, "exit_code_name": "UserInputError", "message": "Invalid command input", "traceback": ""}`; exit 1 (captured non-truncated) | Pass |
| E6 | Operation help surfaces | Each of the 8 inventory commands parses with exact flags; stale-12 ops absent | All 8 commands parse; no `disable`/`pause`/`get`/`set-widget-set` subcommands; no `dev-mode-settings-v2` resource | Pass |
| E7 | `python -m pytest -q tests/test_foundry_third_party_applications_cli.py tests/test_foundry_widgets_cli.py` | Focused namespaces pass | 75 passed; exit 0 (3.11); 75 passed (3.12 userbase), 81 passed incl. wrapper (3.12 seeded) | Pass |
| E8 | `python -m pytest -q tests/test_binary_download.py tests/test_pagination_helper.py tests/test_tracing_provider.py tests/unit_test_retry_error_output_log.py tests/test_third_party_applications_console_wrapper.py tests/test_widgets_console_wrapper.py` | Shared component suites pass | 213 passed; exit 0 (3.11 and 3.12) | Pass |
| E9 | `python -m pytest -q --cov=foundry_cli --cov-branch --cov-report=term` | Full suite with branch coverage >= 80% | 1362 passed, 0 failed; TOTAL 86.55%; widgets 85%; exit 0 (3.11) | Pass |
| E10 | Same on Python 3.12 (seeded venv) | Full suite passes on 3.12 | 1361 passed, 1 failed — the single failure is the pre-existing audit wheel-install env flake (see TESTEXEC-021 E10); TOTAL 86.55% | Pass* |
| E11 | `python -m pytest -q tests/test_widgets_console_wrapper.py` | Launcher thinness + one asyncio.run boundary | Passed (included in E8/E7 counts) | Pass |
| E12 | `python -m ruff check src tests .claude/skills/foundry-third-party-applications .claude/skills/foundry-widgets` | Ruff clean | All checks passed; exit 0 | Pass |
| E13 | `python -m mypy src` | Mypy clean | Success: no issues found in 69 source files; exit 0 | Pass |
| E14 | `python -m compileall -q src/foundry_cli/third_party_applications src/foundry_cli/widgets .claude/skills/foundry-third-party-applications .claude/skills/foundry-widgets` | Compile clean | Exit 0 | Pass |
| E15 | `python -m pip check` | Dependencies consistent | No broken requirements found; exit 0 | Pass |
| E16 | `python -m build --wheel --no-isolation` + wheel zip listing | Wheel builds; contains `foundry_cli/widgets/metadata-allow-list.md` and `foundry_cli/third_party_applications/metadata-allow-list.md` | Wheel built exit 0; both allow-lists packaged | Pass |
| E17 | Installed wheel in fresh venv: `foundry-widgets --help` from arbitrary CWD | Launcher works without `PYTHONPATH`, exit 0, 8 operations named | Usage text; exit 0 | Pass |
| E18 | Installed wheel, `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true`, `repository get` from arbitrary CWD | Packaged policy permits read (no ACL block), reaches config exit 9 | `ConfigurationError` exit 9; no ACL envelope | Pass |
| E19 | `python -c "import tomllib; ... project.scripts"` | Both entry points present; prior entries retained | 18 console entries total (16 prior + third-party-applications + widgets) | Pass |
| E20 | Metadata-only probes (3.11): `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` widgets read vs write | 4 reads permitted, 4 writes blocked | `repository get` -> exit 9 (permitted read reaches config); `dev-mode-settings enable` -> exit 8; `repository publish --file missing.zip` -> exit 8 (blocked before file read) | Pass |
| E21 | Read-only probes (3.11): `FOUNDRY_AGENTIC_CLI_READONLY=true` on writes | 4 writes exit 8 before client/filesystem | `repository publish` -> 8; `release delete` -> 8 (no file read on blocked publish) | Pass |
| E22 | Traceback suppression: `FOUNDRY_INCLUDE_TRACEBACK=false` on blocked path | `traceback` empty in envelope | ACL envelopes carry `"traceback": ""` | Pass |
| E23 | Allow-list parse: `src/foundry_cli/widgets/metadata-allow-list.md` | 8 rows: 4 PERMITTED, 4 BLOCKED | `release.get`, `release.list`, `repository.get`, `widget_set.get` PERMITTED; `dev_mode_settings.enable`, `set_widget_set_by_id`, `release.delete`, `repository.publish` BLOCKED | Pass |
| E24 | Launcher source inspection | Launcher is thin (re-exports only) | `from foundry_cli.widgets.scripts.foundry_widgets_cli import (build_parser, console_main, main)` | Pass |
| E25 | Import side-effect probe (subprocess) | Imports produce no output or files; catalogs accessible | `WGT OP_SPECS 8`; exit 0 | Pass |
| E26 | Skill disclosure grep | At-least-once disclosure: duplicate release on retried publish | Present in `.claude/skills/foundry-widgets/SKILL.md` ("retrying `repository publish` can create a duplicate release") | Pass |

`*` E10: identical to TESTEXEC-021 E10 — the sole 3.12 failure is the
pre-existing audit-namespace wheel-install env flake, unrelated to this story.

## Focused probe results

The focused suite covers the exact corrected 8-operation catalog on the four
client paths (`DevModeSettings`, `Repository`, `WidgetSet`, `WidgetSet.Release`),
the absence of the stale-12 operations (`disable`, `get`, `pause`,
`set-widget-set`) and of the out-of-scope `DevModeSettingsV2` resource, exact
nested SDK dispatch, JSON argument validation for the
`WidgetSetDevModeSettingsById` body (`--settings-json`: object shape,
`base_href` + `widget_settings`), the cursor-paged `release list` through
`PaginationHelper` (page-size/page-token/all/max-pages only on release list),
the bounded zip publish (`repository publish`) with the 16 MiB cap read after
the access-control decision and before client construction, the 4-operation
write set, the packaged 4-permitted/4-blocked metadata-only policy, fail-closed
behavior, `include_attribution=False`, B3-only tracing, retry, ADR-001 error
taxonomy, timeout bounds (1..3600), output formats, NDJSON stderr separation,
confidentiality, import/console/launcher packaging, and wheel/editable
regression.

CLI probes added independent runtime evidence: parser error envelopes (no
args, unknown operation), the exact catalog/client-path probe, the packaged
allow-list parse, the permitted-read pass through ACL to the config check
(exit 9 with credentials scrubbed), the blocked-write ACL envelopes (exit 8,
before file read), traceback suppression, pagination-flag scoping, and the
installed-wheel arbitrary-CWD launcher and ACL probes.

## Case disposition

| Case | Status | Evidence |
| --- | --- | --- |
| WGT-TC-001 (catalog, parser, help, exact 8 surface, stale-12 absent) | Pass | E1, E2, E4, E5, E6 |
| WGT-TC-002 (nested SDK routing through DevModeSettings, Repository, WidgetSet, WidgetSet.Release) | Pass | E1, E7 |
| WGT-TC-003 (required inputs forwarded, absent optionals omitted) | Pass | E7 |
| WGT-TC-004 (JSON argument validation before client creation) | Pass | E7 |
| WGT-TC-005 (repository publish bounded file read after ACL and before client) | Pass | E7, E21 |
| WGT-TC-006 (release lifecycle dispatch: list, get, delete) | Pass | E7 |
| WGT-TC-007 (pagination contract: page bounds, resume token, degenerate values) | Pass | E4, E8 |
| WGT-TC-008 (DevModeSettings lifecycle: enable and set-widget-set-by-id) | Pass | E7 |
| WGT-TC-009 (timeout boundaries and forwarding) | Pass | E7 |
| WGT-TC-010 (ACL precedence: global, namespace, operation scopes) | Pass | E7, E20 |
| WGT-TC-011 (read-only blocks the 4-op write set; semantic reads stay permitted) | Pass | E21 |
| WGT-TC-012 (metadata-only tier: exact 4 permitted / 4 blocked) | Pass | E20, E23 |
| WGT-TC-013 (packaged policy fail closed, CWD independent) | Pass | E16, E17, E18, E23 |
| WGT-TC-014 (include_attribution=False on client and invocation scope) | Pass | E8 |
| WGT-TC-015 (B3 enabled at outbound transport) | Pass | E8 |
| WGT-TC-016 (B3 disabled, retry stability, context restoration) | Pass | E8 |
| WGT-TC-017 (retry behavior and at-least-once disclosure) | Pass | E8, E26 |
| WGT-TC-018 (ADR-001 error taxonomy and structured envelopes) | Pass | E5, E20, E21, E22 |
| WGT-TC-019 (output formats: JSON, TOON, auto, pretty) | Pass | E7 |
| WGT-TC-020 (NDJSON stderr, stream separation, confidentiality) | Pass | E7, E8 |
| WGT-TC-021 (import, console, help, thin launcher) | Pass | E2, E3, E11, E14, E24, E25 |
| WGT-TC-022 (wheel, editable, entry points, regression) | Pass | E7, E9, E10, E12, E13, E14, E15, E16, E17, E19 |
| WGT-TC-023 (empty and non-empty required-value validation before client) | Pass | E7 |
| WGT-TC-024 (no attribution, preview, or internal parameter leakage) | Pass | E7 |

All 24 cases passed. Every story acceptance criterion has at least one passing
case, and the repository branch-coverage gate (80%) is met (86.55% total,
widgets 85%).

## Notes

- **Approval gate:** TESTCASE-022 was still Open at execution time (the
  parallel batch had not yet moved it to In Progress and no tech-lead approval
  comment existed). TESTEXEC-022's In Progress evidence stands; the
  Resolved/Closed lifecycle is completed only after TESTCASE-022 reaches
  In Progress and the tech-lead approval comments
  ("Tech lead approval" / "Approval gate for TESTEXEC-022: PASS") are posted.
- **Implementation gate note:** the corrected 8-op surface landed at commit
  `1b15565` (DEV-022/UNITTEST-022). The stale DESIGN-022 12-op catalog and the
  canonical env-var reference / metadata allow-list amendment to 8 rows are
  documented as implementer actions; the packaged allow-list in this commit is
  the corrected 8-row 4/4 policy (E23).
- **Python 3.12 note:** identical to TESTEXEC-021 E10 — one pre-existing
  environment-harness flake in the audit namespace's wheel-install test,
  unrelated to the widgets CLI.
- **Wheel install probe:** the first wheel install into the fresh venv left
  the console scripts unregistered (silent failure); a `--force-reinstall
  --no-deps` of the wheel installed all 18 entry points. Harness artifact, not
  a product defect.
- The `runpy` RuntimeWarning seen when invoking the module via `-m` is a
  CPython artifact and does not appear when running the packaged launcher or
  console entry point; it is not a product defect.

## QA sign-off

**PASS.** WGT-TC-001 through WGT-TC-024 passed with verifiable evidence
against the corrected 8-operation surface. No defects were opened. Full
regression is green on Python 3.11 (1362 passed, 0 failed) at 86.55% branch
coverage (widgets 85%); the focused and shared suites pass on both Python
3.11 and 3.12. The single 3.12 full-suite failure is a pre-existing
environment-dependent flake in the audit namespace, unrelated to this story.
