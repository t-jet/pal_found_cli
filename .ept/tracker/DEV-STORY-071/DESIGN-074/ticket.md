---
id: DESIGN-074
type: design
title: DEV-STORY-071 design identity and membership lifecycle REST contracts
status: In Progress
created: 2026-10-07
updated: 2026-10-07
priority: High
assignee: tech-lead
reporter: tech-lead
estimated_hours: 4
time_spent_hours: 0.5
---

# DEV-STORY-071 design

## Owned scope
27 exact operation IDs in .ept/docs/deliverables/development/FEATURE-015-rest-operation-partitions.json; partition hash 7f314edf2faf396d384980dcb18a2941547d48aa1dd6ec6c39a79fb68f8f6d22.
Resources: v2.admin.Group, v2.admin.GroupMember, v2.admin.GroupMembership, v2.admin.GroupMembershipExpirationPolicy, v2.admin.GroupProviderInfo, v2.admin.User, v2.admin.UserProviderInfo.
Core069 owns structural contracts, full models/errors, service indexes and common patterns. This story owns resource behavior under references/rest/<version>/<service>/<Resource>.md (numbered leaves at most300lines) and reader examples/fixtures examples/rest/071/ inside standalone pal-found-dev. Tests own tests/test_offline_rest_071.py.

## Acceptance criteria
Finalize source/file ownership, finite estimates and independent lead review; record technical plan in tracker. No content implementation.
Every operation has locally available signature/HTTP/body/typed inputs/results/nested models/errors/effects/availability/modes and bounded recovery. Every example supplies synthetic or precisely described tenant values, actual SDK call, request/response/error assertions. Use actual asynchronous return signatures, not inferred Awaitable types. Keep source silence explicit with authorized tenant verification; invent no universal scope or idempotency guarantee. Independently reconcile full model/error closure;3242 is not a cap. Owned capability workflow covers exact resources in this partition: identity/access and supported reads/mutations, version-specific availability, finite iteration, transport lifetimes, denied operations and uncertain-write effect reconciliation. Admin071 and072 share a namespace but own disjoint resources and never change central service indexes. Dataset074 separates v1/v2 branches, schemas, files and transaction operations; build075 separates schedule/trigger/build completion, checkpoint and health-report state; v1 Ontology077 stays distinct from v2 schema/object/Action contracts.

## Related documentation
BA-DES-015/SA-DES-014 revision2 and closed owner approvals QUESTION179/182. Indexed FEATURE-015-rest-authoring-contract.md and exact partition JSON. Primary SDK1.101.0 commit168d51910570b6966afa2320333ab36f6a3f7ccf/OpenAPI1.1697.0. Supplement SDK silence with relevant official API references while authoring. Preserve351 CLI operations and other authors, Apache2.0 copyright/license/NOTICE. No installation/copy/internal reader links. Final independent REST acceptance093, GitHub-only integrated publication070.

## Estimate and readiness
4 contributor hours; total72h candidate8points within80h two-week budget with reviewer/QA slots. Firstthree operation/example/constraint fixtures measured before scaling; split exact exclusive IDs if capacity exceeded. No implementation before DESIGNClosed, independent lead reviews and parentDevelopmentDoD. No infrastructure change; no DEVOPS child because070 owns release.
