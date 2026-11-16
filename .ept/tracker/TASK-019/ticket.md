---
id: TASK-019
type: task
title: Capture current FEATURE-015 tracker publication snapshot
status: In Progress
priority: High
assignee: devops-engineer
reporter: devops-engineer
created: 2026-11-16
updated: 2026-11-16
---

# TASK-019: Capture current FEATURE-015 tracker publication snapshot

## Description

## Scope
Capture all tracked and nonignored tracker source blobs through a temporary Git index under a writer freeze. Apply only the reviewed historical repairs to the exported isolated copy. Preserve published tracker and engine history.

## Acceptance criteria and deliverables
- Prepare branch feature015/parent-tracker-data with stable as-of tracker capture and provenance, retaining prior repair/archive history.
- Deliver .ept/docs/deliverables/qa/FEATURE-015-tracker-capture-2026-11-16.json with raw Git tree proof, export counts, repair baseline/diff, CODE002 archive proof, CLI status evidence, and source-engine continuity.
- Obtain independent QA before commit or push; publish only after root review.
- Record freeze boundaries and later comments as outside the snapshot. No feature closure or main merge.

## References
TASK-018; TASK-014; .ept/docs/document_index.md; existing DATAHEALTH-release-pin.md.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
