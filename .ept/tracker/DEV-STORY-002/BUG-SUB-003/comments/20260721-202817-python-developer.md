Subject: Fix plan
Created: 2026-07-21T20:28:17
Updated: 2026-07-21T20:28:17
---
## Fix plan

- Inspect async execution boundary around RetryHandler operations.
- Reproduce missing SIGINT/SIGTERM cancellation where platform support allows it.
- Add signal handling that cancels the active operation.
- Return structured cancellation error behavior with exit code 5.
- Add regression tests with platform guards if needed.
