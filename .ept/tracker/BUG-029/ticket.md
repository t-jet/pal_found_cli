---
id: BUG-029
type: bug
title: Checkpoints get-batch guide uses invalid RID string array
status: Closed
affected_version: 419b261aff38227cd1ed63ec2362c7c39e9f5076
created: 2026-10-13
updated: 2026-10-14
priority: Medium
resolution: Done
assignee: qa-engineer
reporter: qa-engineer
---

# BUG-029: Checkpoints get-batch guide uses invalid RID string array

## Description

# Reproduction
WORK-005 / TASK-006 independent FEATURE-012 QA; skills worktree 419b261; CLI tool bfdee738. `pal-found-checkpoints/references/01-record.md` `record.get_batch` says `--records-json` is a JSON array of RID strings and example passes `["ri.checkpoints.main.checkpoint.a"]`. CLI OP_SPECS maps records list to SDK `get_batch(body=...)`. Local SDK `record.py:113` requires `List[GetRecordsBatchRequestElement]`; model at `models.py:630` requires object field `recordRid`. `TypeAdapter(list[GetRecordsBatchRequestElement]).validate_python(["ri.checkpoints.main.checkpoint.a"])` raises ValidationError; `[ {"recordRid":"ri.checkpoints.main.checkpoint.a"} ]` passes.

Expected: offline record and example use the object array accepted by SDK, with omission/result meaning. Actual: documented example is rejected before API call. Severity Medium. No Foundry network request used.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
