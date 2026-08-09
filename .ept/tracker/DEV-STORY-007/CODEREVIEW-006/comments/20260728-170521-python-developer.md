Subject: Correction evidence commit b291eae
Created: 2026-07-28T17:05:21
Updated: 2026-07-28T17:05:21
---
Correction evidence for commit b291eae Handle sync byte iterators in ontologies CLI:
- Fixed _bytes_iter to support sync byte iterables.
- Added regression test covering sync byte iterator handling.
- Verification: focused ontology tests 157 passed; ruff scoped passed; mypy src CLI passed; full pytest 472 passed.
- Blockers/questions: no Blocks or Question links found on CODEREVIEW-006.
