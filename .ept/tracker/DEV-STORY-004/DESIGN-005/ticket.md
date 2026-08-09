---
id: DESIGN-005
type: design
title: Finalize contracts for binary downloads, sessions, and tracing
status: Closed
created: 2026-07-27
updated: 2026-07-27
priority: High
assignee: tech-lead
reporter: manager
estimated_hours: 4
time_spent_hours: 4
---

# DESIGN-005: Finalize contracts for binary downloads, sessions, and tracing

## Description

Finalize implementation contracts for binary downloads, session persistence, tracing, configuration, and common integration.

## Acceptance Criteria

- [x] Decide component interfaces.
- [x] Decide unknown content-length and truncation reporting.
- [x] Decide filename and path containment plus atomic failure semantics.
- [x] Decide alias normalization, corruption handling, and concurrency policy.
- [x] Decide SDK-supported tracing context and retry span policy.
- [x] Document decisions in tracker comments and design deliverables.
- [x] Unblock implementation and test tasks.

## Related Documentation

- .ept/docs/deliverables/architecture/DESIGN-005-common-components.md
- .ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md
- .ept/docs/deliverables/architecture/SAD-001-foundry-cli.md
- .ept/docs/document_index.md

## Notes

Final contracts use bounded limit+1 streaming with nullable source size; normalized aliases with cross-process OS locks, atomic JSON, and nullable session_token; and SDK-native B3 propagation with context-token reset. Integration is defined, child estimates total 48h, and QUESTION-027 is Closed.
