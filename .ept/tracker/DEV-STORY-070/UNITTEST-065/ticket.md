---
id: UNITTEST-065
type: unittest
title: Verify topic integration checks detect actual omissions
status: In Progress
created: 2026-10-06
updated: 2026-10-06
priority: High
assignee: python-developer
reporter: qa-engineer
estimated_hours: 6
---

# Verify topic integration checks detect actual omissions

## Scope and acceptance

Own only pal_found_cli_skills/tests/test_offline_topic_acceptance_guards.py. Seed missing topic/component/access boundary, broken local file/anchor/asset, path escape, leaf>300lines, required-public-reading-only instruction, changed351CLI record, missing20skill audit and stale093REST evidenceSHA. Assert meaningful specific failures; optional provenance remains allowed and approved existing CLI prerequisites stay governed by owning requirements. Use parent.ept/tmp basetemp.

## Related documentation

BA-DES-015 revision 2; SA-DES-014 content-architecture, rest-and-sources, sdk-baseline and verification-and-delivery; approved QUESTION-182 and QUESTION-179; FEATURE-015 Waiting for Implementation; EPIC-015.

## Estimate and readiness

6 contributor hours. Grooming only; do not implement until DESIGN closure, all lead reviews and parent Development DoD. No implementation is claimed by this plan.
