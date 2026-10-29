Subject: Core REST catalog candidate 9a73c1f
Created: 2026-10-11T07:05:09
Updated: 2026-10-11T07:05:09
---
## Implemented and verified
- Commit `9a73c1fef94e609eaa8aa8f8f97750f84ab381ab` contains `scripts/offline_rest_catalog.py`, `maintainer/rest-contract-register.json`, new `maintainer/rest-model-semantic-matrix.json`, 429 contract parts, 100 model parts, 20 namespace indexes, and corrected v1/v2 Dataset.File guides. `maintainer/rest-model-register.json` was unchanged. Git staged path audit found zero out-of-scope paths; cached diff check and Python compile passed.
- Pinned SDK 1.101.0 source commit `168d51910570b6966afa2320333ab36f6a3f7ccf`: rerender reports 425 operations and 3,251 reachable symbols (2,278 models, 964 errors, 9 core). Every namespace index has a capability/lifecycle description. The source-backed review matrix has 3,251 unique symbol IDs, exact definition/page/prose hashes, dependencies and consuming operation IDs; all source-fidelity and local-meaning dispositions remain pending independent review. It flags 489 blank/todo upstream descriptions.
- Reader-facing model prose before untouched exact SDK source fences has zero documentation-domain public URLs. Current full 20-skill URL audit belongs to QA; do not use stale prior counts. Corrected File guide hashes: v1 `005c574e16326d2cb760b7abec840222cd3c879ee3946cf68c68623bb9809b67`, v2 `7a0bf6c4a67c5024a7ecd11184d584a2c02271d4d997fef8b99f0be71204fee0`. These require independent BUG-SUB-024 review.
## Verification and remaining gates
- Focused REST acceptance/wave1 pytest: 522 passed, 2 failed. QA-owned source oracle rejects localized SMB field prose, and QA-owned v1 async get_schema fixture omits required `preview=True`; QA is correcting those tests. No real network was used by these fixture tests.
- DEV-064 remains In Progress: independent per-symbol and operation semantic review, QA audit, all unit/code-review gates and final test pass remain outstanding. No live tenant execution or acceptance claimed.
