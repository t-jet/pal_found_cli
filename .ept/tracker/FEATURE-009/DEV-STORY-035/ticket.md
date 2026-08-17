---
id: DEV-STORY-035
type: dev_story
title: Document all JSON formats and parameter variants in every skill file
status: Deployment
feature_request: FEATURE-009
epic: EPIC-009
created: 2026-08-13
updated: 2026-08-13
priority: High
assignee: tech-lead
reporter: ba
story_points: 13
release_notes: Document every JSON format and parameter variant for each namespace pal-found skill, verify against the CLI parser, and split oversized files within the 300-line limit.
---

## Description
Make each of the 18 final namespace skills self-contained for JSON inputs and parameter variants. Derive formats from the CLI parser and JSON handling, document accepted schemas and flag variants, match docs to implementation, and keep every skill file within the 300-line composition limit by splitting referenced parts when needed.

## Acceptance Criteria
- [ ] Every JSON-bearing option and accepted format is documented for all 18 namespace skills.
- [ ] Required, optional, positional, short, and choice variants match the parser.
- [ ] A user can use each tool from its skill file alone.
- [ ] Every skill and referenced part stays within the 300-line limit.
- [ ] Capability sections from DEV-STORY-034 remain intact.

## Related Documentation
- `.ept/docs/deliverables/business_design/BA-DES-010-business-design.md`
- `.ept/docs/deliverables/architecture/SA-DES-009-technical-design.md`
