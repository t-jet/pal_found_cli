---
id: BUG-032
type: bug
title: Concurrent link creation assigns duplicate IDs and makes removal ambiguous
status: Closed
affected_version: tracker-local-20261014
created: 2026-10-14
updated: 2026-10-14
priority: High
resolution: Done
assignee: project-manager
reporter: project-manager
---

# BUG-032: Concurrent link creation assigns duplicate IDs and makes removal ambiguous

## Description

During TASK-006 QA, two concurrent tracker CLI link create commands for BUG-031 returned LINK-01949. CLI link list BUG-031 showed both RelatesTo links with the same ID. index.py get_next_link_id and increment_link_counter load/write the counter separately without a lock; links.py create_link also writes a shared CSV index. Removing LINK-01949 removes both rows, so ID collision makes targeted removal ambiguous. Reproduced on Windows workspace 2026-10-14; source BUG-031 comment by qa-engineer. Expected unique link IDs and no lost rows under concurrent creates. Actual duplicate ID. I repaired the two BUG-031 links sequentially through CLI as LINK-01950 and LINK-01951. Fix allocation/write transaction with cross-process synchronization and add a concurrent-create regression test. Do not alter closed BUG-006, which concerns CI security.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
