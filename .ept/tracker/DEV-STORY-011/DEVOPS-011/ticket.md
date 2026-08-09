---
id: DEVOPS-011
type: devops
title: Package and verify Foundry AIP Agents entry points
status: Closed
created: 2026-08-09
updated: 2026-08-09
priority: High
assignee: devops-engineer
reporter: workflow-mgr
estimated_hours: 3
time_spent_hours: 3
---

# DEVOPS-011: Package and verify Foundry AIP Agents entry points

## Description

## Description
Package and verify the Foundry AIP Agents console entry, Claude launcher, allow-list, and install behavior. This task is required because the story adds package and runtime entry points that must work outside the repository checkout.

## Acceptance Criteria
- Clean wheel and editable installations succeed.
- Console entry and Claude launcher help work from an empty working directory.
- The packaged metadata allow-list is available outside the repository checkout.
- CI, lint, type, test, and security gates pass on supported Python versions.
- Verification and rollback steps are documented.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
