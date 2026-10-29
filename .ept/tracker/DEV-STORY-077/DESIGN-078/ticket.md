---
id: DESIGN-078
type: design
title: DEV-STORY-077 design v1 Ontology schema object Action and Query lifecycle REST contracts
status: Closed
created: 2026-10-07
updated: 2026-10-07
priority: High
assignee: tech-lead
reporter: tech-lead
estimated_hours: 4
time_spent_hours: 0.5
---

# DEV-STORY-077 design

## Owned scope
23 exact operation IDs in .ept/docs/deliverables/development/FEATURE-015-rest-operation-partitions.json; partition hash b8ddbb4c6908ef43e93f756cf69029b52beda5b486f5ec0131b1c5d66ae50a0e.
Resources: v1.ontologies.Action, v1.ontologies.ActionType, v1.ontologies.Attachment, v1.ontologies.ObjectType, v1.ontologies.Ontology, v1.ontologies.OntologyObject, v1.ontologies.Query, v1.ontologies.QueryType.
Core069 owns structural contracts, full models/errors, service indexes and common patterns. This story owns resource behavior under references/rest/<version>/<service>/<Resource>.md (numbered leaves at most300lines) and reader examples/fixtures examples/rest/077/ inside standalone pal-found-dev. Tests own tests/test_offline_rest_077.py.

## Acceptance criteria
Finalize source/file ownership, finite estimates and independent lead review; record technical plan in tracker. No content implementation.
Every operation has locally available signature/HTTP/body/typed inputs/results/nested models/errors/effects/availability/modes and bounded recovery. Every example supplies synthetic or precisely described tenant values, actual SDK call, request/response/error assertions. Use actual asynchronous return signatures, not inferred Awaitable types. Keep source silence explicit with authorized tenant verification; invent no universal scope or idempotency guarantee. Independently reconcile full model/error closure;3242 is not a cap. Owned capability workflow covers exact resources in this partition: identity/access and supported reads/mutations, version-specific availability, finite iteration, transport lifetimes, denied operations and uncertain-write effect reconciliation. Admin071 and072 share a namespace but own disjoint resources and never change central service indexes. Dataset074 separates v1/v2 branches, schemas, files and transaction operations; build075 separates schedule/trigger/build completion, checkpoint and health-report state; v1 Ontology077 stays distinct from v2 schema/object/Action contracts.

## Related documentation
BA-DES-015/SA-DES-014 revision2 and closed owner approvals QUESTION179/182. Indexed FEATURE-015-rest-authoring-contract.md and exact partition JSON. Primary SDK1.101.0 commit168d51910570b6966afa2320333ab36f6a3f7ccf/OpenAPI1.1697.0. Supplement SDK silence with relevant official API references while authoring. Preserve351 CLI operations and other authors, Apache2.0 copyright/license/NOTICE. No installation/copy/internal reader links. Final independent REST acceptance093, GitHub-only integrated publication070.

## Estimate and readiness
4 contributor hours; total72h candidate8points within80h two-week budget with reviewer/QA slots. Firstthree operation/example/constraint fixtures measured before scaling; split exact exclusive IDs if capacity exceeded. No implementation before DESIGNClosed, independent lead reviews and parentDevelopmentDoD. No infrastructure change; no DEVOPS child because070 owns release.
