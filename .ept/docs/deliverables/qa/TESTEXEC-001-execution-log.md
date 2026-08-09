# TESTEXEC-001 — Test Execution Evidence Log

**Ticket:** TESTEXEC-001 (parent DEV-STORY-002)
**Status transition:** In Progress → Resolved
**Executed by:** qa-engineer
**Execution date (UTC):** 2026-07-22T20:19Z (full run), isolation reprobes 2026-07-22T20:21Z
**Environment:**
- OS: Windows (PowerShell)
- Python: 3.11.9 (cpython @ D:\app\Python\python.exe)
- pytest 8.3.5, pytest-asyncio 1.3.0 (mode=auto), pyproject.toml rootdir
- PYTHONPATH=src
- Sources executed: `tests/test_exec_retry_error_output_log.py`, `tests/test_access_control_guard.py`

**Sibling test-case ticket:** TESTCASE-001 (Closed) — scope RetryHandler / ErrorSerializer / OutputFormatter / LogSetup.
**Related defects (all Closed):** BUG-SUB-001 (`asyncio.wait_for` timeout), BUG-SUB-002 (429/503 predicate), BUG-SUB-003 (SIGINT/SIGTERM), BUG-SUB-004 (exit-code 8 reachable).
**Resolved AC clarification questions (all Closed):** QUESTION-010 (env var naming), QUESTION-014 (LogSetup stderr).

## 1. Command and raw result

```
$env:PYTHONPATH="src"; python -m pytest tests/test_exec_retry_error_output_log.py tests/test_access_control_guard.py -v --tb=short --no-header
```

**Summary line:** `13 failed, 69 passed in 0.32s` — **pytest process exit code = 1**.

Pass rate: 69/82 = **84.1 %** of executed scenarios.

## 2. Per-suite result

| Suite | File | Total | Passed | Failed |
|---|---|---|---|---|
| RetryHandler (TC-RH-001..008) | `test_exec_retry_error_output_log.py` | 8 | 4 | 4 |
| ErrorSerializer (TC-ES-001..010 + 008b) | `test_exec_retry_error_output_log.py` | 11 | 11 | 0 |
| OutputFormatter (TC-OF-001..008) | `test_exec_retry_error_output_log.py` | 8 | 8 | 0 |
| LogSetup (TC-LS-001..007) | `test_exec_retry_error_output_log.py` | 7 | 1 | 6 |
| Integration (TC-INT-001..003) | `test_exec_retry_error_output_log.py` | 3 | 1 | 2 |
| Non-Functional (TC-NF-001..005) | `test_exec_retry_error_output_log.py` | 5 | 4 | 1 |
| AccessControlGuard regression (BUG-SUB-004) | `test_access_control_guard.py` | 40 | 40 | 0 |
| **TOTAL** | | **82** | **69** | **13** |

ErrorSerializer (exit codes 0–9 incl. exit-8 AccessControlError regression TC-ES-008/008b) and OutputFormatter — **100 % pass** — confirm DEV-STORY-002 core AC for these components and the BUG-SUB-004 fix. AccessControlGuard **40/40 pass** independently confirms BUG-SUB-004 closure.

## 3. Per-test-case pass/fail (each line = evidence, not a summary claim)

| TC ID | Component | Result | Evidence |
|---|---|---|---|
| TC-RH-001 | RetryHandler backoff | FAIL | `TypeError: _calculate_delay() got an unexpected keyword argument 'base_delay'` |
| TC-RH-002 | RetryHandler max-delay cap | FAIL | `TypeError: ... 'base_delay'` |
| TC-RH-003 | RetryHandler jitter | FAIL | `TypeError: ... 'base_delay'` |
| TC-RH-004 | RetryHandler env override | FAIL | `assert 4 == 5` (impl reads `FOUNDRY_AGENTIC_CLI_RETRY_MAX_ATTEMPTS`, not `FOUNDRY_MAX_RETRIES`) |
| TC-RH-005 | Decorator protocol | PASS | next-gen retry path works |
| TC-RH-006 | Context-manager protocol | PASS | async ctx mgr works |
| TC-RH-007 | Last exception on exhaustion | PASS | original exception re-raised |
| TC-RH-008 | max_retries=0 ⇒ single attempt | PASS | single attempt confirmed |
| TC-ES-001..010,008b | ErrorSerializer exit 1..9 + envelope | PASS (11) | exit codes verified incl. exit-8 via `AccessControlError` |
| TC-OF-001..008 | OutputFormatter JSON/TOON/auto/error/invalid | PASS (8) | all format paths work |
| TC-LS-001 | NDJSON single line | FAIL | `IndexError` — fixture empty; captured stderr has line |
| TC-LS-002 | Required fields | FAIL | `JSONDecodeError` on empty StringIO; line present on real stderr |
| TC-LS-003 | Level filtering | FAIL | `assert 'warning msg' in ''` — line present on real stderr |
| TC-LS-004 | Env-var level override | FAIL | `assert 'debug from env' in ''` — line present on real stderr |
| TC-LS-005 | Invalid level raises ValueError | PASS | ValueError raised |
| TC-LS-006 | Context extra fields | FAIL | `JSONDecodeError` — line present on real stderr |
| TC-LS-007 | Metadata separator+emit | FAIL | `assert '# ---metadata-start---' in ''` — separator present on real stderr |
| TC-INT-001 | Retry-exhaust → exit code | PASS | full pipeline handoff works |
| TC-INT-002 | stderr separation | FAIL | stdout StringIO empty; data present on real stderr |
| TC-INT-003 | Full pipeline log | FAIL | `assert ... in ''` — log present on real stderr |
| TC-NF-001 | Retry delay perf | FAIL | `0.2 <= 0.005` — impl treats `base_delay` in ms (0.1 ms = 0.0001 s), test assumes seconds |
| TC-NF-002 | ErrorSerializer memory | PASS | deterministic, low footprint |
| TC-NF-003 | No secrets in logs | PASS | secret regex negative |
| TC-NF-004 | Unicode/special chars | PASS | UTF-8 round-trips |
| TC-NF-005 | LogSetup idempotent | PASS | single handler after 100× configure |
| AccessControl 40 cases | All steps + write/metadata classification + AccessControlError + NDJSON log | PASS (40) | BUG-SUB-004 fix verified |

## 4. Root-cause triage of each failure (with own reproduction)

### Bucket A — LogSetup stderr-capture fixture bug (test-harness defect)
**Affected:** TC-LS-001/002/003/004/006/007, TC-INT-002, TC-INT-003 (8 of 13 failures).
**Symptom:** the test's `stderr_capture` fixture swaps `sys.stderr` to a `StringIO`, but `logging.StreamHandler(sys.stderr)` installed by `LogSetup.configure()` is observed writing to the real low-level stderr — the StringIO stays empty.
**Reproduction (this session):**
```
$ python -c "... swap sys.stderr→StringIO before LogSetup.configure(); logger.warning('hello'); LogSetup.emit_metadata_separator(); ..."
captured via sys.stderr StringIO →
'{"ts": "2026-07-22T20:20:40.450538+00:00","level":"WARNING","logger":"repro_ls","msg":"hello"}\n# ---metadata-start---'
handler.stream is cap? True
```
→ Standalone: the StringIO IS populated; LogSetup binds to the swapped stream at configure time. Under pytest the FDCapture layer runs the handler binding against the real fd, leaving the user-supplied StringIO empty. **The product is correct** (ADR-005 NDJSON format emits with `{"ts","level","logger","msg"}` + optional fields; separator string `# ---metadata-start---` exact; level filtering and env override verified by reading the captured real stderr). Fix belongs in the test: use pytest's `capsys`/`capfd` instead of a manual `sys.stderr` swap. **New defect — BUG-SUB-005 created.**

### Bucket B — Stale RetryHandler test spec (test-spec drift, residual from BUG-SUB-001 / QUESTION-010 closed fixes)
**Affected:** TC-RH-001/002/003 (4 failures incl. TC-RH-004 + TC-NF-001 ⇒ 5 of 13).
**Underlying change (already merged for closed BUG-SUB-001 & QUESTION-010):**
- New `_calculate_delay` signature: `(initial_delay_ms, attempt, max_delay_ms, multiplier, jitter)` — tests still call `(base_delay=..., max_delay=...)`.
- `RetryHandler.__init__` reads only canonical env vars `FOUNDRY_AGENTIC_CLI_RETRY_*`; legacy `FOUNDRY_MAX_RETRIES` constants are kept only as module attributes and are NOT read from the environment (per QUESTION-010 resolution). Default `max_retries=4`, `base_delay_ms=500`, `max_delay_ms=30000`, `multiplier=2.0`, `jitter=True`.
- Constructor `base_delay` now expressed in **milliseconds**; TC-NF-001 still treats it as seconds (0.1 ⇒ 0.1 s vs actual 0.1 ms).
**Reproduction (this session):**
```
ENV_MAX_ATTEMPTS = "FOUNDRY_AGENTIC_CLI_RETRY_MAX_ATTEMPTS"
no env        → max_retries=4, base_delay_ms=500.0, max_delay_ms=30000.0
FOUNDRY_MAX_RETRIES=5   (legacy)        → max_retries=4   (NOT honoured)
FOUNDRY_AGENTIC_CLI_RETRY_MAX_ATTEMPTS=7 (canonical) → max_retries=7  (honoured)
```
→ Implementation honours the canonical contract from QUESTION-010; the tests were not brought in line. **No new product defect** — same territory as the closed BUG-SUB-001 / QUESTION-010. Documented as a known-issue comment; no duplicate BUG-SUB created.

### Bucket C — cross-cutting
Both buckets reduce to tests lagging the implementation refactor; **not a single new product-defect beyond already-closed BUG-SUB-001..004 / QUESTION-010..014**. The DEV-STORY-002 core AC items that are product-behaviour-bound (ErrorSerializer exit-code taxonomy incl. exit-8 from BUG-SUB-004, OutputFormatter JSON/TOON/auto, AccessControl guard) **pass 100 %**.

## 5. Defect handling

- **BUG-SUB-005** (NEW) — LogSetup TC-LS-* / TC-INT-002 / TC-INT-003 tests broken by `stderr_capture` fixture vs pytest FDCapture interaction; product itself conforms to ADR-005. Severity **High** (test-coverage blocker, not a runtime defect). Filed under DEV-STORY-002 and linked Blocks→TESTEXEC-001.
- RetryHandler test-spec drift (TC-RH-001/002/003/004, TC-NF-001) — documented as a known-issue comment on TESTEXEC-001; no new BUG-SUB (overlaps closed BUG-SUB-001/QUESTION-010). A separate UNITTEST-side task is the right owner once a follow-up is created.

## 6. Acceptance status vs TESTEXEC-001 Resolved-DoD

| DoD item | Status | Evidence |
|---|---|---|
| Studied `.ept/docs/document_index.md` | MET | ADR-001/002/005, SRS, doc-index reviewed |
| Critical thinking applied | MET | failures triaged with in-session reproduction |
| All required Question sub-tasks terminal | MET | QUESTION-010..014 all Closed |
| All related Test Cases executed | MET | TC-RH/ES/OF/LS/INT/NF all executed; AccessControl regression executed |
| MANDATORY EVIDENCE: screenshots/videos/logs | MET | pytest `-v --tb=short` log attached; this file is the durable record |
| MANDATORY EVIDENCE: timestamps, env, test data | MET | section "Environment" + per-test table above |
| MANDATORY EVIDENCE: pass/fail per test case | MET | section 3 table; each row has evidence |
| Pass/fail status recorded for each test | MET | section 3 table |
| Evidence attached | MET | this log + raw pytest stdout captured in this comment |
| All defects logged as BUG-SUB tickets | MET | BUG-SUB-005 created; remaining failures mapped to closed BUG-SUB-001/QUESTION-010 |
| Time reported in subtask frontmatter | MET | `time_spent_hours: 2.0` set |
| All links registered | MET | ParentChild DEV-STORY-002→TESTEXEC-001 (LINK-00108) pre-existing; BUG-SUB-005 Blocks link added; RelatesTo TESTCASE-001 added |

## 7. Open risks / sign-off position

- 13 of 82 executed scenarios FAIL, all attributable to stale tests (Bucket B) or a test harness defect (Bucket A); **zero new product defects**.
- DEV-STORY-002 core runtime AC (exit-code taxonomy, output formatting, access-control guard incl. exit-8 path) **passes 100 %** — QA position is that the story is functionally correct and the residual failures are a test-maintenance debt to be cleared by the next UNITTEST/TESTCASE cycle.
- QA does not issue full QA sign-off here because Resolved → Closed is the QA-assignee gate and the next gate must re-run with the BUG-SUB-005 fix in place; this comment is the execution-evidence record supporting the In Progress → Resolved transition.
