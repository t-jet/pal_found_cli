Subject: In Progress→Resolved DoD — fix implemented and regression-tested (BUG-SUB-004)
Created: 2026-07-22T13:28:54
Updated: 2026-07-22T13:28:54
---
## Root cause (confirmed)

In `src/foundry_cli/common/error_serializer.py`, `_register_sdk_exceptions()` populated `_EXCEPTION_TO_EXIT_CODE` with the legacy `_SDK*Error` placeholders, stdlib exceptions, and SDK `PalantirRPCException` subclasses, but never registered `foundry_cli.common.access_control_guard.AccessControlError`. Since `AccessControlError` carries no HTTP status, `_classify_http_exception()` returned `None` and `serialize()` fell through to the `EXIT_USER_INPUT` (1) default. The `EXIT_ACCESS_CONTROL = 8` constant existed but was never selected. This matches the triage analysis in comment `20260721-232257-qa-engineer`.

## Fix applied

Registered `AccessControlError → EXIT_ACCESS_CONTROL (8)` inside `_register_sdk_exceptions()`, placed before the SDK best-effort block so it always runs.

The import is lazy (inside the function, wrapped in try/except) to avoid a circular dependency: `access_control_guard` imports `EXIT_ACCESS_CONTROL` from this module at its own import time. Lazy resolution is safe because `_register_sdk_exceptions()` runs only after `EXIT_ACCESS_CONTROL` is defined at module top level.

--- ADR-001 compliance: `AccessControlError` now maps to exit code 8 as required. ---

## Files changed

- `src/foundry_cli/common/error_serializer.py` — +17 lines in `_register_sdk_exceptions()`: AccessControlError registration block.
- `tests/test_exec_retry_error_output_log.py` — updated TC-ES-008 from a gap-analysis stub to a real regression assertion (AccessControlError → 8) and added TC-ES-008b covering the stdout error envelope (type, exit_code_name, message preservation, call_id).

## Defect reproduction (before vs after)

Reproduction command (PowerShell, PYTHONPATH=src), matching the triage scenario:

```
ErrorSerializer().serialize(AccessControlError('...', step=3))
```

- Before: `exit_code = 1` (UserInputError) — defect.
- After: `exit_code = 8` (AccessControlError) — correct per ADR-001.

Stderr NDJSON log now reads: `Serialized AccessControlError to exit code 8 (AccessControlError): ...` (was `... to exit code 1 (UserInputError)`).

## Regression-test evidence

Test file: `tests/test_exec_retry_error_output_log.py`, suite `TestErrorSerializer_TC`.

```
tests/test_exec_retry_error_output_log.py::TestErrorSerializer_TC::test_TC_ES_001_exit_code_1_user_input_error PASSED
tests/test_exec_retry_error_output_log.py::TestErrorSerializer_TC::test_TC_ES_002_exit_code_2_auth_error PASSED
tests/test_exec_retry_error_output_log.py::TestErrorSerializer_TC::test_TC_ES_003_exit_code_3_permission_denied PASSED
tests/test_exec_retry_error_output_log.py::TestErrorSerializer_TC::test_TC_ES_004_exit_code_4_not_found PASSED
tests/test_exec_retry_error_output_log.py::TestErrorSerializer_TC::test_TC_ES_005_exit_code_5_timeout PASSED
tests/test_exec_retry_error_output_log.py::TestErrorSerializer_TC::test_TC_ES_006_exit_code_6_server_error PASSED
tests/test_exec_retry_error_output_log.py::TestErrorSerializer_TC::test_TC_ES_007_exit_code_7_rate_limit PASSED
tests/test_exec_retry_error_output_log.py::TestErrorSerializer_TC::test_TC_ES_008_exit_code_8_access_control PASSED
tests/test_exec_retry_error_output_log.py::TestErrorSerializer_TC::test_TC_ES_008b_access_control_envelope_and_message PASSED
tests/test_exec_retry_error_output_log.py::TestErrorSerializer_TC::test_TC_ES_009_exit_code_9_configuration_error PASSED
tests/test_exec_retry_error_output_log.py::TestErrorSerializer_TC::test_TC_ES_010_error_envelope_schema PASSED

============================= 11 passed in 0.03s ==============================
```

All 11 ErrorSerializer tests pass. The existing exit-code mappings (1-7, 9) are unchanged — TC-ES-001 through TC-ES-007 and TC-ES-009 confirm no regression of other mappings. HTTP 409 still maps to EXIT_USER_INPUT (verified in TC-ES-008).

Import-time wiring verified (no circular import): `_EXCEPTION_TO_EXIT_CODE.get(AccessControlError) == EXIT_ACCESS_CONTROL` resolves True at module load.

## Pre-existing failures (unrelated, out of scope)

The LogSetup (TC-LS-*), Integration (TC-INT-002/003), RetryHandler (TC-RH-*), and access_control_guard write-classification tests fail on baseline (without this change) as well. They concern log formatting precision, retry delay parameter naming, and write-operation heuristics — separate concerns from this fix. TESTEXEC-001 covers their resolution.

## OWASP Top-10 self-review

The change adds one entry to an internal exception-to-exit-code map. No network calls, no input parsing, no auth changes, no new data flows, no secrets. No OWASP Top-10 exposure introduced.

## DoD status (In Progress → Resolved)

| Criterion | Status |
|---|---|
| Studied related documentation | MET (ADR-001, SRS FR-ERR-1/2/5, ADR-005, triage comment 232257) |
| Critical thinking applied | MET (circular-import constraint identified and handled with lazy import) |
| All required questions asked / terminal | MET (none needed — fix path clear) |
| Fix implemented and tested | MET |
| Root cause documented | MET (above) |
| Regression test performed | MET (11/11 ErrorSerializer tests pass) |
| Time reported in subtask frontmatter | MET (time_spent_hours=2.0) |
| All links registered | MET (LINK-00153 Blocks TESTEXEC-001, LINK-00157 ParentChild DEV-STORY-002) |

Ready to transition In Progress → Resolved. Over to @qa-engineer for verification and the Closed transition.
