---
id: DEV-065
type: development
title: Implement independent REST acceptance harness
status: In Progress
created: 2026-10-06
updated: 2026-10-06
priority: High
assignee: python-developer
reporter: qa-engineer
estimated_hours: 18
---

# Implement independent REST acceptance harness

## Scope and acceptance

Own only pal_found_cli_skills/tests/test_offline_rest_acceptance.py and tests/fixtures/offline/rest-acceptance/**. Reconcile exact425 operation IDs/113resources/20namespaces from frozen SDK1.101.0 docs, source and runtime; do not import the production inventory extractor. Independently validate signatures, serialization, aliases, requiredness, defaults, nullable fields, constraints, discriminators/unions, errors, stage, response types and lifetimes, sync/async/raw/stream modes. Reconcile the full transitive model/error closure including compound and indirect forward references;3242 is an initial inventory, never a cap. Aggregate independent exhaustive domain review records and reject unresolved fidelity gaps. Every runnable operation example needs SDK-backed request/response/error assertions. Provide isolated fixture runner denying DNS/socket/HTTP dispatch with failed public-request probe; stage required assets inside the isolated owning skill. Agent reader receives only distributed skill and declared prepared tools/fixtures; source-oracle checks run separately and cannot fill undocumented reader facts. Support J11-J14 and20 independently prepared cases; no distributed content edits. Exclusive fixture ownership: DEV writes only runner.py and transport_data/**; QA owns prompts.json and expected.json, frozen before DEV reads them. DEV must not modify QA expectations. Shared folder globs above identify scope, not permission to overwrite another owner.

## Related documentation

BA-DES-015 revision 2; SA-DES-014 content-architecture, rest-and-sources, sdk-baseline and verification-and-delivery; approved QUESTION-182 and QUESTION-179; FEATURE-015 Waiting for Implementation; EPIC-015.

## Estimate and readiness

18 contributor hours. Grooming only; do not implement until DESIGN closure, all lead reviews and parent Development DoD. No implementation is claimed by this plan.
