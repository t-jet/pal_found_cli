---
id: BUG-SUB-002
type: bug_subtask
title: 'BUG-SUB: RetryHandler missing HTTP 429/503-specific retry predicate (TC1.R3)'
status: New
created: 2026-07-04
updated: 2026-07-04
priority: High
assignee: developer
reporter: qa-engineer
---

# BUG-SUB-002: BUG-SUB: RetryHandler missing HTTP 429/503-specific retry predicate (TC1.R3)

## Description

Discovered during TESTCASE-001 (TC1.R3). DEV-STORY-002 AC requires HTTP 429/503-specific retry predicate but impl uses broad requests.RequestException. Source: TESTCASE-001 comment 20260704-224649-qa-engineer. Component: src/foundry_cli/common/retry.py.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
