---
id: BUG-SUB-015
type: bug_subtask
title: 'SEC-2: public repositories do not consistently ignore local credential files'
status: Closed
created: 2026-08-17
updated: 2026-08-17
priority: High
assignee: python-developer
reporter: qa-engineer
time_spent_hours: 0.42
---

# BUG-SUB-015: SEC-2: public repositories do not consistently ignore local credential files

## Description

PUB-TC-014 failed during TESTEXEC-025 on 2026-08-17. Reproduce from a clean checkout of each canonical repository with: git check-ignore -v -- .env qa-private-key.pem. Actual: the root and tool repositories ignore .env, the skills repository does not, and none of the three ignores the PEM-named fixture. No live credentials are tracked. Expected: all three repositories ignore both local environment files and private-key or certificate containers. The fix must make .env handling consistent, add patterns for *.pem, *.key, *.p12, and *.pfx while allowing documented safe examples, and add automated regression coverage across all three repositories. Environment: Windows 10.0.26200, PowerShell 7.6.5, Git 2.54, public heads root c2c0f741, tool 370c971b, skills 34b6c404. This defect blocks TESTEXEC-025 completion.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
