---
id: DEVOPS-030
type: devops
title: Deploy+verify DEV-STORY-039 datasets/ontologies migration (tool parity 33/67, stale copies removed)
status: Closed
created: 2026-10-01
updated: 2026-10-01
priority: High
assignee: devops-engineer
reporter: devops-engineer
time_spent_hours: 1.0
---

# DEVOPS-030: Deploy+verify DEV-STORY-039 datasets/ontologies migration (tool parity 33/67, stale copies removed)

## Description

Deploy FEATURE-011 DEV-STORY-039 (migrate datasets/ontologies command implementations to the tool and remove stale skill copies) and verify in the target environment.

Deployment mechanism: the datasets/ontologies migration shipped in the same 4 FEATURE-011 skills commits (origin https://github.com/t-jet/pal_found_cli_skills.git, now at 7b1b99f) plus the parent gitlink bump. Tool-side single implementation is the already-published pal_found_cli v0.1.3.

Verification scope:
- Published pal_found_cli tool (v0.1.3) still exposes pal-found-datasets (33 ops) and pal-found-ontologies (67 ops) — tool-side single implementation, stale skill copies removed.
- Fresh recursive clone of public skills repo shows no datasets/ontologies Python script copies remain (0 .py under .agents/skills).
- Persist durable evidence as a comment on this ticket.

Rollback: restore stale copies from origin 4564e78 if a parity regression appears; no tool-side change was required.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
