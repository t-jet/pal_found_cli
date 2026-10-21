---
id: BUG-020
type: bug
title: Models skill misstates paged output and includes invalid training example
status: Closed
affected_version: 419b261aff38227cd1ed63ec2362c7c39e9f5076
created: 2026-10-13
updated: 2026-10-14
priority: Medium
resolution: Done
assignee: project-manager
reporter: qa-engineer
---

# BUG-020: Models skill misstates paged output and includes invalid training example

## Description

# Reproduction
At skills worktree 419b261 and CLI bfdee738, open pal-found-models/references/model-version.md, experiment.md, model-studio-config-version.md, model-studio-run.md, model-studio-trainer.md. Run parser help for the four paged commands and compare CLI _paginate_operation lines 530-565 with each record. Paged stdout is a list, cursor and page count are stderr metadata, yet records promise SDK List*/Search*Response with nextPageToken. Also model-studio-config-version create example passes resources {gpu:V100}; SDK ResourceConfiguration requires memory and cpu. Trainer list names a required trainer ID even though parser and SDK list take none; trainer get discusses empty list; experiment-series json warns about Parquet transfer.
# Expected
Records describe exact CLI output and complete valid examples and operation-specific preconditions.
# Actual
At least these records mislead offline agents. No live credentials or tenant needed; source comparison under WORK-005 design 20261013-113614-@qa-engineer. Severity Medium.
# Scope
FEATURE-012, DEV-STORY-050, TESTEXEC-050, WORK-005. Correct docs and independently retest before closure.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
