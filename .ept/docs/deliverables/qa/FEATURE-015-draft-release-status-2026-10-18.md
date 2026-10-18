# FEATURE-015 draft release status - 2026-10-18

FEATURE-015 remains in draft review. No release merge or tag has been performed in this workflow.

| Repository | Review branch | Candidate | Verification |
|---|---|---|---|
| Skills | [PR #1](https://github.com/t-jet/pal_found_cli_skills/pull/1) | `5d50cf8` (content freeze `68d569c`) | 533 focused tests passed at the content freeze; subsequent commits record independent reviews only. Five ledger and gate tests passed after T06. GitHub validation passed at this exact head. |
| CLI tool | [PR #1](https://github.com/t-jet/pal_found_cli_tool/pull/1) | `0963e6e` | 18 formal DHT-TC-021 CLI scenarios, 51 focused Data Health tests, and all eight GitHub checks passed. |
| Parent | [PR #6](https://github.com/t-jet/pal_found_cli/pull/6) | Draft integration branch | Both candidate submodules initialize; 174 document-index links resolve; the combined tracker suite passed 442 tests after the final tracker snapshot merge. |

The parent draft combines smaller PRs for Data Health design and QA cases, tracker engine fixes, source documents, and tracker history. [Tracker PR #5](https://github.com/t-jet/pal_found_cli/pull/5) at `5cf46a84` preserves the raw snapshot before documented repairs. It contains 1,015 indexed tickets, 1,541 unique links with valid endpoints, and 10,261 comment files matching live bytes. Its tracker suite passed 426 tests. Independent delta QA passed at this exact head: no status drift or link conflicts, and all 33 current comments on BUG-SUB-031/032/033 match the live CLI content. The CLI-only review verified the highest active link ID, 1982; separate branch validation checked the stored counter. The original payload of `LINK-01279` could not be recovered and is documented in the repair ledger. Independent document QA passed all 174 index links and confirmed 102 snapshot documents match their sources.

## Release gate

`python scripts/verify_feature015_release.py` reports no stale candidate or asset hashes at `5d50cf8`. It remains blocked by 353 semantic operation reviews, 425 formal operation QA and provenance items, 139 skill pages, and 31 topics. Topics T01 through T06 have independent acceptance evidence at their current page hashes. Independent review also passed the narrow no-installation correction on 20 pages, including 68 relative links and 39 unique external source URLs. Broader page and journey QA remains open. The earlier whole-bundle URL scan remains historical evidence.

BUG-SUB-031 is Closed after the parser example and boundary handling were corrected and independently retested. DEV-STORY-072 has 34 accepted semantic reviews and six pending operation reviews in the current register; TESTCASE-075 and TESTEXEC-075 remain Open. BUG-SUB-032/033/034 are Closed after independent retests of preview serialization, Object/LinkedObject inputs, and Scenario locators. All 22 REST-081 fixtures execute, but eleven private beta operation semantics remain uncertain and TESTCASE-080/TESTEXEC-080 are Open. The historical REST-081 review record has not been promoted to a full formal QA pass.

BUG-034's DHT-TC-021 case and execution are Closed: nine preview wire requests, nine explicit-false rejects, 51 focused tests, and Ruff passed at the pinned tool commit. Live Foundry tenant behavior remains unverified. BUG-034 remains Open pending the broader release workflow. BUG-035's Audit access correction has a diagnostic PASS; broader page review remains open.

## Local checkout and publication audit

The live parent checkout remains dirty and diverged from remote `main`. A full audit found 1,303 changed entries: 1,301 files and two submodule pointers. Of those files, 1,296 match exact bytes in published draft branches. Five live file versions differ from every draft: `test_links.py`, tracker `index.py` and `tickets.py`, `.id-counters.yaml`, and `.link-index.csv`. The drafts contain newer tracker locking fixes, equivalent counters in a different YAML order, and repaired link rows; the live link index contains malformed rows. These differences are intentional and must not be overwritten by copying the live tree wholesale.

The live skills (`04e860f3`) and tool (`b9c5f8a1`) checkouts are internally clean, with no untracked or unpublished files. Both commits are ancestors of their published draft candidates. Their parent pointers are older than the release pins above. [Agent configuration PR #7](https://github.com/t-jet/pal_found_cli/pull/7) at `e2aedd91` captures the latest self-improvement notes; its composer check passes. Four legacy temporary text files outside `.ept/tmp` already exist on remote `main`; this release draft did not introduce them.

Keep release PRs draft until outstanding reviews and QA records are complete. Re-run the gate and verify exact GitHub heads before any merge or tag.
