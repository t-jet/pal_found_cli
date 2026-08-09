---
id: DEV-STORY-005
type: dev_story
title: foundry-datasets skill (26 operations)
status: Closed
feature_request: FEATURE-001
epic: EPIC-002
created: 2026-04-13
updated: 2026-07-26
priority: Critical
resolution: Done
assignee: architect
reporter: architect
release_notes: foundry-datasets skill - 26 operations covering dataset CRUD, branch management, schema inspection, file upload/download, transaction management. Depends on DEV-STORY-001 through DEV-STORY-004 completion.
---

# DEV-STORY-005: foundry-datasets skill (26 operations)

## Description

Generate and validate the foundry-datasets Claude Code skill package and Python console wrapper. The delivered parser surface exposes the expected 33 foundry-datasets operations/help paths, with dataset CRUD, branch management, schema inspection, file upload/download, and transaction management covered by tests.

## Acceptance Criteria

- [x] foundry-datasets CLI exposes expected 33 operations/parser surface
- [x] QA test cases and execution closed
- [x] deployment DEVOPS-004 closed
- [x] package/console wrapper validation passed
- [x] no unresolved defects

## Related Documentation

- .ept/docs/deliverables/qa/TESTCASE-003-test-cases.md
- tests/test_foundry_datasets_cli.py
- tests/test_datasets_console_wrapper.py
- .claude/skills/foundry-datasets/scripts/foundry_datasets_cli.py
- src/foundry_cli/datasets/scripts/foundry_datasets_cli.py
- README.md

## Notes

Closure readiness verified: all DEV-STORY-005 child tickets are Closed, QA evidence is recorded, DEVOPS-004 is Closed, package and console wrapper validation passed, and no unresolved defects are listed under the story.
