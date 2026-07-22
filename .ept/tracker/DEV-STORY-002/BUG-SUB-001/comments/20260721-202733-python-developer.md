Subject: Fix plan
Created: 2026-07-21T20:27:33
Updated: 2026-07-21T20:27:33
---
## Fix plan

- Inspect RetryHandler call path and current SDK await boundary.
- Reproduce missing timeout with a hanging coroutine regression test.
- Read timeout from FOUNDRY_AGENTIC_CLI_TIMEOUT_S with 30 seconds as default.
- Wrap awaited SDK call with asyncio.wait_for.
- Convert timeout breach to structured error behavior with exit code 5.
- Add regression tests for timeout success and timeout breach.
