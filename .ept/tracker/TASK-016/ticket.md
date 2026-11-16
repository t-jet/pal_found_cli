---
id: TASK-016
type: task
title: Refresh parent agent configuration and contributor notes for PR 7
status: Closed
priority: High
assignee: hr
reporter: hr
created: 2026-10-29
updated: 2026-10-29
---

## Scope
Refresh isolated feature015/parent-agent-config branch for PR 7 with current origin/main and existing live contributor note changes. Preserve prior branch commits and source text. Regenerate agent definitions from existing canonical sources.

## Acceptance Criteria
- Branch contains latest origin/main and prior PR 7 commits.
- Existing live contributor notes retained with verified byte continuity; no new policy introduced.
- Composer --all and --all --check pass; generated definitions match canonical sources.
- Exact file commit independently reviewed before push; remote branch verified after publication.
- Live parent files remain untouched.

## Deliverables
Updated existing contributor notes and generated agent definitions in PR 7; evidence in ticket comments.
