---
id: DEV-046
type: development
title: 'DEV-046: Author offline Ontology discovery operations with Ontologies SKILL.md navigation'
status: Resolved
created: 2026-10-03
updated: 2026-10-03
priority: High
assignee: python-developer
reporter: tech-lead
estimated_hours: 16
time_spent_hours: 3
---

# DEV-046: Author offline Ontology discovery operations

## Description

Author the per-operation offline guidance for the Ontology discovery resource clients (action_type, action_type_full_metadata, linked_object, object_type, ontology, ontology_object, ontology_value_type, query_type; 28 ops) per SA-DES-012/BA-DES-013. Owns the Ontologies SKILL.md navigation and the discovery local part. Each leaf <=300 lines, relative offline-resolving links, preserve shared conventions and FEATURE-011 install prerequisite. Ontologies CLI is hand-rolled; source is pal_found_cli_tool/src/pal_found_cli/ontologies/scripts/pal_found_ontologies_cli.py. Docs-only; no CLI code.

## Acceptance Criteria

- Given every installed operation in the owned Ontology discovery resource clients, when the parser and dispatch inventory (frozen register on the parent story) is compared with the authored skill, then each supported operation has exactly one reachable record and no unsupported call is presented as available.
- Given an owned operation record, when a semantic reviewer checks it against installed CLI behavior and authoritative Foundry evidence, then resource, effect, side effects, every positional/JSON/applicable common input meaning, success/empty/page/pending/error interpretation, and a coherent example are correct and the review is recorded.
- Given the copied Ontologies skill folder without network access, when a novice agent follows a representative example with mock or recorded output for the owned namespace, then it can choose valid inputs and interpret the result; every required local link resolves.
- Given the authored leaf files, when their lengths and links are validated, then each leaf is <=300 lines and uses relative offline-resolving links.
- Given the skill folder, when the FEATURE-011 install prerequisite block is checked, then it still states the python-package dependency with short conda/pip/uv install instructions.

## Related Documentation

- Parent story: DEV-STORY-046 (Ontology discovery, 28 ops)
- Frozen per-operation register (parser/dispatch op keys, source locators, reviewer decisions, QA case IDs): register comment 20261003-174821 on DEV-STORY-046
- BA-DES-013: `.ept/docs/deliverables/business_design/BA-DES-013-offline-foundry-skill-guidance.md`
- SA-DES-012: `.ept/docs/deliverables/architecture/SA-DES-012-offline-foundry-skill-technical-design.md`
- BA-ANA-013: `.ept/docs/deliverables/business_analysis/BA-ANA-013-offline-foundry-knowledge.md`
- feature_request = FEATURE-012 (content preserved from FEATURE-008/009)

## Notes

Owns the Ontologies navigation and discovery local part; the Ontology actions/rich-properties part is owned by DEV-047 (DependsOn 046). Register op keys are frozen at the parent-story comment; do not invent op keys outside it.
