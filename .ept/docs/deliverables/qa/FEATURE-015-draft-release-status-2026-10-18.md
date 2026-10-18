# FEATURE-015 draft release status — 2026-10-18

FEATURE-015 is not released. The branches below are draft review candidates. No commit has been merged into the three repositories' `main` branches for this release, and no tag has been created.

| Repository | Review branch | Candidate | Verification |
|---|---|---|---|
| Skills | [PR #1](https://github.com/t-jet/pal_found_cli_skills/pull/1) | `691107e` (locator correction `86149eb`) | 524 REST acceptance tests, Ruff, and GitHub validation passed; earlier full suite passed 632 tests before the locator correction |
| CLI tool | [PR #1](https://github.com/t-jet/pal_found_cli_tool/pull/1) | `0963e6e` | 18 formal DHT-TC-021 CLI scenarios, 51 focused Data Health tests, and all eight GitHub checks passed |
| Parent | [PR #6](https://github.com/t-jet/pal_found_cli/pull/6) | Draft integration branch | Both candidate submodules initialize; 174 document-index links resolve; 442 tracker tests pass |

The parent draft combines smaller parent PRs for Data Health design and QA cases, tracker engine, source documents, and tracker history. [Tracker PR #5](https://github.com/t-jet/pal_found_cli/pull/5) preserves the raw snapshot before documented repairs. Its final index has 1,015 tickets and 1,543 valid links. Independent tracker data QA passed the final CLI retest after a live link-ID collision was resolved. The original payload of `LINK-01279` could not be recovered; the repair ledger records that limit. Independent docs QA passed: all 174 relative index links resolve and 102 snapshot documents match their sources.

## Release gate

`python scripts/verify_feature015_release.py` on the skills candidate reports no stale candidate or asset hashes. It remains blocked by 354 semantic operation reviews, 425 formal operation QA and provenance items, 144 skill reviews, and 37 topic reviews. Independent review passed the narrow no-installation correction on all 20 changed pages, including 68 relative links and 39 unique external source URLs. Broader semantic review and formal QA for those pages remain open. The URL audit's earlier whole-bundle scan is retained as historical evidence; it has not been promoted to a current review.

DEV-STORY-072 has 35 semantic passes and five uncertain private beta operations. DEV-STORY-081's initial independent review found 11 passes, seven fixture defects, and four uncertain operations. Later review found two Scenario locator response defects in the corrected fixtures; both were fixed and independently retested, and `BUG-SUB-034` is Closed. All 22 REST-081 fixtures execute at the current candidate, while `BUG-SUB-032/033`, `TESTCASE-080`, and `TESTEXEC-080` remain open. BUG-034's DHT-TC-021 case and formal execution are Closed: nine preview wire requests, nine explicit-false rejects, 51 focused tests, and Ruff passed at the pinned tool commit. This does not cover a live Foundry tenant. BUG-034 remains Open pending broader release workflow. BUG-035's Audit access correction has a diagnostic PASS; broader page review remains open.

## Local checkout

The live parent checkout remains dirty and diverged from remote `main`. A fresh byte comparison of its 1,282 reported paths found 1,274 matching the combined draft or the separate [agent configuration draft PR #7](https://github.com/t-jet/pal_found_cli/pull/7). Six files differ because the drafts contain newer tracker engine fixes, intentional index repairs, and a newer document index. The two live submodule checkouts remain at older commits; the combined parent draft pins the candidate SHAs above. Do not treat the live checkout's dirty state as a release artifact.

Keep all release PRs draft until the outstanding reviews and QA records are complete. Re-run the gate and verify exact GitHub heads before any merge or tag.
