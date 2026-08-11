# TESTEXEC-020 - Foundry Data Health CLI execution log

Date: 2026-08-10
Story: DEV-STORY-020
Test design: TESTCASE-020 (20 cases DHT-TC-001..020)
Commit under test: `f63a12c` (DEV-019/DEV-020 implementation + CODEREVIEW-019/020 P1 fix: Claude skills and thin launchers)

## Result

**Pass.** All 20 mandatory cases (DHT-TC-001 through DHT-TC-020) passed. The
focused Data Health suite and the full regression suite are green with branch
coverage above the repository gate on Python 3.11 and 3.12. No defects were
opened; no BUG-SUB was created.

## Baseline and environments

| Item | Value |
| --- | --- |
| Commit under test | `f63a12c` (workflow_tuning_checkpoint-01; DEV-019/DEV-020 implementation + CODEREVIEW-019/020 P1 skill/launcher fix) |
| Workspace | Windows; shared working tree with unrelated in-progress changes |
| Python 3.11 (`.venv`) | CPython 3.11.9; `foundry-sdk 1.102.0`; `pytest 9.0.3` |
| Python 3.12 (uv cache) | CPython 3.12.9; `foundry-sdk 1.102.0`; `pytest 9.1.1`; `pytest-asyncio 1.4.0` |
| Transport | Nested async SDK fakes, installed SDK models, installed SDK exceptions |
| External access | No live Foundry requests (offline environment; no credentials available) |

Routine acceptance uses mocked async SDK transport and real installed SDK
exception classes, exactly as the test-case document prescribes. Live access
was neither approved nor required.

> **Environment note:** the shell carries no ambient `FOUNDRY_*` variables.
> With credentials scrubbed, live-style probes produce the documented
> `ConfigurationError` exit `9` (config check precedes client construction).
> This is environment behavior, not a product defect.

## Command evidence

| ID | Exact command/probe | Expected | Actual | Result |
| --- | --- | --- | --- | --- |
| E1 | `.venv\Scripts\python.exe -m foundry_cli.data_health.scripts.foundry_data_health_cli --help` | Help on stdout, exit 0, 6 operations named | Usage naming `check,check-report`; "6 Data Health API v2 operations"; exit 0 | Pass |
| E2 | `... .claude/skills/foundry-data-health/scripts/foundry_data_health_cli.py --help` | Launcher help, exit 0, 6 operations named | Same usage text; exit 0 | Pass |
| E3 | `... check-report get-latest --help` | `--limit` integer flag present; no pagination flags anywhere | `--limit LIMIT` on get-latest only; no `--page-*` flags; exit 0 | Pass |
| E4 | `... .claude/skills/foundry-data-health/scripts/foundry_data_health_cli.py` (no args) | One JSON user-input envelope on stdout, exit 1, no traceback | `{"error": true, "exit_code": 1, "exit_code_name": "UserInputError", "message": "a DataHealth operation is required", ...}`; exit 1 | Pass |
| E5 | `... check create --config-json not-json` | Invalid JSON rejected before client, exit 1, no payload echo | `{"error": true, "exit_code": 1, ... "message": "config must contain valid JSON", ...}`; exit 1; no echo | Pass |
| E6 | `... check-report get-latest ri.data-health.main.check.qa-001 --limit 101` | Out-of-range limit rejected before client, exit 1 (CODEREVIEW-020 P3 fix) | `{"error": true, "exit_code": 1, ... "message": "limit must be between 1 and 100", ...}`; exit 1 | Pass |
| E7 | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true ... check create --config-json '{"type":"stringSet","target":"users"}'` | Write blocked by ACL, exit 8, no client work | `{"error": true, "exit_code": 8, "exit_code_name": "AccessControlError", "message": "Operation blocked: metadata-only mode active", ...}`; exit 8 | Pass |
| E8 | Same with `check replace` | `replace` classified as write, blocked, exit 8 | Same ACL envelope; exit 8 | Pass |
| E9 | Same with `check get` (permitted read) | Permitted read passes ACL, reaches config, exit 9 (no creds) | `ConfigurationError` exit 9; no ACL envelope | Pass |
| E10 | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true FOUNDRY_INCLUDE_TRACEBACK=false ... check create ...` | Traceback suppressed in ACL envelope | `"traceback": ""`; exit 8 | Pass |
| E11 | Catalog probe: `len(OP_SPECS)`, resource set, client paths | Exactly 6 specs (check 4, check-report 2); paths `('Check',)` and `('Check','CheckReport')`; no pagination | DHT OPS 6; res `{'check','check_report'}`; paths `[('Check',), ('Check','CheckReport')]`; exit 0 | Pass |
| E12 | Allow-list parse: `src/foundry_cli/data_health/metadata-allow-list.md` | 6 rows: 3 PERMITTED (get, check_report.get, check_report.get_latest), 3 BLOCKED (create, delete, replace) | Verified; 3/3 | Pass |
| E13 | `python -m pytest -q tests/test_foundry_checkpoints_cli.py tests/test_foundry_data_health_cli.py tests/test_access_control_guard.py` | Focused Checkpoints+DataHealth+ACL suite passes | 131 passed in 0.54 s; exit 0 (3.11); 131 passed in 0.82 s (3.12) | Pass |
| E14 | `python -m pytest -q tests/test_binary_download.py tests/test_pagination_helper.py tests/test_tracing_provider.py tests/unit_test_retry_error_output_log.py` | Shared component suites pass | 207 passed in 0.42 s; exit 0 | Pass |
| E15 | `python -m pytest -q --cov=foundry_cli --cov-branch --cov-report=term` | Full suite with branch coverage >= 80% | 1276 passed in 53.05 s; TOTAL 86.57%; data_health 90%; exit 0 (3.11) | Pass |
| E16 | Same on Python 3.12.9 | Full suite passes on 3.12 | 1276 passed in 64.51 s; TOTAL 86.57%; exit 0 | Pass |
| E17 | `python -m pytest -q tests/test_foundry_data_health_cli.py::test_metadata_only_permits_exactly_3_blocks_3 tests/test_foundry_data_health_cli.py::test_metadata_only_runtime_permits_three_and_blocks_three tests/test_foundry_data_health_cli.py::test_readonly_blocks_three_write_operations` (+ checkpoints peers) | Exact metadata-only/read-only policy tests pass | 6 passed; exit 0 | Pass |
| E18 | `python -m pytest -q tests/test_foundry_checkpoints_cli.py tests/test_foundry_data_health_cli.py tests/test_tracing_provider.py -k "b3 or attribution or tracing or context"` | B3/attribution subset passes | 15 passed; exit 0 | Pass |
| E19 | `python -m pytest -q tests/test_foundry_checkpoints_cli.py tests/test_foundry_data_health_cli.py -k "toon or format or pretty"` | Output format subset passes | 2 passed; exit 0 | Pass |
| E20 | `python -m pytest -q tests/test_checkpoints_console_wrapper.py tests/test_data_health_console_wrapper.py tests/test_foundry_data_health_cli.py::test_console_main_uses_one_asyncio_run_boundary` | Launcher thinness + one asyncio.run boundary | 8 passed + 2 passed; exit 0 | Pass |
| E21 | `python -m ruff check src tests .claude/skills/foundry-checkpoints .claude/skills/foundry-data-health` | Ruff clean | All checks passed; exit 0 | Pass |
| E22 | `python -m mypy src` | Mypy clean | Success: no issues found in 63 source files; exit 0 | Pass |
| E23 | `python -m compileall -q src/foundry_cli/checkpoints src/foundry_cli/data_health .claude/skills/foundry-checkpoints/scripts .claude/skills/foundry-data-health/scripts` | Compile clean | Exit 0 | Pass |
| E24 | `python -m pip check` | Dependencies consistent | No broken requirements found; exit 0 | Pass |
| E25 | `python -m build --wheel --no-isolation` + wheel zip listing | Wheel builds; contains `foundry_cli/data_health/metadata-allow-list.md` | Wheel built exit 0; both allow-lists packaged | Pass |
| E26 | Installed wheel in fresh venv: `foundry-data-health --help` from arbitrary CWD | Launcher works without `PYTHONPATH`, exit 0, 6 operations named | Usage text; exit 0 | Pass |
| E27 | Installed wheel, `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true`, `check create` from arbitrary CWD | Packaged policy blocks write, exit 8 | `AccessControlError` exit 8 (verified on non-truncated invocation) | Pass |
| E28 | `python -c "import tomllib; ... project.scripts"` | Data Health entry point present; prior entries retained | 16 console entries total (14 prior + checkpoints + data-health) | Pass |
| E29 | Launcher source inspection | Launcher is thin (re-exports only, no copied logic) | `from foundry_cli.data_health.scripts.foundry_data_health_cli import (build_parser, console_main, main)`; exit 0 | Pass |
| E30 | Import side-effect probe (subprocess) | Imports produce no output or files | `import foundry_cli.data_health...` printed catalog only; exit 0 | Pass |

## Focused probe results

The focused suite covers the exact 6-operation catalog (check 4, check-report 2,
corrected from the stale 4-operation count), nested dispatch through
`client.data_health.Check` and the nested `Check.CheckReport`, JSON validation
of the `CheckConfig` discriminated union via `--config-json` before client
creation, the check lifecycle (create/get/replace/delete) with replace-class
write classification, the bounded non-cursor `--limit` (1..100) on
`check-report get-latest` with no pagination flags anywhere in the surface, the
3-operation write set (create/delete/replace) read-only classification, the
packaged 3-permitted/3-blocked metadata-only policy, fail-closed behavior,
`include_attribution=False`, B3-only tracing, retry with at-least-once
disclosure for create/replace, ADR-001 error taxonomy, timeout bounds (1..3600),
output formats, NDJSON stderr separation, confidentiality,
import/console/launcher packaging, and wheel/editable regression.

CLI probes added independent runtime evidence: parser error envelopes (no args,
invalid config JSON, out-of-range limit), the write-block ACL envelope with exit
8 for both `check create` and `check replace`, the permitted-read pass through
ACL to the config check (exit 9 with credentials scrubbed), traceback
suppression, the exact catalog/client-path probe, the packaged allow-list
parse, and the installed-wheel arbitrary-CWD launcher and ACL probes.

## Case disposition

| Case | Status | Evidence |
| --- | --- | --- |
| DHT-TC-001 (catalog, parser, help, exact 6 surface, no pagination flags) | Pass | E1, E3, E4, E11 |
| DHT-TC-002 (nested SDK routing through Check and Check.CheckReport) | Pass | E11, E13 |
| DHT-TC-003 (required inputs forwarded, absent optionals omitted) | Pass | E13 |
| DHT-TC-004 (CheckConfig JSON validation before client creation) | Pass | E5, E13 |
| DHT-TC-005 (check lifecycle: create, get, delete, replace) | Pass | E13 |
| DHT-TC-006 (nested check-report dispatch and bounded --limit) | Pass | E3, E6, E13 |
| DHT-TC-007 (timeout boundaries and forwarding) | Pass | E13 |
| DHT-TC-008 (ACL precedence: global, namespace, operation scopes) | Pass | E7, E13, E17 |
| DHT-TC-009 (read-only blocks 3-op write set; reads stay permitted) | Pass | E13, E17 |
| DHT-TC-010 (metadata-only tier: exact 3 permitted / 3 blocked) | Pass | E12, E17 |
| DHT-TC-011 (packaged policy fail closed, CWD independent) | Pass | E12, E25, E26, E27 |
| DHT-TC-012 (include_attribution=False on client and scope) | Pass | E18 |
| DHT-TC-013 (B3 enabled at outbound transport) | Pass | E14, E18 |
| DHT-TC-014 (B3 disabled, retry stability, context restoration) | Pass | E14, E18 |
| DHT-TC-015 (retry behavior, at-least-once disclosure) | Pass | E14 |
| DHT-TC-016 (ADR-001 error taxonomy and structured envelopes) | Pass | E4, E5, E6, E7, E9, E10 |
| DHT-TC-017 (output formats: JSON, TOON, auto, pretty) | Pass | E19 |
| DHT-TC-018 (NDJSON stderr, stream separation, confidentiality) | Pass | E5, E14 |
| DHT-TC-019 (import, console, help, thin launcher) | Pass | E1, E2, E20, E23, E29, E30 |
| DHT-TC-020 (wheel, editable, entry points, regression) | Pass | E13, E15, E16, E21, E22, E23, E24, E25, E26, E28 |

All 20 cases passed. Every story acceptance criterion has at least one passing
case, and the repository branch-coverage gate (80%) is met on both supported
Python versions.

## Notes

- **CODEREVIEW-020 P1 fix verified (f63a12c):** the previously missing
  `.claude/skills/foundry-data-health/` skill and thin launcher are now
  committed. DHT-TC-019/020 are therefore unconditional and both passed: the
  launcher re-exports `build_parser`, `console_main`, `main` and contains no
  copied catalog or ACL logic (E29).
- **CODEREVIEW-020 P3 fix verified:** the `--limit` flag is locally validated
  (1..100) before client work; `--limit 101` is rejected with a user-input
  envelope and exit 1 (E6), matching the P3 corrective action.
- **Environment note:** with credentials scrubbed, live-style probes produce
  the documented ConfigurationError exit 9 (config check precedes client
  construction). This is environment behavior, not a product defect. No live
  Foundry request was made.
- **Python 3.12 harness:** the first 3.12 focused run failed collection on
  missing `pytest-asyncio`; after installing the plugin into the 3.12 userbase
  the focused and full suites both pass (131 / 1276). This is a test-harness
  gap, not a product defect.
- The `runpy` RuntimeWarning seen when invoking the module via `-m` is a
  CPython artifact and does not appear when running the packaged launcher or
  console entry point; it is not a product defect.

## QA sign-off

**PASS.** DHT-TC-001 through DHT-TC-020 passed with verifiable evidence. No
defects were opened. Full regression is green on Python 3.11 and 3.12
(1276 passed each) with 86.57% branch coverage (data_health 90%), above the 80%
gate.
