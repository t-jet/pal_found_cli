---
id: BUG-SUB-001
type: bug_subtask
title: 'BUG-SUB: RetryHandler missing asyncio.wait_for() timeout (TC1.R2)'
status: Closed
created: 2026-07-04
updated: 2026-07-21
priority: Critical
assignee: python-developer
reporter: qa-engineer
component: src/foundry_cli/common/retry.py
time_spent_hours: 0.42
---

# BUG-SUB-001: RetryHandler missing asyncio.wait_for() timeout (TC1.R2)

## Description

Discovered during TESTCASE-001 scenario TC1.R2. DEV-STORY-002 requires each SDK call to be wrapped in `asyncio.wait_for()` with timeout from `FOUNDRY_AGENTIC_CLI_TIMEOUT_S`, but RetryHandler does not implement that timeout wrapper. Evidence source: TESTCASE-001 comment `20260704-224649-qa-engineer`. Component: `src/foundry_cli/common/retry.py`.

## Acceptance Criteria

- [ ] RetryHandler wraps SDK async calls in `asyncio.wait_for(coro, timeout=timeout_s)`.
- [ ] Timeout value comes from `FOUNDRY_AGENTIC_CLI_TIMEOUT_S`, defaulting to 30 seconds per ADR-002.
- [ ] Timeout breach returns structured timeout error behavior aligned to DEV-STORY-002 and ADR-001 exit code 5.
- [ ] Regression tests cover timeout success and timeout breach paths.

## Related Documentation

- DEV-STORY-002 RetryHandler acceptance criteria
- SRS FR-ASYNC-3 and FR-ERR-1
- ADR-001 Exit Code Taxonomy
- ADR-002 Per-Call Timeout Defaults

## Notes

Triage correction only. No code changed in this handoff.
