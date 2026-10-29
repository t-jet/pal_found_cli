---
id: BUG-SUB-024
type: bug_subtask
title: Dataset File guide omits composed SDK client path
status: Closed
created: 2026-10-09
updated: 2026-10-11
priority: High
assignee: python-developer
reporter: qa-engineer
time_spent_hours: untracked
---

## Severity and version
High; SDK 1.101.0; pal_found_cli_skills candidate based on HEAD b40d0be, 2026-10-09.

## Reproduction
Source-blind J11 artifact .ept/tmp/feature015_rest_semantic_review/reader_j11_j13_j14.md followed the local File guide and authored `client.datasets.File.with_streaming_response.content`. In prepared SDK, `hasattr(client.datasets, "File")` is False and `hasattr(client.datasets.Dataset, "File")` is True. The authored path raises `AttributeError: DatasetsClient object has no attribute File`. Resource-level FileClient fixture exit 0 bypasses root traversal.

## Expected behavior
Standalone local Datasets guidance and a root-client fake-transport example show the correct composed path, method signature and result handling so an offline agent can write executable File operations.

## Acceptance criteria
- Document the verified public FoundryClient route for affected v1/v2 Dataset File operations and related nested resources as applicable.
- Add a root-client fake-transport regression that invokes the full path and checks request/result and named errors.
- Re-run source-blind J11 with corrected skill only; six dimensions pass, including actual composed call.
- Preserve all other frozen operation records and keep the full425 traversal gate under TESTCASE-064.

## Test reference
TESTEXEC-064; BUG-SUB-024 Blocks DEV-STORY-074 and TESTEXEC-064. No live tenant call occurred.
