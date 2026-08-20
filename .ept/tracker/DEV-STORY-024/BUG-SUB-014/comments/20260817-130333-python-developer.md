Subject: Reproduction and application logs
Created: 2026-08-17T13:03:33
Updated: 2026-08-17T13:03:33
---
Reproduced from root HEAD 5bca5d7.

Repository inspection

- Root git ls-tree counts: src=83, tests=44, .agents/skills=37.
- pal_found_cli_tool at ac9c03f contains only .gitignore. It has no pyproject.toml, tests, or CI.
- pal_found_cli_skills at dcbdb4e has no .agents/skills tree or CI.
- Canonical remotes and submodule registration are already correct, so URL alignment is not the cause.

Application log

A clean tool install dry run failed with: Directory ./pal_found_cli_tool is not installable. Neither setup.py nor pyproject.toml found.

The results confirm a content migration defect: root still owns the implementation, tests, and skills, while the published destination repositories lack their required content. The failure is reproducible with the steps in the ticket description and TESTEXEC-024 comment 20260817-125816-workflow-mgr.
