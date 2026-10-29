---
id: CODEREVIEW-061
type: codereview
title: Review REST List Objects limit correction
status: Closed
created: 2026-10-05
updated: 2026-10-05
priority: High
assignee: architect
reporter: architect
estimated_hours: 1
---

## Scope
Independent re-review of the List Objects pagination limit correction to pal-found-dev/references/rest-api.md after CODEREVIEW-059 was closed.

## Acceptance criteria
- Explain that 10,000-object endpoint cap applies to Object Storage V1 backing only; Object Storage V2 has no endpoint cap.
- Example labels any 10,000 work bound as client-chosen, not a universal server limit.
- Verify prose and example against official v2 List Objects endpoint and existing ontology-object guide.
- Confirm regression test covers the distinction and record evidence before closure.
