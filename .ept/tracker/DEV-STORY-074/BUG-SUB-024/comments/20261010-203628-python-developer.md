Subject: 2026-10-10 developer reproduction and fix plan
Created: 2026-10-10T20:36:28
Updated: 2026-10-10T20:36:41
---
## Reproduction and root cause
- SDK 1.101.0, isolated pal-found-dev and synthetic MockTransport. Original J11 source-blind answer: .ept/tmp/feature015_rest_semantic_review/reader_j11_j13_j14.md. It calls client.datasets.File.with_streaming_response.content, but the public FoundryClient.datasets has no File attribute. Recorded error: AttributeError: DatasetsClient object has no attribute File. Detached FileClient fixtures missed lazy public client composition.
- Expected: v1/v2 File calls use client.datasets.Dataset.File, validate bytes and named errors, and stop within finite bounds.
- Current correction: v1/v2 File guides and contracts state the nested route. The root-client regression at pal_found_cli_skills/.agents/skills/pal-found-dev/examples/rest/074/v2/datasets/file_client_route_regression.py invokes both composed clients with MockTransport and asserts path, bytes, omitted size and named 404. Command python -B pal_found_cli_skills/.agents/skills/pal-found-dev/examples/rest/074/v2/datasets/file_client_route_regression.py exited 0; stdout says v1/v2 composed File routes, omitted size, bytes and named error passed. Regression is currently untracked pending owner commit.
- QA evidence: BUG-SUB-024 comment 20261010-012923-qa-engineer and TESTEXEC-064 comment 20261010-012917-qa-engineer record fresh J11 6/6, frozen script/output hashes, DNS/socket denial. Historical J11 3/6 remains. This proves fixture behavior only; live tenant access and all425 semantic review are outstanding.
## Fix plan
1. Keep exact nested route in both File guides and root-client regression; confirm owner commits them.
2. Preserve old and fresh QA evidence and existing Blocks links to DEV-STORY-074 and TESTEXEC-064.
3. Seek independent content review, then advance BUG workflow status only as each DoD passes. No new question is needed because the public SDK resolves the route.
