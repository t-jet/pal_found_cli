---
id: DEV-STORY-074
type: dev_story
title: 'Author offline REST SDK contracts: Datasets across both API versions'
status: Deployment
feature_request: FEATURE-015
epic: EPIC-015
created: 2026-10-06
updated: 2026-10-21
priority: High
assignee: python-developer
reporter: ba
component: skills
story_points: 8
release_notes: Offline SDK1.101.0 knowledge for Datasets across both API versions; every owned contract available locally.
---

# Author offline REST SDK contracts: Datasets across both API versions

## Business outcome
An agent discovers and authors any owned Foundry REST SDK operation using only the standalone pal-found-dev knowledge and prepared SDK/runtime artifacts.

## Owned scope
T37 partition R4; 52 canonical operations in frozen SDK 1.101.0 (all v1.datasets and v2.datasets operations; owns REST dataset transactions and binary/file examples J11/J12). Exact IDs derive from the reviewed SA-DES-014 inventory using these service/resource predicates. All stability states are included. No operation exclusion without recorded Project Owner approval. This story exclusively owns these operation explanations/examples and coordinates shared models under DEV-STORY-069 ownership.

## Acceptance Criteria
- Each owned operation maps to a complete local SDK/HTTP contract, meaningful adaptable example, required input/output/model definitions, effects, permissions/prerequisites, errors, availability restrictions and bounded recovery where applicable.
- Synchronous/asynchronous and raw/streaming response forms have locally navigable guidance where exposed; all transitive models/errors resolve within standalone pal-found-dev.
- Fulfill BA-DES-015 BD-015-01,08,11 and seven-element topic contract; independent source/semantic review covers every owned operation, not only journey samples.
- Independent QA authors fixture expectations and selects service/API-version discovery cases without author assistance. Public internet is blocked; enrollment/fixture boundary and missing prerequisites are explicit.
- Preserve 351 CLI operations, other topic owners and valid knowledge. No installation/copy instructions, required sibling skills or internal development-document references in distributed content.
- Essential CLI defects remain FEATURE-012-owned with a linked acceptance blocker. All owned content gaps must be resolved before acceptance.

## Related Documentation
BA-DES-015 revision2; SA-DES-014 revision2 and SDK inventory 1.101.0; WORK-003; approved historical BA-ANA-016/SA-ANA-016.

## Planning and delivery
Candidate 8 points. Grooming must validate authoring and independent review capacity, exact model-dependency effort and one-sprint feasibility; split further by explicit operation-ID subsets if needed without changing the complete425 union. Requires approved design, DEV-STORY-061 audit/routing and DEV-STORY-069 frozen catalog/common patterns. Stories remain New until FEATURE-015 Waiting for Implementation. No authoring begins during design. Deliver content and review evidence to REST acceptance story and DEV-STORY-070 integration; final publication remains GitHub-only.
