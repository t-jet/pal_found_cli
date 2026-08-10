---
id: QUESTION-035
type: question
title: 'ACL write classification gap: launch/promote_version/pause/unpause inherit read behavior'
status: Canceled
addressed_to: tech-lead
created: 2026-08-09
updated: 2026-08-09
priority: High
reporter: python-developer
---

# QUESTION-035: ACL write classification gap: launch/promote_version/pause/unpause inherit read behavior

## Description

# QUESTION: ACL write classification gap blocks DEV-013/DEV-014 read-only enforcement

## Context
DESIGN-013 (DEV-013) and DESIGN-014 (DEV-014) require the shared `AccessControlGuard` write classification to be corrected so the following operations are classified as writes and blocked under read-only mode:
- `models.model_studio.launch`
- `models.model.promote_version`
- `orchestration.schedule.pause`
- `orchestration.schedule.unpause`

## Problem
`AccessControlGuard._WRITE_VERBS` (src/foundry_cli/common/access_control_guard.py) does NOT include the verbs `launch`, `promote`, `pause`, or `unpause`. The heuristic matches only when the operation name equals a write verb or starts with `<verb>_`. Therefore:
- `launch` → starts with no write verb → classified READ
- `promote_version` → starts with no write verb → classified READ
- `pause` → classified READ
- `unpause` → classified READ

Under global/namespace READONLY these operations would NOT be blocked (exit 8), violating DESIGN-013 "The shared AccessControlGuard write classification must be corrected so launch and promote_version cannot inherit read behavior" and DESIGN-014's 8-operation write set. QA cases MDL-TC-015/016 and ORC-TC-* depend on this.

## Requested decision
Add `launch`, `promote`, `pause`, `unpause` to `_WRITE_VERBS`. This is a shared-infrastructure change so it needs tech-lead approval. Note `launch` and `pause`/`unpause` also appear in other namespaces (e.g. filesystem? aip-agents has no launch) - adding them is low-risk since these are all mutating/cost-bearing operations. `promote` similarly. Verify no existing operation that is genuinely a read would become misclassified.

## Deliverable
Approve/deny adding these four verbs to `_WRITE_VERBS` (or an alternative mechanism, e.g. namespace-specific write-set lists) and specify the required tests.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
