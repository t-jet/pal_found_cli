Subject: 2026-10-11 developer fix and Resolved DoD evidence
Created: 2026-10-11T12:06:56
Updated: 2026-10-11T12:06:56
---
## Fix and verification
- Cause: J11 reader followed a Dataset File guide that omitted the public nested route, so client.datasets.File raised AttributeError. Detached FileClient fixture passed despite the broken root-client path. Reproduction and expected/actual behavior are in comment 20261010-203628-python-developer and the ticket body.
- Fix: committed v1 and v2 File guides in skills commit 9a73c1f state client.datasets.Dataset.File. Their current SHA-256 values match the independent review: v1 005c574e16326d2cb760b7abec840222cd3c879ee3946cf68c68623bb9809b67; v2 7a0bf6c4a67c5024a7ecd11184d584a2c02271d4d997fef8b99f0be71204fee0. The exact v1/v2 operation contracts give the same route.
- Regression: committed a4df63e adds examples/rest/074/v2/datasets/file_client_route_regression.py. I ran it with installed SDK 1.101.0 and httpx.MockTransport: exit 0; both public composed routes, serialized paths, binary bytes, omitted optional size and named missing-file 404 passed. Independent tech-lead PASS is comment 20261011-070608-tech-lead.
- Reader outcome: QA comment 20261010-012923-qa-engineer records fresh isolated J11 6/6 with DNS/socket denied and frozen output; original 3/6 failure remains historical. This establishes source and fixture behavior only. No live tenant call or all425 semantic acceptance is claimed.
- Time: time_spent_hours is recorded as untracked because contributor time across earlier author and resumed work cannot be reconstructed reliably; no fabricated estimate.
- Links: BUG-SUB-024 already blocks DEV-STORY-074 and TESTEXEC-064. No unresolved QUESTION sub-task. Indexed BA-DES-015/SA-DES-014 and SDK 1.101.0 scope reviewed. All In Progress to Resolved criteria are met; QA retains closure verification.
