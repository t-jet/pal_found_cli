---
id: BUG-010
type: bug
title: Admin list skill records name raw page models as SDK results
status: Closed
affected_version: pal_found_cli_skills-worktree
created: 2026-10-12
updated: 2026-10-12
priority: Medium
resolution: Done
assignee: python-developer
reporter: project-manager
component: skills
---

# BUG-010: Admin list skill records name raw page models as SDK results

## Description

# Defect
Nine pal-found-admin list records say the SDK returns a List*Response page model. Public SDK methods return ResourceIterator[T] (async methods return AsyncResourceIterator[T]); Admin CLI consumes the iterator and prints a JSON item array with pagination metadata separately. The records misstate what an offline agent should expect.

## Scope
Correct group.list, group_member.list, group_membership.list, host.list, marking.list, marking_category.list, marking_member.list, marking_role_assignment.list, and user.list. Search operations return their stated response models and are outside this defect.

## Acceptance criteria
- Each list record accurately distinguishes public SDK iterator from CLI JSON result and token metadata.
- Empty page guidance keeps continuation-token behavior accurate.
- Review all nine source signatures and CLI pagination path; run offline skill gate and focused Admin tests.
- Independent QA verifies copied-bundle wording before closure.

Related: FEATURE-012, DEV-STORY-042/043 (Closed), WORK-005.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
