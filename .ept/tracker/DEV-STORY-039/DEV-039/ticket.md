---
id: DEV-039
type: development
title: 'DEV-039: Remove stale datasets/ontologies skill copies; verify tool parity (33/67
  ops)'
status: Closed
created: 2026-10-01
updated: 2026-10-01
priority: High
assignee: tech-lead
reporter: tech-lead
estimated_hours: 8
time_spent_hours: 8
---

# DEV-039: DEV-039: Remove stale datasets/ontologies skill copies; verify tool parity (33/67 ops)

## Description

Implementation for DEV-STORY-039.

Scope per BA-DES-012 / SA-DES-011: delete .agents/skills/pal-found-datasets/scripts/pal_found_datasets_cli.py (467 lines) and .agents/skills/pal-found-ontologies/scripts/pal_found_ontologies_cli.py (442 lines); rebase both SKILL.md to invoke installed pal-found-datasets / pal-found-ontologies; verify tool-side parity with unchanged behavior (datasets 33 ops, ontologies 67 ops). No net-new tool command; all 18 pal-found-* stay installed. Deliverable in pal_found_cli_skills .agents/skills/.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
