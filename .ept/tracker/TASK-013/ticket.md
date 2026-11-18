---
id: TASK-013
type: task
title: Manage completion of open BUG and BUG-SUB tasks
status: In Progress
priority: High
assignee: project-manager
reporter: project-manager
created: 2026-10-25
updated: 2026-11-17
---

# TASK-013: Manage completion of open BUG and BUG-SUB tasks

## Scope
Manage the original four-ticket batch: BUG-035, BUG-SUB-025, BUG-SUB-027 and BUG-SUB-028. Preserve independent QA and original failure history.

## Acceptance criteria
- Each scoped bug is Closed through its actual role and workflow, or has an explicit evidenced blocker and responsible next action.
- Closure evidence identifies the reviewed source revision and independent QA; published drafts do not stand in for final main publication.
- BUG-035 remains pending until the final accepted skills main revision and parent pin satisfy its QA criteria.
- Verify statuses and blocking links through the tracker CLI and record progress in comments.

## Related documentation
.ept/docs/document_index.md; FEATURE-015 canonical draft release status; BA-DES-015 and SA-DES-014; DEV-STORY-070 and DEVOPS-047.

## Ownership
Project Manager coordinates; responsible developer, reviewer and QA roles execute their stages. Scope changes require an explicit ticket reference; BUG-050 is tracked separately under FEATURE-015.
