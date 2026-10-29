Subject: 2026-10-11 developer reproduction and correction plan
Created: 2026-10-11T22:29:48
Updated: 2026-10-11T22:29:48
---
## Reproduction and requirement
BA-DES-015 J12 and SA-DES-014 J12 require transaction create/upload/get/commit/abort, staged and branch file visibility, finite Build status, and reconciliation after uncertain writes. The original source-blind artifact in `pal_found_cli_skills/tests/fixtures/feature015_qa/evidence/feature015-j12-reader/reader-results.md` scored 4/6; `feature015_rest_semantic_review/j12_independent_score.md` records missing staged File.get/content, postcommit Branch/File checks, and FAILED/CANCELED handling. Expected: one composed public SDK route with these checks and no blind write replay. Actual: individual method fixtures passed while the composed journey omitted them.

## Environment and logs
Pinned `foundry_sdk` 1.101.0; synthetic SDK MockTransport, denied DNS/socket, no tenant operation. `python -B .agents/skills/pal-found-dev/examples/rest/074/v2/datasets/staged_commit_journey.py` exited 0: seven staged transaction and Build outcomes passed with public network denied. `python -m py_compile` exited 0; all three guide Python blocks parsed; scoped `git diff --cached --check` exited 0. Commit `d2ce40a` contains only the integrated journey, Transaction guide, and Build guide. The guide Build.jobs loop was exercised through the public SDK route with empty intermediary and repeated cursor rejection; the local probe was temporary and is not release evidence.

## Correction plan and review boundary
Keep the original 4/6 failure as history. Ask independent tech lead to make the source/API review durable in a ticket comment and QA to score the final committed candidate using the fresh isolated J12 reader. The independent reviewer handoff reports PASS for `d2ce40a` source/API and seven fixture cases; no formal peer ticket comment exists yet. Resolve this bug only after final six-dimension QA PASS and peer record. OWASP self-check: synthetic credential only, bounded polling/pages, no public network, no live write; tenant identity and permissions remain prerequisites. Actual contributor hours were not measured, so time spent is untracked.
