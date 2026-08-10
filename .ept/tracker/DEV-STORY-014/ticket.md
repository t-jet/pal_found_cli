---
id: DEV-STORY-014
type: dev_story
title: foundry-orchestration skill (20 operations)
status: Closed
feature_request: FEATURE-001
epic: EPIC-006
created: 2026-04-13
updated: 2026-08-10
priority: High
assignee: architect
reporter: architect
release_notes: 'Adds the foundry-orchestration skill exposing all 20 Orchestration API v2 operations
  across 5 SDK classes (build: cancel, create, get, get_batch, jobs, search; job:
  get, get_batch; schedule: create, delete, get, get_affected_resources, get_batch,
  pause, replace, run, runs, unpause; schedule_version: get, schedule) as a subprocess-invocable
  CLI that reuses the EPIC-001 common library (AccessControlGuard, RetryHandler, OutputFormatter,
  ErrorSerializer, LogSetup, TracingProvider, PaginationHelper). Attribution headers
  are NOT injected (orchestration is outside FR-ATTR-4 scope; include_attribution=False).
  Under the metadata-only tier, the 8 mutating operations (build.cancel, build.create,
  schedule.create, schedule.delete, schedule.pause, schedule.replace, schedule.run,
  schedule.unpause) are blocked while the 12 read operations are permitted. The 3
  cursor-paged commands (build.jobs, build.search, schedule.runs) use PaginationHelper
  with the exact-page pattern.'
---

# DEV-STORY-014: foundry-orchestration skill (20 operations)

## Description

Generate and validate all 20 orchestration namespace operations. Covers schedule management, build triggering, job status monitoring.

## New to Open DoD evidence (2026-08-09, architect)

- Studied related documentation: document_index, SRS-001, SAD-001, ADR-001/002/004/005/006/007, canonical env var reference, metadata allow-list, vendored SDK orchestration namespace
- Critical thinking applied; no open questions
- No QUESTION sub-tasks open under this ticket
- FEATURE-001 confirmed Waiting for Implementation
- Epic link established: LINK-00276 (EpicLink to EPIC-006)
- Feature links established: LINK-00274 (Contains), LINK-00275 (ParentChild)
- Required fields validated: status New, assignee architect, priority High, created/updated dates present
- Technical scope documented in comment 20260809-200456-architect

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
