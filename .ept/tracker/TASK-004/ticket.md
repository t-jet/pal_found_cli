---
id: TASK-004
type: task
title: Publish pal_found_cli_tool v0.1.4 to PyPI and t-jet Conda
status: Blocked
priority: High
assignee: devops-engineer
reporter: project-manager
created: 2026-10-05
updated: 2026-10-06
component: distribution
---

# Publish pal_found_cli_tool v0.1.4 to PyPI and t-jet Conda

## Scope
Publish the current approved pal_found_cli_tool source as v0.1.4 using the existing PyPI and t-jet Conda release workflow. FEATURE-012 retains its actual workflow status.

## Acceptance criteria
- BUG-SUB-019 is repaired and independently verified before selecting the release source.
- Record immutable source commit, tag, package version, artifact names, and PyPI/Conda version alignment.
- Run full tests and artifact metadata/content checks, then verify a clean install from staging/TestPyPI.
- Publish to production PyPI and t-jet Conda through the established pipeline, then verify clean installs and CLI smoke tests from each channel.
- Record public package URLs, workflow run IDs, artifact hashes, verification commands, and outcomes in ticket comments.
