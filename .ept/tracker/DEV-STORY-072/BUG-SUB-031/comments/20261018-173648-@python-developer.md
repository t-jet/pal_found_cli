Subject: Root cause, integrated fix, file hashes and regression evidence
Created: 2026-10-18T17:36:48
Updated: 2026-10-18T17:36:48
---
Root cause: the original offline fixture accepted a response with neither a parsed nor an error entry for its submitted string. The local contract also repeated the SDK's "at most 1000" wording without the API's minimum size, duplicate-count rule, or boundary errors. The SDK 1.101.0 method lists only CbacUnavailable and ParseClassificationsPermissionDenied as typed operation errors and forwards empty and 1001-entry lists to HTTP unchanged.

Fix: the example now uses the official API sample pair, MTS//MNF and INVALID_MARKING, and checks both result maps, their disjointness, complete coverage of requested strings, and the parsed/error values. Contract and guide state 1..1000 submitted entries, duplicate counting with parse-once behavior, MissingBatchRequest for empty input, and BatchRequestSizeExceededLimit for >1000 input. These API boundary errors are distinguished from the SDK-declared named errors. A new focused MockTransport regression test verifies both invalid lengths reach HTTP without SDK prevalidation.

Official source: https://www.palantir.com/docs/foundry/api/v2/admin-v2-resources/markings/parse-classifications
Implementation: skills integration commit 68d569c76a2a30bbc33a267ce6395d09435a97c6 (source fix commit 1dec2c160803342370bcc6b4e720ed83bfa6e9b6). SHA-256 at integration commit:
- .agents/skills/pal-found-dev/examples/rest/072/v2/admin/Marking/parse_classifications.py: b2532e2461210e5c8df72820167611863d7edef7926f9db37fb3830beeb7941e
- .agents/skills/pal-found-dev/references/rest/contracts/v2/admin/Marking/parse_classifications.md: 7b93c4d8dc997e9f0871555944b3f5d734aee2cc4da583eee66a0b7f8bc627c6
- .agents/skills/pal-found-dev/references/rest/v2/admin/Marking.md: 6b6c17e3cfba69ce8f9f07007da521af3267f539cfbdd9c907c6e6a9c0bf2bd0
- tests/test_marking_parse_classifications.py: 880d6838838915649f10355ac41830178aa53f3aad2163ca7c8b3379fba5b42f

Regression: python -m pytest -q tests/test_offline_rest_wave1.py tests/test_marking_parse_classifications.py -> 520 passed. Ruff check of example and new test passed. Git diff check passed with cr-at-eol for existing CRLF docs. Independent QA retest at source fix commit reported PASS; formal TESTCASE-075 and TESTEXEC-075 remain Open. Existing RelatesTo/Contains links retained. Time spent: 0.25 hours in ticket frontmatter.
