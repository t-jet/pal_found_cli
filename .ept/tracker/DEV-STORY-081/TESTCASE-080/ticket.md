---
id: TESTCASE-080
type: testcase
title: DEV-STORY-081 testcase v2 Ontology object set scenario and transaction lifecycle REST contracts
status: Open
created: 2026-10-07
updated: 2026-10-07
priority: High
assignee: qa-engineer
reporter: tech-lead
estimated_hours: 6
---

# DEV-STORY-081 testcase

## Owned scope
22 exact operation IDs in .ept/docs/deliverables/development/FEATURE-015-rest-operation-partitions.json; partition hash ff2ddcac52a14d423998aa91fbcd9cd3fb78ce56b1a4c3f736a906c84f245a7e.
Resources: v2.ontologies.LinkedObject, v2.ontologies.OntologyObject, v2.ontologies.OntologyObjectSet, v2.ontologies.OntologyScenario, v2.ontologies.OntologyTransaction.
Core069 owns structural contracts, full models/errors, service indexes and common patterns. This story owns resource behavior under references/rest/<version>/<service>/<Resource>.md (numbered leaves at most300lines) and reader examples/fixtures examples/rest/081/ inside standalone pal-found-dev. Tests own tests/test_offline_rest_081.py.

## Acceptance criteria
Independent QA derives source expectations before authored outputs. Formal TESTCASE stays Open until real runnable implementation exists. Define every-owned-method assertions and isolated v2 Ontology object set scenario and transaction lifecycle success/adverse cases.
Every operation has locally available signature/HTTP/body/typed inputs/results/nested models/errors/effects/availability/modes and bounded recovery. Every example supplies synthetic or precisely described tenant values, actual SDK call, request/response/error assertions. Use actual asynchronous return signatures, not inferred Awaitable types. Keep source silence explicit with authorized tenant verification; invent no universal scope or idempotency guarantee. Independently reconcile full model/error closure;3242 is not a cap. Owned capability workflow covers exact resources in this partition: identity/access and supported reads/mutations, version-specific availability, finite iteration, transport lifetimes, denied operations and uncertain-write effect reconciliation. v2 Ontology079/081/083 share a namespace but own disjoint resources and never change central service indexes. Schema/interface contracts differ from object/set/scenario/transaction and Action/Query/attachment/time-series behavior. Function085 owns platform Function/Query/value-type versions; connectivity089 distinguishes source connection, stream record delivery and asynchronous SQL result lifecycle. Media/widget091 covers actual binary/media identities, supported transformations, development settings and published-release effects; resource copy/move and platform publication remain legitimate capability operations.

## Related documentation
BA-DES-015/SA-DES-014 revision2 and closed owner approvals QUESTION179/182. Indexed FEATURE-015-rest-authoring-contract.md and exact partition JSON. Primary SDK1.101.0 commit168d51910570b6966afa2320333ab36f6a3f7ccf/OpenAPI1.1697.0. Supplement SDK silence with relevant official API references while authoring. Preserve351 CLI operations and other authors, Apache2.0 copyright/license/NOTICE. No installation/copy/internal reader links. Final independent REST acceptance093, GitHub-only integrated publication070.

## Estimate and readiness
6 contributor hours; total72h candidate8points within80h two-week budget with reviewer/QA slots. Firstthree operation/example/constraint fixtures measured before scaling; split exact exclusive IDs if capacity exceeded. No implementation before DESIGNClosed, independent lead reviews and parentDevelopmentDoD. No infrastructure change; no DEVOPS child because070 owns release.
