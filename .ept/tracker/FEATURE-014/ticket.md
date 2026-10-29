---
id: FEATURE-014
type: feature
title: Distribute pal_found_cli_skills as installable PyPI and Conda packages
status: Canceled
created: 2026-10-05
updated: 2026-10-06
priority: High
assignee: ba
reporter: project-manager
component: skills
---

# Distribute pal_found_cli_skills as installable PyPI and Conda packages

## Business need
Users need to install the pal_found_cli_skills repository as a versioned bundle from PyPI or the t-jet Conda channel alongside the CLI package. This adds a distribution option for the existing skill repository.

## Proposed acceptance criteria for BA/SA refinement
- Define a package layout that installs all skill entry points and local references intact and a documented discovery/install path for supported harnesses.
- Publish matching versions to PyPI and Conda from one reviewed source revision, with correct metadata and license.
- Verify clean installs from each channel and offline navigation of installed skill content; document upgrade and removal behavior.
- Keep existing git-clone/copy distribution working until a migration is explicitly approved.

## Scope
Run BA and SA analysis, then design and developer stories before implementation or publication. Related work: FEATURE-007 and FEATURE-013.
