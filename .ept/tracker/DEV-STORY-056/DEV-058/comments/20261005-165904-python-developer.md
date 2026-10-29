Subject: Correction: local SDK paths removed
Created: 2026-10-05T16:59:04
Updated: 2026-10-05T16:59:04
---
After CODEREVIEW-058, removed 19 remaining shorthand SDK docs/v2 references from the existing skill pages: admin (entry and four reference guides), audit, checkpoints (entry and guide), data-health (entry and guide), media-sets, ontologies, sql-queries (entry and guide), streams, third-party-applications (entry and guide), widgets (entry and guide). Public Palantir links and operation meaning remain. Earlier changes removed five .ept SDK paths from inputs.md and the widgets SA-DES citation; 18 entry points had EOF whitespace corrected. Verification: rg -n docs/v[12] .agents/skills (no matches); focused pytest tests/test_foundry_development_skill.py tests/test_offline_skill_gate.py tests/test_skill_documentation.py: 16 passed; git diff --check clean. No new or deleted files in this correction. Parent PM will commit this correction with the test update.
