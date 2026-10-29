---
id: BUG-SUB-032
type: bug_subtask
title: DEV-STORY-081 beta REST fixtures omit preview query
status: Closed
created: 2026-10-16
updated: 2026-10-18
priority: High
assignee: python-developer
reporter: qa-engineer
component: skills
time_spent_hours: 0.2
---

# BUG-SUB-032: DEV-STORY-081 beta REST fixtures omit preview query

## Description

Affected candidate: pal-found-dev 4ab4e6f, SDK 1.101.0. Independent source review before TESTEXEC-080. Reproduce: run python -B .agents/skills/pal-found-dev/examples/rest/081/v2/ontologies/OntologyObjectSet/invoke_create_temporary.py from skills root. Fixture passes, but EXPECTED_QUERY.preview is None and invoke omits preview. The same omission affects all 14 beta operations in DEV-STORY-081. Expected: beta calls and mock assertions send preview=true, as required by the official Create Temporary Object Set and Load Object Set Objects Or Interfaces API references. Actual: SDK request omits preview entirely; current success mocks accept it. Add a regression check per beta operation and retest source-derived behavior. TESTCASE-080 and TESTEXEC-080 remain Open; this is diagnostic review, not formal sign-off.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
