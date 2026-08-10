---
id: DEV-013
type: development
title: 'DEV-STORY-013 DEV: foundry-models CLI implementation'
status: Closed
created: 2026-08-09
updated: 2026-08-10
priority: High
assignee: python-developer
reporter: architect
estimated_hours: 16
time_spent_hours: 16
---

# DEV-013: DEV-STORY-013 DEV: foundry-models CLI implementation

## Description

# DEV-013: DEV-STORY-013 DEV: foundry-models CLI implementation

## Description

Implement the foundry-models CLI exposing exactly the 23 cataloged Models v2 operations per DEV-STORY-013 and DESIGN-013-models-cli.md: live-deployment transform-json; model create/get/promote-version; model-version create/get/list; experiment get/search; experiment-series json/parquet; experiment-artifact-table json/parquet; model-studio create/get/launch; model-studio-config-version create/get/latest/list; model-studio-run list; model-studio-trainer get/list. Use the public nested SDK clients, the shared common components (AccessControlGuard, PaginationHelper, RetryHandler, OutputFormatter, ErrorHandler, LoggingManager, FoundryClientFactory, invocation_scope, BinaryDownloadHandler), and package the metadata-only policy.

## Acceptance Criteria

- [x] Exactly 23 commands exposed with the documented dispatch paths and HTTP routes; no fake discovery, preview, internal, raw, or stream commands.
- [x] JSON flags validated before client creation; invalid JSON or wrong top-level shape exits 1 via the standard error envelope without echoing sensitive content.
- [x] Exactly four cursor-paged commands use PaginationHelper (experiment search, model-version list, model-studio-config-version list, model-studio-run list) with at most 40 pages; offset/page_size on series/artifact JSON are service slicing only; trainer list has no pagination flags.
- [x] Streamed downloads (series parquet, artifact-table json/parquet) use streaming SDK access and BinaryDownloadHandler with atomic persistence, metadata envelope, bounded memory, and response closure on every path.
- [x] AccessControlGuard runs before client and file effects; write set includes transform_json, creates, promote_version, and launch; experiment search remains a semantic read.
- [x] Metadata-only policy packaged and fail-closed: exactly 12 permitted reads, 11 blocked operations.
- [x] include_attribution=False throughout; no attribution env handling; B3 context restored after success and failure.
- [x] Retries follow ADR-004 with cursor-local state; at-least-once duplicate and cost risk documented.
- [x] Output follows shared stdout/stderr/exit-code contracts; logs, errors, and tracebacks never expose credentials, request bodies, model inputs, experiment content, or downloaded bytes.
- [x] Console entry point and Claude skill launcher wired; pyproject updated.

## Related Documentation

- .ept/docs/deliverables/architecture/DESIGN-013-models-cli.md
- .ept/docs/deliverables/architecture/DESIGN-005-common-components.md
- .ept/docs/deliverables/architecture/DESIGN-012-language-models-cli.md

## Notes

Follows the established namespace CLI pattern from DESIGN-010/011/012.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
