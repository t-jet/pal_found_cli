# FEATURE-015 draft release status

Last source verification: 2026-11-19 UTC. FEATURE-015 final acceptance and skills-main publication remain pending. TASK-024 completed its bounded source publication; TASK-022 remains In Progress for the paired parent publication. These drafts do not establish a completed feature release.

## Reviewed source pair

| Repository | Revision | Verification |
| --- | --- | --- |
| Skills | Draft [PR #1](https://github.com/t-jet/pal_found_cli_skills/pull/1), `163cb1f6d28f11eca51384f86c462761a69acd6f` | [Exact-head validation](https://github.com/t-jet/pal_found_cli_skills/actions/runs/44407202903) passed Ruff and 8,015 tests. [Original CI proof](FEATURE-015-skills-ci-163cb1f.json) and [immutable source checkpoint](FEATURE-015-skills-checkpoint-163cb1f.json) retain observation times and execution boundaries. |
| CLI tool | Main `01cd9e91e98dc27ca03bfbf0031ee7807684a7ba`, normally merged [PR #4](https://github.com/t-jet/pal_found_cli_tool/pull/4) | All eight [fresh exact-main checks](https://github.com/t-jet/pal_found_cli_tool/actions/runs/44407624639) passed. [Main proof](FEATURE-015-tool-ci-01cd9e9.json), [independent QA](FEATURE-015-tool-main-independent-qa-01cd9e9.json) and [normal merge binding](FEATURE-015-tool-merge-01cd9e9.json) confirm exact reviewed tree and two direct parents. Additional `update-pip-graph` success is recorded separately. |
| Parent release draft | [PR #1](https://github.com/t-jet/pal_found_cli/pull/1) | Carries paired skills `163cb1f`/tool `01cd9e9` pins and retained immutable evidence. Its final published commit is recorded in the publication-time remote proof and TASK-022 comment after review and push. |
| Combined parent draft | [PR #6](https://github.com/t-jet/pal_found_cli/pull/6) | Integrates the release branch and this canonical status. Final published head is recorded after review and push; source pins do not imply final feature acceptance. |
| Tracker capture | [PR #5](https://github.com/t-jet/pal_found_cli/pull/5), `ef0c090d7b31999dab635a9fd492a95552385a36` | Frozen November 16 capture; later workflow and selected publication-time exports remain outside it. |
| Agent configuration | [PR #7](https://github.com/t-jet/pal_found_cli/pull/7), `b60555e85e927cca44d7a230d5911bef2ab2b839` | Reviewed configuration history retained. TASK-016 is Closed. |

Tool main tree `fd73eff4cc59d0136383949385e9498e3ada0ba4` equals candidate `5da77b017c3690a062fe041ae07799ac428e2f1b`. Its direct parents are prior main `1e2e61bc0a56afe9af75e77170358d93ff6cf9d1` and that candidate. [Candidate CI](FEATURE-015-tool-ci-5da77b0.json) remains a separate run. Parent main remains `c87925c9921be68549da7537b88a162326ad2273`; existing draft ancestry is retained.

## Accepted and pending QA

| Acceptance group | Accepted | Remaining |
| --- | --- | --- |
| Operation meanings | 425 of 425 register entries|0|
| Formal operation QA | 261 of 425|164|
| Whole skill pages | 153 of 192|39 page files plus overall signoff: 40 gates|
| Non-REST development topics | 36 of 36|Integrated workflow/journey gates remain separate|
| Model meanings | 3,251 definitions|Source/dependency closure does not replace formal operation QA|

The release diagnostic retains 164 formal QA gaps,164 corresponding provenance gaps and 40 skill-review gates. Candidate, bundle and asset checks add no new blockers. G1-G7 are not waived. All 20 skill identities and 351 existing CLI operation records remain preserved.

| Story | Accepted formal evidence |
| --- | --- |
| DEV-STORY-071 |27 operations,486 checks, 74 declared errors|
| DEV-STORY-072 |40 operations,612 checks,113 declared errors|
| DEV-STORY-074 |52 operations, 1,060 assertion rows,288 declared errors|
| DEV-STORY-075 |29 operations, 1,012 checks, 44 declared errors|
| DEV-STORY-077 |23 operations,597 checks: 587 operation checks and 10 annex checks; original November 16 formal run|
| DEV-STORY-079 |32 operations,original 1,564 PASS/0 FAIL including 25 annex scenarios; separate approval overlay|
| DEV-STORY-085 |11 operations, 91 checks|
| DEV-STORY-087 |47 operations,894 checks,171 declared errors|

REST077 recovery on November 17 closed its execution record and advanced the story to Deployment without another run. Original archive, canonical manifest, inventory and 142 full comment bodies remain under pinned skills `maintainer/evidence/rest077/`. Isolation evidence includes one actual `create_connection` probe and three patched entry points; CPU usage was not recorded.

REST079 metadata publication `a1d0647f9bac67d2a17bf7f603bd7a633b22a5f5` preserves the distinct original executor and original PENDING history, with actual approval in a separate overlay. Exactly 32 QA-status/executor pairs change;393 other rows remain unchanged. The historical 4,371-file executed bundle differs from current content in two corrected foreign guides; relevant 079 inputs match. This is not a formal rerun or whole-current-bundle execution.

REST081 `fefe77f638c9f40e29280dcafd05ebfb1a419586` and REST083 `163cb1f6d28f11eca51384f86c462761a69acd6f` publish independently reviewed native-unit coverage and original evidence. REST081 author and peer final runs each passed 1,019 tests; five independent mutants were killed. REST083 author and peer each passed 941 tests, plus 15 independent probe cases and six independently replayed mutants; its original 9,743-byte test prefix remains intact. Local publication integration passed 1,960 focused tests and 61 guards on the exact recorded tree. Unit publication adds no formal acceptance.

Root reviewed 49 publication paths, 17 original unit artifacts and 5,308 unchanged baseline blobs. Historical failed REST081 XML whitespace remains byte-exact. Original identities, paths, provenance and replay limits remain explicit in the pinned archive manifests. Content anchor `b601a40fe6a97ad5a66c400a5bfd5be5563fd4d1` and bundle digest `7c75d27f7c1558ffef6579df8025d1ed1b6f268d1a2d37f36754393967977d83` are unchanged.

## Historical skills checkpoints and guidance

[4de1e23](FEATURE-015-skills-ci-4de1e23.json) retains the previous 229 formal acceptances and 2,391 targeted/44 guard publication results. [ff70c30](FEATURE-015-skills-ci-ff70c30.json) retains REST073 unit-only publication and its original focused/guard/full-CI boundaries. The author 6,134 full-suite and distinct peer 1,911 focused results are separate historical runs.

[51f594c](FEATURE-015-skills-ci-51f594c.json) records the corrected REST073 guidance. Exactly two third-party guides change after the original 4,639-file preservation boundary; the other 4,637 protected files remain unchanged through that correction. `ThirdPartyApplication` returns only `rid`; `Version` returns only `version`. Request context and composed Website state supply the other information. Six affected semantic bindings received fresh independent review; other 419 rows and historical reviews remain unchanged. The reanchor changes only the global candidate and canonical bundle digest; seven pre-existing generator differences remain outside scope.

REST079/089 and REST073 native-unit archives remain in the pinned skills repository with original reports, JUnit, probes, source and mutation evidence. REST089 Arrow decoding evidence remains distinct from its transport-only placeholder and linked CSV lifecycle. REST073 restore guidance preserves the SDK docstring promising no effect for a nontrashed resource and qualifies its conflict with `ResourceNotDirectlyTrashed`. The SDK method does dispatch POST; the uncertainty concerns server behavior and the docstring's promised outcome.

Original failures remain archived: REST087 harness normalization, REST081 asynchronous response misuse, REST091 invalid PNG CRC, Third-party conflict wording and REST077 case controls. BUG-SUB-025's separate J12 reader passed 12 synthetic scenarios and all six grading criteria; broader journeys remain separate. No live Foundry tenant acceptance is claimed.

## CLI corrections and bounded security mitigation

The retained Geotemporal latest-value and historic-stream commands now preserve both legacy operation identities, literal routes, typed results, guards and authenticated SDK transport on SDK 1.101.0/1.111.0, with SDK 1.79.0 native positive control. Native methods take precedence; fallback applies only when these two methods are absent. Current `loadEntries` has a different contract. Global `ENABLED=false` returns exit 8 before SDK construction. Legacy backend availability and every possible SDK version remain unverified.

The [immutable tool evidence archive](FEATURE-015-tool-corrections-2026-11-19.zip) and [inventory](FEATURE-015-tool-corrections-2026-11-19-inventory.json) retain original harnesses, three corrected-candidate independent reports with 197 checks (66/66/65), literal route/model/error/retry/timeout/output/download/cancellation/inventory evidence, manifests, build logs, original wheel/sdist and full license bytes. The typing build used staged tree `46cdb36` with then-head `a8f23fd`; its version and source boundary remain historical. MIT and Apache-2.0 obligations are retained in Python and Conda metadata. Initial mypy failures and separate corrected checks are preserved.

The optional-body cases within the original 197 CLI checks used HTTP 200 empty bodies. A separate native decoder probe on all three SDK versions returns `None` for empty HTTP 200/204 and raises `ValidationError` for literal JSON `null`; it does not certify literal-null CLI success. The original probe, results and QA qualification remain archived without replay.

BUG-051 adds only four scanner/CI files after the accepted seven-file runtime/license candidate. Default local Safety policy and all seven runtime/license/test files remain byte-identical. Genuine Ubuntu/Linux live-database scanning with Safety 3.8.1/filelock 3.32.7 reports zero unsuppressed findings and exactly three temporarily ignored advisories. Residual vulnerabilities remain. Expiry is 2026-12-02 UTC; guarded CI refuses execution from that date. Unrelated findings and expired entries still fail; cache 0, full installed environment scanning, `pip check`, Bandit and strict failure remain enforced. The Windows synthetic-database exact/unrelated/expired backend checks are retained separately from genuine Linux scans.

Fresh main CI passed 1,506 tests with six warnings in each of four Ubuntu/Windows Python 3.11/3.12 jobs, including 16 scanner-boundary tests per job. Independent main QA verified all eight required names, exact head/tree/parents and original security/matrix logs. TASK-025 remains Open, owned by DevOps, first upstream review due 2026-11-24. Remove the exceptions earlier when a supported patched Safety release resolves the dependency; no automatic renewal is authorized.

Earlier Models and Third-party runtime fixes retain their original independent multi-SDK and CLI-page evidence. BUG-035 still requires an accepted skills-main pin for closure. [Shared CLI](FEATURE-015-shared-cli-corrections-2026-10-20/README.md), [Functions SSE](FEATURE-015-functions-sse-correction-2026-10-21/README.md), and [Filesystem/SQL](FEATURE-015-filesystem-sql-corrections-2026-10-21/README.md) archives retain their original heads and installation/test limits. Later evidence does not relabel those runs.

## Frozen tracker and remaining release work

The [capture manifest](FEATURE-015-tracker-capture-2026-11-16.json), [independent QA](FEATURE-015-tracker-capture-2026-11-16-independent-qa.json) and [evidence](FEATURE-015-tracker-capture-2026-11-16-evidence.json) describe only the November 16 12:54:42-12:55:13 UTC snapshot: 12,626 source files, 1,051 tickets across all statuses, 11,542 comments and 1,589 links. Its tree remains `afb9986836b50317116c0448bac91f652b4bb105`. Later workflow closures and selected CLI exports in the tool archive are publication-time captures outside it.

Six historical CSV repairs, the unrecoverable LINK-01279 boundary, raw link CSV and legacy CODE002 archive remain preserved. Engine bytes remain equal to reviewed commit `0b94163c:.ept/tools/tracker`; `0b94163c` identifies a commit, not a tree. No new engine execution is claimed. Configuration and prior integration ancestry remain retained.

The live parent checkout remains dirty and is outside these isolated release edits. DEVOPS-047 stays Open until G1-G7 acceptance is complete. Final skills-main publication, accepted parent pin and G8 verification follow the owning release work. No feature tag, package upload or live tenant deployment is included.
