---
id: BUG-SUB-020
type: bug_subtask
title: Source review matrix cites three URLs absent from mapped skill section
status: Closed
created: 2026-10-05
updated: 2026-10-05
priority: Medium
assignee: python-developer
reporter: qa-engineer
estimated_hours: 1
time_spent_hours: 0.25
---

# BUG-SUB-020: Source review matrix cites three URLs absent from mapped skill section

## Description

## Reproduction
Parse the 37 source-review rows in .ept/docs/deliverables/development/DEV-STORY-060-foundry-skill-source-review.md. For each row, compare its Official source URL with links in the mapped pal-found-dev file. Three rows fail: 5.1 Developer Console overview; 6 Widget lifecycle Custom Widgets overview; 7.2 Git branch settings.

## Expected
Every matrix row cites a URL present in its mapped skill section or explains equivalent source mapping.

## Actual
The three cited URLs are absent from applications-branching-security.md, although all three official pages resolve. Exact matrix check: 37 rows, 3 mismatches.

## Environment
Windows PowerShell, Python 3, local workspace 2026-10-05; no Foundry credentials. Found during TESTEXEC-060.

## Fix
Update matrix citations to exact relevant URLs already in the skill, or add the cited official URLs to correct skill sections if required for coverage. Recheck every matrix row. Severity Medium; affected local revision 45bc51d plus uncommitted FEATURE-013 work.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
