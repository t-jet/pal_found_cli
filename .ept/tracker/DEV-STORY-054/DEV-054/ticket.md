---
id: DEV-054
type: development
title: 'DEV-054: Author offline Third Party Applications and Widgets operations'
status: Closed
created: 2026-10-03
updated: 2026-10-12
priority: High
assignee: python-developer
reporter: tech-lead
estimated_hours: 11
time_spent_hours: 3
---

# DEV-054: Author offline Third Party Applications and Widgets operations

## Description

Author the per-operation offline guidance for the Third Party Applications (9 ops) and Widgets (8 ops) resource clients per SA-DES-012/BA-DES-013 (17 ops total). Owns these two namespace skill folders. Each leaf <=300 lines, relative offline-resolving links, preserve shared conventions and FEATURE-011 install prerequisite. Docs-only; no CLI code.

## Acceptance Criteria

- Given every installed operation in the owned Third Party Applications and Widgets resource clients, when the parser and dispatch inventory (frozen register on the parent story) is compared with the authored skill, then each supported operation has exactly one reachable record and no unsupported Widgets legacy entry is presented as callable.
- Given an owned operation record, when a semantic reviewer checks it against installed CLI behavior and authoritative Foundry evidence, then resource, effect, side effects, every positional/JSON/applicable common input meaning, success/empty/page/pending/error interpretation, and a coherent example are correct and the review is recorded.
- Given the copied Third Party Applications / Widgets skill folders without network access, when a novice agent follows a representative example with mock or recorded output for each owned namespace, then it can choose valid inputs and interpret the result; every required local link resolves.
- Given the authored leaf files, when their lengths and links are validated, then each leaf is <=300 lines and uses relative offline-resolving links.
- Given the skill folder, when the FEATURE-011 install prerequisite block is checked, then it still states the python-package dependency with short conda/pip/uv install instructions.

## Related Documentation

- Parent story: DEV-STORY-054 (Third Party Applications/Widgets, 17 ops)
- Frozen per-operation register (parser/dispatch op keys, source locators, reviewer decisions, QA case IDs): register comment 20261003-174943 on DEV-STORY-054
- BA-DES-013: `.ept/docs/deliverables/business_design/BA-DES-013-offline-foundry-skill-guidance.md`
- SA-DES-012: `.ept/docs/deliverables/architecture/SA-DES-012-offline-foundry-skill-technical-design.md`
- BA-ANA-013: `.ept/docs/deliverables/business_analysis/BA-ANA-013-offline-foundry-knowledge.md`
- feature_request = FEATURE-012 (content preserved from FEATURE-008/009)

## Notes

Owns the Third Party Applications and Widgets skill folders. The four unsupported Widgets legacy design rows are documented as non-callable (negative-check only), consistent with the register decision at the parent-story comment; do not invent op keys outside it.
