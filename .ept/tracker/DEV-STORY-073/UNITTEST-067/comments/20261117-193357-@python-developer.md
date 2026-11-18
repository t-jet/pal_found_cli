Subject: Native SDK101 transport test plan and readiness
Created: 2026-11-17T19:33:57
Updated: 2026-11-17T19:33:57
---
## Plan
1. Add only tests/test_offline_rest_073.py in isolated clean worktree at 4de1e23e98017536bcff0eef2aa1d057e576e056. Preserve existing semantics/restore guards and all other tracked bytes.
2. Reconcile 11 resource modules with frozen SDK1.101.0 commit168d51910570b6966afa2320333ab36f6a3f7ccf and independently recorded source oracle. Exercise all48 ordinary/raw sync/async calls and all33 streaming sync/async calls (258 available forms); assert15 void operations have no streaming wrappers. Verify exact escaped wire requests, typed results and165 named-error entries.
3. Cover eight bounded two-page pagers with direct async iterators, unfinished stream closure/cancellation, buffered cancellation rejection, binary log/download and upload, project template invocation, void204 results and rejected request mutations. Use real SDK with httpx.MockTransport and denied external network.
4. Run focused tests, existing073 guards, lint and appropriate full-suite checks with QA artifacts under parent .ept/tmp. Submit author evidence for separate independent peer review; no commit, publication or formal acceptance claimed.
## Readiness
Read document index, indexed FEATURE-015-rest-authoring-contract.md, exact partition, full current ticket metadata/DoD, DEV068 plan, DESIGN068 technical plan and independent lead approvals, and parent Development checkpoint. DESIGN068 Closed; DEV068 In Progress and existing runnable48 examples ready for tests. No linked open question blocks UNIT067. Current Open DoD met by this test plan and linked documentation. Restore no-op prose versus ResourceNotDirectlyTrashed remains source-policy uncertainty; tests preserve both facts without platform-policy claims.
