---
id: WORK-006
type: workitem
title: Exercise offline novice-agent result interpretation
status: Closed
created: 2026-10-12
updated: 2026-10-12
priority: High
assignee: qa-engineer
reporter: project-manager
estimated_hours: 6
time_spent_hours: 2.0
---

# WORK-006: Exercise offline novice-agent result interpretation

## Scope

Independently exercise representative FEATURE-012 user journeys using copied skill folders, installed CLI help, and recorded or mocked Foundry responses. Cover pagination, errors, permissions, and asynchronous outcomes. Reconcile the closed TESTEXEC-055 claims against actual assertions.

## Acceptance criteria

- [x] Capture task prompts, selected namespace and command, valid inputs, predicted Foundry effect, mocked or recorded response, interpretation, and exact pass/fail for representative capability journeys.
- [x] Include empty-page pagination, local access-control and Foundry permission failures, malformed input, and asynchronous start plus final-state follow-up.
- [x] Preserve executable probe or reproducible commands and durable evidence; identify which statements are simulated rather than live tenant results.
- [x] Record defects or corrections in separate active tickets and retest them.
- [x] Reconcile TESTEXEC-055 zero-record PASS claims with this independent evidence without editing the archived ticket.

## Deliverables

- `.ept/docs/deliverables/qa/WORK-006-offline-novice-agent-evidence.md`
- Tracker comments linking evidence, defects, results, and remaining coverage.

## Related documentation

- `.ept/docs/deliverables/business_analysis/BA-ANA-013-offline-foundry-knowledge.md`
- `.ept/docs/deliverables/business_design/BA-DES-013-offline-foundry-skill-guidance.md`
- `.ept/docs/deliverables/architecture/SA-DES-012-offline-foundry-skill-technical-design.md`

Estimate: 6 hours. Parent: TASK-006. Owner: qa-engineer.
