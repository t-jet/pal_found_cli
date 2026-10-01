---
id: EPIC-011
type: epic
title: Skills are documentation-only and rely on the packaged CLI
status: Done
created: 2026-09-30
updated: 2026-10-01
priority: High
resolution: Done
assignee: ba
reporter: ba
component: skills
---

# EPIC-011: Skills are documentation-only and rely on the packaged CLI

## Description

# EPIC-011: Skills are documentation-only and rely on the packaged CLI

## Description

End-to-end scenario covering the delivered skill-content model for the Foundry agent skills: each skill in `pal_found_cli_skills` consists solely of documentation (a `SKILL.md` file) that invokes the packaged CLI commands (`pal-found-*`). No separate Python scripts live inside the skill folders. Any additional Python code or standalone command implementation must live in the tool itself (`pal_found_cli_tool`), exposed through its console entry points.

## Scope

- Transform all 18+ namespace skills to a documentation-only content model: remove or rework the current launcher scripts (e.g. `pal_found_admin_cli.py`) so each skill is only a `SKILL.md` that invokes the CLI.
- Migrate command implementations that must stay as Python/CLI code into `pal_found_cli_tool` and expose them via `pal-found-*` entry points.
- Rely on the installed/packaged CLI for all skill behavior; skills require no Python knowledge.
- Deliver a consistent, human-maintainable skill repository where documentation is the deliverable and command logic lives in the tool.

## Exit criteria

- All skills are documentation-only (no Python scripts in skill folders).
- Any remaining command implementation lives in `pal_found_cli_tool`.
- Skills invoke only the packaged `pal-found-*` CLI commands.
- EPIC-011 is linked to FEATURE-011 via a bidirectional FeatureContains link.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
