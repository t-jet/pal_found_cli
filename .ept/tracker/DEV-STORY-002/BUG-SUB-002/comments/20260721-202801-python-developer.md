Subject: Fix plan
Created: 2026-07-21T20:28:01
Updated: 2026-07-21T20:28:01
---
## Fix plan

- Inspect RetryHandler retry predicate and current error types.
- Reproduce current HTTP 429 and 503 behavior.
- Add predicate that retries only HTTP 429 and 503 under existing backoff config.
- Confirm unrelated request exceptions do not retry.
- Add regression tests for 429 retry, 503 retry, and non-retryable behavior.
