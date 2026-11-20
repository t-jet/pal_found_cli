Subject: Correction plan and reproduced root cause
Created: 2026-11-19T14:23:51
Updated: 2026-11-19T14:23:51
---
## 2026-11-19 correction plan

Read indexed SA-DES-014 section 2.2, the REST authoring handoff, and the independent review. The two reader examples append each page then continue whenever a token exists. Repeated tokens or an endless sequence of fresh tokens have no page, item, or elapsed-time stop; their final membership assertions could imply complete enumeration after a caller interrupts them. The independent SDK-shaped probe reproduced 100 duplicate pages before its external guard stopped request 101.

1. Correct the two owned worked examples in an isolated skills worktree at commit 163cb1f6. Add finite page and item budgets, a deadline checked before each request, repeated-token detection, and an explicit partial-result outcome. Preserve empty-page continuation, normal terminal completion, object identity, and raw-response closure.
2. Add one focused offline regression that executes both published algorithms with repeated tokens, fresh tokens beyond limits, empty intermediate pages, normal completion, and closure. Run the existing 081 and native SDK gates.
3. Update only register rows that point to these two behavior pages: their behavior hashes and semantic disposition become pending independent review. Report exact hashes, tests, scope and limits to the architect. No SDK, model, fixture, CLI, other guide, or global anchor change is planned.

The bound prevents new calls after its deadline check; an in-flight synchronous SDK call can finish later. A partial result must not be reported as a complete inventory. No tenant behavior is inferred from the offline probe.
