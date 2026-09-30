---
id: BUG-SUB-018
type: bug_subtask
title: 'BUG-SUB: Install documentation (README/PyPI long description) lacks auth and .env
  setup guidance'
status: Closed
created: 2026-09-30
updated: 2026-09-30
priority: Medium
assignee: qa-engineer
reporter: qa-engineer
---

# BUG-SUB-018: BUG-SUB: Install documentation (README/PyPI long description) lacks auth and .env setup guidance

## Description

The install documentation for pal_found_cli (README.md, which is also the PyPI long description) does not include any authentication or .env configuration guidance.

Steps to reproduce:
1) Read pal_found_cli_tool/README.md (PyPI long description source).
2) Search for FOUNDRY_TOKEN, .env, authentication, or auth.
3) Compare with the shipped .env.example which documents FOUNDRY_TOKEN and FOUNDRY_HOSTNAME.

Expected behavior: The install documentation (TESTCASE-029 case 2) should include a short .env / FOUNDRY_TOKEN authentication setup step so a user who installs the package can configure credentials, per the story scope (install, auth/.env guidance).

Actual behavior: README.md contains only install, upgrade, command, conda, and repository-link sections. There is no .env, FOUNDRY_TOKEN, or authentication guidance anywhere in the install docs / PyPI long description. The .env.example exists in the repo but is not referenced by the README.

Severity: Medium. Without auth guidance in the documented install path, a new user cannot configure the CLI to authenticate to Foundry after following the docs.

Affected version: pal_found_cli 0.1.2 (README as published on the PyPI page).

Found during: TESTEXEC-029 (DEV-STORY-029).

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
