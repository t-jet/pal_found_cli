---
id: DEV-043
type: development
title: 'DEV-043: Author offline Admin governance and Audit operations in Admin/Audit skills'
status: Closed
created: 2026-10-03
updated: 2026-10-12
priority: High
assignee: python-developer
reporter: tech-lead
estimated_hours: 18
time_spent_hours: 3
---

# DEV-043: Author offline Admin governance and Audit operations

## Description

Author the per-operation offline guidance for the Admin governance resource clients (cbac, host, marking, marking_category, marking_member, marking_role_assignment, organization, organization_guest_member, organization_role_assignment) plus Audit (log_file) per SA-DES-012/BA-DES-013 (28 + 2 = 30 ops). Owns the separate Admin governance part and the Audit skill; coordinates the Admin SKILL.md navigation link with the identity owner (DEV-042). Each leaf <=300 lines, relative offline-resolving links, preserve shared conventions and FEATURE-011 install prerequisite. Docs-only; no CLI code.

## Acceptance Criteria

- Given every installed operation in the owned Admin governance and Audit resource clients, when the parser and dispatch inventory (frozen register on the parent story) is compared with the authored skill, then each supported operation has exactly one reachable record and no unsupported call is presented as available.
- Given an owned operation record, when a semantic reviewer checks it against installed CLI behavior and authoritative Foundry evidence, then resource, effect, side effects, every positional/JSON/applicable common input meaning, success/empty/page/pending/error interpretation, and a coherent example are correct and the review is recorded.
- Given the copied Admin governance and Audit skill folders without network access, when a novice agent follows a representative example with mock or recorded output for each owned namespace, then it can choose valid inputs and interpret the result; every required local link resolves.
- Given the authored leaf files, when their lengths and links are validated, then each leaf is <=300 lines and uses relative offline-resolving links.
- Given the skill folder, when the FEATURE-011 install prerequisite block is checked, then it still states the python-package dependency with short conda/pip/uv install instructions.

## Related Documentation

- Parent story: DEV-STORY-043 (Admin governance + Audit, 30 ops)
- Frozen per-operation register (parser/dispatch op keys, source locators, reviewer decisions, QA case IDs): register comment 20261003-174720 on DEV-STORY-043
- BA-DES-013: `.ept/docs/deliverables/business_design/BA-DES-013-offline-foundry-skill-guidance.md`
- SA-DES-012: `.ept/docs/deliverables/architecture/SA-DES-012-offline-foundry-skill-technical-design.md`
- BA-ANA-013: `.ept/docs/deliverables/business_analysis/BA-ANA-013-offline-foundry-knowledge.md`
- feature_request = FEATURE-012 (content preserved from FEATURE-008/009)

## Notes

DependsOn DEV-STORY-042 (Admin identity/access). Owns the Admin governance part (CBAC, host, markings, organizations) and the Audit skill; does not edit the Admin SKILL.md navigation owned by identity. Register op keys are frozen at the parent-story comment; do not invent op keys outside it.
