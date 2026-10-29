---
id: UNITTEST-064
type: unittest
title: Prove REST acceptance rejects incomplete or unsafe coverage
status: In Progress
created: 2026-10-06
updated: 2026-10-06
priority: High
assignee: python-developer
reporter: qa-engineer
estimated_hours: 10
---

# Prove REST acceptance rejects incomplete or unsafe coverage

## Scope and acceptance

Own only pal_found_cli_skills/tests/test_offline_rest_acceptance_guards.py. Seed missing/duplicate operation owner, wrong signature/alias/requiredness/default/constraint/discriminator/error/stage/mode, missing indirect or compound forward reference, unresolved model destination and wrong source revision. Assert each corresponding gate fails. Test external-network probe, repeated/empty cursor, stream closure, timeout after write and exhausted status budget. Tests use parent.ept/tmp basetemp and independent expected values, not the production generator as its own oracle.

## Related documentation

BA-DES-015 revision 2; SA-DES-014 content-architecture, rest-and-sources, sdk-baseline and verification-and-delivery; approved QUESTION-182 and QUESTION-179; FEATURE-015 Waiting for Implementation; EPIC-015.

## Estimate and readiness

10 contributor hours. Grooming only; do not implement until DESIGN closure, all lead reviews and parent Development DoD. No implementation is claimed by this plan.
