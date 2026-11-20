---
id: TASK-026
type: task
title: Release proxy fix and current tool main to PyPI and Conda
status: Closed
priority: High
assignee: devops-engineer
reporter: devops-engineer
created: 2026-11-19
updated: 2026-11-20
component: release
---

# TASK-026: Release proxy fix and current tool main to PyPI and Conda

## Scope
Publish next available version of pal_found_cli from verified tool main ancestry plus independently accepted BUG-052 proxy fix. Include all changes already on tool main; exclude unaccepted FEATURE-015 branches and dirty parent state. Project Owner explicitly authorized new PyPI and t-jet Conda publication.

## Acceptance criteria
- Source commit descends from current remote tool main and contains reviewed BUG-052 fix; independent QA accepts actual proxy routing, bypass, and direct behavior.
- Candidate passes all eight CI jobs, including Windows/Linux Python 3.11/3.12, security scan, metadata and build gates.
- Tag-derived wheel, sdist and noarch Conda artifacts use one new version and include MIT AND Apache-2.0 license metadata plus both license files. Record artifact SHA-256 values.
- Clean package installs verify version, public commands and proxy regression against a controlled fixture.
- Publish tag through existing Test PyPI, production PyPI and t-jet Conda mechanisms; verify actual registry artifacts and versions, source commit, tag, CI and release run, hashes, smoke outputs and any limits as ticket comments. Conda build alone does not satisfy publication.
- Preserve rollback path and keep credentials out of logs and comments.

## Related documentation
- .ept/docs/document_index.md
- .ept/docs/deliverables/qa/WORK-007-release-pin-plan.md
- pal_found_cli_tool/pyproject.toml
- pal_found_cli_tool/.github/workflows/ci.yml
- pal_found_cli_tool/.github/workflows/publish.yml
- pal_found_cli_tool/conda.recipe/meta.yaml
- BUG-052 proxy report and release acceptance.
