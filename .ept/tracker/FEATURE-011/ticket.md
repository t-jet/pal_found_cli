---
id: FEATURE-011
type: feature
title: Skills must use CLI interface only and not contain separate python scripts
status: Closed
created: 2026-09-30
updated: 2026-10-01
priority: Medium
resolution: Done
assignee: ba
reporter: project-manager
---

# FEATURE-011: Skills must use CLI interface only and not contain separate python scripts

## Description

New requirement from Project Owner: Skills should NOT include separate Python scripts. If additional Python code or separate command implementations are needed, they must live in the tool itself (pal_found_cli_tool). Skills must use only the CLI interface and must not require Python knowledge.

Implications for the pal_found_cli_skills repository: the .agents/skills/pal-found-* skill folders currently contain launcher scripts (e.g. pal_found_admin_cli.py) that are thin wrappers importing from the tool. These should be removed or reworked so each skill consists solely of documentation (SKILL.md) that invokes the packaged CLI commands (pal-found-*).

This is a cross-cutting requirement affecting all 18+ namespace skills plus any command implementations moved into the tool. Requires analysis of the current launcher/entry-point design and the tool's console entry points.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
