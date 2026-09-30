---
id: BUG-SUB-017
type: bug_subtask
title: 'BUG-SUB: PyPI project metadata missing project URLs (repository/homepage/docs), license,
  and classifiers'
status: Closed
created: 2026-09-30
updated: 2026-09-30
priority: High
assignee: qa-engineer
reporter: qa-engineer
---

# BUG-SUB-017: BUG-SUB: PyPI project metadata missing project URLs (repository/homepage/docs), license, and classifiers

## Description

PyPI package pal_found_cli 0.1.2 page metadata is missing repository/homepage/documentation links, a license, and classifiers.

Steps to reproduce:
1) Anonymous GET https://pypi.org/pypi/pal_found_cli/json (probe029-meta.out).
2) Inspect info.project_urls, info.license, info.classifiers.
3) Inspect pal_found_cli_tool/pyproject.toml for [project.urls], license, classifiers.

Expected behavior: The published metadata (and the PyPI project page, TESTCASE-029 case 1/4) should expose repository/homepage/docs URLs, a license (e.g. Apache-2.0 or per repo LICENSE), and classifiers (e.g. Programming Language :: Python :: 3.11/3.12), consistent with the DESIGN deliverables for the package page.

Actual behavior: info.project_urls = null, info.license = null, info.classifiers = []; pyproject.toml declares no [project.urls], no license field, and no classifiers. The PyPI project page therefore cannot render Repository/Homepage/Documentation links or a license/classifier section.

Severity: Medium. The package must be republished with corrected metadata (add [project.urls], license, classifiers to pyproject.toml) so the public project page exposes the repository and license as required by TESTCASE-029.

Affected version: pal_found_cli 0.1.2 (published 2026-09-30, CI run 36681617309).

Found during: TESTEXEC-029 (DEV-STORY-029).

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
