---
id: BUG-022
type: bug
title: Orchestration skill misstates paged output and schedule inputs
status: Closed
affected_version: 419b261aff38227cd1ed63ec2362c7c39e9f5076
created: 2026-10-13
updated: 2026-10-14
priority: Medium
resolution: Done
assignee: project-manager
reporter: qa-engineer
---

# BUG-022: Orchestration skill misstates paged output and schedule inputs

## Description

# Reproduction
At skills worktree 419b261 and CLI bfdee738, inspect pal-found-orchestration/references/01-build-job.md and 02-schedule.md for build.jobs, build.search, schedule.runs, schedule.create and schedule.replace. CLI PAGINATED_OPS and _paginate_operation show list stdout plus separate stderr cursor/page metadata; three records promise ListJobsOfBuildResponse, SearchBuildsResponse or ListRunsOfScheduleResponse as CLI result and direct nextPageToken. Schedule create and replace records describe trigger as possibly empty when caller lacks read permission, but the flag supplies a request trigger; this does not explain the input meaning. Several read-only schedule records copy a schedule-management permission precondition.
# Expected
Operation records describe actual CLI result shape and the required trigger input without misleading preconditions.
# Actual
Five records fail semantic guidance; read-only records suggest write permission. Source comparison under WORK-005 approved design 20261013-113614-@qa-engineer. No live tenant used. Severity Medium.
# Scope
FEATURE-012, DEV-STORY-051, TESTEXEC-051, WORK-005. Correct docs, retest source hashes.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
