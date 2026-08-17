---
id: DEV-STORY-034
type: dev_story
title: Add capability descriptions to every specific skill with source references
status: Deployment
feature_request: FEATURE-008
epic: EPIC-009
created: 2026-08-13
updated: 2026-08-13
priority: High
assignee: tech-lead
reporter: ba
story_points: 8
release_notes: Add official-source-backed capability descriptions to all 18 namespace pal-found skills, matched to each operation set and reviewed for consistency.
---

## Description
Add a capability-description section to each of the 18 namespace skills in the final `.agents/skills/pal-found-*` tree. Use brief official Palantir sources, match each description to the actual operation set, record source URL and review date, and check for conflicting facts.

## Acceptance Criteria
- [ ] All 18 namespace skills contain a capability description.
- [ ] Each description matches the operations exposed by its launcher.
- [ ] Each description cites an official Palantir source URL and review date.
- [ ] A consistency review finds no conflicting capability facts.
- [ ] The change remains static skill content and preserves JSON/parameter sections.

## Related Documentation
- `.ept/docs/deliverables/business_design/BA-DES-009-business-design.md`
- `.ept/docs/deliverables/architecture/SA-DES-008-technical-design.md`
