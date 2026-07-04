# TESTCASE-001 — QA Test Cases for RetryHandler, ErrorSerializer, OutputFormatter, LogSetup

**Parent:** DEV-STORY-002
**Status:** In Progress → Resolved (pending QA review)
**Author:** qa-engineer
**Date:** 2026-07-04
**Scope:** Functional, integration, and non-functional verification of the four components in `src/foundry_cli/common/` (`retry.py`, `error_serializer.py`, `output_formatter.py`, `log_setup.py`) against DEV-STORY-002 acceptance criteria and ADRs 001, 002, 004, 005.

## Coverage Matrix

| AC area (DEV-STORY-002) | Test case IDs |
|---|---|
| RetryHandler — backoff, env vars, jitter, decorator/ctx mgr, timeout | TC1.1–TC1.9 |
| ErrorSerializer — exit codes 0–9, envelope, SDK mapping | TC2.1–TC2.11 |
| OutputFormatter — JSON/TOON/auto, overrides, stderr separation | TC3.1–TC3.9 |
| LogSetup — NDJSON, fields, level, separator | TC4.1–TC4.8 |
| Integration | TC5.1–TC5.3 |
| Non-functional (performance, security, memory) | TC6.1–TC6.5 |

## Test Cases

### TC1 — RetryHandler (`src/foundry_cli/common/retry.py`)

**Reference:** ADR-002 (Call Timeout Defaults), DEV-STORY-002 RetryHandler AC, FR-ERR-3, FR-ERR-4, FR-ASYNC-3.

**Function/API under test:** `RetryHandler.__init__`, `_calculate_delay`, `execute`, `__call__` (decorator), `context()` (async context manager).

| ID | Scenario | Input | Expected Result | Pass Criteria |
|---|---|---|---|---|
| TC1.1 | Exponential backoff delay calculation | `_calculate_delay(base_delay=1.0, attempt=2, max_delay=30.0, jitter=False)` | Returns `4.0` (1.0 × 2²) | Equality, no jitter variance |
| TC1.2 | `max_delay` cap respected | `_calculate_delay(base_delay=10.0, attempt=5, max_delay=30.0, jitter=False)` | Returns `30.0` (capped) | `result == 30.0` |
| TC1.3 | Jitter bounded within ±10% | 1000 calls of `_calculate_delay(1.0, 1, 30.0, jitter=True)` (expected base 2.0) | All results in `[1.8, 2.2]` | `1.8 ≤ r ≤ 2.2` for all calls |
| TC1.4 | Env var override `FOUNDRY_MAX_RETRIES` | `monkeypatch.setenv("FOUNDRY_MAX_RETRIES", "5")`, construct `RetryHandler()` | `handler.max_retries == 5` | Field matches env value |
| TC1.5 | Env var override `FOUNDRY_RETRY_BASE_DELAY` / `_MAX_DELAY` | `setenv` both, construct handler | `base_delay`/`max_delay` reflect values | Field equality |
| TC1.6 | Env var `FOUNDRY_RETRY_JITTER=false` disables jitter | `setenv("FOUNDRY_RETRY_JITTER", "false")` | `handler.jitter is False` | Boolean false parsed |
| TC1.7 | Decorator retries on retryable exception then succeeds | `@RetryHandler(max_retries=3)` wrapping async fn raising `requests.ConnectionError` on calls 1–2, returning `"ok"` on call 3 | Returns `"ok"`, exactly 3 invocations | Mock call count == 3 |
| TC1.8 | `max_retries=0` disables retry; last exception propagated | `RetryHandler(max_retries=0)`, async fn always raises `requests.ConnectionError` | `execute()` raises `ConnectionError`, 1 invocation | Single attempt, original exception re-raised |
| TC1.9 | Async context manager protocol works | `async with RetryHandler().context() as h: await h.execute(fn)` returning `"done"` | Returns `"done"`, no exception | Result equality |

**Negative / regression (flagged discrepancies vs. DEV-STORY-002 AC):**

| ID | Scenario | Expected Finding |
|---|---|---|
| TC1.R1 | AC names env vars `FOUNDRY_AGENTIC_CLI_RETRY_INITIAL_DELAY_MS`, `_MAX_DELAY_MS`, `_MULTIPLIER`, `_MAX_ATTEMPTS`. Implementation reads `FOUNDRY_MAX_RETRIES`, `FOUNDRY_RETRY_BASE_DELAY`, `FOUNDRY_RETRY_MAX_DELAY`, `FOUNDRY_RETRY_JITTER`. | MISMATCH — raise BUG-SUB; document expected-vs-actual env var contract. |
| TC1.R2 | AC requires `asyncio.wait_for()` timeout from `FOUNDRY_AGENTIC_CLI_TIMEOUT_S` (default 30s). | NOT IMPLEMENTED — code calls `await coro_func(...)` with no timeout; raise BUG-SUB. |
| TC1.R3 | AC requires retry specifically on HTTP 429 and 503; default `retry_on` is `requests.RequestException`/`ConnectionError` (no status-code predicate). | GAP — verify whether a 503/429 response is actually retried; raise BUG-SUB. |
| TC1.R4 | AC requires `SIGINT`/`SIGTERM` cancellation. | NOT IMPLEMENTED — no signal handling in `retry.py`; raise BUG-SUB. |

### TC2 — ErrorSerializer (`src/foundry_cli/common/error_serializer.py`)

**Reference:** ADR-001 (Exit Code Taxonomy), FR-ERR-1/2/5.

**API under test:** `ErrorSerializer.serialize`, `_classify_http_exception`, `create_error_envelope`, `get_exit_code_name`.

| ID | Scenario | Input | Expected exit code | Pass Criteria |
|---|---|---|---|---|
| TC2.1 | ValueError → UserInputError | `ValueError("bad arg")` | 1 | exit_code == 1 |
| TC2.2 | SDK AuthenticationError / 401 → AuthenticationError | SDK auth exc OR exc with `response.status_code=401` | 2 | exit_code == 2 |
| TC2.3 | 403 → PermissionDeniedError | exc with `response.status_code=403` | 3 | exit_code == 3 |
| TC2.4 | 404 / FileNotFoundError → NotFoundError | `FileNotFoundError()`; 404 response | 4 | exit_code == 4 |
| TC2.5 | `asyncio.TimeoutError` → TimeoutError | `asyncio.TimeoutError()` | 5 | exit_code == 5 |
| TC2.6 | 500/502/504 → ServerError | response.status_code 500/502/504 | 6 | exit_code == 6 |
| TC2.7 | 429 → RateLimitExhausted | response.status_code 429 | 7 | exit_code == 7 |
| TC2.8 | `ImportError`/`ModuleNotFoundError`/`EnvironmentError` → ConfigurationError | each exception | 9 | exit_code == 9 |
| TC2.9 | 503 excluded from ServerError | response.status_code 503 | NOT 6 (falls through to default 1 or unmapped) | exit_code != 6 (matches ADR-001 exclusion) |
| TC2.10 | JSON envelope emitted on stdout with required fields | any exception, capture stdout | JSON line with `error, exit_code, exit_code_name, message, exception_type, traceback, call_id` | All keys present; valid JSON |
| TC2.11 | `FOUNDRY_INCLUDE_TRACEBACK=false` suppresses traceback | env set false, serialize exc | `traceback == ""` in envelope | Empty traceback field |

**Negative / regression:**

| ID | Scenario | Expected Finding |
|---|---|---|
| TC2.R1 | AC specifies exit code 8 = `AccessControlError`. No exception type maps to 8 in `_register_sdk_exceptions`. | GAP — code 8 unreachable via `serialize()`; raise BUG-SUB. |
| TC2.R2 | AC specifies envelope fields `{type, message, http_status, details, attempt, operation, call_id}`. Implementation emits `{error, exit_code, exit_code_name, message, exception_type, traceback, call_id}` and omits `attempt`, `operation`, `details`. | MISMATCH — raise BUG-SUB; document expected-vs-actual schema. |

### TC3 — OutputFormatter (`src/foundry_cli/common/output_formatter.py`)

**Reference:** ADR-004 (Format Auto-Selection), FR-OUT-1…7.

**API under test:** `OutputFormatter._select_format`, `format`, `format_error`, `emit`, `emit_error`, `emit_to_stderr`.

| ID | Scenario | Input | Expected Format | Pass Criteria |
|---|---|---|---|---|
| TC3.1 | Explicit `json` wins | `format_setting="json"`, list of uniform dicts | json | output parseable as JSON |
| TC3.2 | Explicit `toon` wins | `format_setting="toon"`, list of uniform dicts | toon | table-style output |
| TC3.3 | auto + dict → json | `format_setting="auto"`, `{"k":1}` | json | JSON |
| TC3.4 | auto + empty list → json | `format_setting="auto"`, `[]` | json | JSON `[]` |
| TC3.5 | auto + uniform dict list → toon | `format_setting="auto"`, `[{a,b},{a,b}]` | toon | TOON table |
| TC3.6 | auto + non-uniform field sets → json | `format_setting="auto"`, `[{a,b},{a,c}]` | json | JSON |
| TC3.7 | auto + non-dict items → json | `format_setting="auto"`, `[1,2,3]` | json | JSON |
| TC3.8 | `--pretty` enables indentation | `pretty=True`, json format | multi-line indented | contains `\n` and 2-space indent |
| TC3.9 | `format_error` always JSON regardless of setting | `format_setting="toon"`, error dict | json | JSON output |

**Negative / regression:**

| ID | Scenario | Expected Finding |
|---|---|---|
| TC3.R1 | AC: `--format json|toon|auto` invalid value should error. `format("auto"→invalid "yaml")` raises `ValueError`. | Confirmed — verify error message lists valid values. |
| TC3.R2 | AC: TOON must integrate `toon-python >=0.9,<1.0`. Implementation renders a hand-rolled ASCII table, NOT the `toon-python` library. | MISMATCH — raise BUG-SUB (functionality present but library not used). |
| TC3.R3 | AC: pagination metadata must use `# ---metadata-start---` separator. `emit_to_stderr` writes plain JSON, no separator. | GAP — `LogSetup.emit_metadata` has separator; `OutputFormatter.emit_to_stderr` does not. Raise BUG-SUB. |
| TC3.R4 | AC: "Binary download envelopes always use JSON." Not implemented in OutputFormatter. | GAP — raise BUG-SUB (verify with binary envelope test once API exposed). |
| TC3.R5 | AC: env var `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT` respected. | Confirmed via `OutputFormatter.__init__`. |

### TC4 — LogSetup (`src/foundry_cli/common/log_setup.py`)

**Reference:** ADR-005 (Log Format), NFR-IFACE-2.

**API under test:** `LogSetup.configure`, `reset`, `emit_metadata_separator`, `emit_metadata`, `_NdJsonFormatter.format`, `get_logger`.

| ID | Scenario | Input | Expected | Pass Criteria |
|---|---|---|---|---|
| TC4.1 | NDJSON single-line output | capture stderr after `logger.warning("x")` | exactly one JSON line | line count == 1; valid JSON |
| TC4.2 | Required fields present | parse NDJSON line | keys `ts, level, logger, msg` all present | All keys exist |
| TC4.3 | ISO 8601 UTC timestamp | parse `ts` field | matches `^\d{4}-\d{2}-\d{2}T...+00:00$` | Regex match |
| TC4.4 | Optional context field passthrough | `logger.warning("m", extra={"op":"x","attempt":2,"delay_ms":500})` | those keys present in JSON | Keys present with correct values |
| TC4.5 | Level filtering via `FOUNDRY_AGENTIC_CLI_LOG_LEVEL=ERROR` | setenv, INFO log | no output on stderr | stderr empty |
| TC4.6 | Default level WARNING | no env, DEBUG+INFO logs | only WARNING+ emitted | Only WARNING/ERROR lines |
| TC4.7 | Unsupported level raises ValueError | `configure("TRACE")` | `ValueError` raised | Exception raised |
| TC4.8 | Metadata separator exact string | `emit_metadata_separator()` | stderr line == `# ---metadata-start---` | Exact match |

**Negative / regression:**

| ID | Scenario | Expected Finding |
|---|---|---|
| TC4.R1 | AC: supported levels are `DEBUG, INFO, WARNING, ERROR`. Code also accepts `CRITICAL`. | MINOR — confirm with architect whether CRITICAL should be allowed; document. |
| TC4.R2 | AC: log file with rotation mentioned in DEV-STORY-002 title ("log file, rotation"). Not implemented — only stderr handler. | GAP — raise BUG-SUB or clarification QUESTION (AC ambiguity: ADR-005 says stderr only). |

### TC5 — Integration

| ID | Scenario | Steps | Expected |
|---|---|---|---|
| TC5.1 | RetryHandler + ErrorSerializer | Force `RetryHandler` exhaustion on `requests.ConnectionError`, pass exception to `ErrorSerializer.serialize` | Exit code 1 (default) — verify mapping. Note: AC expects retryable HTTP exhaustion → 7, currently missing. |
| TC5.2 | OutputFormatter + LogSetup | Run `formatter.emit(data)` then `LogSetup.emit_metadata(meta)`, capture stdout and stderr | stdout has formatted data only; stderr has metadata + separator; streams do not cross-contaminate. |
| TC5.3 | Full pipeline (all four components) | Configure logging, decorate async call with RetryHandler, on failure serialize via ErrorSerializer and emit_error via OutputFormatter | Each component behaves per its unit test; no exceptions raised during handoff; exit code propagates. |

### TC6 — Non-Functional

| ID | Scenario | Method | Threshold | Pass Criteria |
|---|---|---|---|---|
| TC6.1 | Error serialization latency | `time.perf_counter` around 1000 `serialize()` calls, take p95 | <5 ms per call | p95 < 5 ms |
| TC6.2 | Format selection latency | 1000 `_select_format()` calls p95 | <10 ms | p95 < 10 ms |
| TC6.3 | Log setup latency | `LogSetup.configure()` (after reset) | <10 ms | <10 ms |
| TC6.4 | Secret leakage check | Serialize exceptions containing token-like strings, scan envelope for known secret patterns | No secret substring present in `message`/`traceback` when `FOUNDRY_INCLUDE_TRACEBACK=false` | Regex negative match |
| TC6.5 | No log handler duplication | Call `LogSetup.configure()` 100x in 10 threads concurrently | Exactly 1 handler on root logger | `len(root.handlers) == 1` |

## Acceptance Criteria Coverage

- AC1 RetryHandler — covered by TC1.1–TC1.9 + TC1.R1–R4 (regressions flagging AC gaps).
- AC2 ErrorSerializer — covered by TC2.1–TC2.11 + TC2.R1–R2.
- AC3 OutputFormatter — covered by TC3.1–TC3.9 + TC3.R1–R5.
- AC4 LogSetup — covered by TC4.1–TC4.8 + TC4.R1–R2.
- Integration & quality — covered by TC5.*, TC6.*, plus code-coverage target tracked in TESTEXEC-001.

## Notes

- Implementation files DO exist on disk (`retry.py`, `error_serializer.py`, `output_formatter.py`, `log_setup.py`); test cases reference real functions/classes — DoD "MANDATORY: Test scenarios reference actual implemented features" is satisfied.
- Several AC discrepancies identified (TC1.R1–R4, TC2.R1–R2, TC3.R2–R4, TC4.R2). These are documented as regression test cases here; QA recommends creating BUG-SUB tickets under DEV-STORY-002 before TESTEXEC-001 can pass cleanly. None block TESTCASE-001 from Resolved (DoD only requires that cases reference real features and cover the ACs).
- Test execution (pass/fail) is the responsibility of TESTEXEC-001, not this ticket.
