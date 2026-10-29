---
id: BUG-021
type: bug
title: Functions query attribution rejects plain SDK string
status: Closed
affected_version: bfdee7388ce2a8b2d592f17f1ba1d6f10a0424aa
created: 2026-10-13
updated: 2026-10-13
priority: High
resolution: Done
assignee: project-manager
reporter: qa-engineer
---

# BUG-021: Functions query attribution rejects plain SDK string

## Description

# Reproduction
Tool commit bfdee7388ce2a8b2d592f17f1ba1d6f10a0424aa; local SDK v2 source core/models.py:45 defines Attribution = str. For either `query execute` or `query streaming-execute`, pass `--attribution my-app` with otherwise valid query name and parameters. The operation spec at functions CLI lines 81-140 lists attribution in `json_args`; `_coerce_arg` lines 265-270 runs `json.loads`. Direct `_coerce_arg("my-app", json_arg=True)` raises JSONDecodeError.

Expected: CLI accepts a plain attribution string and passes it as SDK Attribution. Actual: plain string is JSON-decoded and fails before SDK call. A JSON-quoted spelling works, contrary to documented flag meaning.

Found during WORK-005 / TASK-006 independent FEATURE-012 semantic review, Functions `query.execute` and `query.streaming_execute`. Severity High because optional documented input is unusable in normal form. No credentials used.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
