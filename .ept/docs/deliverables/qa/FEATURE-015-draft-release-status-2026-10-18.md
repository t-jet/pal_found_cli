# FEATURE-015 draft release status

Last verified: 2026-10-20 (Europe/Sofia). FEATURE-015 remains in draft review. No release merge or tag has been performed in this workflow.

| Repository | Draft | Candidate | Verification |
|---|---|---|---|
| Skills | [PR #1](https://github.com/t-jet/pal_found_cli_skills/pull/1) | `f1b5db8`, content freeze `7e79d1c` | Fifteen additional whole pages and 47 REST semantic reviews accepted. Eleven Functions operations passed formal QA. Focused suite passed 540 tests; four Functions evidence tests passed. All 36 development topics retain acceptance. |
| CLI tool | [PR #1](https://github.com/t-jet/pal_found_cli_tool/pull/1) | `0963e6e` | All eight GitHub checks passed. Formal DHT-TC-021 passed 18 CLI scenarios and 51 focused Data Health tests. |
| Parent | [PR #6](https://github.com/t-jet/pal_found_cli/pull/6) | Integration branch, with both pins above | Tracker engine previously passed 442 tests. Latest data-only capture passed independent integrity and byte-comparison QA; engine source is unchanged. |

The topic review corrected two substantive omissions: Action Test run can execute result-producing external calls, and Compute Module Pipeline mode manages its output dataset transactions. Both corrections passed independent retest. Their source and audit hashes match current bytes. Seven unchanged source URL locations were moved to their new lines; the historical whole-bundle URL scan was not promoted to a new scan. Application/widget compile evidence uses a synthetic schema and proves no tenant binding or execution.

Both Data Health pages passed independent whole-page review at current hashes. `get-latest --limit` bounds a single response. Core, Checkpoints and Orchestration reviews corrected CLI examples, configuration precedence, error/output behavior, build-search filtering, schedule recovery and seven preview limitations. Three Admin pages passed retest after six preview examples, two nonpaged lists, CBAC handling and mutation recovery were corrected. These reviews establish accurate guidance for pinned tool `0963e6e`; underlying tool defects remain open.

## Remaining release gates

The verifier reports no stale candidate or asset hashes. It remains blocked by:

- 414 formal operation QA items and their provenance.
- 289 semantic operation reviews and their provenance.
- 94 skill-review gate items: 93 pages plus the overall audit signoff.

The T01-T36 topic gate is complete. T37 REST, journey acceptance, other skill pages, and live Foundry behavior have separate scopes. Existing independent FEATURE-012 evidence still matches 343 operation records, tool code, and SDK hashes; this supports those record portions, not whole-page acceptance.

DEV-STORY-072 now has all 40 operation semantic reviews accepted against frozen SDK 1.101.0 and current fixtures. BUG-SUB-029/030/031 are Closed after independent retests; TESTCASE-075 and TESTEXEC-075 remain Open. DEV-STORY-081 has eleven non-private operation semantic reviews accepted and eleven private-beta reviews pending. BUG-SUB-032/033/034 are Closed, while TESTCASE-080 and TESTEXEC-080 remain Open. Historical defect findings remain preserved with current retest evidence.

DEV-STORY-073 now has 47 semantic operation acceptances. Five corrected fixtures passed independent retest and 13 mutation regression tests. `Resource.restore` remains uncertain because its documented active-resource behavior conflicts with a declared error. Historical findings remain preserved; formal operation execution is pending.

DEV-STORY-085 is Deployment. All six children, including CODEREVIEW-083, TESTCASE-082 and TESTEXEC-082, are Closed. Independent formal execution passed all eleven cases with 91 checks and denied public sockets; source and asset identities match accepted records. Archived harness, log and closure exports have integrity checks. Historical implementation hours are unknown; tracker entries record only measured session work.

BUG-036 through BUG-042 block affected DEV-STORY-070 acceptance: environment format default, genuine TOON encoding, structured parser errors, timeout consistency, total attempt count, seven required preview selectors, and build-search filter validation. Candidate implementation is committed in an isolated tool checkout; the published tool pin remains `0963e6e` pending review and QA. All 330 independent contract probes passed, but the broad regression gate remains open while legacy test oracles and environment isolation are corrected. Clean wheel/sdist installs passed on Python 3.11 and 3.12; final packaging verification continues. These results do not close the defects.

QUESTION-192 and QUESTION-193 are Closed after independent PM acceptance. The [contract amendment](../architecture/FEATURE-015-shared-cli-contract-amendment-2026-10-20.md) records one effective SDK/outer timeout, four total calls by default, and the explicit historical TOON dependency/API correction to `toon-format==1.2.0` and `toon_format.dumps()`. The architect's follow-up preserves HTTP 429 exhaustion exit 7 and HTTP 503 exhaustion exit 6. Implementation and packaging checks remain separate gates.

BUG-034 remains Open pending the broader workflow despite its closed DHT-TC-021 case/execution. BUG-035 has a targeted Audit correction PASS; broader page review remains open.

## Tracker and local checkout

[Tracker PR #5](https://github.com/t-jet/pal_found_cli/pull/5) at `9fcbac92` contains 1,026 indexed tickets, 1,566 unique links with valid endpoints, counter 2015, and 10,421 comment files matching live bytes. Independent [snapshot QA](../../feature015_tracker_capture_qa_2026-10-20.json) passed with zero errors. It preserves the raw snapshot and documented repairs, including the unrecoverable `LINK-01279` limit. Functions review/case/execution blockers and resolved question blockers were removed through the live workflow. Seven tool defects remain In Progress and block affected DEV-STORY-070 acceptance.

The live parent checkout remains dirty and diverged from remote `main`. The latest byte audit found 1,482 changed entries: 1,475 files match the integration or agent-configuration draft, five file versions differ, and two entries are submodule pointers. The differing files are the document index, three older tracker code/test files, and the malformed live link CSV. Drafts contain newer documentation/code and repaired links. Copying the live tree wholesale would discard those repairs.

Live skills and tool checkouts are internally clean at older commits that are ancestors of their published candidates. [Agent configuration PR #7](https://github.com/t-jet/pal_found_cli/pull/7) at `1218b00e` matches all live self-improvement notes byte for byte and passes the composer check. Four legacy temporary text files outside `.ept/tmp` already exist on remote `main`; this release draft did not introduce them.

Keep release PRs draft. Independent page/REST reviews, shared tool correction and tracker snapshot verification continue. Verify exact heads and rerun the release gate before any merge or tag.
