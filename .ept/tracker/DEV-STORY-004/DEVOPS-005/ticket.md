---
id: DEVOPS-005
type: devops
title: Verify packaging and CI readiness for common components
status: Closed
created: 2026-07-27
updated: 2026-07-28
priority: High
assignee: devops-engineer
reporter: manager
estimated_hours: 2
---

# DEVOPS-005: Verify packaging and CI readiness for common components

## Description

Verify package artifacts, CI filesystem coverage, dependency scanning, and release readiness for the new common components.

## Acceptance Criteria

- [ ] Inspect the built wheel and source distribution contents and confirm that all new common-component modules and required package data are included.
- [ ] CI runs filesystem behavior tests on both Ubuntu and Windows, including path containment, atomic persistence and cleanup, alias locking, and platform-specific file handling.
- [ ] Dependency scanning is enforced as a required failing gate. The scan must not use ignore-success, continue-on-error, or any equivalent setting that masks findings or command failures.
- [ ] Ruff, mypy, pytest with at least 80% coverage, Bandit, package build, and Twine artifact checks all pass.
- [ ] Existing package installation and default runtime behavior remain compatible.
- [ ] Evidence records commands, tool versions, Ubuntu and Windows runner results, dependency-scan output, artifact inclusion inspection, coverage result, and build/Twine output.

## Related Documentation

- .ept/docs/deliverables/architecture/DESIGN-005-common-components.md

## Notes

Attach readiness evidence to the tracker before deployment work is considered complete.
