---
id: DEV-STORY-030
type: dev_story
title: Verify skill discovery per harness and write onboarding instructions
status: QA
feature_request: FEATURE-006
epic: EPIC-009
created: 2026-08-13
updated: 2026-08-13
priority: High
assignee: tech-lead
reporter: ba
story_points: 5
release_notes: Verify discovery of 19 pal-found skills under .agents/skills for each supported harness and publish onboarding instructions for non-native discovery.
---

## Description
Verify harness discovery after the canonical 19-skill migration. Record native discovery, configured pointers, or manual wiring for each supported harness, and provide onboarding steps for harnesses that do not scan the standard path. Keep the legacy location read-only until verification passes.

## Acceptance Criteria
- [ ] Inventory identifies main `pal-found` plus 18 `pal-found-*` skills under `.agents/skills`.
- [ ] Discovery result and method are recorded for every supported harness.
- [ ] Non-native harnesses have exact onboarding steps and target paths.
- [ ] No skill content exists only under `.claude/skills` after migration.
- [ ] Evidence records commands, paths, and observed results.

## Related Documentation
- `.ept/docs/deliverables/business_design/BA-DES-007-business-design.md`
- `.ept/docs/deliverables/architecture/SA-DES-006-technical-design.md`
