---
id: DEVOPS-004
type: devops
title: 'DEVOPS-005: Deploy foundry-datasets skill'
status: Closed
created: 2026-05-18
updated: 2026-07-26
priority: High
assignee: devops-engineer
reporter: architect
time_spent_hours: 2
---

# DEVOPS-004: DEVOPS-005: Deploy foundry-datasets skill

## Description

Package and deploy foundry-datasets skill to .claude/skills/foundry-datasets/ structure, validate installation and CLI entry point.

## Acceptance Criteria

- [x] foundry-datasets skill package structure present
- [x] console entry point import/install path works
- [x] CLI parser/help smoke passes
- [x] foundry-datasets QA and wrapper tests pass
- [x] package build includes wrapper modules
- [x] deployment evidence recorded
- [x] no unresolved defects

## Related Documentation

- .ept/docs/deliverables/qa/TESTCASE-003-test-cases.md
- .claude/skills/foundry-datasets/scripts/foundry_datasets_cli.py
- tests/test_foundry_datasets_cli.py
- tests/test_datasets_console_wrapper.py
- src/foundry_cli/datasets/scripts/foundry_datasets_cli.py
- pyproject.toml
- README.md

## Notes

Deployment readiness confirmed from restored console wrapper/package entry point, passing foundry-datasets QA and wrapper tests, prior build/twine/package checks, and no unresolved BUG-SUB children under DEV-STORY-005.
