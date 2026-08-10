# TESTEXEC-013 - Foundry Models CLI execution log

Date: 2026-08-10
Story: DEV-STORY-013
Test design: TESTCASE-013
Commit under test: `bd13955`
Environment: Windows; CPython 3.11.9; `foundry-sdk 1.101.0`; `pytest 9.0.3`; venv `.venv`

## Result

**Pass.** All 28 mandatory cases (MDL-TC-001 through MDL-TC-028) passed. The
focused Models suite and the full regression suite are green with branch
coverage above the repository gate. No defects were opened.

## Baseline and environments

| Item | Value |
| --- | --- |
| Commit under test | `bd13955` (DEV-013/DEV-014 implementation) |
| Workspace | Windows; shared working tree with unrelated in-progress changes |
| Python 3.11 | CPython 3.11.9; `foundry-sdk 1.101.0`; `pytest 9.0.3` |
| Transport | Nested async SDK fakes, installed SDK models, installed SDK exceptions |
| External access | No credentials, no live Foundry requests |

Routine acceptance uses mocked async SDK transport and real installed SDK
exception classes, exactly as the test-case document prescribes. Live access
was neither approved nor required.

## Command evidence

| ID | Exact command/probe | Expected | Actual | Result |
| --- | --- | --- | --- | --- |
| E1 | `.venv\Scripts\python.exe -m pytest -q tests/test_foundry_models_cli.py` | Focused Models suite passes | 33 passed in 0.98 s; exit 0 | Pass |
| E2 | `python -m foundry_cli.models.scripts.foundry_models_cli --help` | Help on stdout, exit 0, 23 operations named | Usage with 10 resource groups and 23 operations; exit 0 | Pass |
| E3 | `python .claude/skills/foundry-models/scripts/foundry_models_cli.py --help` | Thin launcher help, exit 0 | Same help; exit 0 | Pass |
| E4 | `python .claude/skills/foundry-models/scripts/foundry_models_cli.py` (no args) | One JSON user-input envelope on stdout, exit 1, no traceback | `{"error": true, "exit_code": 1, "exit_code_name": "UserInputError", "message": "a Models operation is required", ...}` on stdout; exit 1 | Pass |
| E5 | `... live-deployment transform-json ri.models.main.live-deployment.test --input-json not-json` | Invalid JSON rejected before client, exit 1, no payload echo | `{"error": true, "exit_code": 1, ... "message": "input must contain valid JSON", ...}`; exit 1; no echo | Pass |
| E6 | `... bogus-op` | Unknown operation rejected, exit 1 | `{"error": true, "exit_code": 1, ... "message": "Invalid command input", ...}`; exit 1 | Pass |
| E7 | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=1 ... model create --name test-model --parent-folder-rid ri.compass.main.folder.test` | ACL denial envelope, exit 8, no client work | `{"error": true, "exit_code": 8, "exit_code_name": "AccessControlError", ...}`; exit 8 | Pass |
| E8 | `FOUNDRY_INCLUDE_TRACEBACK=false` + E7 | Traceback suppressed in envelope | `"traceback": ""` in envelope; exit 8 | Pass |
| E9 | `... model get ri.models.main.model.test --timeout 0` | Invalid timeout rejected before ACL/client, exit 1 | `{"error": true, "exit_code": 1, ... "message": "timeout must be between 1 and 3600 seconds", ...}`; exit 1 | Pass |
| E10 | `python -m pytest -q tests/test_foundry_models_cli.py tests/test_foundry_orchestration_cli.py tests/test_access_control_guard.py` | Focused Models+Orchestration+ACL suite passes | 137 passed in 1.60 s; exit 0 | Pass |
| E11 | `python -m pytest -q tests/test_pagination_helper.py tests/test_binary_download.py tests/test_tracing_provider.py` | Shared component suites pass | 58 passed in 0.30 s; exit 0 | Pass |
| E12 | `python -m pytest -q` | Full regression passes | 1089 passed in 32.30 s; exit 0 | Pass |
| E13 | `python -m pytest -q --cov=foundry_cli --cov-branch --cov-report=term --cov-fail-under=80` | Full suite with branch coverage >= 80% | 1089 passed in 43.49 s; TOTAL 85.50%; Models module 89% branch; exit 0 | Pass |
| E14 | `python -m ruff check src tests .claude/skills/foundry-models .claude/skills/foundry-orchestration` | Ruff clean | All checks passed; exit 0 | Pass |
| E15 | `python -m mypy src` | Mypy clean | Success: no issues found in 45 source files; exit 0 | Pass |
| E16 | `python -m compileall -q src/foundry_cli/models src/foundry_cli/orchestration .claude/skills/foundry-models/scripts .claude/skills/foundry-orchestration/scripts` | Compile clean | Exit 0 | Pass |
| E17 | `python -m build --wheel --no-isolation --outdir _wheelhouse .` | Local wheel builds | `foundry_cli-0.1.0-py3-none-any.whl` built; exit 0 | Pass |
| E18 | Wheel archive inspection | Models allow-list and entry points present; prior entries retained | `foundry_cli/models/metadata-allow-list.md` present; `foundry-models` and `foundry-orchestration` entry points present; 10 console entries total (8 prior + 2 new) | Pass |
| E19 | `python -m pip check` | Dependencies consistent | No broken requirements found; exit 0 | Pass |

## Focused probe results

The focused suite covers the exact 23-operation catalog, nested routing across
the ten client paths, JSON argument validation, exactly four cursor-paged
commands with the 40-page cap, service slicing for series/artifact JSON, the
three streamed downloads with atomic persistence and unsafe-name rejection,
ACL precedence and the 7-operation write set, the 12/11 metadata-only policy,
fail-closed behavior, attribution suppression, B3-only tracing, retry, ADR-001
error taxonomy, timeout bounds, output formats, NDJSON stderr separation,
confidentiality, import/console/launcher packaging, and wheel/editable
regression.

CLI probes added independent runtime evidence: parser error envelopes, invalid
JSON and timeout rejection before client or ACL work, ACL denial with exit 8,
traceback suppression via `FOUNDRY_INCLUDE_TRACEBACK=false`, and the launcher
help surfaces.

## Case disposition

| Case | Status | Evidence |
| --- | --- | --- |
| MDL-TC-001 (catalog, parser, help, 23 surface) | Pass | E1, E2, E4, E6 |
| MDL-TC-002 (nested SDK routing) | Pass | E1, E10 |
| MDL-TC-003 (required inputs, absent optionals omitted) | Pass | E1 |
| MDL-TC-004 (JSON validation before client) | Pass | E1, E5 |
| MDL-TC-005 (exactly four paged commands) | Pass | E1, E10 |
| MDL-TC-006 (exact-page batch, EOF, 40-page cap) | Pass | E1, E11 |
| MDL-TC-007 (pagination retry resets cursor state) | Pass | E1, E11 |
| MDL-TC-008 (service slicing, no PaginationHelper) | Pass | E1 |
| MDL-TC-009 (trainer list no pagination flags) | Pass | E1 |
| MDL-TC-010 (download below byte limit) | Pass | E1, E11 |
| MDL-TC-011 (download above limit, one probe byte) | Pass | E1, E11 |
| MDL-TC-012 (download failure/cancel clean atomically) | Pass | E1, E11 |
| MDL-TC-013 (unsafe output names rejected) | Pass | E1 |
| MDL-TC-014 (ACL precedence) | Pass | E1, E10 |
| MDL-TC-015 (read-only blocks 7-op write set) | Pass | E1, E10 |
| MDL-TC-016 (launch/promote keep write classification) | Pass | E1, E10 |
| MDL-TC-017 (metadata-only 12/11) | Pass | E1, E7, E10 |
| MDL-TC-018 (fail closed, CWD independent) | Pass | E1, E18 |
| MDL-TC-019 (include_attribution=False) | Pass | E1, E10 |
| MDL-TC-020 (B3 at outbound transport) | Pass | E1, E11 |
| MDL-TC-021 (B3 disabled, retry stability, restore) | Pass | E1, E11 |
| MDL-TC-022 (retry behavior, at-least-once) | Pass | E1, E11 |
| MDL-TC-023 (ADR-001 taxonomy) | Pass | E1, E4, E5, E7, E9 |
| MDL-TC-024 (timeout bounds and forwarding) | Pass | E1, E9 |
| MDL-TC-025 (output formats) | Pass | E1, E10 |
| MDL-TC-026 (NDJSON stderr, confidentiality) | Pass | E1, E8 |
| MDL-TC-027 (import, console, help, thin launcher) | Pass | E2, E3, E16 |
| MDL-TC-028 (wheel, editable, entry points, regression) | Pass | E12, E13, E14, E15, E17, E18, E19 |

All 28 cases passed. Every one of the 15 story acceptance criteria has at least
one passing case, and the repository branch-coverage gate (80%) is met.

## Notes

- The `runpy` RuntimeWarning seen when invoking the module via `-m` is a
  CPython artifact and does not appear when running the packaged launcher or
  console entry point; it is not a product defect.
- `FOUNDRY_INCLUDE_TRACEBACK` defaults to true and is documented in
  `.env.example`; setting it to `false` yields an empty `traceback` field in
  error envelopes. This is the designed confidentiality control, not a defect.
- Requests emitted warnings about globally installed `urllib3` and character
  detection packages, and pytest-asyncio warned about its default fixture loop
  scope. Both are environment-level and did not affect results.

## QA sign-off

**PASS.** MDL-TC-001 through MDL-TC-028 passed with verifiable evidence. No
defects were opened. Full regression is green (1089 passed) with 85.50% branch
coverage, above the 80% gate. All 15 story acceptance criteria have passing
coverage.
