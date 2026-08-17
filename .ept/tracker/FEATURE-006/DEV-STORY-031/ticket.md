---
id: DEV-STORY-031
type: dev_story
title: Migrate and rename all skills into the standard .agents/skills folder
status: QA
feature_request: FEATURE-006
epic: EPIC-009
created: 2026-08-13
updated: 2026-08-13
priority: High
assignee: tech-lead
reporter: ba
story_points: 8
release_notes: Move and rename the 19 skills into .agents/skills with pal-found names, updated frontmatter, launchers, references, and a rollback-safe legacy transition.
---

## Description
Move the 19 skills from `.claude/skills` into the canonical `.agents/skills` tree and apply the confirmed `pal-found` naming. Update frontmatter, launcher names, internal references, AGENTS.md, and distribution references while keeping one canonical copy and preserving rollback until discovery passes.

## Acceptance Criteria
- [ ] The final tree contains `pal-found` plus 18 `pal-found-*` skills under `.agents/skills`.
- [ ] Frontmatter, launcher names, and cross-references use the final names.
- [ ] Legacy content is read-only during migration and is removed or reduced to a pointer after verification.
- [ ] No CLI behavior, operations, or data change.
- [ ] Rollback preserves the last known-good skill tree.

## Related Documentation
- `.ept/docs/deliverables/business_design/BA-DES-007-business-design.md`
- `.ept/docs/deliverables/architecture/SA-DES-006-technical-design.md`
- `.ept/docs/deliverables/architecture/SA-DES-010-technical-design.md`
