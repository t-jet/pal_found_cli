---
id: DESIGN-014
type: design
title: 'DEV-STORY-014 DESIGN: orchestration skill OP_SPECS and implementation plan'
status: Closed
created: 2026-08-09
updated: 2026-08-09
priority: High
assignee: tech-lead
reporter: architect
estimated_hours: 6
---

# DESIGN-014: DEV-STORY-014 DESIGN: orchestration skill OP_SPECS and implementation plan

## Description

Define the implementation plan for the foundry-orchestration CLI exposing all 20 Orchestration API v2 operations across Build, Job, Schedule, ScheduleRun, and ScheduleVersion client paths. The design deliverable is .ept/docs/deliverables/architecture/DESIGN-014-orchestration-cli.md and the document index is updated.

## Acceptance Criteria

- [ ] Design deliverable completed at .ept/docs/deliverables/architecture/DESIGN-014-orchestration-cli.md.
- [ ] Document index updated for the design deliverable.
- [ ] Operation catalog confirmed: 20 commands per the authoritative catalog in DEV-STORY-014 (cross-validated from SDK source, canonical env var reference, and metadata allow-list).
- [ ] Client paths mapped: Build (6 ops), Job (2), Schedule (10), ScheduleVersion (2), ScheduleRun (0 — sub-client exists, no public methods).
- [ ] JSON args defined and validated before client creation for schedule.create, schedule.replace, and build.create.
- [ ] Pagination scope defined: exactly three cursor-paged commands (build.jobs, build.search, schedule.runs) via PaginationHelper with the exact-page pattern; batch get_batch and search responses are single-call, no paging.
- [ ] ACL write classification confirmed: 8 mutating operations blocked; 12 read operations permitted; get_affected_resources is a semantic read despite POST.
- [ ] Metadata-only policy packaged with exact 12-permitted/8-blocked behavior.
- [ ] No-attribution runtime (orchestration outside FR-ATTR-4) and SDK-native B3 tracing confirmed.
- [ ] Implementation, test, packaging, estimate, and risk plan documented.
- [ ] Story sprint fit confirmed with total child estimate.
- [ ] All child tickets exist and links are registered: DESIGN-014, DEV-014, UNITTEST-014, CODEREVIEW-014, TESTCASE-014, TESTEXEC-014, DEVOPS-014.

## Related Documentation

- .ept/docs/deliverables/architecture/DESIGN-014-orchestration-cli.md
- .ept/docs/document_index.md
- DEV-STORY-014 (comment 20260809-200456-architect — technical scope and operation catalog)

## Notes

No active design blockers or open questions identified.
