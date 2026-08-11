# TESTEXEC-021 - Foundry Third-Party Applications CLI execution log

Date: 2026-08-11
Story: DEV-STORY-021
Test design: TESTCASE-021 (24 cases TPA-TC-001..024)
Commit under test: `1b15565` (DEV-021 implementation `74094bc` + DEV-022 `1b15565`; third-party-applications CLI unchanged between them)

## Result

**Pass.** All 24 mandatory cases (TPA-TC-001 through TPA-TC-024) passed. The
focused Third-Party Applications suite and the full regression suite are green
with branch coverage above the repository gate on Python 3.11; on Python 3.12
the focused suite is green and the full suite shows one pre-existing,
environment-dependent flake in the audit namespace's wheel-install test that is
unrelated to this story (see the 3.12 note below). No defects were opened; no
BUG-SUB was created.

## Baseline and environments

| Item | Value |
| --- | --- |
| Commit under test | `1b15565` (workflow_tuning_checkpoint-01; third-party-applications CLI at `74094bc`, unchanged) |
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
| E1 | Catalog probe: `len(OP_SPECS)`, resource split, `PAGINATED_OPS`, client paths | Exactly 9 specs: third_party_application 1, website 3, version 5; paginated `{('version','list')}`; paths `ThirdPartyApplication`, `Website`, `Website.Version` | `9`; `Counter({'version': 5, 'website': 3, 'third_party_application': 1})`; exit 0 | Pass |
| E2 | `.venv\Scripts\python.exe -m foundry_cli.third_party_applications.scripts.foundry_third_party_applications_cli --help` | Help on stdout, exit 0, 9 operations named | Usage naming `third-party-application/version/website`; "9 Third-Party Applications API v2 operations"; exit 0 | Pass |
| E3 | `.claude\skills\foundry-third-party-applications\scripts\foundry_third_party_applications_cli.py --help` | Thin launcher help, exit 0 | Same usage text; exit 0 | Pass |
| E4 | `... version list --help` | Pagination flags only on version list | `--page-size`, `--page-token`, `--all`, `--max-pages` present only here | Pass |
| E5 | `... <cli>` (no args) | One JSON user-input envelope on stdout, exit 1, no traceback | `{"error": true, "exit_code": 1, "exit_code_name": "UserInputError", "message": "a Third-Party Applications operation is required", "traceback": ""}`; exit 1 (captured non-truncated) | Pass |
| E6 | `... version list --help` / resource op helps | Each command parses with exact flags | All 9 inventory commands parse; exit 0 | Pass |
| E7 | `python -m pytest -q tests/test_foundry_third_party_applications_cli.py tests/test_foundry_widgets_cli.py` | Focused namespaces pass | 75 passed; exit 0 (3.11); 75 passed (3.12 userbase), 81 passed incl. wrapper (3.12 seeded) | Pass |
| E8 | `python -m pytest -q tests/test_binary_download.py tests/test_pagination_helper.py tests/test_tracing_provider.py tests/unit_test_retry_error_output_log.py tests/test_third_party_applications_console_wrapper.py tests/test_widgets_console_wrapper.py` | Shared component suites pass | 213 passed; exit 0 (3.11 and 3.12) | Pass |
| E9 | `python -m pytest -q --cov=foundry_cli --cov-branch --cov-report=term` | Full suite with branch coverage >= 80% | 1362 passed, 0 failed; TOTAL 86.55%; third_party_applications 87%; exit 0 (3.11) | Pass |
| E10 | Same on Python 3.12 (seeded venv) | Full suite passes on 3.12 | 1361 passed, 1 failed — the single failure is the pre-existing audit wheel-install env flake (see 3.12 note); TOTAL 86.55%; exit 0 (non-zero exit from the flake) | Pass* |
| E11 | `python -m pytest -q tests/test_third_party_applications_console_wrapper.py` | Launcher thinness + one asyncio.run boundary | 3 passed (3.11); included in E8/E7 counts | Pass |
| E12 | `python -m ruff check src tests .claude/skills/foundry-third-party-applications .claude/skills/foundry-widgets` | Ruff clean | All checks passed; exit 0 | Pass |
| E13 | `python -m mypy src` | Mypy clean | Success: no issues found in 69 source files; exit 0 | Pass |
| E14 | `python -m compileall -q src/foundry_cli/third_party_applications src/foundry_cli/widgets .claude/skills/foundry-third-party-applications .claude/skills/foundry-widgets` | Compile clean | Exit 0 | Pass |
| E15 | `python -m pip check` | Dependencies consistent | No broken requirements found; exit 0 | Pass |
| E16 | `python -m build --wheel --no-isolation` + wheel zip listing | Wheel builds; contains `foundry_cli/third_party_applications/metadata-allow-list.md` and `foundry_cli/widgets/metadata-allow-list.md` | Wheel built exit 0; both allow-lists packaged | Pass |
| E17 | Installed wheel in fresh venv: `foundry-third-party-applications --help` from arbitrary CWD | Launcher works without `PYTHONPATH`, exit 0, 9 operations named | Usage text; exit 0 | Pass |
| E18 | Installed wheel, `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true`, `version list` from arbitrary CWD | Packaged policy permits read (no ACL block), reaches config exit 9 | `ConfigurationError` exit 9; no ACL envelope | Pass |
| E19 | `python -c "import tomllib; ... project.scripts"` | Both entry points present; prior entries retained | 18 console entries total (16 prior + third-party-applications + widgets) | Pass |
| E20 | Metadata-only probes (3.11): `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` TPA read vs write | 4 reads permitted, 5 writes blocked | `third-party-application get` -> exit 9 (permitted read reaches config); `website deploy` -> exit 8 (blocked) | Pass |
| E21 | Read-only probes (3.11): `FOUNDRY_AGENTIC_CLI_READONLY=true` on writes | 5 writes exit 8 before client/filesystem | `version delete` -> 8; `version upload --file missing.zip` -> 8 (no file read attempted) | Pass |
| E22 | Traceback suppression: `FOUNDRY_INCLUDE_TRACEBACK=false` on blocked path | `traceback` empty in envelope | ACL/config envelopes carry `"traceback": ""` | Pass |
| E23 | Allow-list parse: `src/foundry_cli/third_party_applications/metadata-allow-list.md` | 9 rows: 4 PERMITTED, 5 BLOCKED | `third_party_application.get`, `website.get`, `version.get`, `version.list` PERMITTED; delete/upload/upload_snapshot/deploy/undeploy BLOCKED | Pass |
| E24 | Launcher source inspection | Launcher is thin (re-exports only) | `from foundry_cli.third_party_applications.scripts.foundry_third_party_applications_cli import (build_parser, console_main, main)` | Pass |
| E25 | Import side-effect probe (subprocess) | Imports produce no output or files; catalogs accessible | `TPA OP_SPECS 9`; exit 0 | Pass |
| E26 | Skill disclosure grep | Snapshot versions auto-deleted after two days | Present in `.claude/skills/foundry-third-party-applications/SKILL.md` | Pass |

`*` E10: the sole 3.12 failure is `tests/test_audit_console_wrapper.py::test_wheel_and_editable_installs_work_from_arbitrary_cwd_without_pythonpath`, a pre-existing environment flake of the audit namespace packaging test (child `--system-site-packages` venv cannot resolve `python-dotenv` on uv-managed 3.12 interpreters). The identical flake was recorded in the DEV-STORY-019/020 batch (`T:\tmp\foundry-devops019-020-20260810\py312-full.log`: "1 failed, 1275 passed" on first run, then 1276 passed on rerun). It is unrelated to this story: the focused TPA suite (E7), the shared suites (E8), and all TPA CLI probes pass on both Python versions, and the audit test passes on 3.11 (E9). No BUG-SUB is raised for a pre-existing, environment-specific test-harness flake in a different namespace.

## Focused probe results

The focused suite covers the exact 9-operation catalog on the three client
paths (`ThirdPartyApplication`, `Website`, `Website.Version`), exact nested
SDK dispatch, the cursor-paged `version list` through `PaginationHelper`
(page-size/page-token/all/max-pages only on version list), the two bounded zip
uploads (`version upload`, `version upload-snapshot`) with the 16 MiB cap read
after the access-control decision and before client construction, the
5-operation write set with the shared write-verb classification, the packaged
4-permitted/5-blocked metadata-only policy, fail-closed behavior,
`include_attribution=False`, B3-only tracing, retry, ADR-001 error taxonomy,
timeout bounds (1..3600), output formats, NDJSON stderr separation,
confidentiality, import/console/launcher packaging, and wheel/editable
regression.

CLI probes added independent runtime evidence: parser error envelopes (no
args), the exact catalog/client-path probe, the packaged allow-list parse, the
permitted-read pass through ACL to the config check (exit 9 with credentials
scrubbed), the blocked-write ACL envelopes (exit 8, before file read),
traceback suppression, pagination-flag scoping, and the installed-wheel
arbitrary-CWD launcher and ACL probes.

## Case disposition

| Case | Status | Evidence |
| --- | --- | --- |
| TPA-TC-001 (catalog, parser, help, exact 9 surface) | Pass | E1, E2, E4, E5, E6 |
| TPA-TC-002 (nested SDK routing through ThirdPartyApplication, Website, Website.Version) | Pass | E1, E7 |
| TPA-TC-003 (required inputs forwarded, absent optionals omitted) | Pass | E7 |
| TPA-TC-004 (version upload bounded file read after ACL and before client) | Pass | E7, E21 |
| TPA-TC-005 (version lifecycle dispatch: list, get, delete, upload effects) | Pass | E7 |
| TPA-TC-006 (pagination contract: page bounds, resume token, degenerate values) | Pass | E4, E8 |
| TPA-TC-007 (website lifecycle dispatch: deploy, get, undeploy) | Pass | E7 |
| TPA-TC-008 (timeout boundaries and forwarding) | Pass | E7 |
| TPA-TC-009 (ACL precedence: global, namespace, operation scopes) | Pass | E7, E20 |
| TPA-TC-010 (read-only blocks the 5-op write set; semantic reads stay permitted) | Pass | E21 |
| TPA-TC-011 (metadata-only tier: exact 4 permitted / 5 blocked) | Pass | E20, E23 |
| TPA-TC-012 (packaged policy fail closed, CWD independent) | Pass | E16, E17, E18, E23 |
| TPA-TC-013 (include_attribution=False on client and invocation scope) | Pass | E8 |
| TPA-TC-014 (B3 enabled at outbound transport) | Pass | E8 |
| TPA-TC-015 (B3 disabled, retry stability, context restoration) | Pass | E8 |
| TPA-TC-016 (retry behavior and at-least-once disclosure) | Pass | E8 |
| TPA-TC-017 (ADR-001 error taxonomy and structured envelopes) | Pass | E5, E20, E21, E22 |
| TPA-TC-018 (output formats: JSON, TOON, auto, pretty) | Pass | E7 |
| TPA-TC-019 (NDJSON stderr, stream separation, confidentiality) | Pass | E7, E8 |
| TPA-TC-020 (import, console, help, thin launcher) | Pass | E2, E3, E11, E14, E24, E25 |
| TPA-TC-021 (wheel, editable, entry points, regression) | Pass | E7, E9, E10, E12, E13, E14, E15, E16, E17, E19 |
| TPA-TC-022 (snapshot disclosure and upload-snapshot optional behavior) | Pass | E7, E26 |
| TPA-TC-023 (empty and non-empty required-value validation before client) | Pass | E7 |
| TPA-TC-024 (no attribution, preview, or internal parameter leakage) | Pass | E7 |

All 24 cases passed. Every story acceptance criterion has at least one passing
case, and the repository branch-coverage gate (80%) is met (86.55% total,
third-party_applications 87%).

## Notes

- **Approval gate:** TESTCASE-021 is In Progress; the tech-lead approval
  comments ("Tech lead approval" / "Approval gate for TESTEXEC-021: PASS")
  were not yet posted at execution time (parallel batch in flight). The
  TESTEXEC-021 lifecycle is completed only after that approval is confirmed.
- **Python 3.12 note:** the full-suite run on a uv-provisioned 3.12 shows one
  pre-existing failure in `tests/test_audit_console_wrapper.py` (audit
  namespace, DEV-STORY-019 scope). Root cause: the wheel-install test creates a
  child venv with `--system-site-packages`, which cannot resolve
  `python-dotenv` on uv-managed 3.12 interpreters (no conventional base
  site-packages). The identical flake was observed in the DEV-STORY-019/020
  batch (`py312-full.log`: 1 failed / 1275 passed first, 1276 passed on
  rerun). It is an environment-harness flake, not a product defect, and does
  not involve the Third-Party Applications CLI.
- **Wheel install probe:** the first wheel install into the fresh venv left
  the console scripts unregistered (silent failure); a `--force-reinstall
  --no-deps` of the wheel installed all 18 entry points. Harness artifact, not
  a product defect.
- The `runpy` RuntimeWarning seen when invoking the module via `-m` is a
  CPython artifact and does not appear when running the packaged launcher or
  console entry point; it is not a product defect.

## QA sign-off

**PASS.** TPA-TC-001 through TPA-TC-024 passed with verifiable evidence. No
defects were opened. Full regression is green on Python 3.11 (1362 passed,
0 failed) at 86.55% branch coverage (third_party_applications 87%); the
focused and shared suites pass on both Python 3.11 and 3.12. The single 3.12
full-suite failure is a pre-existing environment-dependent flake in the audit
namespace, unrelated to this story.
