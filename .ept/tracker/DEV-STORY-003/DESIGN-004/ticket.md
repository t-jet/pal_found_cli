---
id: DESIGN-004
type: design
title: Design AccessControlGuard and PaginationHelper implementation plan
status: Closed
created: 2026-07-22
updated: 2026-07-22
priority: Critical
assignee: architect
reporter: architect
estimated_hours: 3
time_spent_hours: 3
---

## Scope
Prepare the implementation plan for AccessControlGuard and PaginationHelper under DEV-STORY-003.

Use DEV-STORY-003, QUESTION-006, SRS-001 FR-ACL/FR-PAG, SAD-001 common module guidance, ADR-001, ADR-005, ADR-007, and the canonical metadata allow-list as source material.

## Acceptance criteria
- Define the ACL precedence order: operation ENABLED=false, namespace ENABLED=false, operation READONLY override, namespace READONLY override, global READONLY, namespace METADATA_ONLY override, global METADATA_ONLY, default full access.
- Confirm first matching rule wins, ENABLED=false takes precedence over READONLY overrides, and METADATA_ONLY=true blocks writes.
- Define metadata allow-list parsing: use only canonical backticked SDK paths marked PERMITTED; deny unclassified operations by default.
- Define PaginationHelper behavior for --page-size, --page-token, --batch-pages, batch aggregation, max batch cap, SDK token propagation, and null/no-more-pages metadata.
- Specify stderr metadata output after # ---metadata-start--- per ADR-005.
- Split delivery work across DEV, UNITTEST, CODEREVIEW, TESTCASE, and TESTEXEC.
- Record risks and mitigations for ACL precedence, allow-list drift, SDK pagination behavior, and CLI flag coverage.
- Confirm scope fits one sprint and no DEVOPS subtask is needed because the change is limited to Python common modules, CLI integration, and tests.
