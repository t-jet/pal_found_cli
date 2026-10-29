---
id: DEV-STORY-069
type: dev_story
title: Author bounded local REST and SDK recipe contracts
status: Development
feature_request: FEATURE-015
epic: EPIC-015
created: 2026-10-06
updated: 2026-10-06
priority: High
assignee: python-developer
reporter: ba
component: skills
story_points: 8
release_notes: Complete offline SDK1.101.0 catalog and shared development patterns for all425 operations.
---

# Complete offline REST SDK catalog and common development patterns

## Business outcome
An agent selects any Foundry Platform SDK 1.101.0 operation and derives its invocation from a complete local catalog inside standalone pal-found-dev.

## Owned scope
T37 common catalog/navigation, immutable SDK baseline, compatibility delta against supplied 1.79.0 source, deterministic structural operation/model/error knowledge and shared SDK/HTTP/authentication/response patterns. All 425 canonical operations, 113 resources, 20 service/API-version namespaces and 3,242 reachable contract symbols (2,278 models and 964 error symbols). Domain stories exclusively own operation behavior explanation/examples and exhaustive source review; this story owns catalog mechanics, shared model organization and common patterns.

## Acceptance Criteria
- Freeze SDK1.101.0 commit168d51910570b6966afa2320333ab36f6a3f7ccf/OpenAPI1.1697.0 and exact inventory hashes; distinguish API versions, generated0.0.0 placeholder and actual prepared runtime version. Record supplied1.79.0 compatibility differences without modifying that checkout or reducing425 coverage.
- Deterministically derive structural contracts from official SDK documentation/source, retain applicable license attribution, and provide readable local navigation for every operation plus complete transitive model/error closure.
- Every operation record includes exact client/method/signature, HTTP semantics, typed inputs/output, nested definitions, documented restrictions and direct route to domain-owned behavior/examples. Zero uncovered operations, unresolved model/error references or unreviewed differences.
- Common patterns explain synchronous/asynchronous clients, supported raw/streaming wrappers, authentication/identity, binary/stream lifecycle, errors, finite pagination/polling, timeout/retry and safe uncertain-write reconciliation.
- Fulfill BA-DES-015 BD-015-01,08,11. All knowledge fits standalone pal-found-dev; public links optional attribution. Enrollment-specific values are declared prerequisites with local derivation/validation guidance.
- Preserve351 CLI operations and all unrelated topic content. Add no installation/copy prose or internal reader references.

## Related Documentation
BA-DES-015 revision2; SA-DES-014 revision2 and exact SDK inventories; WORK-003.

## Planning and delivery
Replaces prior ten-method scope. Candidate8points; grooming validates deterministic catalog implementation, maintenance/review effort and sprint capacity or splits explicit deliverables before development. Domain stories depend on accepted freeze/common structure; final comprehensive behavior/closure evidence belongs to separate REST acceptance story, and integrated GitHub-only release belongs to DEV-STORY-070. ParentFEATURE015 InDesign, retainNew until specificWaitingImplementation readiness gate is met. No skill implementation during design.


## Closure reconciliation
The 3,242 extracted model/error symbols are an initial inventory. Independently reconcile source definitions, including indirect or compound forward references; add and review every required symbol omitted by extraction. Acceptance requires the complete corrected closure, not an exact numerical cap.
