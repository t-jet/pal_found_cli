Subject: 2026-10-11 root cause and in-progress evidence
Created: 2026-10-11T22:30:43
Updated: 2026-10-11T22:30:43
---
## Root cause
The local per-operation examples checked request and response shapes separately. No composed J12 path checked transaction-view File.get/content before commit, branch-view File.get/content after commit, or the difference between a terminal Build status and successful completion. The original reader therefore produced an incomplete sequence despite six method fixtures passing.

## Implemented correction
Commit `d2ce40a` adds a root-client SDK 1.101.0 journey with seven finite MockTransport cases: SUCCEEDED, FAILED, CANCELED, RUNNING after budget, lost upload reply, lost commit reply, and explicit abort. It asserts staged and committed file views, known transaction RID reconciliation, and exactly one create/upload/commit mutation where applicable. Transaction.md and Build.md explain the lifecycle and finite Build.jobs diagnostics. The public SDK jobs cursor probe and the seven-case journey exited 0 without public DNS/socket access. These are synthetic fixtures, not live tenant execution.

## Remaining verification
Independent tech-lead handoff reports source/API PASS for `d2ce40a`, pending durable peer comment. QA reports a final-candidate source-blind provisional 6/6 on snapshot `6949469` with 20 consulted files byte-matching, pending committed hashes and formal score. Preserve original 4/6 evidence. Do not resolve until these two records are durable. Contributor time remains untracked because actual hours were not measured.
