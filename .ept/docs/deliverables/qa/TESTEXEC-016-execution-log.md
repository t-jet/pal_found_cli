# TESTEXEC-016 - Foundry Streams CLI execution log

Date: 2026-08-10
Story: DEV-STORY-016
Test design: TESTCASE-016
Commit under test: `0c88063`
Environment: Windows; CPython 3.11.9; `foundry-sdk 1.102.0`; venv `.venv`

## Result

**Pass.** All 24 mandatory cases (STR-TC-001 through STR-TC-024) passed. The
focused Streams suite and the full regression suite are green with branch
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
| E2 | `python -m foundry_cli.streams.scripts.foundry_streams_cli --help` | Help on stdout, exit 0, 15 operations named | Usage naming `dataset,stream,subscriber`; exit 0 | Pass |
| E3 | `python .claude/skills/foundry-streams/scripts/foundry_streams_cli.py --help` | Thin launcher help, exit 0 | Same help; exit 0 | Pass |
| E4 | `... foundry_streams_cli.py` (no args) | One JSON user-input envelope on stdout, exit 1, no traceback | `{"error": true, "exit_code": 1, "exit_code_name": "UserInputError", ...}` on stdout; exit 1 | Pass |
| E5 | `... stream publish-record ri.foundry.main.dataset.stream-test master --record-json not-json` | Invalid JSON rejected before client, exit 1, no payload echo | `{"error": true, "exit_code": 1, ...}`; exit 1; no echo | Pass |
| E6 | `... bogus-op` | Unknown operation rejected, exit 1 | `{"error": true, "exit_code": 1, ... "message": "Invalid command input", ...}`; exit 1 | Pass |
| E7 | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=1 ... stream publish-record ... --record-json '{"value":"qa-record-001"}'` | ACL denial envelope, exit 8, no client work | `{"error": true, "exit_code": 8, "exit_code_name": "AccessControlError", ...}`; exit 8 | Pass |
| E8 | `... stream get ri.foundry.main.dataset.stream-test master --timeout 3601` | Invalid timeout rejected before ACL/client, exit 1 | `{"error": true, "exit_code": 1, ...}`; exit 1 | Pass |
| E9 | `... stream get-records ... --partition-id 0 --max-records 10001` | Max-records above bound rejected, exit 1 | `{"error": true, "exit_code": 1, ...}`; exit 1 | Pass |
| E10 | `... stream publish-binary-record ... --file C:\definitely\missing.bin` | Missing file rejected before client, exit 1 | `{"error": true, "exit_code": 1, ...}`; exit 1 | Pass |
| E11 | Credentials scrubbed; `... stream get ...` | ConfigurationError envelope, exit 9 | `{"error": true, "exit_code": 9, "exit_code_name": "ConfigurationError", ...}`; exit 9 | Pass |
| E12 | `python -m pytest -q tests/test_access_control_guard.py tests/test_foundry_sql_queries_cli.py tests/test_foundry_streams_cli.py` | ACL+focused suite passes | 131 passed in 0.84 s; exit 0 | Pass |
| E13 | `python -m pytest -q tests/test_binary_download.py tests/test_pagination_helper.py tests/test_tracing_provider.py` | Shared component suites pass | 58 passed in 0.30 s; exit 0 | Pass |
| E14 | `python -m pytest -q tests/test_foundry_streams_cli.py -k "binary or publish or max_records or reset or timeout or batch"` | Batch/publish/reset subset passes | 15 passed; exit 0 | Pass |
| E15 | 16 MiB oversize file probe: 16,777,217-byte file, `... stream publish-binary-record ... --file <oversize>` | Oversized file rejected with UserInputError, exit 1, before client | `{"error": true, "exit_code": 1, "exit_code_name": "UserInputError", "message": "file exceeds the maximum publish size", ...}`; exit 1 | Pass |
| E16 | `python -m pytest -q --cov=foundry_cli --cov-branch --cov-report=term` | Full suite with branch coverage >= 80% | 1148 passed in 55.14 s; TOTAL 86.06%; streams module 90% branch; exit 0 | Pass |
| E17 | `python -m ruff check src tests .claude/skills/foundry-sql-queries .claude/skills/foundry-streams` | Ruff clean | All checks passed; exit 0 | Pass |
| E18 | `python -m mypy src` | Mypy clean | Success: no issues found in 51 source files; exit 0 | Pass |
| E19 | `python -m compileall -q src/foundry_cli/sql_queries src/foundry_cli/streams .claude/skills/foundry-sql-queries/scripts .claude/skills/foundry-streams/scripts` | Compile clean | Exit 0 | Pass |
| E20 | `python -c "tomllib ... project.scripts"` | Streams entry point present; prior entries retained | `foundry-streams` present; 12 console entries total (10 prior + sql-queries + streams) | Pass |
| E21 | `python -m pip check` | Dependencies consistent | No broken requirements found; exit 0 | Pass |
| E22 | `... stream get-records --help` | `--partition-id` required, `--max-records` optional | `--partition-id` required positional option; `--max-records` optional | Pass |

## Focused probe results

The focused suite covers the exact 15-operation catalog (Dataset 1, Stream 8,
Subscriber 6) across the three nested client paths, JSON argument validation,
the ADR-003 batch-response pattern for record reads with bounded
`--max-records` caps and single aggregated emission, offset semantics with
`--auto-commit` defaulting off, the bounded 16 MiB binary file publish, the
streams namespace timeout override (`FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S`,
default 120), ACL precedence and the 10-operation write set including the
`reset` write-verb classification, the 3/12 metadata-only policy, fail-closed
behavior, attribution suppression, B3-only tracing, retry, ADR-001 error
taxonomy, timeout bounds, output formats, NDJSON stderr separation,
confidentiality, import/console/launcher packaging, and wheel/editable
regression.

CLI probes added independent runtime evidence: parser error envelopes, invalid
JSON, timeout, max-records bound, and missing-file rejection before client or
ACL work, ACL denial with exit 8, configuration failure with exit 9, the
16 MiB oversize-file rejection, and the `get-records` flag surface.

## Case disposition

| Case | Status | Evidence |
| --- | --- | --- |
| STR-TC-001 (catalog, parser, help, exact 15 surface) | Pass | E1, E2, E4, E6 |
| STR-TC-002 (nested SDK routing across three client paths) | Pass | E1, E12 |
| STR-TC-003 (required inputs, absent optionals omitted) | Pass | E1, E22 |
| STR-TC-004 (JSON validation before client) | Pass | E1, E5 |
| STR-TC-005 (ADR-003 batch: get-records aggregates, limits) | Pass | E1, E14, E22 |
| STR-TC-006 (ADR-003 batch: read-records offsets semantics) | Pass | E1, E14 |
| STR-TC-007 (batch-read volume boundaries) | Pass | E1, E9, E14 |
| STR-TC-008 (bounded binary publish before client) | Pass | E1, E10, E14, E15 |
| STR-TC-009 (streams namespace timeout override) | Pass | E1, E8 |
| STR-TC-010 (ACL precedence) | Pass | E1, E7, E12 |
| STR-TC-011 (read-only blocks 10-op write set) | Pass | E1, E12 |
| STR-TC-012 (reset verb keeps write classification) | Pass | E1, E14 |
| STR-TC-013 (metadata-only 3/12) | Pass | E1, E7, E12 |
| STR-TC-014 (fail closed, CWD independent) | Pass | E1, E20 |
| STR-TC-015 (include_attribution=False) | Pass | E1, E12 |
| STR-TC-016 (B3 at outbound transport) | Pass | E1, E13 |
| STR-TC-017 (B3 disabled, retry stability, restore) | Pass | E1, E13 |
| STR-TC-018 (retry behavior, at-least-once) | Pass | E1, E13 |
| STR-TC-019 (ADR-001 taxonomy) | Pass | E1, E4, E5, E7, E8, E9, E10, E11 |
| STR-TC-020 (timeout bounds and forwarding) | Pass | E1, E8 |
| STR-TC-021 (output formats) | Pass | E1, E12 |
| STR-TC-022 (NDJSON stderr, confidentiality) | Pass | E1 |
| STR-TC-023 (import, console, help, thin launcher) | Pass | E2, E3, E19 |
| STR-TC-024 (wheel, editable, entry points, regression) | Pass | E16, E17, E18, E19, E20, E21 |

All 24 cases passed. Every story acceptance criterion has at least one passing
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
- The story title and ADR-003/SAD-001 reference "17 operations"; the vendored
  SDK exposes exactly 15 (Dataset 1, Stream 8, Subscriber 6) and the case set,
  DESIGN-016, and the metadata allow-list are concordant at 15. This is
  documented design staleness, not a defect.
- `FOUNDRY_INCLUDE_TRACEBACK=false` yields an empty `traceback` field in error
  envelopes. This is the designed confidentiality control, not a defect.

## QA sign-off

**PASS.** STR-TC-001 through STR-TC-024 passed with verifiable evidence. No
defects were opened. Full regression is green (1148 passed) with 86.06% branch
coverage; streams namespace at 90% branch.
