---
id: BUG-SUB-003
type: bug_subtask
title: 'BUG-SUB: RetryHandler missing SIGINT/SIGTERM signal handling (TC1.R4)'
status: Closed
created: 2026-07-04
updated: 2026-07-21
priority: Critical
assignee: python-developer
reporter: qa-engineer
component: src/foundry_cli/common/retry.py
time_spent_hours: 0.33
---

# BUG-SUB-003: RetryHandler missing SIGINT/SIGTERM signal handling (TC1.R4)

## Description

Discovered during TESTCASE-001 scenario TC1.R4. DEV-STORY-002 and ADR-002 require SIGINT/SIGTERM to cancel the current operation and return structured timeout/cancellation behavior, but RetryHandler does not implement signal handling. Evidence source: TESTCASE-001 comment `20260704-224649-qa-engineer`. Component: `src/foundry_cli/common/retry.py`.

## Acceptance Criteria

- [ ] RetryHandler cancels the active async operation on SIGINT.
- [ ] RetryHandler cancels the active async operation on SIGTERM.
- [ ] Canceled operations produce structured JSON error output and exit code 5 per ADR-001 and ADR-002.
- [ ] Regression tests cover signal-triggered cancellation behavior where platform support allows it.

## Related Documentation

- DEV-STORY-002 RetryHandler acceptance criteria
- SRS FR-ASYNC-4
- ADR-001 Exit Code Taxonomy
- ADR-002 Per-Call Timeout Defaults

## Notes

Triage correction only. No code changed in this handoff.
