---
id: BUG-SUB-014
type: bug_subtask
title: Physical repository split leaves tool and skills repositories empty
status: Closed
created: 2026-08-17
updated: 2026-08-17
priority: High
assignee: python-developer
reporter: python-developer
time_spent_hours: 1.8
---

# BUG-SUB-014: Physical repository split leaves tool and skills repositories empty

## Description

Defect found during TESTEXEC-024 QA rerun.

Steps to reproduce

1. Clone https://github.com/t-jet/pal_found_cli with recursive submodules.
2. At root 5bca5d760, count tracked src, tests, and .agents/skills paths.
3. Inspect tool commit ac9c03f and skills commit dcbdb4e for migrated source, tests, packaging, skills, and CI.
4. Run moved-path git history checks in both split repositories.
5. Create a clean tool virtual environment, install the tool, and run its tests and launcher.
6. Run root tests and the split static checks.

Expected

Tool implementation, tests, packaging, and CI belong to pal_found_cli_tool. Skill folders and their CI belong to pal_found_cli_skills. Root no longer owns those paths. Migration retains usable history, and clean installation plus tests work from the split repositories.

Actual

Root still tracks src=83, tests=44, and .agents/skills=37. pal_found_cli_tool has one commit and only .gitignore; src, tests, pyproject.toml, and CI are absent. pal_found_cli_skills has three commits and only LICENSE plus README; .agents/skills and CI are absent. Moved-path logs are empty. Clean tool installation exits 1 with neither setup.py nor pyproject.toml, leaving no tests or launcher. Root package installation and help still work. Root tests report 1375 passed and 3 stale-date fixture failures; split static checks pass 13/13 but do not cover migration.

Acceptance impact

The repositories are public and clonable, but the physical split acceptance criteria are not met. Canonical repositories do not contain their owned deliverables and cannot be installed or tested independently. Full QA evidence is in TESTEXEC-024 comment 20260817-125816-workflow-mgr.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
