---
id: TASK-014
type: task
title: Prepare FEATURE-015 parent draft checkpoint
status: Closed
priority: High
assignee: devops-engineer
reporter: devops-engineer
created: 2026-10-29
updated: 2026-11-17
---

## Scope

Merge fresh origin/main into isolated parent draft branch. Preserve draft commits. Advance paired tool and skills gitlinks only after ancestry checks. Update canonical QA status and document index with exact pinned CI evidence. Prepare reviewable commit for PR 1. Do not publish release, move DEVOPS-047, or push before paired final heads arrive.

## Acceptance criteria

- [x] Draft branch contains latest origin/main and preserves prior commits.
- [x] Paired gitlinks checked for ancestry and pinned to approved CI-green heads.
- [x] Canonical QA status, index, and machine CI proof agree with pinned heads.
- [x] Reviewable commit prepared; PR 1 updated only after paired heads confirmed.
- [x] Ticket comments record evidence and any remaining publication blockers.

## Related documentation

- `.ept/docs/document_index.md`
- `.ept/docs/deliverables/architecture/SA-DES-014-offline-development-knowledge/verification-and-delivery.md`
- `.ept/docs/deliverables/qa/FEATURE-015-draft-release-status-2026-10-18.md` at combined parent draft `6245e6264cc8e1f041e21c31b3e1ab6694c2b66f`.

## Published checkpoint

Parent PR 1 is open and draft at `734012c71594454c8ad24745587a2fe323f2420e`. Combined PR 6 is open and draft at `6245e6264cc8e1f041e21c31b3e1ab6694c2b66f`; it publishes the reconciled canonical status and index. Both pin approved skills `77b101fb7c5e51fa5f785b2147d97cdfff703133` and tool main `1e2e61bc0a56afe9af75e77170358d93ff6cf9d1`.

FEATURE-015 acceptance remains open: 219 formal operation reviews and 40 page/overall checks are pending. DEVOPS-047 remains Open. Retain evidence and active worktrees while review remains open.
