---
id: BUG-SUB-003
type: bug_subtask
title: 'BUG-SUB: RetryHandler missing SIGINT/SIGTERM signal handling (TC1.R4)'
status: New
created: 2026-07-04
updated: 2026-07-04
priority: Medium
assignee: developer
reporter: qa-engineer
---

# BUG-SUB-003: BUG-SUB: RetryHandler missing SIGINT/SIGTERM signal handling (TC1.R4)

## Description

Discovered during TESTCASE-001 (TC1.R4). DEV-STORY-002 AC requires SIGINT/SIGTERM signal handling but RetryHandler does not implement it. Source: TESTCASE-001 comment 20260704-224649-qa-engineer. Component: src/foundry_cli/common/retry.py.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
