---
id: DESIGN-013
type: design
title: 'DEV-STORY-013 DESIGN: models skill OP_SPECS and implementation plan'
status: Closed
created: 2026-08-09
updated: 2026-08-09
priority: High
assignee: tech-lead
reporter: architect
estimated_hours: 6
---

# DESIGN-013: DEV-STORY-013 DESIGN: models skill OP_SPECS and implementation plan

## Description

# DESIGN-013: DEV-STORY-013 DESIGN: models skill OP_SPECS and implementation plan

## Description

Define the implementation plan for the foundry-models CLI exposing all 23 Models API v2 operations across LiveDeployment, Model, Model.Version, Model.Experiment, Model.Experiment.Series, Model.Experiment.ArtifactTable, ModelStudio, ModelStudio.ConfigVersion, ModelStudio.Run, and ModelStudio.Trainer client paths. The design deliverable is .ept/docs/deliverables/architecture/DESIGN-013-models-cli.md and the document index is updated.

## Acceptance Criteria

- [x] Design deliverable completed at .ept/docs/deliverables/architecture/DESIGN-013-models-cli.md.
- [x] Document index updated for the design deliverable.
- [x] Operation catalog confirmed: 23 commands per the authoritative catalog in DEV-STORY-013.
- [x] Client paths mapped including nested Version, Experiment, Series, ArtifactTable, ConfigVersion, Run, and Trainer clients.
- [x] JSON args defined and validated before client creation.
- [x] Pagination scope defined: exactly four cursor-paged commands via PaginationHelper; offset/page_size are service-side slicing only; trainer list has no cursor.
- [x] Streamed downloads defined: series parquet and artifact-table json/parquet via BinaryDownloadHandler with atomic persistence.
- [x] ACL write classification corrected: launch and promote_version are writes; experiment search is a semantic read.
- [x] Metadata-only policy packaged with exact 12-permitted/11-blocked behavior.
- [x] No-attribution runtime and SDK-native B3 tracing confirmed.
- [x] Implementation, test, packaging, estimate, and risk plan documented.
- [x] Story sprint fit confirmed with total child estimate.
- [x] All child tickets exist and links are registered: DESIGN-013, DEV-013, UNITTEST-013, CODEREVIEW-013, TESTCASE-013, TESTEXEC-013, DEVOPS-013.

## Related Documentation

- .ept/docs/deliverables/architecture/DESIGN-013-models-cli.md
- .ept/docs/document_index.md

## Notes

No active design blockers or open questions identified.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
