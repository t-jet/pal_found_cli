---
id: TESTCASE-004
type: testcase
title: Design QA cases for ACL and pagination
status: New
created: 2026-07-22
updated: 2026-07-22
priority: Critical
assignee: qa-engineer
reporter: architect
estimated_hours: 4
---

## Scope
Design QA cases for command-line ACL and pagination behavior.

## Acceptance criteria
- Write Given/When/Then cases for ACL precedence conflicts, including ENABLED=false precedence and READONLY=false overrides.
- Cover global metadata-only behavior: datasets.file.content denied, datasets.dataset.get permitted by allow-list, read_table denied, and writes blocked.
- Cover metadata allow-list parsing, including canonical backticked SDK paths and PERMITTED status only.
- Cover pagination CLI behavior for --page-size, --page-token, and --batch-pages.
- Include invalid and zero page sizes, max batch cap, no next token, stderr metadata separator, and SDK pagination propagation.
- Verify every paginated operation exposes --page-size, --page-token, and --batch-pages.
- Mark smoke tests that can run without external dependencies and label environment-dependent cases clearly.
