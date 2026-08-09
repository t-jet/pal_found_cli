---
id: DESIGN-012
type: design
title: Design Foundry Language Models CLI and inference controls
status: Closed
created: 2026-08-09
updated: 2026-08-09
priority: High
assignee: tech-lead
reporter: tech-lead
estimated_hours: 4
time_spent_hours: 4
---

# DESIGN-012: Design Foundry Language Models CLI and inference controls

## Description

Produce the implementation-ready Language Models design and register it in the document index.

## Acceptance Criteria

- Define the exact two-operation SDK and HTTP contract with public JSON flags and exact internal keyword names.
- Correct AccessControlGuard by adding messages and embeddings to _WRITE_VERBS; specify ENABLED, read-only override, metadata-only, and Tier 3 tests.
- Define attribution=True, B3 restoration, privacy, retry/timeout/error, JSON output, packaging, and installed execution.
- Include artifact ownership, dependencies, risks, estimates, QA matrix, rollback concerns, and document-index link.
- Close before DEV-STORY-012 enters Development.

## Related Documentation

- DEV-STORY-012
- .ept/docs/document_index.md

## Notes

No open question.
