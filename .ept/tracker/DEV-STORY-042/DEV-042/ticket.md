---
id: DEV-042
type: development
title: 'DEV-042: Author offline Admin identity and access operations in Admin skill'
status: Resolved
created: 2026-10-03
updated: 2026-10-03
priority: High
assignee: python-developer
reporter: tech-lead
component: skills
estimated_hours: 20
time_spent_hours: 4
---

# DEV-042: Author offline Admin identity and access operations

## Description

Author the per-operation offline guidance for the Admin identity/access resource clients per SA-DES-012/BA-DES-013: authentication_provider, enrollment, enrollment_role_assignment, group, group_member, group_membership, group_membership_expiration_policy, group_provider_info, role, user, user_provider_info (38 ops). Owns the Admin navigation plus the identity part. Each leaf <=300 lines, relative offline-resolving links, preserve shared conventions and FEATURE-011 install prerequisite. Docs-only; no CLI code.

## Acceptance Criteria

- Given every installed operation in the owned Admin identity/access resource clients, when the parser and dispatch inventory (frozen register on the parent story) is compared with the authored skill, then each supported operation has exactly one reachable record and no unsupported call is presented as available.
- Given an owned operation record, when a semantic reviewer checks it against installed CLI behavior and authoritative Foundry evidence, then resource, effect, side effects, every positional/JSON/applicable common input meaning, success/empty/page/pending/error interpretation, and a coherent example are correct and the review is recorded.
- Given the copied Admin skill folder without network access, when a novice agent follows a representative example with mock or recorded output for the owned namespace, then it can choose valid inputs and interpret the result; every required local link resolves.
- Given the authored leaf files, when their lengths and links are validated, then each leaf is <=300 lines and uses relative offline-resolving links.
- Given the skill folder, when the FEATURE-011 install prerequisite block is checked, then it still states the python-package dependency with short conda/pip/uv install instructions.

## Related Documentation

- Parent story: DEV-STORY-042 (Admin identity/access, 38 ops)
- Frozen per-operation register (parser/dispatch op keys, source locators, reviewer decisions, QA case IDs): register comment 20261003-174711 on DEV-STORY-042
- BA-DES-013: `.ept/docs/deliverables/business_design/BA-DES-013-offline-foundry-skill-guidance.md`
- SA-DES-012: `.ept/docs/deliverables/architecture/SA-DES-012-offline-foundry-skill-technical-design.md`
- BA-ANA-013: `.ept/docs/deliverables/business_analysis/BA-ANA-013-offline-foundry-knowledge.md`
- feature_request = FEATURE-012 (content preserved from FEATURE-008/009)

## Notes

Owns the Admin identity part; the Admin governance/audit part is owned by DEV-043 (DependsOn 042). Coordination required so the Admin SKILL.md navigation link stays consistent. Register op keys are frozen at the parent-story comment; do not invent op keys outside it.
