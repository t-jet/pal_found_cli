# TESTEXEC-014 - Foundry Orchestration CLI execution log

Date: 2026-08-10
Story: DEV-STORY-014
Test design: TESTCASE-014
Commit under test: `bd13955`
Environment: Windows; CPython 3.11.9; `foundry-sdk 1.101.0`; `pytest 9.0.3`; venv `.venv`

## Result

**Pass.** All 23 mandatory cases (ORC-TC-001 through ORC-TC-023) passed. The
focused Orchestration suite and the full regression suite are green with branch
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
| E1 | `.venv\Scripts\python.exe -m pytest -q tests/test_foundry_orchestration_cli.py` | Focused Orchestration suite passes | 32 passed in 0.70 s; exit 0 | Pass |
| E2 | `python -m foundry_cli.orchestration.scripts.foundry_orchestration_cli --help` | Help on stdout, exit 0, 20 operations named | Usage with 4 client groups and 20 operations; exit 0 | Pass |
| E3 | `python .claude/skills/foundry-orchestration/scripts/foundry_orchestration_cli.py --help` | Thin launcher help, exit 0 | Same help; exit 0 | Pass |
| E4 | `python .claude/skills/foundry-orchestration/scripts/foundry_orchestration_cli.py` (no args) | One JSON user-input envelope on stdout, exit 1, no traceback | `{"error": true, "exit_code": 1, "exit_code_name": "UserInputError", "message": "an Orchestration operation is required", ...}` on stdout; exit 1 | Pass |
| E5 | `... build get-batch --build-rids-json not-json` | Invalid JSON rejected before client, exit 1, no payload echo | `{"error": true, "exit_code": 1, ... "message": "build_rids must contain valid JSON", ...}`; exit 1; no echo | Pass |
| E6 | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=1 ... build create --target-json '{"type":"upstream","datasetRids":["ri.foundry.main.dataset.test"]}' --fallback-branches-json '["master"]'` | ACL denial envelope, exit 8, no client work | `{"error": true, "exit_code": 8, "exit_code_name": "AccessControlError", ...}`; exit 8 | Pass |
| E7 | `... build search --where-json '{}' --timeout 3601` | Invalid timeout rejected before ACL/client, exit 1 | `{"error": true, "exit_code": 1, ... "message": "timeout must be between 1 and 3600 seconds", ...}`; exit 1 | Pass |
| E8 | `... build search --where-json '{}'` (no credentials) | Config failure before any SDK work | `{"error": true, "exit_code": 9, "exit_code_name": "ConfigurationError", "message": "Missing FOUNDRY_TOKEN and/or FOUNDRY_HOSTNAME...", ...}`; exit 9 | Pass |
| E9 | `FOUNDRY_TOKEN=x FOUNDRY_HOSTNAME=example.com ... build search` (no --where-json) | Known design note: optional `where` vs SDK-required; fails gracefully | `{"error": true, "exit_code": 1, ... "exception_type": "ValidationError", ...}`; exit 1; no traceback | Pass |
| E10 | `python -m pytest -q tests/test_foundry_models_cli.py tests/test_foundry_orchestration_cli.py tests/test_access_control_guard.py` | Focused Models+Orchestration+ACL suite passes | 137 passed in 1.60 s; exit 0 | Pass |
| E11 | `python -m pytest -q tests/test_pagination_helper.py tests/test_binary_download.py tests/test_tracing_provider.py` | Shared component suites pass | 58 passed in 0.30 s; exit 0 | Pass |
| E12 | `python -m pytest -q` | Full regression passes | 1089 passed in 32.30 s; exit 0 | Pass |
| E13 | `python -m pytest -q --cov=foundry_cli --cov-branch --cov-report=term --cov-fail-under=80` | Full suite with branch coverage >= 80% | 1089 passed in 43.49 s; TOTAL 85.50%; Orchestration module 91% branch; exit 0 | Pass |
| E14 | `python -m ruff check src tests .claude/skills/foundry-models .claude/skills/foundry-orchestration` | Ruff clean | All checks passed; exit 0 | Pass |
| E15 | `python -m mypy src` | Mypy clean | Success: no issues found in 45 source files; exit 0 | Pass |
| E16 | `python -m compileall -q src/foundry_cli/models src/foundry_cli/orchestration .claude/skills/foundry-models/scripts .claude/skills/foundry-orchestration/scripts` | Compile clean | Exit 0 | Pass |
| E17 | `python -m build --wheel --no-isolation --outdir _wheelhouse .` | Local wheel builds | `foundry_cli-0.1.0-py3-none-any.whl` built; exit 0 | Pass |
| E18 | Wheel archive inspection | Orchestration allow-list and entry points present; prior entries retained | `foundry_cli/orchestration/metadata-allow-list.md` present; `foundry-models` and `foundry-orchestration` entry points present; 10 console entries total (8 prior + 2 new) | Pass |
| E19 | `python -m pip check` | Dependencies consistent | No broken requirements found; exit 0 | Pass |

## Focused probe results

The focused suite covers the exact 20-operation catalog with ScheduleRun absent,
nested routing across the four client paths, JSON argument validation, exactly
three cursor-paged commands with the 40-page cap, single-call batch and search
behavior, ACL precedence and the 8-operation write set, semantic reads
(`build search`, `schedule get-affected-resources`) under read-only and
metadata-only modes, the 12/8 metadata-only policy, fail-closed behavior,
attribution suppression, B3-only tracing, retry, ADR-001 error taxonomy,
timeout bounds, output formats, NDJSON stderr separation, confidentiality,
import/console/launcher packaging, and wheel/editable regression.

CLI probes added independent runtime evidence: parser error envelopes, invalid
JSON and timeout rejection before ACL or client work, ACL denial with exit 8,
config failure with exit 9, and the graceful ValidationError exit 1 when the
design-mandated optional `build search --where-json` is omitted (known
non-blocking design note from CODEREVIEW-014).

## Case disposition

| Case | Status | Evidence |
| --- | --- | --- |
| ORC-TC-001 (catalog, parser, help, exact 20 surface) | Pass | E1, E2, E4 |
| ORC-TC-002 (nested SDK routing, ScheduleRun absent) | Pass | E1, E10 |
| ORC-TC-003 (required inputs, absent optionals omitted) | Pass | E1 |
| ORC-TC-004 (JSON validation before client) | Pass | E1, E5 |
| ORC-TC-005 (exactly three paged commands) | Pass | E1, E10 |
| ORC-TC-006 (exact-page batch, EOF, 40-page cap) | Pass | E1, E11 |
| ORC-TC-007 (pagination retry resets cursor state) | Pass | E1, E11 |
| ORC-TC-008 (batch and search single-call) | Pass | E1, E10 |
| ORC-TC-009 (ACL precedence) | Pass | E1, E10 |
| ORC-TC-010 (read-only blocks 8-op write set) | Pass | E1, E10 |
| ORC-TC-011 (semantic reads despite POST) | Pass | E1, E10 |
| ORC-TC-012 (metadata-only 12/8) | Pass | E1, E6, E10 |
| ORC-TC-013 (fail closed, CWD independent) | Pass | E1, E18 |
| ORC-TC-014 (include_attribution=False) | Pass | E1, E10 |
| ORC-TC-015 (B3 at outbound transport) | Pass | E1, E11 |
| ORC-TC-016 (B3 disabled, retry stability, restore) | Pass | E1, E11 |
| ORC-TC-017 (retry behavior, at-least-once) | Pass | E1, E11 |
| ORC-TC-018 (ADR-001 taxonomy) | Pass | E1, E4, E5, E6, E8, E9 |
| ORC-TC-019 (timeout bounds and forwarding) | Pass | E1, E7 |
| ORC-TC-020 (output formats) | Pass | E1, E10 |
| ORC-TC-021 (NDJSON stderr, confidentiality) | Pass | E1 |
| ORC-TC-022 (import, console, help, thin launcher) | Pass | E2, E3, E16 |
| ORC-TC-023 (wheel, editable, entry points, regression) | Pass | E12, E13, E14, E15, E17, E18, E19 |

All 23 cases passed. Every story acceptance criterion and the ticket's explicit
coverage list (build 6, job 2, schedule 10, schedule_version 2, schedule_run 0)
has at least one passing case, and the repository branch-coverage gate (80%) is
met.

## Notes

- The `runpy` RuntimeWarning seen when invoking the module via `-m` is a
  CPython artifact and does not appear when running the packaged launcher or
  console entry point; it is not a product defect.
- `build search` declares `--where-json` as optional while the SDK marks
  `where` required. This is a design-originated discrepancy already recorded as
  a non-blocking finding in CODEREVIEW-014. The runtime fails gracefully with a
  structured envelope and exit 1, so no defect ticket is warranted.
- Requests emitted warnings about globally installed `urllib3` and character
  detection packages, and pytest-asyncio warned about its default fixture loop
  scope. Both are environment-level and did not affect results.

## QA sign-off

**PASS.** ORC-TC-001 through ORC-TC-023 passed with verifiable evidence. No
defects were opened. Full regression is green (1089 passed) with 85.50% branch
coverage, above the 80% gate. All 20 story operations have passing coverage.
