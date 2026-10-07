---
id: DEV-047
type: development
title: 'DEV-047: Author offline Ontology actions and rich properties content'
status: Resolved
created: 2026-10-03
updated: 2026-10-03
priority: High
assignee: python-developer
reporter: tech-lead
estimated_hours: 20
time_spent_hours: 3
---

# DEV-047: Author offline Ontology actions and rich properties operations

## Description

Author the per-operation offline guidance for the Ontology action/rich-property resource clients (action, attachment, attachment_property, cipher_text_property, geotemporal_series_property, media_reference_property, ontology_interface, ontology_object_set, ontology_transaction, query, time_series_property_v2, time_series_value_bank_property; 39 ops) per SA-DES-012/BA-DES-013. Owns the separate Ontologies action/property part. Each leaf <=300 lines, relative offline-resolving links, preserve shared conventions and FEATURE-011 install prerequisite. Docs-only; no CLI code.

## Acceptance Criteria

- Given every installed operation in the owned Ontology action/rich-property resource clients, when the parser and dispatch inventory (frozen register on the parent story) is compared with the authored skill, then each supported operation has exactly one reachable record and no unsupported call is presented as available.
- Given an owned operation record, when a semantic reviewer checks it against installed CLI behavior and authoritative Foundry evidence, then resource, effect, side effects, every positional/JSON/applicable common input meaning, success/empty/page/pending/error interpretation, and a coherent example are correct and the review is recorded.
- Given the copied Ontologies skill folder without network access, when a novice agent follows a representative example with mock or recorded output for the owned namespace, then it can choose valid inputs and interpret the result; every required local link resolves.
- Given the authored leaf files, when their lengths and links are validated, then each leaf is <=300 lines and uses relative offline-resolving links.
- Given the skill folder, when the FEATURE-011 install prerequisite block is checked, then it still states the python-package dependency with short conda/pip/uv install instructions.

## Related Documentation

- Parent story: DEV-STORY-047 (Ontology actions and rich properties, 39 ops)
- Frozen per-operation register (parser/dispatch op keys, source locators, reviewer decisions, QA case IDs): register comment 20261003-174831 on DEV-STORY-047
- BA-DES-013: `.ept/docs/deliverables/business_design/BA-DES-013-offline-foundry-skill-guidance.md`
- SA-DES-012: `.ept/docs/deliverables/architecture/SA-DES-012-offline-foundry-skill-technical-design.md`
- BA-ANA-013: `.ept/docs/deliverables/business_analysis/BA-ANA-013-offline-foundry-knowledge.md`
- feature_request = FEATURE-012 (content preserved from FEATURE-008/009)

## Notes

DependsOn DEV-STORY-046 (Ontology discovery). Owns the Ontology actions/rich-properties part; coordinates its SKILL.md link with the discovery owner (DEV-046). Register op keys are frozen at the parent-story comment; do not invent op keys outside it.
