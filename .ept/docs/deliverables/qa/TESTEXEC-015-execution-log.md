# TESTEXEC-015 - Foundry SQL Queries CLI execution log

Date: 2026-08-10
Story: DEV-STORY-015
Test design: TESTCASE-015
Commit under test: `0c88063`
Environment: Windows; CPython 3.11.9; `foundry-sdk 1.102.0`; venv `.venv`

## Result

**Pass.** All 22 mandatory cases (SQL-TC-001 through SQL-TC-022) passed. The
focused SQL Queries suite and the full regression suite are green with branch
coverage above the repository gate. No defects were opened.

## Baseline and environments

| Item | Value |
| --- | --- |
| Commit under test | `0c88063` (DEV-015/DEV-016 implementation) |
| Workspace | Windows; shared working tree with unrelated in-progress changes |
| Python 3.11 | CPython 3.11.9; `foundry-sdk 1.102.0` |
| Transport | Nested async SDK fakes, installed SDK models, installed SDK exceptions |
| External access | No credentials, no live Foundry requests |

Routine acceptance uses mocked async SDK transport and real installed SDK
exception classes, exactly as the test-case document prescribes. Live access
was neither approved nor required.

> **Environment note:** the shell environment carries ambient test credentials
> (`FOUNDRY_TOKEN=dummy`, `FOUNDRY_HOSTNAME=example.palantirfoundry.com`,
> `FOUNDRY_INCLUDE_TRACEBACK=false`); no `.env` file exists. With credentials
> present the client is constructed and a network attempt yields
> `ConnectionError` retries ending in exit `6`; with credentials scrubbed the
> documented `ConfigurationError` exit `9` is produced. This is environment
> leakage, not a product defect, and is not used as case evidence where exit `9`
> is the expected outcome.

## Command evidence

| ID | Exact command/probe | Expected | Actual | Result |
| --- | --- | --- | --- | --- |
| E1 | `.venv\Scripts\python.exe -m pytest -q tests/test_foundry_sql_queries_cli.py tests/test_foundry_streams_cli.py` | Focused SQL+Streams suite passes | 57 passed in 0.80 s; exit 0 | Pass |
| E2 | `python -m foundry_cli.sql_queries.scripts.foundry_sql_queries_cli --help` | Help on stdout, exit 0, 5 operations named | Usage naming `query`; exit 0 | Pass |
| E3 | `python .claude/skills/foundry-sql-queries/scripts/foundry_sql_queries_cli.py --help` | Thin launcher help, exit 0 | Same help; exit 0 | Pass |
| E4 | `... foundry_sql_queries_cli.py` (no args) | One JSON user-input envelope on stdout, exit 1, no traceback | `{"error": true, "exit_code": 1, "exit_code_name": "UserInputError", ...}` on stdout; exit 1 | Pass |
| E5 | `... query execute --query "SELECT 1" --fallback-branch-ids-json not-json` | Invalid JSON rejected before client, exit 1, no payload echo | `{"error": true, "exit_code": 1, ...}`; exit 1; no echo | Pass |
| E6 | `... bogus-op` | Unknown operation rejected, exit 1 | `{"error": true, "exit_code": 1, ... "message": "Invalid command input", ...}`; exit 1 | Pass |
| E7 | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=1 ... query cancel ri.sqlqueries.main.query.test` | ACL denial envelope, exit 8, no client work | `{"error": true, "exit_code": 8, "exit_code_name": "AccessControlError", ...}`; exit 8 | Pass |
| E8 | `... query get-status ri.sqlqueries.main.query.test --timeout 0` | Invalid timeout rejected before ACL/client, exit 1 | `{"error": true, "exit_code": 1, ...}`; exit 1 | Pass |
| E9 | Credentials scrubbed; `... query get-status ri.sqlqueries.main.query.test` | ConfigurationError envelope, exit 9 | `{"error": true, "exit_code": 9, "exit_code_name": "ConfigurationError", "message": "Missing FOUNDRY_TOKEN and/or FOUNDRY_HOSTNAME...", ...}`; exit 9 | Pass |
| E10 | `python -m pytest -q tests/test_access_control_guard.py tests/test_foundry_sql_queries_cli.py tests/test_foundry_streams_cli.py` | ACL+focused suite passes | 131 passed in 0.84 s; exit 0 | Pass |
| E11 | `python -m pytest -q tests/test_binary_download.py tests/test_pagination_helper.py tests/test_tracing_provider.py` | Shared component suites pass | 58 passed in 0.30 s; exit 0 | Pass |
| E12 | `python -m pytest -q tests/test_foundry_sql_queries_cli.py -k "download or binary or atomic or unsafe or arrow"` | Binary download subset passes | 4 passed; exit 0 | Pass |
| E13 | `python -m pytest -q --cov=foundry_cli --cov-branch --cov-report=term` | Full suite with branch coverage >= 80% | 1148 passed in 55.14 s; TOTAL 86.06%; sql_queries module 89% branch; exit 0 | Pass |
| E14 | `python -m ruff check src tests .claude/skills/foundry-sql-queries .claude/skills/foundry-streams` | Ruff clean | All checks passed; exit 0 | Pass |
| E15 | `python -m mypy src` | Mypy clean | Success: no issues found in 51 source files; exit 0 | Pass |
| E16 | `python -m compileall -q src/foundry_cli/sql_queries src/foundry_cli/streams .claude/skills/foundry-sql-queries/scripts .claude/skills/foundry-streams/scripts` | Compile clean | Exit 0 | Pass |
| E17 | `python -c "tomllib ... project.scripts"` | SQL Queries entry point present; prior entries retained | `foundry-sql-queries` present; 12 console entries total (10 prior + sql-queries + streams) | Pass |
| E18 | `python -m pip check` | Dependencies consistent | No broken requirements found; exit 0 | Pass |
| E19 | `... query get-results --help` | `--output` registered on get-results | `--output OUTPUT` present | Pass |
| E20 | `... query execute-ontology --help` | No `--output` on execute-ontology | No `--output` (correct per corrected inventory) | Pass |

## Focused probe results

The focused suite covers the exact 5-operation catalog through the single
`SqlQuery` client path, nested routing, JSON argument validation, the two
Arrow byte-result downloads (`execute-ontology`, `get_results`) with bounded
atomic persistence and unsafe-name rejection, ACL precedence and the
3-operation write set, the 1/4 metadata-only policy, fail-closed behavior,
attribution suppression, B3-only tracing, retry, ADR-001 error taxonomy,
timeout bounds, output formats, NDJSON stderr separation, confidentiality,
import/console/launcher packaging, and wheel/editable regression.

CLI probes added independent runtime evidence: parser error envelopes, invalid
JSON and timeout rejection before client or ACL work, ACL denial with exit 8,
configuration failure with exit 9, traceback suppression via
`FOUNDRY_INCLUDE_TRACEBACK=false`, and the operation flag surfaces
(`--output` on get-results only).

## Case disposition

| Case | Status | Evidence |
| --- | --- | --- |
| SQL-TC-001 (catalog, parser, help, exact 5 surface) | Pass | E1, E2, E4, E6 |
| SQL-TC-002 (nested SDK routing through SqlQuery) | Pass | E1, E10 |
| SQL-TC-003 (required inputs, absent optionals omitted) | Pass | E1, E19, E20 |
| SQL-TC-004 (JSON validation before client) | Pass | E1, E5 |
| SQL-TC-005 (Arrow download below byte limit) | Pass | E1, E11, E12 |
| SQL-TC-006 (Arrow download above limit, one probe byte) | Pass | E1, E11 |
| SQL-TC-007 (download failure/cancel clean atomically) | Pass | E1, E11 |
| SQL-TC-008 (unsafe output names rejected) | Pass | E1, E12, E19, E20 |
| SQL-TC-009 (ACL precedence) | Pass | E1, E7, E10 |
| SQL-TC-010 (read-only blocks 3-op write set) | Pass | E1, E10 |
| SQL-TC-011 (metadata-only 1/4) | Pass | E1, E7, E10 |
| SQL-TC-012 (fail closed, CWD independent) | Pass | E1, E17 |
| SQL-TC-013 (include_attribution=False) | Pass | E1, E10 |
| SQL-TC-014 (B3 at outbound transport) | Pass | E1, E11 |
| SQL-TC-015 (B3 disabled, retry stability, restore) | Pass | E1, E11 |
| SQL-TC-016 (retry behavior, at-least-once) | Pass | E1, E11 |
| SQL-TC-017 (ADR-001 taxonomy) | Pass | E1, E4, E5, E7, E8, E9 |
| SQL-TC-018 (timeout bounds and forwarding) | Pass | E1, E8 |
| SQL-TC-019 (output formats) | Pass | E1, E10 |
| SQL-TC-020 (NDJSON stderr, confidentiality) | Pass | E1 |
| SQL-TC-021 (import, console, help, thin launcher) | Pass | E2, E3, E16 |
| SQL-TC-022 (wheel, editable, entry points, regression) | Pass | E13, E14, E15, E16, E17, E18 |

All 22 cases passed. Every story acceptance criterion has at least one passing
case, and the repository branch-coverage gate (80%) is met.

## Notes

- The shell environment carries ambient test credentials
  (`FOUNDRY_TOKEN=dummy`, `FOUNDRY_HOSTNAME=example.palantirfoundry.com`,
  `FOUNDRY_INCLUDE_TRACEBACK=false`). With credentials set, a live-style probe
  reaches the network and ends in `ConnectionError` retry exhaustion with exit
  `6`; with credentials scrubbed the documented `ConfigurationError` exit `9`
  is produced. This is environment leakage, not a product defect, and exit `9`
  evidence was captured with scrubbed credentials.
- The `runpy` RuntimeWarning seen when invoking the module via `-m` is a
  CPython artifact and does not appear when running the packaged launcher or
  console entry point; it is not a product defect.
- `FOUNDRY_INCLUDE_TRACEBACK=false` yields an empty `traceback` field in error
  envelopes. This is the designed confidentiality control, not a defect.

## QA sign-off

**PASS.** SQL-TC-001 through SQL-TC-022 passed with verifiable evidence. No
defects were opened. Full regression is green (1148 passed) with 86.06% branch
coverage; sql_queries namespace at 89% branch.
