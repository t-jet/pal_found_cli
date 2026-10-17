# FEATURE-015 draft release status — 2026-10-18

FEATURE-015 is not released. The branches below are draft review candidates. No commit has been merged into the three repositories' `main` branches for this release, and no tag has been created.

| Repository | Review branch | Candidate | Verification |
|---|---|---|---|
| Skills | [PR #1](https://github.com/t-jet/pal_found_cli_skills/pull/1) | `416747d` (content freeze `d6e2b8e`) | 632 local tests and GitHub validation passed |
| CLI tool | [PR #1](https://github.com/t-jet/pal_found_cli_tool/pull/1) | `0963e6e` | 51 focused Data Health tests and all eight GitHub checks passed |
| Parent | [PR #6](https://github.com/t-jet/pal_found_cli/pull/6) | Draft integration branch | Both candidate submodules initialize; 174 document-index links resolve; tracker suite passes |

The parent draft combines smaller parent PRs for Data Health design and QA cases, tracker engine, source documents, and tracker history. [Tracker PR #5](https://github.com/t-jet/pal_found_cli/pull/5) preserves the raw snapshot before documented repairs. Its final index has 1,014 tickets and 1,543 valid links. The original payload of `LINK-01279` could not be recovered; the repair ledger records that limit. Independent tracker data QA remains open.

## Release gate

`python scripts/verify_feature015_release.py` on the skills candidate reports no stale candidate or asset hashes. It remains blocked by 354 semantic operation reviews, 425 formal operation QA and provenance items, 144 skill reviews, and 37 topic reviews. The 20 skill pages changed by the no-installation correction need fresh reviewer evidence. The URL audit's earlier scan is retained as historical evidence; it has not been promoted to a current review.

DEV-STORY-072 has 35 semantic passes and five uncertain private beta operations. DEV-STORY-081's last independent retest found 11 passes, seven fixture defects and four uncertain operations. The seven fixtures were corrected in the current candidate and passed local execution; an independent semantic retest of that new head is still required. BUG-034's Data Health wire retest passed, but DHT-TC-021 needs independent case approval in `TESTCASE-085` and formal execution in `TESTEXEC-085`. BUG-035's Audit access correction passed an earlier defect retest; its changed skill page still needs review at the current hash.

## Local checkout

The live parent checkout remains dirty and diverged from remote `main`. A byte comparison of its 1,253 reported changes found 1,245 files published byte for byte across the combined draft and the separate [agent configuration draft PR #7](https://github.com/t-jet/pal_found_cli/pull/7). Six files differ because the drafts contain newer tracker engine fixes, intentional index repairs, and a newer document index. The two live submodule checkouts remain at older commits; the combined parent draft pins the candidate SHAs above. The four deleted temporary files from local history were not carried into the drafts. Do not treat the live checkout's dirty state as a release artifact.

Keep all release PRs draft until the outstanding reviews and QA records are complete. Re-run the gate and verify exact GitHub heads before any merge or tag.
