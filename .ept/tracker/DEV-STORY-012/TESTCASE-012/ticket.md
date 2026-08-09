---
id: TESTCASE-012
type: testcase
title: Design Foundry Language Models CLI QA cases
status: Closed
created: 2026-08-09
updated: 2026-08-09
priority: High
assignee: qa-engineer
reporter: qa-engineer
estimated_hours: 4
time_spent_hours: 4
---

# TESTCASE-012: Design Foundry Language Models CLI QA cases

## Description

Design executable, traceable QA cases for both Language Models commands and every story criterion.

## Acceptance Criteria

- Cover both operations, every scalar and JSON input, exact SDK routing, validation, inference-write ACL modes and overrides, attribution, B3, retry/errors, output, privacy, and excluded features.
- Cover wheel/editable install, console and launcher help, packaged policy, and empty-working-directory execution.
- Define setup, data, command, stdout, stderr, exit, SDK/filesystem effects, cleanup, and expected result for every case.
- Obtain and record tech-lead approval before TESTEXEC-012 starts.

## Related Documentation

- DEV-STORY-012
- DESIGN-012

## Notes

Blocked on approved design.
