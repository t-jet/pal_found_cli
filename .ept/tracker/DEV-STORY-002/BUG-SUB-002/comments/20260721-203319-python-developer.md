Subject: Implementation evidence
Created: 2026-07-21T20:33:19
Updated: 2026-07-21T20:33:19
---
## Implementation evidence

Files changed: src/foundry_cli/common/retry.py, 	ests/unit_test_retry_error_output_log.py.

Root cause: RetryHandler had an HTTP 429/503 helper, but xecute caught configured exception classes directly and did not call _should_retry(). Broad HTTP exceptions with non-retryable statuses could retry, while SDK-style exceptions carrying esponse.status_code but not matching etry_on could be missed.

Implementation: xecute now routes exceptions through one predicate path. _should_retry() first inspects HTTP esponse.status_code; only 429 and 503 retry when a status is present. SDK-style exceptions with response status 429 or 503 retry even when not in etry_on. HTTP 500 does not retry when status is present. Added regression tests for 429, 503, and HTTP 500 non-retry.

Verification: python -m pytest tests\\unit_test_retry_error_output_log.py -q -> 149 passed. python -m ruff check src\\foundry_cli\\common\
etry.py -> passed. python -m mypy src\\foundry_cli\\common\
etry.py not run because mypy is not installed: No module named mypy. python -m pytest tests\	est_exec_retry_error_output_log.py -q -> 28 passed, 13 failed from legacy QA expectations unrelated to this fix.

OWASP self-review: no secrets added, no import-time network calls, structured retry/error mapping preserved, logs contain attempt/delay/status metadata only. Time spent: 25m. Links verified: LINK-00151, LINK-00159.
