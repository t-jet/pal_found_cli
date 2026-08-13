---
id: EPIC-009
type: epic
title: Harness-agnostic distribution and self-contained content of Foundry agent skills
status: Open
created: 2026-08-11
updated: 2026-08-11
priority: High
assignee: project-owner
reporter: project-owner
---

# EPIC-009: Harness-agnostic distribution and self-contained content of Foundry agent skills

## Description

End-to-end scenario: Foundry agent skills are distributed by cloning the foundry_cli_skills repository and copying the skills into any harness's .agents/skills folder. Each skill is self-contained: it requires the installed foundry_cli_tool Python package (with install instructions), includes a brief Palantir Foundry platform description (main skill) and capability descriptions (specific skills) taken from official Palantir Foundry web pages, and documents all JSON formats and allowed parameter variants so no external source is needed to use the CLI.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
