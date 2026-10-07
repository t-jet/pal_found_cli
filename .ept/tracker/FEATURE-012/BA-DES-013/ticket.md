---
id: BA-DES-013
type: ba_subtask_design
title: 'BA design: Offline Foundry skill guidance'
status: Closed
created: 2026-10-03
updated: 2026-10-03
priority: Medium
assignee: ba
reporter: project-manager
component: skills
time_spent_hours: 2.0
---

# BA design: Offline Foundry skill guidance

## Purpose

Turn the approved BA-ANA-013 requirements and SA-ANA-013 constraints into detailed, reviewable business design for the distributed Foundry skills. Keep the design within FEATURE-012 scope and the QUESTION-152 local-reference decision.

## Acceptance criteria

- Produce a business design deliverable under `.ept/docs/deliverables/business_design/` that traces BR-012-01..11 and AC-012-01..13 into detailed skill content and review criteria.
- Specify the end-to-end agent flow from Foundry primer through capability selection, input preparation, invocation, and result interpretation for every supported operation.
- Define the content and acceptance checks for each operation's effect, parameter meaning, side effects, results, errors, and offline references.
- Describe distribution and migration of the documented skills without changing installed CLI behavior; mark UI and new API design as not applicable where justified.
- Create and link Developer Stories under FEATURE-012 for the implementation scope, and obtain required Project Owner, architect, and lead developer reviews.
