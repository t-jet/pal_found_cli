---
id: UNITTEST-023
type: unittest
title: 'UNITTEST-023: Verification of the foundry/ knowledge skill content'
status: Closed
created: 2026-08-11
updated: 2026-08-11
priority: High
assignee: python-developer
reporter: architect
estimated_hours: 12
time_spent_hours: 12
---

# UNITTEST-023: UNITTEST-023: Verification of the foundry/ knowledge skill content

## Description

# UNITTEST-023: Verification of the foundry/ knowledge skill content

## Description

Verification sub-task for the documentation story DEV-STORY-023. For this documentation story, UNITTEST performs content-accuracy verification of the authored `foundry/` knowledge skill against the authoritative sources.

## Acceptance Criteria

- [x] Verify all 20 namespace entries and operation counts in the knowledge skill match the canonical env-var reference, the metadata allow-list, and test-asserted OP_SPECS counts
- [x] Verify auth guide correctness (UserTokenAuth from FOUNDRY_TOKEN, FOUNDRY_HOSTNAME via AsyncClientFactory, ADR-006 search order)
- [x] Verify access control guide correctness (8-step precedence per ADR-007, control variable naming patterns)
- [x] Verify TOON explanation matches ADR-004 rule
- [x] Verify exit-code taxonomy matches ADR-001
- [x] Verify widgets known-limitation statement matches QUESTION-043 decision
- [x] Markdown lint clean on all authored files
- [x] All verification results documented as a comment on this ticket
- [x] Time reported in sub-task frontmatter

## Deliverables

- Verification report comment on this ticket

## Notes

No code under test — content accuracy verification against authoritative references.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
