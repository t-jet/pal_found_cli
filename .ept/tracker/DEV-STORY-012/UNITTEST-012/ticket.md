---
id: UNITTEST-012
type: unittest
title: Add Foundry Language Models CLI unit and integration tests
status: Closed
created: 2026-08-09
updated: 2026-08-09
priority: High
assignee: python-developer
reporter: python-developer
estimated_hours: 8
time_spent_hours: 8
---

# UNITTEST-012: Add Foundry Language Models CLI unit and integration tests

## Description

Add unit and installed-package coverage for the full Language Models contract.

## Acceptance Criteria

- Cover the exact catalog, parser, JSON shapes, scalar validation, nested SDK routes, signatures, and response serialization.
- Use actual SDK clients and error classes for routing, retry, and ADR exit behavior.
- Cover ENABLED denial, write-verb read-only defaults and overrides, metadata-only, Tier 3, and guard-before-client ordering.
- Cover attribution and B3 restoration on success, retry, timeout, failure, and cancellation.
- Cover privacy, output, import, console, launcher, wheel/editable installs, and policy lookup outside the repository.
- Maintain at least 80% branch coverage and pass supported-version quality gates.

## Related Documentation

- DEV-STORY-012
- DESIGN-012

## Notes

Blocked on approved design.
