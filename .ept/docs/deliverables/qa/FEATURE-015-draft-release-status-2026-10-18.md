# FEATURE-015 draft release status

Last verified: 2026-11-16 (Europe/Sofia). FEATURE-015 remains Waiting for Implementation. Its 24 active stories remain nonterminal; nine historical duplicates remain terminal. Tool corrections have been released separately. The complete skills feature has not reached release acceptance.

## Published and local revisions

| Repository | Published revision | Current evidence |
| --- | --- | --- |
| Skills | Draft [PR #1](https://github.com/t-jet/pal_found_cli_skills/pull/1), `3d5536cfe024bed6d8dbfbdc27cc65f700b7e95f` | [Validation passed](https://github.com/t-jet/pal_found_cli_skills/actions/runs/43825527620). Later domain corrections and acceptance changes remain local until the next verified draft push. |
| CLI tool | Main `223d2c0bfe3b4ed9a1f8aa35cc98a07cf2a3238f`, merged [PR #2](https://github.com/t-jet/pal_found_cli_tool/pull/2) | All eight [main CI checks passed](https://github.com/t-jet/pal_found_cli_tool/actions/runs/40949790522). Main preserves reviewed `db72226` as a direct parent and has the same source tree. |
| Parent | Main `c87925c9921be68549da7537b88a162326ad2273`; draft [PR #6](https://github.com/t-jet/pal_found_cli/pull/6) is being refreshed | Main pins skills `716a85b` and tool `a3a38ec`. Published release draft `2b836b42` pairs skills `3d5536c` with tool `223d2c0`; the combined draft still requires reconciliation. |

These revisions have different scopes. A successful tool merge does not complete FEATURE-015 or publish local skills and tracker changes.

## Current QA boundary

The published skills checkpoint records 359 of 425 operation meanings accepted and 206 of 425 formal operation reviews accepted. Remaining gates are 66 semantic reviews, 219 formal operation reviews, and 42 page/signoff items (41 pages plus overall signoff). Whole-page review accepts 151 of 192 pages. All 36 non-REST development topics and 3,251 model meanings retain independent acceptance. Later local promotions must pass validation and remote verification before they change these published counts.

| Story | Accepted formal evidence | Workflow |
| --- | --- | --- |
| DEV-STORY-071 | 27 operations, 486 checks, 74 declared errors; preserved archive and full comments. | Deployment |
| DEV-STORY-072 | 40 operations, 612 checks, 113 declared errors. | Deployment |
| DEV-STORY-074 | 52 operations, 1,060 assertion rows, 288 declared errors; original failed harness attempt preserved. | Deployment |
| DEV-STORY-075 | 29 operations, 1,012 checks, 44 declared errors; synthetic lifecycle and all supported transport modes. | Deployment |
| DEV-STORY-085 | Eleven Functions SDK operations and 91 checks with public sockets denied. | Deployment |
| DEV-STORY-087 | 47 operations, 894 checks, 171 declared errors. Two failed harness attempts and independent corrections remain preserved. | Deployment |

REST-075 and REST-087 formal acceptance is published within `3d5536c`, including commit `ebb535a`. REST-077 and REST-079 corrections passed separate semantic retests for all 23 and 32 operations. Models passed independent review of all 14 pages and 80 actual CLI probes against the corrected tool. Their published acceptance records preserve the initial failures and exact reviewed hashes.

Fresh independent retests now pass the eleven remaining REST-081 operations, all 25 REST-083 operations and all 29 REST-091 operations. Their local integration remains separate from the published counts above. Original review-harness mistakes and the later PNG CRC failure are preserved alongside their corrections. REST-073 Resource.restore has a confirmed guidance defect: unqualified SDK no-op prose conflicts with the declared ResourceNotDirectlyTrashed error. Its behavior and generated-contract correction still require independent acceptance.

BUG-SUB-025 is Closed after a separate J12 reader completed twelve offline scenarios and an independent grader passed all six criteria. Its preserved evidence distinguishes synthetic execution from live platform validation. Broader journey and integrated workflow acceptance remain separate.

## CLI corrections

BUG-036 through BUG-045 are Closed. BUG-034 is Closed. BUG-035 remains Resolved and requires the published accepted skills pin before final QA closure. BUG-046 is Closed with resolution Done after developer resolution and independent QA verified the published Models fix; only its verified blocking link was removed. BUG-047 Models guidance corrections passed independent review and are published in the skills draft; role-specific workflow closure remains pending.

- [Shared CLI evidence](FEATURE-015-shared-cli-corrections-2026-10-20/README.md) records 1,684 regression tests, 330 contract probes and six clean installation paths at historical tool `657215f`. Those packaging results do not describe every later revision.
- [Functions SSE correction](FEATURE-015-functions-sse-correction-2026-10-21/README.md) records real SDK SSE decoding, scoped retry/client handling, buffered NDJSON and independent SDK 1.101/1.111 checks.
- [Filesystem and SQL corrections](FEATURE-015-filesystem-sql-corrections-2026-10-21/README.md) records required-query forwarding, JSON decoding and actual SDK wire checks.

The Models fix preserves native SDK validation and scopes integer-path conversion to the affected resource request. Independent QA passed 39 Models tests and fourteen additional cases on each supported SDK version, including the original zero-request failure, exact route, output fallback, denials, error limits and cleanup. No global SDK patch or new runtime policy was added. All requests used synthetic inputs and mocked transport; no live tenant acceptance is claimed.

The published skills checkpoint `3d5536c` retains a 1,323-test local pass at its acceptance parent `0be7645`, followed by a validation-evidence-only commit and successful exact-head GitHub validation. This does not claim those local tests ran at a later unpublished head. Ten legacy metadata rows remain UNCERTAIN in an earlier adapter scan and require separate compatibility review.

## Remaining publication work

DEVOPS-047 remains Open because G1-G7 acceptance is incomplete. Final skills publication, paired parent pin, remote verification and G8 evidence follow accepted integrated QA. No feature tag, package upload or live tenant deployment is claimed.

Tracker [PR #5](https://github.com/t-jet/pal_found_cli/pull/5) still contains the older `3ae09324` capture. New ticket closures, comments and links require a stable recapture and independent verification. Preserve its six historical CSV repairs and documented unrecoverable LINK-01279 boundary. Historical capture counts and byte audits must not be presented as current.

Agent-configuration [PR #7](https://github.com/t-jet/pal_found_cli/pull/7) is published at `b60555e85e927cca44d7a230d5911bef2ab2b839` preserving both current main and its prior published branch. All sixteen committed note files matched the verified live snapshot; generator checks passed. TASK-016 is Closed.

The live parent checkout remains dirty. Existing local edits are preserved. Release, tracker and configuration branches need separate review and remote verification before the combined draft can claim they are all published.
