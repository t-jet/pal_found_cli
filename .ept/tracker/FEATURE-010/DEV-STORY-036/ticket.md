---
id: DEV-STORY-036
type: dev_story
title: Rename package, commands, skill folders and repositories per confirmed mapping
status: Deployment
feature_request: FEATURE-010
epic: EPIC-010
created: 2026-08-13
updated: 2026-08-13
priority: High
assignee: tech-lead
reporter: ba
story_points: 13
release_notes: Rename repositories, package, distribution, commands, and skill identifiers to the confirmed pal_found_/pal-found- mapping while preserving behaviour and coordinating shared skill-tree work.
---

## Description
Apply the confirmed `pal_found_` and `pal-found-` mapping to repositories, package/import names, distribution metadata, commands, CI and release references, and the coordinated skill rename. Preserve operations, behavior, data, authentication, ACLs, output, exit codes, retry, and tracing. DEV-STORY-031 owns the physical skill-tree migration.

## Acceptance Criteria
- [ ] Repository and submodule names use `pal_found_cli`, `pal_found_cli_tool`, and `pal_found_cli_skills`.
- [ ] Package/import and distribution metadata use `pal_found_cli`.
- [ ] Public entry points and skill identifiers use `pal-found-`.
- [ ] CI, release, coverage, tests, and references use the confirmed mapping.
- [ ] Out-of-scope SDK and environment identifiers remain unchanged.
- [ ] Full behavior and rollback checks are defined; no partial rename ships.

## Related Documentation
- `.ept/docs/deliverables/business_design/BA-DES-011-business-design.md`
- `.ept/docs/deliverables/architecture/SA-DES-010-technical-design.md`
