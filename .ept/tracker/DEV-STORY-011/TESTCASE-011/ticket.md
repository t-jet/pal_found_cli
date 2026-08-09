---
id: TESTCASE-011
type: testcase
title: Design Foundry AIP Agents CLI QA cases
status: Closed
created: 2026-08-09
updated: 2026-08-09
priority: High
assignee: qa-engineer
reporter: workflow-mgr
estimated_hours: 6
time_spent_hours: 6
---

# TESTCASE-011: Design Foundry AIP Agents CLI QA cases

## Description

Design traceable QA cases for every command and DEV-STORY-011 acceptance criterion, including observable output, exit codes, and filesystem effects. Tech-lead reviews the completed test cases and records approval before TESTEXEC-011 may start.

## Acceptance Criteria

- Cases cover all 15 SDK operations, local purge, and every story acceptance criterion.
- Session cancel cases verify optional --response scalar markdown forwarding and rejection of the obsolete response-json option.
- Each case defines stdout, stderr, exit code, filesystem effects, setup, and expected result.
- Tier 3 cases cover the exact six permitted and nine blocked operations plus purge policy.
- Pagination, eager bytes, alias expiry and collision, package installation, and redaction are covered.
- Cases remain traceable to the story, DESIGN-011, and implementation routes.
- Tech-lead reviews the full test-case set and records approval in this ticket before TESTEXEC-011 starts.
- The existing TESTCASE-011 Blocks TESTEXEC-011 link remains until approval and test-case completion.

## Related Documentation

- .ept/docs/deliverables/architecture/DESIGN-011-aip-agents-cli.md
- DEV-STORY-011

## Notes

Tracker configuration has no reviewer field; reviewer assignment and approval are recorded in comments.
