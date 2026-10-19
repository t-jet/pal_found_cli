# FEATURE-015 draft release status

Last verified: 2026-10-19 (Europe/Sofia). FEATURE-015 remains in draft review. No release merge or tag has been performed in this workflow.

| Repository | Draft | Candidate | Verification |
|---|---|---|---|
| Skills | [PR #1](https://github.com/t-jet/pal_found_cli_skills/pull/1) | `cb096d1`, content freeze `6205cd7` | GitHub validation passed. All 36 development topics have independent semantic/source acceptance; nine topic/author tests passed. Actual TypeScript 7.0.2 compiled the application/widget examples with zero diagnostics. |
| CLI tool | [PR #1](https://github.com/t-jet/pal_found_cli_tool/pull/1) | `0963e6e` | All eight GitHub checks passed. Formal DHT-TC-021 passed 18 CLI scenarios and 51 focused Data Health tests. |
| Parent | [PR #6](https://github.com/t-jet/pal_found_cli/pull/6) | Integration branch, with both pins above | Combined tracker suite passed 442 tests after the latest snapshot merge. |

The topic review corrected two substantive omissions: Action Test run can execute result-producing external calls, and Compute Module Pipeline mode manages its output dataset transactions. Both corrections passed independent retest. Their source and audit hashes match current bytes. Seven unchanged source URL locations were moved to their new lines; the historical whole-bundle URL scan was not promoted to a new scan. Application/widget compile evidence uses a synthetic schema and proves no tenant binding or execution.

The latest Data Health capability correction removes an unsupported pagination-helper claim. `get-latest --limit` bounds a single response. This authored correction is published, but its full-page independent retest remains pending because the assigned reviewer hit an agent usage limit. Five current ledger/URL checks passed. No acceptance was inferred from the interrupted review.

## Remaining release gates

The verifier reports no stale candidate or asset hashes. It remains blocked by:

- 425 formal operation QA items and their provenance.
- 336 semantic operation reviews and their provenance.
- 109 skill-review gate items: 108 pages plus the overall audit signoff.

The T01-T36 topic gate is complete. T37 REST, journey acceptance, other skill pages, and live Foundry behavior have separate scopes. Existing independent FEATURE-012 evidence still matches 343 operation records, tool code, and SDK hashes; this supports those record portions, not whole-page acceptance.

DEV-STORY-072 now has all 40 operation semantic reviews accepted against frozen SDK 1.101.0 and current fixtures. BUG-SUB-029/030/031 are Closed after independent retests; TESTCASE-075 and TESTEXEC-075 remain Open. DEV-STORY-081 has eleven non-private operation semantic reviews accepted and eleven private-beta reviews pending. BUG-SUB-032/033/034 are Closed, while TESTCASE-080 and TESTEXEC-080 remain Open. Historical defect findings remain preserved with current retest evidence.

For DEV-STORY-085, UNITTEST-082 and QUESTION-190 are Closed, DEV-082 is Resolved, CODEREVIEW-083 is Open, TESTCASE-082 is In Progress, and TESTEXEC-082 is Open. Two source-derived Functions edge tests are integrated. Formal code review and test-case design were interrupted by agent usage limits; the eleven operation QA statuses remain pending. Historical implementation hours are unknown; tracker entries record only measured work from these sessions.

BUG-034 remains Open pending the broader workflow despite its closed DHT-TC-021 case/execution. BUG-035 has a targeted Audit correction PASS; broader page review remains open.

## Tracker and local checkout

[Tracker PR #5](https://github.com/t-jet/pal_found_cli/pull/5) at `9f3c1eba` contains 1,016 indexed tickets, 1,543 unique links with valid endpoints, counter 1987, and 10,308 comment files matching live bytes. Snapshot validation found zero errors. It preserves the raw snapshot and documented repairs, including the unrecoverable `LINK-01279` limit. The review blocker now runs from CODEREVIEW-083 to DEV-082; its obsolete reverse link was removed through the live workflow. This latest capture has local validation; an additional independent delta review is still pending.

The live parent checkout remains dirty and diverged from remote `main`. The latest byte audit found 1,355 changed entries: 1,347 files match the integration or agent-configuration draft, six file versions differ, and two entries are submodule pointers. The differing files are the document index, three older tracker code/test files, counter YAML ordering, and the malformed live link CSV. Drafts contain newer documentation/code and repaired links. Copying the live tree wholesale would discard those repairs.

Live skills and tool checkouts are internally clean at older commits that are ancestors of their published candidates. [Agent configuration PR #7](https://github.com/t-jet/pal_found_cli/pull/7) at `f8e567e2` matches all live self-improvement notes byte for byte and passes the composer check. Four legacy temporary text files outside `.ept/tmp` already exist on remote `main`; this release draft did not introduce them.

Keep release PRs draft. Resume independent page reviews, Functions code/test-case review, and formal operation execution when delegated review capacity is available. Verify exact heads and rerun the release gate before any merge or tag.
