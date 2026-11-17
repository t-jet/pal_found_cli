# FEATURE-015 draft release status

Last verified: 2026-11-17 (Europe/Sofia). FEATURE-015 remains Waiting for Implementation. Its 24 implementation stories remain nonterminal; nine historical duplicates remain terminal. The reviewed skills checkpoint is published for review. Final feature acceptance and skills main publication remain pending.

## Published revisions

| Repository | Published revision | Verification |
| --- | --- | --- |
| Skills | Draft [PR #1](https://github.com/t-jet/pal_found_cli_skills/pull/1), `4de1e23e98017536bcff0eef2aa1d057e576e056` | [Exact-head validation passed](https://github.com/t-jet/pal_found_cli_skills/actions/runs/44084297861). All 425 operation meanings are accepted. |
| CLI tool | Main `1e2e61bc0a56afe9af75e77170358d93ff6cf9d1`, merged [PR #3](https://github.com/t-jet/pal_found_cli_tool/pull/3) | Eight candidate checks and all eight [fresh main checks passed](https://github.com/t-jet/pal_found_cli_tool/actions/runs/43951678939). Main contains reviewed `9e5a83d` as a direct parent and has the same tree. |
| Parent release draft | [PR #1](https://github.com/t-jet/pal_found_cli/pull/1), `a2215f5aa7607e29afe773ecdb32a47880cf0cc7` | Paired pins are skills `4de1e23` and tool `1e2e61bc`; both preserve prior main and draft ancestry. |
| Tracker capture | [PR #5](https://github.com/t-jet/pal_found_cli/pull/5), `ef0c090d7b31999dab635a9fd492a95552385a36` | Independent source-capture QA passed 47 checks. The capture has a fixed timestamp boundary described below. |
| Agent configuration | [PR #7](https://github.com/t-jet/pal_found_cli/pull/7), `b60555e85e927cca44d7a230d5911bef2ab2b839` | Sixteen committed note files matched the verified live snapshot; generator checks passed. TASK-016 is Closed. |

Combined [parent PR #6](https://github.com/t-jet/pal_found_cli/pull/6) integrates these reviewed histories and paired pins. Parent main remains `c87925c9921be68549da7537b88a162326ad2273`, with older skills `716a85b` and tool `a3a38ec` pins. Published draft revisions do not establish a completed feature release.

## Accepted and pending QA

| Acceptance group | Accepted | Remaining |
| --- | --- | --- |
| Operation meanings | 425 of 425 | 0 |
| Formal operation QA | 229 of 425 | 196 |
| Whole skill pages | 153 of 192 | 39 pages plus overall signoff: 40 items |
| Non-REST development topics | 36 of 36 | Other integrated workflow and journey gates remain separate. |
| Model meanings | 3,251 definitions | Accepted source and dependency closure retained; this does not replace formal operation QA. |

The release verifier reports the expected 196 formal operation items and 40 page/signoff items. Source, asset, candidate, model and topic checks have no additional errors at the published checkpoint. No pending item is an approved exception.

| Story | Accepted formal evidence | Workflow boundary |
| --- | --- | --- |
| DEV-STORY-071 | 27 operations, 486 checks, 74 declared errors. | Deployment |
| DEV-STORY-072 | 40 operations, 612 checks, 113 declared errors. | Deployment |
| DEV-STORY-074 | 52 operations, 1,060 assertion rows, 288 declared errors. | Deployment |
| DEV-STORY-075 | 29 operations, 1,012 checks, 44 declared errors. | Deployment |
| DEV-STORY-077 | 23 operations, 597 checks: 587 operation checks and ten annex checks. Original formal run on November 16. | Deployment |
| DEV-STORY-085 | Eleven operations and 91 checks. | Deployment |
| DEV-STORY-087 | 47 operations, 894 checks, 171 declared errors. | Deployment |

REST-077 implementation, unit work, architect review, formal cases and execution are Closed. Independent acceptance covers its 23 operations using the original November 16 formal execution. The source cases were Closed before that run. November 17 workflow recovery closed the execution record and advanced the story to Deployment; it did not rerun the tests. The earlier case dry run and peer controls remain separate from the formal result. Original archive bytes, canonical manifest, inventory and 142 full comment bodies are retained under the pinned skills `maintainer/evidence/rest077/`, with acceptance and source-binding proofs. Isolation evidence includes one actual `create_connection` probe and three patched entry points; CPU usage was not recorded.

REST-079 and REST-089 each add one independently reviewed unit test file with author, peer, executable probe, JUnit, source-binding and mutation evidence under `maintainer/evidence/unit079089-20261117/`. These test-only changes preserve product skill and fixture bytes. Their formal operation QA remains pending.

REST-073 restore guidance now explains the conflict between SDK no-op prose and ResourceNotDirectlyTrashed. The generated contract preserves the source quote and links the qualified recovery guidance. The semantic review passes; actual server policy remains unknown. Seven pre-existing generation differences were preserved; a baseline comparison proved the patch changes only the intended restore contract.

Original failures remain archived. These include REST-087 harness normalization issues, REST-081 asynchronous response misuse in a review harness, the REST-091 invalid PNG CRC, Third-party conflict-status wording, and REST-077 case-control findings. Corrections retain separate authors, reviewers, exact hashes and evidence boundaries.

BUG-SUB-025 is Closed after a separate J12 reader completed twelve synthetic offline scenarios and an independent grader passed all six criteria. Broader integrated journey acceptance remains separate. All requests in these reports used synthetic data and controlled transports; no live Foundry tenant acceptance is claimed.

## CLI and guidance corrections

BUG-034, BUG-036 through BUG-049 are Closed with their verified blocking links removed and other relationships preserved. BUG-035 remains Resolved and requires the final accepted skills main pin before QA closure. The Models and Third-party guidance bugs are accepted within the published draft scope; their closure does not complete FEATURE-015.

The Models config-version fix preserves native validation and scopes integer-path conversion to the affected resource request. Independent QA passed 39 Models tests and fourteen additional cases on each supported SDK version. Fourteen Models pages passed 80 actual CLI probes; their hashes remain unchanged in the current draft.

The Third-party fix adds the missing ThirdPartyApplication SDK parent for eight Website/Version commands. Independent QA passed 51 native CLI cases per SDK version, eighteen console subprocesses and two launcher checks. Both standalone pages passed review against the fixed runtime. Conflict recovery explicitly handles exit 1/ConflictError without a guaranteed http_status field. No SDK monkeypatch or new runtime policy was added.

- [Shared CLI evidence](FEATURE-015-shared-cli-corrections-2026-10-20/README.md) records historical tests and six installation paths at tool `657215f`; those packaging results do not describe every later revision.
- [Functions SSE correction](FEATURE-015-functions-sse-correction-2026-10-21/README.md) records SDK decoding, scoped retry/client handling and independent SDK checks.
- [Filesystem and SQL corrections](FEATURE-015-filesystem-sql-corrections-2026-10-21/README.md) records query forwarding, JSON decoding and actual SDK wire checks.

The current skills checkpoint passed 2,391 combined targeted tests and 44 metadata/acceptance guards, Ruff and byte/diff checks, followed by exact-head GitHub validation. All 4,637 tracked product and fixture files match the previous published checkpoint. The earlier 1,323-test result belongs to its original head.

An earlier adapter scan had ten uncertain rows; eight Third-party paths were subsequently confirmed defective and corrected. Independent QA of the two legacy Geotemporal CLI commands found their enabled paths return exit 1 with `UserInputError` and an underlying `AttributeError` before HTTP on SDK 1.101.0 and 1.111.0. Disabled feature guards return exit 8 before SDK construction. Both legacy methods exist in frozen SDK 1.79; the two supported test versions expose only `load_geotemporal_series_entries`. QUESTION-196 is In Progress with Architect for classification against the approved conditional availability, supported SDK range and 351-operation preservation contract. It blocks DEV-STORY-070, whose prior status was Development. No product correction or unsupported-operation waiver has been accepted; the technical classification remains pending.

## Tracker and working copies

The [capture manifest](FEATURE-015-tracker-capture-2026-11-16.json), [independent QA](FEATURE-015-tracker-capture-2026-11-16-independent-qa.json) and [evidence](FEATURE-015-tracker-capture-2026-11-16-evidence.json) describe the Git-native snapshot frozen on 2026-11-16 at 12:54:42-12:55:13 UTC. It contains 12,626 canonical source files, 1,051 indexed tickets across all statuses, 11,542 comments and 1,589 links. Later workflow changes, including current QA closures, are outside that snapshot.

Six historical CSV repairs, the unrecoverable LINK-01279 boundary, exact raw link CSV and legacy CODE002 archive remain preserved. All 45 engine files are unchanged in the capture branch. The combined branch retains the newer reviewed engine; independent merge review confirmed that incoming functionality was preserved. No new engine test run is claimed for an unchanged engine.

The live parent checkout remains dirty, and later workflow records are not included in the frozen capture. Isolated release branches preserve those live edits. DEVOPS-047 remains Open until G1-G7 acceptance is complete; final skills main publication, accepted parent pin and G8 verification follow that work. No feature tag, package upload or live tenant deployment is claimed.
