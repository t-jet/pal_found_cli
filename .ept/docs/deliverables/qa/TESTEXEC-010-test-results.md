# TESTEXEC-010 - Foundry Audit CLI test results

## Execution summary

| Field | Result |
|---|---|
| Story | DEV-STORY-010 |
| Test specification | [TESTCASE-010](TESTCASE-010-test-cases.md) |
| Design | [DESIGN-010](../architecture/DESIGN-010-audit-cli.md) |
| Reviewed commit | `87d817c6f9d3329b57fadd20f3df84f93be9d570` |
| Branch | `workflow_tuning_checkpoint-01` |
| Execution date | 2026-08-01 |
| Execution window | 21:08-21:23 Europe/Sofia |
| Host | Windows 10.0.26200.0, PowerShell 7.6.4 |
| Python | 3.11.9 and 3.12.0 |
| Network | Disabled for dependency resolution and Foundry calls |
| Test transport | SDK fakes, public-only stream doubles, temporary files, local wheel installs |
| Test cases | 26 passed, 0 failed, 0 blocked |
| Defects | None |
| QA result | APPROVED |
| Time spent | 0.25 hours |

TESTCASE-010 SHA-256 was `D23211062DC01AA657CD54C092EAA77240CF69A991901F0E3536DB47372FB2BB` at execution start. The Audit implementation and its two test modules were clean at reviewed HEAD. `pyproject.toml`, the document index, and other unrelated workspace files already had local edits; this execution did not attribute or modify those changes except for the index entry named below.

## Commands and gate results

All package commands used `PIP_NO_INDEX=1`. Temporary build tools and environments lived under `T:\tmp\testexec010-*`; no live Foundry endpoint or package registry was contacted.

| ID | Command | Result |
|---|---|---|
| EX-01 | `python -m pytest -q tests/test_foundry_audit_cli.py tests/test_audit_console_wrapper.py` | PASS: 83/83 in 13.77 s on Python 3.11.9. |
| EX-02 | `python -m pytest tests --cov=foundry_cli --cov-branch --cov-report=term-missing --cov-report=xml:T:\tmp\testexec010-coverage.xml -q` | PASS: 933/933 in 23.97 s; branch coverage 82.66%, above 80%. |
| EX-03 | `D:\app\Python-3.12\python.exe -m pytest -q tests` with an offline temporary user base | PASS: 933/933 in 19.09 s on Python 3.12.0. |
| EX-04 | `python -m ruff check src/ tests/` | PASS: all checks passed. |
| EX-05 | `python -m mypy src/` | PASS: no issues in 32 source files. |
| EX-06 | `python -m bandit -r src/ --severity-level high` | PASS: 6,689 lines scanned; 0 high, medium, low, or undefined findings. |
| EX-07 | `python -m compileall -q src .claude/skills/foundry-audit/scripts` with a temporary bytecode prefix | PASS. |
| EX-08 | Local wheel build, wheel policy inspection, wheel install, `foundry-audit --help`, packaged ACL probe, Claude launcher help, editable install, and repeat help/policy probes from an arbitrary CWD | PASS: each process exited 0; both operations listed; `list=PERMITTED`, `content=BLOCKED`. |
| EX-09 | Python 3.12 standalone import of the package and CLI with stdout/stderr captured | PASS: exit 0, stdout 0 bytes, stderr 0 bytes, no filesystem mutation. |

### Environment incidents

The first strict-offline wrapper attempt stopped during build setup because Python 3.11 had no local `wheel` package and build isolation could not download `setuptools>=68.0`. A standalone reproduction failed at the same setup point before product code ran. Temporary local wheel tooling and no-build-isolation mode resolved it; EX-01 then passed 83/83. This was an environment setup issue, not a product defect.

The first manual help assertion treated PowerShell's output array as a scalar and reported failure even though the installed command returned 0. Raw capture showed the correct help text. Joining the captured lines corrected the harness assertion; wheel and editable smoke checks then passed. No product change was made.

The shared Python 3.11 installation emits a `RequestsDependencyWarning` because its global `requests`, `urllib3`, and `chardet` versions do not agree. The warning contained no secret or audit data. The clean Python 3.12 offline environment produced zero stdout and stderr for the exact import check. This host warning is not a DEV-STORY-010 defect.

## Case results

### Interface, input, and timeout cases

| Case | Command/function and data | Expected | Actual and evidence | Result |
|---|---|---|---|---|
| AUD-TC-001 | `OP_SPECS`, `build_parser`, `_spec_for`, `_get_client`; both commands and one unknown operation | Two unique operations; exact `audit.Organization.LogFile` route; unknown input exits 1 | Exact two-entry catalog and nested route asserted by `test_catalog_contains_exact_two_unique_nested_operations`, parser and client-route tests; EX-01/03 green | PASS |
| AUD-TC-002 | Root/operation help, missing command, bad flag, missing positional, bad integer | Help exits 0; parser failures emit JSON on stdout and exit 1 before config/client | Help and parser parameter sets passed; installed and launcher help also exited 0 in EX-08 | PASS |
| AUD-TC-003 | Dates `2024-02-29`, malformed/impossible dates, initial request without start date, continuation token | Strict dates become `date`; bad or missing initial date exits 1 before ACL/client; continuation may omit date | All date and cursor parameter sets passed; invalid-date main test confirmed no ACL/client call | PASS |
| AUD-TC-004 | Timeouts 1, 30, 3600; CLI 17; configured 42 | Valid boundaries accepted; one selected value reaches retry and SDK | Boundary and forwarding tests passed on both Python versions | PASS |
| AUD-TC-005 | Timeouts 0, 3601, -1, and invalid parser input | JSON user-input error, exit 1, no ACL/client/path | Validation and main ordering tests passed; no download path created | PASS |

### Pagination and retry cases

| Case | Command/function and data | Expected | Actual and evidence | Result |
|---|---|---|---|---|
| AUD-TC-006 | Raw first page, empty page, supplied `cursor-002`, page size 2 | Decode one server page; forward dates, cursor, page size, timeout; exact metadata | Raw wrapper decoded once; records, cursor, counts, and kwargs matched expected values | PASS |
| AUD-TC-007 | Two-page chain, early EOF, 45-page chain with batch 999 | Exact server-page count; stop at EOF; fetch at most 40 and return `p40` | Multi-page tests reported 2 pages at EOF and exactly 40 calls/items for capped chain | PASS |
| AUD-TC-008 | Page two fails once, then two-page retry succeeds | Fresh helper and original cursor; no duplicate records/counts/output | Calls were initial, second, initial, second; final count was 2 pages/2 items with unique output | PASS |
| AUD-TC-009 | HTTP 503 then success; repeated HTTP 429 | 503 recovers; exhausted 429 returns JSON exit 7 without duplicate data | Both retry paths and ADR serializer checks passed | PASS |

### Access-control cases

| Case | Command/function and data | Expected | Actual and evidence | Result |
|---|---|---|---|---|
| AUD-TC-010 | Global metadata-only; namespace override; operation disable | `list` permitted, `content` blocked; operation override wins | Guard tests passed; content raised ACL exit 8; precedence step was 1 | PASS |
| AUD-TC-011 | Content denial with factory/filesystem/context sentinels | ACL runs first; no scope/client/transport/path; prior B3 context unchanged | Guard was the only reachable operation; factory was not constructed; context-preservation contract covered by ordering and B3 isolation checks | PASS |
| AUD-TC-012 | Wheel and editable installs from arbitrary CWD without `PYTHONPATH` | Packaged allow-list exists; list permitted/content blocked in both installs | Wheel contained `foundry_cli/audit/metadata-allow-list.md`; wheel and editable probes printed `POLICY=PASS` in EX-01/08 | PASS |

### Stream, path, cancellation, and cleanup cases

| Case | Command/function and data | Expected | Actual and evidence | Result |
|---|---|---|---|---|
| AUD-TC-013 | `abc`, limit 5 | Three-byte complete file, non-truncated JSON envelope, closed stream/context | Stored bytes, size 3, source size 3, closure, and one published file matched | PASS |
| AUD-TC-014 | `abcde`, limit 5 | Exact-limit complete file; EOF probe; `truncated=false` | File and envelope reported exact size 5 and non-truncated; context closed | PASS |
| AUD-TC-015 | `abcdefghi` plus unread sentinel, limit 5 | Store `abcde`; one probe byte; lower bound 6; do not read sentinel chunk | File size 5, truncated true, source null, lower bound 6; stream index proved bounded observation | PASS |
| AUD-TC-016 | Public-only stream fake and handler spy | Streaming wrapper only; unavailable length/encoding/MIME all `None`; no eager/private access | Handler captured all three `None` values; source guard and response fake recorded no private access | PASS |
| AUD-TC-017 | Partial stream then `OSError` or cancellation | Error 6 or cancellation 5; no partial/temp file; all contexts close | Both injected failures left an empty root; cancellation mapped to exit 5; streams and contexts closed | PASS |
| AUD-TC-018 | Retry: partial transport failure, then `complete` | Failed attempt removed; one complete published file; both responses close | Exactly one file remained with `complete`; both stream/context pairs closed | PASS |
| AUD-TC-019 | Traversal, separators, absolute, NUL, `.`, `..` | JSON user-input exit 1; no root or escaped file | Every unsafe name raised `InvalidDownloadError` with exit-code contract 1; root was absent | PASS |

### Output, error, tracing, packaging, and regression cases

| Case | Command/function and data | Expected | Actual and evidence | Result |
|---|---|---|---|---|
| AUD-TC-020 | Empty/uniform/non-uniform list data, cursor, JSON/TOON/auto | Success data once on stdout; pagination metadata once on stderr; no audit record in diagnostics | Main list test parsed stdout and confirmed cursor metadata on stderr without record leakage; formatter regressions passed | PASS |
| AUD-TC-021 | Content with JSON/TOON/auto and secret payload sentinel | Standard JSON metadata only; no content/token/body in stdout, stderr, or logs | Main forced JSON for content; bounded tests and captured streams showed no payload or secret leakage | PASS |
| AUD-TC-022 | User input, 401, 403, 404, timeout, cancellation, 503, 429, ACL, config, filesystem, unexpected error | Exact ADR-001 codes 1-9 and one JSON error envelope on stdout | Parameterized serializer tests returned 1, 2, 3, 4, 5, 6, 7, 8, and 9 as specified; no raw traceback | PASS |
| AUD-TC-023 | Enabled tracing, clean SDK context, captured prepared transport | Valid 32-char trace ID, 16-char span ID, sampled value; B3 only | Client creation and outbound attempt captures carried valid `X-B3-*`; no W3C headers | PASS |
| AUD-TC-024 | Disabled tracing; enabled retry; prior context; formatter failure | No B3 when disabled; same B3 across retries; no W3C; exact prior values restored | Enabled/disabled parameter sets, retry captures, formatter-failure restore, and source checks all passed | PASS |
| AUD-TC-025 | Package/launcher imports, help, `console_main`, empty arbitrary CWD | No config/network/path side effects; clean import; help 0; one `asyncio.run`; thin launcher | Python 3.12 import was 0/0 bytes and exit 0; help/launcher tests and one-boundary spy passed; empty CWD stayed empty | PASS |
| AUD-TC-026 | Local wheel/editable installs; arbitrary-CWD console/launcher/policy; full suites and quality gates | Installs and help pass; existing scripts remain; Python 3.11/3.12 suites pass; coverage at least 80%; static/security gates pass | EX-01 through EX-09 passed: 83 targeted, 933 full on each Python, 82.66% coverage, clean Ruff/mypy/Bandit/compile and package smoke | PASS |

## Traceability and security verification

| Story acceptance criterion | Passing evidence |
|---|---|
| AC 1: initial list route, data, cursor, exit 0 | AUD-TC-001, 003, 006, 020 |
| AC 2: exact N pages, 40 cap, accurate counts | AUD-TC-007, 008 |
| AC 3: missing/malformed date, no client, exit 1 | AUD-TC-002, 003, 005, 022 |
| AC 4: public bounded stream, `None` headers, one probe, cleanup | AUD-TC-013 through 019, 021 |
| AC 5: list permitted/content blocked before client/path | AUD-TC-010 through 012 |
| AC 6: B3 scope, retry stability, no W3C, restore | AUD-TC-011, 023, 024 |
| AC 7: ADR errors, atomic cleanup, no sensitive leakage | AUD-TC-009, 017 through 022 |
| AC 8: installed console and Claude launcher | AUD-TC-012, 025, 026 |

Security checks confirmed that content used only the public streaming response, private SDK fields were inaccessible, eager decoding was absent, unsafe filenames created no path, failed attempts published no partial data, ACL ran before client/filesystem work, and audit content or credential sentinels did not appear in captured output.

## Defects and risks

- Product defects: none.
- Open blocking defects: none.
- Non-blocking environment observation: the shared Python 3.11 installation has an unrelated dependency warning on `requests` import. Clean Python 3.12 execution had no import output, and all functional and security assertions passed.
- Pytest emitted a deprecation warning because `asyncio_default_fixture_loop_scope` is unset. It did not affect execution results.

## QA sign-off

All 26 approved cases passed. Targeted tests, both supported Python full suites, branch coverage, static analysis, type checking, security scanning, compilation, wheel/editable installs, arbitrary-CWD entry points, packaged ACL policy, cleanup, and security assertions passed. No linked defect is required.

QA execution is approved. Formal tracker sign-off is READY to post after the authorized helper records TESTCASE-010 and TESTEXEC-010 in terminal status.
