---
id: UNITTEST-013
type: unittest
title: 'DEV-STORY-013 UNITTEST: models CLI parser dispatch and infra tests'
status: Closed
created: 2026-08-09
updated: 2026-08-09
priority: High
assignee: python-developer
reporter: architect
estimated_hours: 12
time_spent_hours: 12
---

# UNITTEST-013: DEV-STORY-013 UNITTEST: models CLI parser dispatch and infra tests

## Description

# UNITTEST-013: DEV-STORY-013 UNITTEST: models CLI parser dispatch and infra tests

## Description

Write the unit test suite for the foundry-models CLI covering the 23-command catalog: parser and dispatch, JSON validation, nested client routing, pagination bounds, streaming download behavior, ACL write/read classification, metadata-only 12/11 policy, tracing, retries, output contracts, and privacy of logs and errors. Add integration coverage for packaging and the Claude launcher.

## Acceptance Criteria

- [x] Tests cover Python 3.11 and 3.12 via the repository matrix.
- [x] Exact signatures, routes, dispatch, and parsing covered for all 23 commands.
- [x] Pagination, streaming, ACL, tracing, retry, output, privacy, and packaging covered.
- [x] All unit tests are real unit tests (no external connections) and pass 100%.
- [x] At least 80% coverage on the new models namespace (branch coverage).
- [x] Time reported in the subtask frontmatter.

## Related Documentation

- .ept/docs/deliverables/architecture/DESIGN-013-models-cli.md
- .ept/docs/deliverables/qa/TESTCASE-010-test-cases.md (pattern reference)

## Notes

Run via pytest with the repository coverage configuration.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
