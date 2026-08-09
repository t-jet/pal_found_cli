---
id: DEVOPS-007
type: devops
title: 'DEV-STORY-006 DEVOPS: package/verify foundry-filesystem console entry point install'
status: Closed
created: 2026-07-29
updated: 2026-07-29
priority: High
assignee: architect
reporter: architect
estimated_hours: 3
time_spent_hours: 3
---

# DEVOPS-007: DEV-STORY-006 DEVOPS: package/verify foundry-filesystem console entry point install

## Description

**Scope**: Verify the packaged `foundry-filesystem` console script installs (`pip install -e .`) and runs (`foundry-filesystem --help` → exit 0). Confirm Skill package present under `.claude/skills/foundry-filesystem/`.

**Acceptance Criteria**: Given/When/Then — `foundry-filesystem --help` returns exit 0; package importable; entry point registered in pyproject.toml `[project.scripts]`; skill SKILL.md present with frontmatter. Estimated 3h.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
