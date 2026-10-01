---
id: DEV-STORY-038
type: dev_story
title: Convert the 16 thin-wrapper skills to documentation-only
status: Closed
feature_request: FEATURE-011
epic: EPIC-011
created: 2026-09-30
updated: 2026-10-01
priority: High
resolution: Done
assignee: python-developer
reporter: ba
component: skills
story_points: 5
release_notes: Remove the 16 thin-wrapper launcher scripts from the skills repository and rebase each SKILL.md to invoke the installed pal-found-* commands, so every namespace skill is documentation only with no Python scripts.
---

# DEV-STORY-038: Convert the 16 thin-wrapper skills to documentation-only

## Description

Convert the 16 thin-wrapper namespace skills under
`.agents/skills/pal-found-*` to the doc-only model. Remove each
`scripts/pal_found_<ns>_cli.py` launcher (10-26 lines each), keep the
`SKILL.md`, and rebase every command example to invoke the installed
`pal-found-<ns>` command by name. No skill folder may retain a `scripts/`
directory or any Python code.

Affected skills (16): pal-found-admin, pal-found-aip-agents, pal-found-audit,
pal-found-checkpoints, pal-found-connectivity, pal-found-data-health,
pal-found-filesystem, pal-found-functions, pal-found-language-models,
pal-found-media-sets, pal-found-models, pal-found-orchestration,
pal-found-sql-queries, pal-found-streams, pal-found-third-party-applications,
pal-found-widgets.

## Acceptance Criteria

- [ ] Given any of the 16 namespace skills, when the skill is inspected, then it contains no Python script and no `scripts/` directory (AC-D-012-01).
- [ ] Given a converted skill, when its `SKILL.md` is read, then every command example invokes a `pal-found-*` command and no example uses `python ..._cli.py` (AC-D-012-02).
- [ ] Given a user without Python knowledge, when they follow a skill, then they invoke the documented `pal-found-<ns>` command by name (AC-D-012-03).

## Related Documentation

- `.ept/docs/deliverables/business_design/BA-DES-012-doc-only-skills.md`
- `.ept/docs/deliverables/business_analysis/BA-ANA-012-doc-only-skills.md`
