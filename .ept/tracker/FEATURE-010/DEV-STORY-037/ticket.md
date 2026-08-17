---
id: DEV-STORY-037
type: dev_story
title: Documentation sweep, migration notes and behaviour verification for the rename
status: Deployment
feature_request: FEATURE-010
epic: EPIC-010
created: 2026-08-13
updated: 2026-08-14
priority: High
assignee: tech-lead
reporter: ba
story_points: 8
release_notes: Complete the rename documentation sweep, publish migration guidance, and verify unchanged behaviour and renamed entry points after the coordinated migration.
---

## Description
Run the final documentation sweep, publish migration guidance, and verify unchanged behavior after the coordinated rename. Cover indexes, build/test/release references, repository and package migration, skill references, redirects, rollback, full gates, and all 18 renamed entry points. Do not redo migration work owned by DEV-STORY-031 or DEV-STORY-036.

## Acceptance Criteria
- [ ] In-scope docs and indexes use the confirmed mapping, with old names retained only where historical or explicitly out of scope.
- [ ] Migration notes cover repositories, package installs, commands, skill references, redirects, and rollback.
- [ ] Full test, static, security, and coverage gates pass.
- [ ] All 18 renamed entry points smoke-run successfully.
- [ ] Evidence is tied to the final commit and final namespace.

## Related Documentation
- `.ept/docs/deliverables/business_design/BA-DES-011-business-design.md`
- `.ept/docs/deliverables/architecture/SA-DES-010-technical-design.md`
