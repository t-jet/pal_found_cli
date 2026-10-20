---
id: DEV-048
type: development
title: 'DEV-048: Author offline Connectivity Checkpoints and Data Health operations'
status: Closed
created: 2026-10-03
updated: 2026-10-12
priority: High
assignee: python-developer
reporter: tech-lead
estimated_hours: 16
time_spent_hours: 4
---

# DEV-048: Author offline Connectivity, Checkpoints and Data Health operations

## Description

Author the per-operation offline guidance for the Connectivity (20 ops), Checkpoints (3 ops) and Data Health (6 ops) resource clients per SA-DES-012/BA-DES-013 (29 ops total). Owns these three namespace skill folders. Each leaf <=300 lines, relative offline-resolving links, preserve shared conventions and FEATURE-011 install prerequisite. Docs-only; no CLI code.

## Acceptance Criteria

- Given every installed operation in the owned Connectivity, Checkpoints and Data Health resource clients, when the parser and dispatch inventory (frozen register on the parent story) is compared with the authored skill, then each supported operation has exactly one reachable record and no unsupported call is presented as available.
- Given an owned operation record, when a semantic reviewer checks it against installed CLI behavior and authoritative Foundry evidence, then resource, effect, side effects, every positional/JSON/applicable common input meaning, success/empty/page/pending/error interpretation, and a coherent example are correct and the review is recorded.
- Given the copied Connectivity / Checkpoints / Data Health skill folders without network access, when a novice agent follows a representative example with mock or recorded output for each owned namespace, then it can choose valid inputs and interpret the result; every required local link resolves.
- Given the authored leaf files, when their lengths and links are validated, then each leaf is <=300 lines and uses relative offline-resolving links.
- Given the skill folder, when the FEATURE-011 install prerequisite block is checked, then it still states the python-package dependency with short conda/pip/uv install instructions.

## Related Documentation

- Parent story: DEV-STORY-048 (Connectivity/Checkpoints/Data Health, 29 ops)
- Frozen per-operation register (parser/dispatch op keys, source locators, reviewer decisions, QA case IDs): register comment 20261003-174840 on DEV-STORY-048
- BA-DES-013: `.ept/docs/deliverables/business_design/BA-DES-013-offline-foundry-skill-guidance.md`
- SA-DES-012: `.ept/docs/deliverables/architecture/SA-DES-012-offline-foundry-skill-technical-design.md`
- BA-ANA-013: `.ept/docs/deliverables/business_analysis/BA-ANA-013-offline-foundry-knowledge.md`
- feature_request = FEATURE-012 (content preserved from FEATURE-008/009)

## Notes

Owns the Connectivity, Checkpoints and Data Health skill folders. Register op keys are frozen at the parent-story comment; do not invent op keys outside it.
