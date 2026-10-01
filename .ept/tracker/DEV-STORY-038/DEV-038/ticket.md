---
id: DEV-038
type: development
title: 'DEV-038: Convert 16 thin-wrapper skills to doc-only (remove scripts, rebase SKILL.md,
  add install-requirement)'
status: Closed
created: 2026-10-01
updated: 2026-10-01
priority: High
assignee: python-developer
reporter: tech-lead
estimated_hours: 12
time_spent_hours: 12
---

# DEV-038: DEV-038: Convert 16 thin-wrapper skills to doc-only (remove scripts, rebase SKILL.md, add install-requirement)

## Description

Implementation for DEV-STORY-038.

Scope per BA-DES-012 / SA-DES-011: for each of the 16 namespace skills (admin, aip-agents, audit, checkpoints, connectivity, data-health, filesystem, functions, language-models, media-sets, models, orchestration, sql-queries, streams, third-party-applications, widgets): delete scripts/pal_found_<ns>_cli.py, rebase SKILL.md so every command example invokes the installed pal-found-<ns> command (no 'python ..._cli.py'), and add the install-requirement block (pal_found_cli package dep; one-line conda '-c t-jet' / pip / uv per QUESTION-149). No skill folder retains a scripts/ dir or any Python. Deliverable in pal_found_cli_skills .agents/skills/.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
