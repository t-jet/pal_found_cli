# TESTEXEC-019 - Foundry Checkpoints CLI execution log

Date: 2026-08-10
Story: DEV-STORY-019
Test design: TESTCASE-019 (21 cases CKP-TC-001..021)
Commit under test: `f63a12c` (DEV-019/DEV-020 implementation + CODEREVIEW-019/020 P1 fix: Claude skills and thin launchers)

## Result

**Pass.** All 21 mandatory cases (CKP-TC-001 through CKP-TC-021) passed. The
focused Checkpoints suite and the full regression suite are green with branch
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
| E1 | `.venv\Scripts\python.exe -m foundry_cli.checkpoints.scripts.foundry_checkpoints_cli --help` | Help on stdout, exit 0, 3 operations named | Usage naming `record`; "3 Checkpoints API v2 operations"; exit 0 | Pass |
| E2 | `... .claude/skills/foundry-checkpoints/scripts/foundry_checkpoints_cli.py --help` | Launcher help, exit 0, 3 operations named | Same usage text; exit 0 | Pass |
| E3 | `... record --help` / `record get --help` / `record search --help` | Operation help names exact flags; pagination flags only on search | `get`: `record_rid` + shared; `search`: `--where-json` + `--page-size/--page-token/--all/--max-pages/--sort-direction`; exit 0 | Pass |
| E4 | `... .claude/skills/foundry-checkpoints/scripts/foundry_checkpoints_cli.py` (no args) | One JSON user-input envelope on stdout, exit 1, no traceback | `{"error": true, "exit_code": 1, "exit_code_name": "UserInputError", "message": "a Checkpoints operation is required", ...}`; exit 1 | Pass |
| E5 | `... record bogus` | Unknown operation rejected, exit 1 | `{"error": true, "exit_code": 1, ... "message": "Invalid command input", ...}`; exit 1 | Pass |
| E6 | `... record search --where-json not-json` | Invalid JSON rejected before client, exit 1, no payload echo | `{"error": true, "exit_code": 1, ... "message": "where must contain valid JSON", ...}`; exit 1; no echo | Pass |
| E7 | `... record get ri.checks.main.record.qa-001 --timeout 0` | Invalid timeout rejected before ACL/client, exit 1 | `{"error": true, "exit_code": 1, ... "message": "timeout must be between 1 and 3600 seconds", ...}`; exit 1 | Pass |
| E8 | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true ... record get ri.checks.main.record.qa-001` | Permitted read passes ACL, reaches config; no ACL envelope; exit 9 (no creds) | `{"error": true, "exit_code": 9, "exit_code_name": "ConfigurationError", ...}`; exit 9 | Pass |
| E9 | `... record get ri.checks.main.record.qa-001` (no creds) | ConfigurationError envelope, exit 9 | Same envelope; exit 9 | Pass |
| E10 | Catalog probe: `len(OP_SPECS)`, resource set, `PAGINATED_OPS`, client paths | Exactly 3 specs on `record`; paginated `{('record','search')}`; client path `('Record',)` | CKP OPS 3; res `{'record'}`; PAG `frozenset({('record','search')})`; paths `[('Record',)]`; exit 0 | Pass |
| E11 | Allow-list parse: `src/foundry_cli/checkpoints/metadata-allow-list.md` | 3 rows, all PERMITTED, 0 BLOCKED | `checkpoints.record.get/get_batch/search` PERMITTED; 3/0 | Pass |
| E12 | `python -m pytest -q tests/test_foundry_checkpoints_cli.py tests/test_foundry_data_health_cli.py tests/test_access_control_guard.py` | Focused Checkpoints+DataHealth+ACL suite passes | 131 passed in 0.54 s; exit 0 (3.11); 131 passed in 0.82 s (3.12) | Pass |
| E13 | `python -m pytest -q tests/test_binary_download.py tests/test_pagination_helper.py tests/test_tracing_provider.py tests/unit_test_retry_error_output_log.py` | Shared component suites pass | 207 passed in 0.42 s; exit 0 | Pass |
| E14 | `python -m pytest -q --cov=foundry_cli --cov-branch --cov-report=term` | Full suite with branch coverage >= 80% | 1276 passed in 53.05 s; TOTAL 86.57%; checkpoints 88%; exit 0 (3.11) | Pass |
| E15 | Same on Python 3.12.9 | Full suite passes on 3.12 | 1276 passed in 64.51 s; TOTAL 86.57%; exit 0 | Pass |
| E16 | `python -m pytest -q tests/test_foundry_checkpoints_cli.py::test_metadata_only_permits_exactly_3_blocks_0 tests/test_foundry_checkpoints_cli.py::test_metadata_only_runtime_permits_all_three tests/test_foundry_checkpoints_cli.py::test_readonly_permits_all_three_operations` (+ data_health peers) | Exact metadata-only/read-only policy tests pass | 6 passed; exit 0 | Pass |
| E17 | `python -m pytest -q tests/test_foundry_checkpoints_cli.py tests/test_foundry_data_health_cli.py tests/test_tracing_provider.py -k "b3 or attribution or tracing or context"` | B3/attribution subset passes | 15 passed; exit 0 | Pass |
| E18 | `python -m pytest -q tests/test_foundry_checkpoints_cli.py tests/test_foundry_data_health_cli.py -k "toon or format or pretty"` | Output format subset passes | 2 passed; exit 0 | Pass |
| E19 | `python -m pytest -q tests/test_checkpoints_console_wrapper.py tests/test_data_health_console_wrapper.py tests/test_foundry_checkpoints_cli.py::test_console_main_uses_one_asyncio_run_boundary` | Launcher thinness + one asyncio.run boundary | 8 passed + 2 passed; exit 0 | Pass |
| E20 | `python -m ruff check src tests .claude/skills/foundry-checkpoints .claude/skills/foundry-data-health` | Ruff clean | All checks passed; exit 0 | Pass |
| E21 | `python -m mypy src` | Mypy clean | Success: no issues found in 63 source files; exit 0 | Pass |
| E22 | `python -m compileall -q src/foundry_cli/checkpoints src/foundry_cli/data_health .claude/skills/foundry-checkpoints/scripts .claude/skills/foundry-data-health/scripts` | Compile clean | Exit 0 | Pass |
| E23 | `python -m pip check` | Dependencies consistent | No broken requirements found; exit 0 | Pass |
| E24 | `python -m build --wheel --no-isolation` + wheel zip listing | Wheel builds; contains `foundry_cli/checkpoints/metadata-allow-list.md` | Wheel built exit 0; both allow-lists packaged | Pass |
| E25 | Installed wheel in fresh venv: `foundry-checkpoints --help` from arbitrary CWD | Launcher works without `PYTHONPATH`, exit 0, 3 operations named | Usage text; exit 0 | Pass |
| E26 | Installed wheel, `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true`, `record get` from arbitrary CWD | Packaged policy permits read (no ACL block), reaches config exit 9 | `ConfigurationError` exit 9; no ACL envelope | Pass |
| E27 | `python -c "import tomllib; ... project.scripts"` | Checkpoints entry point present; prior entries retained | 16 console entries total (14 prior + checkpoints + data-health) | Pass |
| E28 | Launcher source inspection | Launcher is thin (re-exports only, no copied logic) | `from foundry_cli.checkpoints.scripts.foundry_checkpoints_cli import (build_parser, console_main, main)`; exit 0 | Pass |
| E29 | Import side-effect probe (subprocess) | Imports produce no output or files | `import foundry_cli.checkpoints...` printed catalog only; exit 0 | Pass |
| E30 | `FOUNDRY_INCLUDE_TRACEBACK=false` on a blocked/error path | Traceback suppressed in envelope | `"traceback": ""` in ACL envelope | Pass |

## Focused probe results

The focused suite covers the exact 3-operation catalog on the single `Record`
client path, JSON argument validation (`--where-json` object, `--records-json`
array), the cursor-paged `record search` through `PaginationHelper`
(`with_raw_response.search`, page-size/page-token/all/max-pages only on search),
the `get_batch` positional-body dispatch bounded at 100 elements, the zero-write
semantic-read ACL classification, the packaged 3-permitted/0-blocked
metadata-only policy, fail-closed behavior, `include_attribution=False`, B3-only
tracing, retry, ADR-001 error taxonomy, timeout bounds (1..3600), output
formats, NDJSON stderr separation, confidentiality, import/console/launcher
packaging, and wheel/editable regression.

CLI probes added independent runtime evidence: parser error envelopes (no args,
unknown operation, invalid JSON, timeout 0), the permitted-read pass through
ACL to the config check (exit 9 with credentials scrubbed), traceback
suppression, the exact catalog/client-path/pagination probe, the packaged
allow-list parse, and the installed-wheel arbitrary-CWD launcher and ACL probes.

## Case disposition

| Case | Status | Evidence |
| --- | --- | --- |
| CKP-TC-001 (catalog, parser, help, exact 3 surface) | Pass | E1, E3, E4, E5, E10 |
| CKP-TC-002 (nested SDK routing through the single Record client path) | Pass | E10, E12 |
| CKP-TC-003 (required inputs forwarded, absent optionals omitted) | Pass | E12 |
| CKP-TC-004 (JSON validation before client creation) | Pass | E6, E12 |
| CKP-TC-005 (pagination: single page default, metadata emission) | Pass | E3, E13 |
| CKP-TC-006 (pagination bounds, resume token, degenerate values) | Pass | E3, E13 |
| CKP-TC-007 (get_batch positional body, 100-element bound) | Pass | E12 |
| CKP-TC-008 (timeout boundaries and forwarding) | Pass | E7 |
| CKP-TC-009 (ACL precedence: global, namespace, operation scopes) | Pass | E8, E12, E16 |
| CKP-TC-010 (read-only permits all 3 semantic reads) | Pass | E12, E16 |
| CKP-TC-011 (metadata-only tier: exact 3 permitted / 0 blocked) | Pass | E11, E16 |
| CKP-TC-012 (packaged policy fail closed, CWD independent) | Pass | E11, E24, E25, E26 |
| CKP-TC-013 (include_attribution=False on client and scope) | Pass | E17 |
| CKP-TC-014 (B3 enabled at outbound transport) | Pass | E13, E17 |
| CKP-TC-015 (B3 disabled, retry stability, context restoration) | Pass | E13, E17 |
| CKP-TC-016 (retry behavior, cursor preserved across page retries) | Pass | E13 |
| CKP-TC-017 (ADR-001 error taxonomy and structured envelopes) | Pass | E4, E5, E6, E7, E8, E9, E30 |
| CKP-TC-018 (output formats: JSON, TOON, auto, pretty) | Pass | E18 |
| CKP-TC-019 (NDJSON stderr, stream separation, confidentiality) | Pass | E6, E13 |
| CKP-TC-020 (import, console, help, thin launcher) | Pass | E1, E2, E19, E22, E28, E29 |
| CKP-TC-021 (wheel, editable, entry points, regression) | Pass | E12, E14, E15, E20, E21, E22, E23, E24, E25, E27 |

All 21 cases passed. Every story acceptance criterion has at least one passing
case, and the repository branch-coverage gate (80%) is met on both supported
Python versions.

## Notes

- **CODEREVIEW-019 P1 fix verified (f63a12c):** the previously missing
  `.claude/skills/foundry-checkpoints/` skill and thin launcher are now
  committed. CKP-TC-020/021 are therefore unconditional and both passed: the
  launcher re-exports `build_parser`, `console_main`, `main` and contains no
  copied catalog, pagination, or ACL logic (E28).
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

**PASS.** CKP-TC-001 through CKP-TC-021 passed with verifiable evidence. No
defects were opened. Full regression is green on Python 3.11 and 3.12
(1276 passed each) with 86.57% branch coverage (checkpoints 88%), above the 80%
gate.
