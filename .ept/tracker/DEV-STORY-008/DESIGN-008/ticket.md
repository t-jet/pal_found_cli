---
id: DESIGN-008
type: design
title: 'DEV-STORY-008 DESIGN: functions skill OP_SPECS and implementation plan'
status: Closed
created: 2026-07-29
updated: 2026-07-29
priority: High
assignee: tech-lead
reporter: manager
estimated_hours: 4
time_spent_hours: 4
---

# DESIGN-008: DEV-STORY-008 DESIGN: functions skill OP_SPECS and implementation plan

## Description

Define the implementation plan for foundry-functions CLI exposing all 7 Functions API v2 operations across Query, ValueType, and ValueType.VersionId client paths. The design deliverable is .ept/docs/deliverables/architecture/DESIGN-008-functions-cli.md and the document index is updated.

## Acceptance Criteria

- [x] Design deliverable completed at .ept/docs/deliverables/architecture/DESIGN-008-functions-cli.md.
- [x] Document index updated for the design deliverable.
- [x] Operation catalog confirmed: query execute/get/get-by-rid/get-by-rid-batch/streaming-execute; value-type get; version-id get.
- [x] Client paths mapped: Query, ValueType, ValueType.VersionId.
- [x] JSON args defined: parameters, attribution, body.
- [x] Boolean flags defined: include_prerelease, preview.
- [x] No pagination operations identified.
- [x] Implementation, test, packaging, estimate, and risk plan documented.
- [x] Story sprint fit confirmed with total child estimate of 33h.
- [x] All child tickets exist and links are registered: DESIGN-008, DEV-008, UNITTEST-008, CODEREVIEW-008, TESTCASE-008, TESTEXEC-008, DEVOPS-008.

## Related Documentation

- .ept/docs/deliverables/architecture/DESIGN-008-functions-cli.md
- .ept/docs/document_index.md

## Notes

No active design blockers or open questions identified.
