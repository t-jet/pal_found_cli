---
id: BUG-SUB-033
type: bug_subtask
title: DEV-STORY-081 object and link examples lack meaningful result and error checks
status: Open
created: 2026-10-16
updated: 2026-10-16
priority: High
assignee: python-developer
reporter: qa-engineer
component: skills
---

# BUG-SUB-033: DEV-STORY-081 object and link examples lack meaningful result and error checks

## Description

Affected candidate: pal-found-dev 4ab4e6f, SDK 1.101.0. Independent source review before TESTEXEC-080. Reproduce: inspect references/rest/v2/ontologies/OntologyObject.md and LinkedObject.md, then run each of their seven examples/rest/081 fixtures. The worked example sections contain prose only. OntologyObject.get and LinkedObject.get_linked_object mock SUCCESS={} and assert only that empty object decodes; list/search examples mock data=[{}] and do not assert IDs, selected properties, or a search filter. All seven fixtures set ERRORS=[] despite documented LinkedObjectNotFound or ObjectsExceededLimit for applicable methods. Expected: each owned operation gives an adaptable SDK call with representative request/result/error assertions, identity and page assertions, and a named failure where declared by the source. Actual: transport-only placeholders all pass without proving those behaviors. TESTCASE-080 and TESTEXEC-080 remain Open; this is diagnostic review, not formal sign-off.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
