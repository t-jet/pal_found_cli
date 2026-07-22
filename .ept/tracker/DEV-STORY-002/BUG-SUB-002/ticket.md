---
id: BUG-SUB-002
type: bug_subtask
title: 'BUG-SUB: RetryHandler missing HTTP 429/503-specific retry predicate (TC1.R3)'
status: Closed
created: 2026-07-04
updated: 2026-07-21
priority: Critical
assignee: python-developer
reporter: qa-engineer
component: src/foundry_cli/common/retry.py
time_spent_hours: 0.42
---

# BUG-SUB-002: RetryHandler missing HTTP 429/503-specific retry predicate (TC1.R3)

## Description

Discovered during TESTCASE-001 scenario TC1.R3. DEV-STORY-002 requires retry behavior for HTTP 429 and 503 only, but current RetryHandler behavior is described as using a broad `requests.RequestException` predicate. Evidence source: TESTCASE-001 comment `20260704-224649-qa-engineer`. Component: `src/foundry_cli/common/retry.py`.

## Acceptance Criteria

- [ ] RetryHandler retries HTTP 429 responses according to configured backoff settings.
- [ ] RetryHandler retries HTTP 503 responses according to configured backoff settings.
- [ ] RetryHandler does not retry unrelated request exceptions unless they map to the approved retryable conditions.
- [ ] Regression tests cover 429 retry, 503 retry, and non-retryable exception behavior.

## Related Documentation

- DEV-STORY-002 RetryHandler acceptance criteria
- SRS FR-ERR-3 and FR-ERR-4
- SAD-001 retry sequence
- ADR-005 Structured Log Format

## Notes

Triage correction only. No code changed in this handoff.
