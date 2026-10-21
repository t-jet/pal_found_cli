---
id: SA-DES-013
type: sa_subtask_design
title: Design self-contained Foundry development skill
status: Closed
created: 2026-10-04
updated: 2026-10-05
priority: High
assignee: architect
reporter: project-manager
component: skills
time_spent_hours: 1.0
---

# SA-DES-013: Design self-contained Foundry development skill

## Description
Detail pal-found-dev file architecture, official source and SDK evidence mapping, REST example contract, offline link and distribution constraints, cleanup migration, tests, review, and risk controls. Coordinate BA-DES-014 and Developer Story decomposition.

## Acceptance Criteria
- [x] Define affected skill, README, validation, CLI, and Foundry API interfaces and state which endpoint/command surfaces change.
- [x] Map all nine substantive coverage groups and the separate REST topic to owned local files and public source evidence.
- [x] Specify REST/SDK example, auth, pagination, error, output, and write-safety contracts.
- [x] Specify cleanup rules for internal documentation links and copy-folder instructions, including five inputs.md paths and the draft cross-skill link.
- [x] Define offline independent-folder distribution, tests, source review, nonfunctional limits, migration, rollback, and disjoint one-sprint story boundaries.
- [x] Deliver `.ept/docs/deliverables/architecture/SA-DES-013-foundry-development-skill-technical-design.md` and register it in `.ept/docs/document_index.md`.
- [ ] Obtain BA, lead developer, and Project Owner design approvals through Question tickets.

## Related Documentation
- `.ept/docs/deliverables/architecture/SA-ANA-014-foundry-development-skill-architecture.md`
- `.ept/docs/deliverables/business_analysis/BA-ANA-014-user-facing-foundry-skills.md`
- `.ept/docs/deliverables/business_design/BA-DES-014-user-facing-foundry-skills.md`
- `.ept/docs/customer_input/development-skill-coverage.md`
