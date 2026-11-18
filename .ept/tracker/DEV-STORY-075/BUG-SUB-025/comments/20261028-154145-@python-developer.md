Subject: Committed final-candidate J12 evidence satisfies developer resolution gate
Created: 2026-10-28T15:41:45
Updated: 2026-10-28T15:41:45
---
## Root cause and implemented correction

The original per-operation examples checked shapes independently. They did not compose staged File.get/content checks before commit, branch/file checks after commit, or distinguish a terminal Build state from successful completion. The original source-blind reader therefore scored 4/6 despite six method fixtures passing.

The historical implementation and independent source/API review are recorded in comments 20261011-223043-python-developer and 20261011-223156-tech-lead for d2ce40a. Current evidence is bound to committed skills revision `e44b97ed51f438ea495096287565cd064c77b150` rather than reusing the earlier fixture hash. The current composed journey SHA256 is `b260986ea80bb57f0e25c72b728918291484eab242b4bf1ab8ff63622fdf076e`; Transaction.md is `d16435f483e07e822d7b79fd13b06744ca196c1f594f985a490f5b8c6c51c3ef` and Build.md is `ad26f97daf4f9b9a117c28f343794e5eb710e0967d85072976985d4541b64499`.

## Committed independent verification

- Fresh reader `/root/j12_reader_recover_20261028` used only the standalone skill and prepared SDK 1.101.0 runtime. Its reader answer SHA256 is `65cc2f91075a54a5902e948801d706c87a119ec404f6044bcb04bee559015fe8`.
- Separate grader `/root/j12_independent_grade_20261028` approved all six rubric dimensions, reproduced all 12 synthetic scenarios, and verified artifact/source integrity. Grade SHA256 is `0b81f4c254d2f21cf19217e4eb9c158a2430d2d4a5809718d96e899b0a0f582c`.
- Durable acceptance: `maintainer/j12-independent-acceptance-20261028.json`, SHA256 `6acb2c856d19e3478879cb984b9ac62f2352b5b9ddd33f0044f58fa2ac54cae9`. Archive context: `maintainer/evidence/j12-20261028/archive-context.json`, SHA256 `5fc3edf93369f1ab06466fe00e4ef44073da7dd77b4f03f8f3cfaaaabe781828`.
- All 90 original archived artifacts plus acceptance/context are committed and unchanged. All 23 consulted current source files match both their recorded hashes and that commit. The complete 4,437-file historical snapshot manifest and original 4/6 failure artifacts are preserved without claiming every current unconsulted file equals the historical snapshot.
- Current composed seven-case regression evidence is retained separately from the fresh 12-scenario reader and independent reproduction. This handoff verifies existing immutable evidence; it does not claim an additional runtime retest.

## In Progress DoD and handoff

Related documentation was consulted through `.ept/docs/document_index.md` and the approved SA-DES-014 verification rubric. Required fields, parent context, root cause, implementation, regression and linked evidence were checked. No Question sub-task or Question link exists on this bug. Contributor hours remain explicitly `untracked` in frontmatter, as approved in comment 20261011-223401-python-developer; no numeric contributor time is invented.

The committed-evidence prerequisite in that comment is now satisfied. Resolve for separate QA verification only. Preserve Blocks `LINK-01894` to TESTEXEC-064 and RelatesTo `LINK-01893` to DEV-STORY-074; QA owns the verified blocker removal and final closure.

These are synthetic SDK HTTP and offline reader results, not live tenant mutations, authorization, server-side builds or OS-wide network isolation. Full REST075 formal QA, TESTEXEC-064's remaining scope, publication and FEATURE-015 release acceptance remain separate gates.
