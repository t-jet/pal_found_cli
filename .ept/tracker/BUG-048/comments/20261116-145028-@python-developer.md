Subject: 2026-11-16 developer readiness and runtime correction plan
Created: 2026-11-16T14:50:28
Updated: 2026-11-16T14:50:28
---
## Open readiness
Reviewed all five comments, five links, indexed BA-DES-015/SA-DES-014 ownership and verification guidance. Reproduction, environment, expected/actual behavior and frozen logs are attached in ticket and QA comment. Native SDK hierarchy identifies a bounded path defect; no unanswered requirement needs a Question. Historical Closed tickets stay unchanged.
## Plan
1. Isolate published main 223d2c0bfe3b4ed9a1f8aa35cc98a07cf2a3238f; verify source hash.
2. Add native SDK transport regression coverage and reproduce failures before correcting eight OP_SPECS paths.
3. Run actual CLI parser/guards against SDK 1.101.0 and 1.111.0, assert wire contracts, paging/recovery, errors and pre-HTTP denials.
4. Submit exact source/test hashes and checks for separate peer review and independent QA. No commit, push or Resolved transition before review.
