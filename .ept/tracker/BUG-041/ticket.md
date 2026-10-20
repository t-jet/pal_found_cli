---
id: BUG-041
type: bug
title: Checkpoints and Orchestration CLI omit required preview query on seven endpoints
status: In Progress
affected_version: 0963e6e006f82ad1997be0e22c6b750ed0bbce3b
created: 2026-10-20
updated: 2026-10-20
priority: High
assignee: python-developer
reporter: project-manager
component: shared-cli
---

# BUG-041: Checkpoints and Orchestration CLI omit required preview query on seven endpoints

## Description

## Observed defect
Pinned tool0963e6e006f82ad1997be0e22c6b750ed0bbce3b with Foundry Platform SDK1.101.0 cannot expose or forward required preview=true for seven documented operations: Checkpoints record.get/get_batch/search; Orchestration job.get/get_batch and schedule_version.get/schedule.

## Reproduce
Inspect OP_SPECS, build_parser and adapter kwargs in src/pal_found_cli/checkpoints/scripts/pal_found_checkpoints_cli.py and src/pal_found_cli/orchestration/scripts/pal_found_orchestration_cli.py. No preview option/forwarding exists for those operations. Independent QA captured synthetic SDK RequestInfo for documented examples and observed preview=None. Compare official endpoint references below, which require preview=true. No live enrollment called; server rejection is inferred from API contract rather than claimed as observed.

## Expected versus actual
Expected supported CLI calls can send documented required preview=true (with explicit preview prerequisite); explicit false behavior is validated consistently with endpoint requirement. Actual current commands cannot express required query. Parser and synthetic examples passing do not establish server acceptance.

## Acceptance criteria
- Correct all seven endpoint adapters with an approved preview input policy; do not silently mutate unrelated operations.
- Independent actual SDK HTTP wire tests assert preview=true query for every operation, including paginated Checkpoints search requests.
- Define and test omission/explicit-false/invalid-input behavior; no tenant access required for request construction proof.
- Code review and QA record exact corrected tool revision; update and retest affected five skill pages and preserve operation inventory.
- Do not infer live authorization or server mutation outcomes from fixtures.

## Existing coverage and ownership
BUG-034 covers six Data Health endpoints only, not these seven; TESTCASE/TESTEXEC085 likewise limited to Data Health. New defect relates to BUG-034 for shared policy consistency, not duplicate endpoint scope. Closed REST BUG-SUB-032 concerns a separate fixture domain. FEATURE-012 owns existing CLI correctness; affected FEATURE-015 DEV-STORY-070 BD-015-09/11/12 acceptance is blocked until corrected and independently retested. Documentation limitation disclosure does not waive API contract.

## Independent evidence
.ept/tmp/feature015_core_schedule_final_review.json and feature015_core_schedule_probe.json; reviewer /root/core_and_schedule_final_qa. Review reports138 pinned tool tests and23 documented examples passing, but explicitly separates preview deficiency. Current five affected pages now disclose gap; no tool fix claimed.

## Official source references
- https://www.palantir.com/docs/foundry/api/checkpoints-v2-resources/records/get-records-batch
- https://www.palantir.com/docs/foundry/api/checkpoints-v2-resources/records/get-record
- https://www.palantir.com/docs/foundry/api/checkpoints-v2-resources/records/search-records
- https://www.palantir.com/docs/foundry/api/orchestration-v2-resources/jobs/get-job
- https://www.palantir.com/docs/foundry/api/orchestration-v2-resources/jobs/get-jobs-batch
- https://www.palantir.com/docs/foundry/api/orchestration-v2-resources/schedule-versions/get-schedule-version
- https://www.palantir.com/docs/foundry/api/orchestration-v2-resources/schedule-versions/get-schedule-of-schedule-version
- https://www.palantir.com/docs/foundry/api/orchestration-v2-resources/schedules/pause-schedule
- https://www.palantir.com/docs/foundry/api/orchestration-v2-resources/builds/get-builds-batch


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
