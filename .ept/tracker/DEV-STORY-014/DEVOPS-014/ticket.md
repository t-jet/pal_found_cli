---
id: DEVOPS-014
type: devops
title: 'DEVOPS-014: packaging and deployment for foundry-orchestration CLI'
status: Closed
created: 2026-08-09
updated: 2026-08-10
priority: High
assignee: devops-engineer
reporter: architect
estimated_hours: 3
time_spent_hours: 1.0
---

# DEVOPS-014: DEVOPS-014: packaging and deployment for foundry-orchestration CLI

## Description

...# DEVOPS-014: packaging and deployment for foundry-orchestration CLI

## Description

Package and deploy the foundry-orchestration CLI (DEV-014) following the DEVOPS-010/011/012/013 convention: clean-archive build, wheel/editable installation, console entry-point smoke test, security gates, Python 3.11/3.12 checks, and rehearsed rollback. Deliverable: deployment report under .ept/docs/deliverables/devops/.

## Acceptance Criteria

- [ ] Clean-archive build passes (sdist + wheel per PEP 517).
- [ ] Wheel and editable installation verified; console entry point `foundry-orchestration` smoke-tested (help output).
- [ ] Package data includes the foundry-orchestration skill launcher.
- [ ] Python 3.11 and 3.12 gates green.
- [ ] Security gates (bandit + safety) green.
- [ ] Deployment report documented under .ept/docs/deliverables/devops/ (mirrors DEVOPS-013 deployment report).
- [ ] Rehearsed rollback steps verified.

## Related Documentation

- .ept/docs/deliverables/architecture/DESIGN-014-orchestration-cli.md
- .ept/docs/deliverables/devops/DEVOPS-013-deployment-report.md (sibling reference)
- pyproject.toml

## Notes

Deployment to production follows after QA closes; this sub-task prepares and rehearses the release.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
