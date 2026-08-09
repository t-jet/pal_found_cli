---
id: BUG-SUB-005
type: bug_subtask
title: 'BUG-SUB: LogSetup/Integration TC-LS-001/002/003/004/006/007 + TC-INT-002/003 fail
  due to stderr_capture fixture / pytest FDCapture interaction'
status: Closed
created: 2026-07-22
updated: 2026-07-26
priority: Critical
assignee: qa-engineer
reporter: qa-engineer
time_spent_hours: 1
---

# BUG-SUB-005: BUG-SUB: LogSetup/Integration TC-LS-001/002/003/004/006/007 + TC-INT-002/003 fail due to stderr_capture fixture / pytest FDCapture interaction

## Description

# BUG-SUB-005: LogSetup/Integration test failures from `stderr_capture` fixture / pytest FDCapture interaction

## Parent
DEV-STORY-002 (containing TESTEXEC-001).

## Severity
High — blocks 8 of the 13 currently-failing TESTEXEC-001 scenarios, preventing a clean QA pass; not a runtime defect.

## Affected Version
- Repo: foundry_cli (DEV-STORY-002 implementation: `src/foundry_cli/common/log_setup.py`, `src/foundry_cli/common/output_formatter.py`).
- Test files: `tests/test_exec_retry_error_output_log.py` (suites `TestLogSetup_TC`, `TestIntegration_TC`).
- Found during: TESTEXEC-001 execution on 2026-07-22.

## Affected test cases (evidence from `pytest -v --tb=short`)
- `TestLogSetup_TC::test_TC_LS_001_ndjson_format_single_json_line` — `IndexError: list index out of range` (StringIO empty).
- `TestLogSetup_TC::test_TC_LS_002_required_fields_present` — `json.JSONDecodeError: Expecting value` (StringIO empty).
- `TestLogSetup_TC::test_TC_LS_003_log_level_filtering` — `assert 'warning msg' in ''` (StringIO empty).
- `TestLogSetup_TC::test_TC_LS_004_env_var_log_level_override` — `assert 'debug from env' in ''` (StringIO empty).
- `TestLogSetup_TC::test_TC_LS_006_context_extra_fields_in_log` — `json.JSONDecodeError` (StringIO empty).
- `TestLogSetup_TC::test_TC_LS_007_metadata_separator_and_emit` — `assert '# ---metadata-start---' in ''` (StringIO empty).
- `TestIntegration_TC::test_TC_INT_002_stderr_separation` — `assert 'error' in ''` (stdout StringIO empty; data found on real stderr).
- `TestIntegration_TC::test_TC_INT_003_full_pipeline` — `assert 'Pipeline completed with error' in ''` (data found on real stderr).

In all failing cases the pytest `Captured stderr call` section shows the expected NDJSON line / separator / payload — i.e. the product emitted the correct bytes, but they went to the real stderr, not the test's StringIO.

## Steps to Reproduce
1. From repo root: `$env:PYTHONPATH="src"; python -m pytest tests/test_exec_retry_error_output_log.py::TestLogSetup_TC -v --tb=short`.
2. Observe every suite-4 test except `TC-LS-005` fails with empty-StringIO asserts.
3. Failure reproduces in isolation too: `python -m pytest tests/test_exec_retry_error_output_log.py::TestLogSetup_TC::test_TC_LS_001_ndjson_format_single_json_line -v --tb=long` — same IndexError.

## Expected Behavior
LogSetup tests must reliably capture NDJSON output on stderr and assert on it, so that ADR-005 conformance (schema `{"ts","level","logger","msg"}` + optional fields, separator `# ---metadata-start---`, level filtering, env-var override) is verified by CI.

## Actual Behavior
The `stderr_capture` / `stdout_capture` fixtures replace `sys.stderr`/`sys.stdout` with a `StringIO`, but `logging.StreamHandler(sys.stderr)` installed by `LogSetup.configure()` and the direct `sys.stderr.write(...)` calls in `emit_metadata_separator`/`emit_metadata` end up writing to pytest's captured real fd; the test-side StringIO stays empty.

## Root Cause (QA diagnosis; developer to confirm during fix)
Standalone reproduction OUTSIDE pytest confirms LogSetup behaves correctly (`h.stream is cap → True`, StringIO populated). Under pytest the global FDCapture layer swaps `<stderr>` fd 2, so by the time the test's own fixture swaps `sys.stderr` to a StringIO, the logging handler (which reads `sys.stderr` fresh at `configure()` time) still binds to the still-swapped real-fd object owned by pytest's capture. The fixture interaction is faulty.

## Recommended Fix
- Replace the manual `sys.stderr = io.StringIO()` swap with pytest's built-in `capsys` (captures at the `sys.stdout`/`sys.stderr` attribute level) or `capfd` (captures at the file-descriptor level — recommended when the code under test writes through the logging module or calls `print(..., file=sys.stderr)`).
- Alternatively, parametrise the LogSetup handler to accept an injectable stream for testability.
- The product code itself does NOT need changes for Bucket A.

## Evidence
- Full pytest run with per-case status: `TESTEXEC-001-execution-log.md` (sections 1–4).
- Standalone repro output captured 2026-07-22T20:20Z and 20:21Z.

## Test Execution Reference
TESTEXEC-001 (DEV-STORY-002 QA test execution). Relates to closed QUESTION-014 (LogSetup stderr-only per ADR-005) — the ADR-005 contract itself is satisfied; this is purely a test-harness issue.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
