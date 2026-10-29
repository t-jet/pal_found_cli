Subject: Source-backed REST model corrections 1099bae
Created: 2026-10-11T22:32:41
Updated: 2026-10-11T22:32:41
---
## Candidate correction
- Commit `1099bae3cc8c6dbcf9e5682595cb3717f9e41908` changes exactly ten scoped files: `scripts/offline_rest_catalog.py`, `maintainer/rest-model-semantic-matrix.json`, and eight local model pages for v1/v2 `TransactionNotOpen`, v1/v2 `PropertyValue`, v2 `AgentRid`, `ConnectionWorker`, `CreateConnectionRequestConnectionWorker` and `CreateConnectionRequestUnknownWorker`. Git staged path audit found zero unexpected/missing files; postcommit owned paths were clean.
- Pinned SDK 1.101.0 rerender returned 425 operations and 3,251 symbols. Matrix page hashes match all 3,251 current pages. Both PropertyValue pages derive all 21 type-to-JSON encodings from frozen SDK `docs/v1|v2/Ontologies/models/PropertyValue.md`, include 21 JSON-parseable synthetic examples each, and record pinned documentation hashes. Exact SDK Python source fences remain intact. Transaction recovery uses the reported status and authorized reads without assuming write replay; Agent RID discovery and Connection worker variants match exposed SDK methods/unions.
## Verification and remaining gates
- `tests/test_offline_rest_acceptance.py`: 6 passed; generator Python compile and scoped `git diff --check` passed. These structural checks do not approve reader semantics. Independent model reviewer is rechecking changed pages; all unreviewed matrix rows remain pending. The prior all-skills URL audit snapshot predates these skill edits and requires QA refresh. No live tenant execution claimed.
- `.ept/docs/document_index.md` two-link maintenance is managed by the project manager under the relevant documentation scope; this DEV-064 content commit did not edit that index. DEV-064 remains In Progress pending independent review and remaining gates.
