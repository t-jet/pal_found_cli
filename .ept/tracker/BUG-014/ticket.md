---
id: BUG-014
type: bug
title: Dataset and Filesystem skill records misstate inputs and results
status: Closed
affected_version: pal_found_cli_skills-worktree
created: 2026-10-12
updated: 2026-10-13
priority: Medium
resolution: Done
assignee: project-manager
reporter: project-manager
component: skills
---

# BUG-014: Dataset and Filesystem skill records misstate inputs and results

## Description

# Defect
Independent source review of FEATURE-012 found Dataset and Filesystem record errors. Dataset branch.create permits an uncommitted transaction in prose though SDK raises TransactionNotCommitted. dataset.jobs omits order/branch/paging flags. view.create example omits required stopPropagatingMarkingIds. Six Dataset and five Filesystem paginated records name raw SDK page models as CLI results; CLI emits collected items with token metadata on stderr. folder.children gives wrong CLI default page size. resource.get_by_path_batch says compare requested RIDs instead of paths. Three Filesystem reference intros contain stray parser. text.

## Acceptance criteria
- Correct each cited input, effect, result and example against CLI parser and local SDK signatures/models.
- Keep BUG-012 runtime pagination loss tracked separately; docs must not imply it is fixed.
- Run offline skill gate and relevant parser/validation tests.
- Independent QA source-checks corrected rows and copied bundle, recording pass/fail counts.

Related: FEATURE-012 DEV-STORY-044/045, WORK-005, BUG-012.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
