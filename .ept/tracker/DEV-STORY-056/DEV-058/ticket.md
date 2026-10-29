---
id: DEV-058
type: development
title: Remove internal references and copy guidance
status: Closed
created: 2026-10-05
updated: 2026-10-05
priority: High
assignee: python-developer
reporter: project-manager
estimated_hours: 5
time_spent_hours: 1
---

# DEV-058: Remove internal references and copy guidance

## Scope
Edit existing pal-found and 18 namespace skill folders only. Preserve platform explanations, 351 CLI operation records, examples, and local navigation.

## Acceptance criteria
- No distributed skill page directs readers to ADRs, tickets, BA/SA deliverables, local SDK source paths, or other project authoring artifacts.
- No distributed skill page instructs readers to copy an entire skill folder or references folder.
- All local links still resolve inside their skill folder; public Palantir links and useful CLI install guidance remain.
- Existing operation and documentation gates pass, and changed Markdown has no whitespace errors.
- DEV-058 records changed files and verification evidence before code review.
