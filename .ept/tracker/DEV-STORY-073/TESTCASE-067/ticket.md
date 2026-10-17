---
id: TESTCASE-067
type: testcase
title: DEV-STORY-073 testcase J13 governance REST contracts
status: Open
created: 2026-10-06
updated: 2026-10-06
priority: High
assignee: qa-engineer
reporter: tech-lead
estimated_hours: 6
---

# DEV-STORY-073 testcase

## Owned scope
48 exact operation IDs in .ept/docs/deliverables/development/FEATURE-015-rest-operation-partitions.json; partition hash 017ec8aa12d0a850dd391ab0fbf961d3cfaf81f74f7eef2880948b00c53aee0c.
Resources: v2.audit.LogFile, v2.filesystem.Folder, v2.filesystem.Project, v2.filesystem.ProjectResourceReference, v2.filesystem.Resource, v2.filesystem.ResourceRole, v2.filesystem.ResourceTag, v2.filesystem.Space, v2.third_party_applications.ThirdPartyApplication, v2.third_party_applications.Version, v2.third_party_applications.Website.
Core069 owns structural contracts, full models/errors, service indexes and common patterns. This story owns resource behavior under references/rest/<version>/<service>/<Resource>.md (numbered leaves at most300lines) and reader examples/fixtures examples/rest/073/ inside standalone pal-found-dev. Tests own tests/test_offline_rest_073.py.

## Acceptance criteria
Independent QA derives source expectations before authored outputs. Formal TESTCASE stays Open until real runnable implementation exists. Define every-owned-method assertions and isolated J13 governance success/adverse cases.
Every operation has locally available signature/HTTP/body/typed inputs/results/nested models/errors/effects/availability/modes and bounded recovery. Every example supplies synthetic or precisely described tenant values, actual SDK call, request/response/error assertions. Use actual asynchronous return signatures, not inferred Awaitable types. Keep source silence explicit with authorized tenant verification; invent no universal scope or idempotency guarantee. Independently reconcile full model/error closure;3242 is not a cap. Governance covers hierarchy traversal and supported modification/access/uncertain-write recovery; AIP covers actual agents/versions/sessions and model capabilities, private/beta enablement, denied access, canceled streams and finite continuation as applicable to owned operations.

## Related documentation
BA-DES-015/SA-DES-014 revision2 and closed owner approvals QUESTION179/182. Indexed FEATURE-015-rest-authoring-contract.md and exact partition JSON. Primary SDK1.101.0 commit168d51910570b6966afa2320333ab36f6a3f7ccf/OpenAPI1.1697.0. Supplement SDK silence with relevant official API references while authoring. Preserve351 CLI operations and other authors, Apache2.0 copyright/license/NOTICE. No installation/copy/internal reader links. Final independent REST acceptance093, GitHub-only integrated publication070.

## Estimate and readiness
6 contributor hours; total72h candidate8points within80h two-week budget with reviewer/QA slots. Firstthree operation/example/constraint fixtures measured before scaling; split exact exclusive IDs if capacity exceeded. No implementation before DESIGNClosed, independent lead reviews and parentDevelopmentDoD. No infrastructure change; no DEVOPS child because070 owns release.
