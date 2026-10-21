# FEATURE-015 draft release status

Last verified: 2026-10-22 (Europe/Sofia). FEATURE-015 remains in draft review. No feature release merge, tag, package upload or live tenant deployment has been performed in this workflow.

## Published candidates

| Repository | Draft | Reviewed candidate | Verification |
| --- | --- | --- | --- |
| Skills | [PR #1](https://github.com/t-jet/pal_found_cli_skills/pull/1) | `2190c40c3f73636b91348167b86cdb1bd7fb6fd7` | GitHub validation passed. Accepted records have no stale source, asset or candidate hashes. |
| CLI tool | [PR #1](https://github.com/t-jet/pal_found_cli_tool/pull/1) | `a3a38ec434fdb046c329b850e716dc541fa87ecd` | All eight GitHub checks passed: Ruff, mypy, Python 3.11/3.12 tests on Windows/Linux, security and package build. |
| Parent | [PR #6](https://github.com/t-jet/pal_found_cli/pull/6) | Paired pins above; release branch `2034b66`, tracker capture `3ae09324` | Both reviewed pins advanced together. Reviewed code, QA artifacts and repaired tracker capture are integrated. |

The skills release verifier remains blocked by 322 formal operation QA items, 237 semantic operation reviews and 64 skill-review items (63 pages plus overall signoff). Journey acceptance and other workflow gates remain separate. These counts are pending work, not approved exceptions.

## Accepted QA

All 36 development topics retain independent acceptance. Whole-page review now accepts 129 of 192 pages at current hashes. Recent accepted groups include Admin governance/Audit, Datasets, Functions, Filesystem, AIP Agents and SQL. Their reports preserve original findings, separate authors and independent retests. URL-location repairs retain the historical scan's scope; they do not claim a new whole-bundle URL scan.

| Story | Formal result | Current workflow |
| --- | --- | --- |
| DEV-STORY-072 | 40 operations, 612 checks and all 113 declared errors passed. Seventy archived artifacts have verified hashes. | Deployment; all six workflow children Closed. |
| DEV-STORY-074 | 52 operations, 1,060 assertion rows and all 288 declared errors passed. Eighty-seven archived artifacts have verified hashes. | Deployment; all six workflow children Closed. |
| DEV-STORY-085 | Eleven Functions SDK operations and 91 checks passed with public sockets denied. | Deployment; all six workflow children Closed. |

Story 074 retains its first failed harness attempt and the independently approved correction to typed-value normalization. Original case literals and all 156 assets remained unchanged. Full comment exports and mutation records are preserved; the concurrent read-log corruption and its canonical transcript repair are documented. No failed attempt was presented as a successful run.

REST-074 has 52 accepted semantic reviews, including eight corrected fixtures and independent retests. REST-073 has 47 accepted meanings; Resource.restore remains uncertain because the SDK no-op prose conflicts with a declared error. Its accurate Filesystem guidance explains that conflict without waiving the operation gate. DEV-STORY-081 retains eleven non-private semantic acceptances and eleven private-beta reviews pending. BUG-SUB-025 and its J12 dependency remain active.

## CLI corrections and evidence boundaries

BUG-036 through BUG-045 are Closed with resolution Done. Their verified blocking links were removed; other relationships remain. DEV-STORY-070 remains Development and BUG-034 still blocks it through LINK-01959. BUG-035 has a targeted Audit correction PASS and the Audit whole page is accepted; its broader workflow remains separate.

- [Shared CLI evidence](FEATURE-015-shared-cli-corrections-2026-10-20/README.md) records 1,684 regression tests, 330 contract probes and actual SDK build-search pagination at tool `657215f`. Six clean installs, six dependency checks and twelve console TOON round trips cover wheel, sdist and Conda on Python 3.11/3.12 at that original head. Follow-up annotation-only `2feb1fe` has independent continuity and passing CI evidence.
- [Functions SSE correction](FEATURE-015-functions-sse-correction-2026-10-21/README.md) records BUG-043 at `ddfab5d`: real SDK SSE decoding inside retry/client scopes, buffered NDJSON, timeout/cancellation/cleanup, six pages and seven examples. Independent tests passed 103 cases on SDK 1.101 and 46 on SDK 1.111. Existing REST-085 SDK SSE evidence remains valid; the defect was in the CLI adapter.
- [Filesystem and SQL corrections](FEATURE-015-filesystem-sql-corrections-2026-10-21/README.md) records BUG-044 positional JSON decoding at `0669700` and BUG-045 required-query forwarding at `a3a38ec`. Filesystem review passed all 31 actual SDK HTTP examples, eight boolean and five pagination probes; the author passed 144 tests on each SDK release. SQL independent QA passed five wire cases on each SDK release; the author passed 30 tests on each. Four Filesystem and two SQL pages passed independent retest.

These later candidates have exact-head CI builds and scoped runtime checks. The six-install package reports remain tied to `657215f`; they are not rebuild results for every later head. All requests used synthetic inputs and mocked transport. Ten legacy metadata rows in the adapter scan remain UNCERTAIN and need separate compatibility review; structural adapter checks do not replace full operation acceptance.

QUESTION-192 and QUESTION-193 are Closed after independent acceptance. The [approved contract amendment](../architecture/FEATURE-015-shared-cli-contract-amendment-2026-10-20.md) records one effective SDK/outer timeout, four total calls by default, preserved explicit max_retries compatibility, and the TOON dependency/API correction to toon-format 1.2.0 and toon_format.dumps(). The architect's follow-up preserves HTTP 429 exhaustion exit 7 and HTTP 503 exhaustion exit 6.

## Tracker and working copies

[Tracker PR #5](https://github.com/t-jet/pal_found_cli/pull/5) at `3ae09324cb54890e623370c21da7f32d01b81bf9` contains 1,029 indexed tickets, 1,566 valid unique links and 10,870 comments matching live bytes. [Independent capture QA](../../feature015_tracker_capture_qa_2026-10-22.json) passed with zero errors and stable live/capture fingerprints. Counter 2028 exceeds maximum surviving link ID 2027 after verified blocker removal. The six historical CSV repairs, original archive hash and unrecoverable LINK-01279 boundary remain intact.

Tracker QA covers captured data. Its 45 tracked engine files are unchanged from that branch's previous head; this does not assert that older live engine files equal the separately reviewed integration code. The integration engine previously passed 442 tests; no engine source changed in this capture.

The live parent checkout remains dirty. At the [latest byte audit](../../feature015_local_publication_audit_2026-10-22.json), main was 11 commits ahead and seven behind origin/main. Of 474 dirty entries, 473 files matched the integration or agent-configuration draft exactly; the only different dirty file was the malformed live link CSV, whose repaired draft passed independent QA. This audit compares dirty entries, not every source file in the repositories. Copying the live tree wholesale would discard newer code and documented repairs.

Agent-configuration [PR #7](https://github.com/t-jet/pal_found_cli/pull/7) remains at `1218b00e`; the latest comparison found no live self-improvement note differences. Keep all release PRs draft and rerun exact-head verification and the release gate before any release merge or tag.
