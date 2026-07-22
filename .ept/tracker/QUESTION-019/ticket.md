---
id: QUESTION-019
type: question
title: 'QUESTION: TESTCASE-003 D-5 file upload reads entire file into memory; no size guard'
status: Closed
addressed_to: architect
created: 2026-07-04
updated: 2026-07-05
priority: Critical
assignee: architect
reporter: qa-engineer
---

# QUESTION-019: QUESTION: TESTCASE-003 D-5 file upload reads entire file into memory; no size guard

## Description

foundry_datasets_cli.py L218-220 fobj.read() then content=<bytes>. No upload-size guard exists. Risk: OOM / SDK limit exceeded. See TESTCASE-003-test-cases.md D-5.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
