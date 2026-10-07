---
id: DEV-STORY-048
type: dev_story
title: Document offline Connectivity Checkpoints and Data Health operations
status: Development
feature_request: FEATURE-012
epic: EPIC-012
created: 2026-10-03
updated: 2026-10-03
priority: Medium
assignee: python-developer
reporter: ba
component: skills
story_points: 12
release_notes: Connectivity, Checkpoints and Data Health operations have complete offline Foundry guidance.
---

# Document offline Connectivity Checkpoints and Data Health operations

## Scope
connectivity: all 20 operations; checkpoints: all 3 operations; data_health: all 6 operations. Own these three namespace skill folders.

## Acceptance criteria
- Given every installed operation in the owned resource clients, when the parser and dispatch inventory is compared with the skill, then each supported operation has exactly one reachable record and no unsupported call is presented as available.
- Given an owned operation record, when a semantic reviewer checks it against installed CLI and authoritative Foundry evidence, then resource, effect, side effects, every positional/JSON/applicable common input meaning, success/empty/page/pending/error interpretation, and a coherent example are correct and the review is recorded.
- Given the copied owned skill folder without network access, when a novice agent follows a representative example with mock or recorded output for each owned namespace, then it can choose valid inputs and interpret the result; every required local link resolves.

Trace: FEATURE-012, BA-ANA-013 BR-012-01..11 as applicable, BA-DES-013 AC-D-013-01..09 as applicable, and SA-DES-012. Grooming confirms one-sprint fit; no new CLI or Foundry operation. Remain New until FEATURE-012 reaches Waiting for Implementation.

During grooming, freeze the exact parser and dispatch operation keys owned by this story at the pinned tool commit and attach the reviewed per-operation register with source locators, reviewer decisions, and QA case IDs.

## Source documents

- `.ept/docs/deliverables/business_analysis/BA-ANA-013-offline-foundry-knowledge.md`
- `.ept/docs/deliverables/business_design/BA-DES-013-offline-foundry-skill-guidance.md`
- `.ept/docs/deliverables/architecture/SA-DES-012-offline-foundry-skill-technical-design.md`
