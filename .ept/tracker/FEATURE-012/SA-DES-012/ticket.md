---
id: SA-DES-012
type: sa_subtask_design
title: 'SA design: Offline Foundry skill guidance'
status: Closed
created: 2026-10-03
updated: 2026-10-03
priority: Medium
assignee: architect
reporter: project-manager
component: skills
time_spent_hours: 1.5
---

# SA design: Offline Foundry skill guidance

## Purpose

Produce the technical design for FEATURE-012 from the approved BA-ANA-013 and SA-ANA-013 analyses. Specify how 19 distributed skill entry points and any packaged local Markdown parts provide complete offline Foundry context while execution stays in installed `pal-found-*` commands.

## Acceptance criteria

- Produce a technical design deliverable under `.ept/docs/deliverables/architecture/` covering skill content layout, navigation, packaging, source traceability, and migration steps.
- Define an evidence-backed coverage inventory for every supported CLI operation, including Foundry effect, parameters, results, failures, and material side effects.
- Specify checks for operation coverage, local-link integrity after distribution, semantic accuracy, and offline use; distinguish unsupported catalogue entries.
- Identify affected interfaces, non-functional requirements, rollout and rollback steps, and any infrastructure change or justified absence of one.
- Coordinate with BA-DES-013 and obtain required Project Owner and BA reviews before closure.
