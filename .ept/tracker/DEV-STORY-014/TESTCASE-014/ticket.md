---
id: TESTCASE-014
type: testcase
title: 'TESTCASE-014: QA test cases for foundry-orchestration CLI'
status: Closed
created: 2026-08-09
updated: 2026-08-10
priority: High
assignee: qa-engineer
reporter: architect
estimated_hours: 8
time_spent_hours: 8
---

# TESTCASE-014: TESTCASE-014: QA test cases for foundry-orchestration CLI

## Description

# TESTCASE-014: QA test cases for foundry-orchestration CLI

## Description

Design QA test cases for the foundry-orchestration CLI (DEV-014) covering the 20-operation catalog, parser and dispatch, nested SDK routing, JSON argument validation, access control precedence, metadata-only tier, pagination, retry, error serialization, output formats, tracing, packaging, and the console entry point. Deliverable: .ept/docs/deliverables/qa/TESTCASE-014-test-cases.md (mirrors TESTCASE-013 conventions). Runs in parallel with development.

## Acceptance Criteria

- [ ] Test case design document created at .ept/docs/deliverables/qa/TESTCASE-014-test-cases.md.
- [ ] Coverage of all 20 operations: build (6), job (2), schedule (10), schedule_version (2), schedule_run (0).
- [ ] ACL precedence cases: global → namespace → operation controls; readonly blocking the 8 mutating operations (exit code 8, denying rule on stderr).
- [ ] Metadata-only tier cases: 12 PERMITTED / 8 BLOCKED exact match.
- [ ] Pagination cases: build.jobs, build.search, schedule.runs (page_size, page_token, --all, --max-pages, exact-page); get_batch single-call.
- [ ] JSON validation cases for schedule.create, schedule.replace, build.create (invalid input rejected pre-client).
- [ ] Retry and error-serialization cases per ADR-001/002; output-format cases per ADR-004; NDJSON stderr logging per ADR-005.
- [ ] Tracing cases: include_attribution=False; B3 propagation.
- [ ] Packaging cases: console entry point, skill launcher, help output.
- [ ] Smoke/environment labels consistent with sibling TESTCASE docs.

## Related Documentation

- .ept/docs/deliverables/architecture/DESIGN-014-orchestration-cli.md
- DEV-STORY-014 comment 20260809-200456-architect
- .ept/docs/deliverables/qa/TESTCASE-013-test-cases.md (sibling reference)

## Notes

Runs in parallel with development; execution in TESTEXEC-014 after DEV-014 closes.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
