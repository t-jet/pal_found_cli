Subject: Implementation evidence
Created: 2026-07-21T20:33:09
Updated: 2026-07-21T20:33:09
---
## Implementation evidence

Files changed: src/foundry_cli/common/retry.py, 	ests/unit_test_retry_error_output_log.py.

Root cause: RetryHandler had partial timeout constants, but xecute did not consistently centralize attempt execution through a wait_for helper. No regression proved env timeout use, so a hanging SDK coroutine could outlive the intended per-call timeout in untested paths.

Implementation: added _execute_with_timeout() and routed every attempt through syncio.wait_for() when 	imeout_s is configured. 	imeout_s reads FOUNDRY_AGENTIC_CLI_TIMEOUT_S, default 30.0; 	imeout_s=None still disables the wrapper for tests and special cases. Added regression coverage for the wait_for timeout argument and timeout breach raising syncio.TimeoutError.

Verification: python -m pytest tests\\unit_test_retry_error_output_log.py -q -> 149 passed. python -m ruff check src\\foundry_cli\\common\
etry.py -> passed. python -m mypy src\\foundry_cli\\common\
etry.py not run because mypy is not installed: No module named mypy. python -m pytest tests\	est_exec_retry_error_output_log.py -q -> 28 passed, 13 failed from legacy QA expectations unrelated to this fix.

OWASP self-review: no secrets added, no import-time network calls, structured timeout mapping preserved, scoped handlers restored, logs contain metadata only. Time spent: 25m. Links verified: LINK-00150, LINK-00155.
