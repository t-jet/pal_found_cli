---
id: BUG-024
type: bug
title: AIP Agents offline skill misstates selectors and CLI results
status: Closed
affected_version: 419b261aff38227cd1ed63ec2362c7c39e9f5076
created: 2026-10-13
updated: 2026-10-13
priority: Medium
resolution: Done
assignee: project-manager
reporter: qa-engineer
---

# BUG-024: AIP Agents offline skill misstates selectors and CLI results

## Description

# Scope and evidence
WORK-005 / TASK-006 source-backed review, FEATURE-012 AIP Agents skill, current skills worktree at 419b261; CLI tool bfdee738.

- `agent.get` and `agent_version.get` records say a local session alias must resolve. Parser takes agent RID (plus version) and CLI only loads alias for `_ALIAS_BOUND`; no alias input for either operation.
- `agent.all_sessions` says agent RID is a precondition and result contains agent entries. Parser takes no RID; SDK returns sessions iterator.
- `agent.all_sessions`, `agent_version.list`, `session.list` name page response models as CLI result. CLI `_paginate_operation` collects `data` and prints item list; pagination metadata is separate.
- `session.create` says CLI returns SDK Session. CLI `_create_session` returns local SessionState dict with alias and no session_token; `session_manager.py:79-93` defines its fields.

Expected: offline agent sees actual selectors and printed result shape, especially aliases and page lists. Actual: records misstate prerequisites or result identity. Reproduce by comparing named records under `.agents/skills/pal-found-aip-agents/references/` with parser/dispatch at CLI lines 101-270, 356-501, 501-535, 650-690 and SDK AIP client method return types. Severity Medium; no live credentials needed.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
