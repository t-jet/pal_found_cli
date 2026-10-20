---
id: QUESTION-193
type: question
title: Correct TOON distribution version and API references without changing library requirement
status: Closed
addressed_to: architect
created: 2026-10-20
updated: 2026-10-20
priority: High
assignee: architect
reporter: architect
time_spent_hours: 0.12
---

# QUESTION-193: Correct TOON distribution version and API references without changing library requirement

## Description

## Question
Which installable distribution, exact stable version and callable API correct historical TOON dependency references while preserving Closed QUESTION-012 choice of actual official TOON library and ADR-004 selection rules?

## Research Done
Reviewed indexed SRS-001142/C-2/OI-6, SAD-001 dependency table, accepted ADR-004, Closed QUESTION-012 architectural answer and QA closure, BUG-037 report, pinned tool0963 formatter and dependency omission. Tracker search TOON found only Closed012 and BUG037, so no duplicate packaging question.

Primary sources: https://pypi.org/pypi/toon-python/json returns404; https://pypi.org/pypi/toon-format/json identifies official https://github.com/toon-format/toon-python repository. Available releases0.1.0,0.9.0b1,1.0.0,1.1.0,1.2.0 contain no stable>=0.9,<1.0. Official1.2.0 distribution is toon-format, moduletoon_format, dumps/loads and encode/decode; toon.from_list absent. Official wheel SHA256 d94db4b088a281a7bbc85e75d7fbd24e6a0ec7bc110edb129285259eca6522c0; Python>=3.10. Downloaded verified wheel and three roundtrip probes pass for escaping/unicode/null/bool/nested data; this is architectural API verification only.

## Acceptance criteria
Record precise distribution/version/API correction, source provenance and rationale, preserve actual-library requirement and ADR-004 format-selection behavior. Identify required specification remediation and regression/DevOps installation checks. No custom renderer, deferral, capability waiver or claim of completed implementation. Architect decides bounded technical reference; BA verifies preserved business acceptance before requester closure.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
