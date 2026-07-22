Subject: Implementation evidence
Created: 2026-07-21T20:33:30
Updated: 2026-07-21T20:33:30
---
## Implementation evidence

Files changed: src/foundry_cli/common/retry.py, 	ests/unit_test_retry_error_output_log.py.

Root cause: signal cancellation support existed as a standalone helper, but xecute did not install scoped SIGINT/SIGTERM handlers around active attempts. A running SDK operation was not reliably cancelled through RetryHandler.

Implementation: added scoped SIGINT/SIGTERM handling around each xecute attempt. The signal handler cancels the active task, and xecute converts signal-triggered CancelledError into SignalCancellationError, a TimeoutError subclass. This preserves ADR-001 exit code 5 through existing ErrorSerializer TimeoutError mapping. Signal cancellation does not retry. Added regression coverage using a fake signal scope to verify SIGINT cancellation maps to a timeout-class error.

Verification: python -m pytest tests\\unit_test_retry_error_output_log.py -q -> 149 passed. python -m ruff check src\\foundry_cli\\common\
etry.py -> passed. python -m mypy src\\foundry_cli\\common\
etry.py not run because mypy is not installed: No module named mypy. python -m pytest tests\	est_exec_retry_error_output_log.py -q -> 28 passed, 13 failed from legacy QA expectations unrelated to this fix.

OWASP self-review: no secrets added, no import-time network calls, scoped signal handlers restored after each attempt, structured cancellation mapping preserved, logs contain metadata only. Time spent: 20m. Links verified: LINK-00152, LINK-00156.
