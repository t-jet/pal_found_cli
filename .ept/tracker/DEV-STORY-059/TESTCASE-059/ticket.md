---
id: TESTCASE-059
type: testcase
title: Specify REST guide acceptance scenarios
status: Closed
created: 2026-10-05
updated: 2026-10-05
priority: High
assignee: qa-engineer
reporter: project-manager
estimated_hours: 2
time_spent_hours: 0.1
---

## Scope
Define QA cases for DEV-STORY-059 and AC-D-014-05/06/07.

## Acceptance criteria
- Given direct HTTP, Python SDK, OSDK, and CLI choices, when a reader selects one, then scope and supported operations stay distinct.
- Given the read-only dataset example, when checked against official API and local SDK v2 docs, then host, method, path, argument, auth, permission, response, release stage, and errors agree.
- Given paged, binary, error, timeout, and asynchronous write paths, then guidance explains tokens, byte handling, retry bounds, and state checks.
- Specify evidence, preconditions, expected outputs, edge and negative cases; use placeholder credentials only.
