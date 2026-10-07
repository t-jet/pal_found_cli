---
id: DEV-049
type: development
title: 'DEV-049: Author offline AIP Agents Functions and Language Models operations'
status: Resolved
created: 2026-10-03
updated: 2026-10-03
priority: High
assignee: python-developer
reporter: tech-lead
estimated_hours: 14
time_spent_hours: 3
---

# DEV-049: Author offline Agents, Functions and Language Models operations

## Description

Author the per-operation offline guidance for the AIP Agents (15 ops), Functions (7 ops) and Language Models (2 ops) resource clients per SA-DES-012/BA-DES-013 (24 ops total). Owns these three namespace skill folders. Each leaf <=300 lines, relative offline-resolving links, preserve shared conventions and FEATURE-011 install prerequisite. Docs-only; no CLI code.

## Acceptance Criteria

- Given every installed operation in the owned Agents, Functions and Language Models resource clients, when the parser and dispatch inventory (frozen register on the parent story) is compared with the authored skill, then each supported operation has exactly one reachable record and no unsupported call is presented as available.
- Given an owned operation record, when a semantic reviewer checks it against installed CLI behavior and authoritative Foundry evidence, then resource, effect, side effects, every positional/JSON/applicable common input meaning, success/empty/page/pending/error interpretation, and a coherent example are correct and the review is recorded.
- Given the copied Agents / Functions / Language Models skill folders without network access, when a novice agent follows a representative example with mock or recorded output for each owned namespace, then it can choose valid inputs and interpret the result; every required local link resolves.
- Given the authored leaf files, when their lengths and links are validated, then each leaf is <=300 lines and uses relative offline-resolving links.
- Given the skill folder, when the FEATURE-011 install prerequisite block is checked, then it still states the python-package dependency with short conda/pip/uv install instructions.

## Related Documentation

- Parent story: DEV-STORY-049 (Agents/Functions/Language Models, 24 ops)
- Frozen per-operation register (parser/dispatch op keys, source locators, reviewer decisions, QA case IDs): register comment 20261003-174850 on DEV-STORY-049
- BA-DES-013: `.ept/docs/deliverables/business_design/BA-DES-013-offline-foundry-skill-guidance.md`
- SA-DES-012: `.ept/docs/deliverables/architecture/SA-DES-012-offline-foundry-skill-technical-design.md`
- BA-ANA-013: `.ept/docs/deliverables/business_analysis/BA-ANA-013-offline-foundry-knowledge.md`
- feature_request = FEATURE-012 (content preserved from FEATURE-008/009)

## Notes

Owns the AIP Agents, Functions and Language Models skill folders. Register op keys are frozen at the parent-story comment; do not invent op keys outside it.
