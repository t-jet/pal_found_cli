---
id: BUG-SUB-004
type: bug_subtask
title: 'BUG-SUB: ErrorSerializer exit code 8 (AccessControlError) unreachable via serialize()
  (TC2.R1)'
status: New
created: 2026-07-04
updated: 2026-07-04
priority: High
assignee: developer
reporter: qa-engineer
---

# BUG-SUB-004: BUG-SUB: ErrorSerializer exit code 8 (AccessControlError) unreachable via serialize() (TC2.R1)

## Description

Discovered during TESTCASE-001 (TC2.R1). DEV-STORY-002 AC requires exit code 8 for AccessControlError but it is unreachable via serialize(). Source: TESTCASE-001 comment 20260704-224649-qa-engineer. Component: src/foundry_cli/common/error_serializer.py.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
