---
id: UNITTEST-039
type: unittest
title: 'UNITTEST-039: Unit tests for datasets/ontologies migration (copies removed, tool
  parity 33/67)'
status: Closed
created: 2026-10-01
updated: 2026-10-01
priority: High
assignee: python-developer
reporter: tech-lead
estimated_hours: 6
time_spent_hours: 6
---

# UNITTEST-039: UNITTEST-039: Unit tests for datasets/ontologies migration (copies removed, tool parity 33/67)

## Description

Unit tests for DEV-039.

Cover: (1) datasets/ontologies skill folders have no scripts/ dir and no pal_found_datasets_cli.py / pal_found_ontologies_cli.py; (2) SKILL.md invokes pal-found-datasets/pal-found-ontologies; (3) tool pal-found-datasets exposes 33 ops and pal-found-ontologies 67 ops (parity preserved); (4) all 18 pal-found-* entry points remain callable. On pal_found_cli_skills tests/ per repo harness.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
