---
id: EPIC-003
type: epic
title: Ontology & Functions Skills
status: Done
created: 2026-04-13
updated: 2026-07-30
priority: Critical
resolution: Done
assignee: architect
reporter: architect
---

# EPIC-003: Ontology & Functions Skills

## Description

Implement two Claude Code skills that expose Foundry API v2 Ontology and Functions namespaces to AI agents. These are Phase 2 high-priority skills (Sprint 3-4) that enable agents to interact with Foundry's knowledge graph and data transformation services.

## Scope

- `foundry-ontologies` skill (DEV-STORY-007): 67 operations. Current tracker evidence and metadata allow-list rows use 67 as the authoritative scope. Older 55-operation references are stale.
- `foundry-functions` skill (DEV-STORY-008): 7 operations.

Combined EPIC-003 scope: 74 operations.

## Technical requirements

- Both skills must implement the 8-step access control precedence model from SRS-001 section 4.2.
- TOON format auto-selection must follow ADR-004.
- Structured error handling must follow ADR-001.
- Retry logic and timeouts must follow ADR-002.
- NDJSON logging to stderr must follow ADR-005.
- Attribution injection is required for ontology query operations under FR-ATTR-4.

## Acceptance criteria

- [ ] DEV-STORY-007 (`foundry-ontologies` skill) reaches Done/Closed with all 67 operations implemented, tested, and validated.
- [ ] DEV-STORY-008 (`foundry-functions` skill) reaches Done/Closed with all 7 operations implemented, tested, and validated.
- [ ] Both skills are deployed to `.claude/skills/foundry-{namespace}/`.
- [ ] All operations follow common patterns from EPIC-001.
- [ ] Attribution headers are injected for `ontologies.query.*` operations.
- [ ] TOON format rendering works for list operations.
- [ ] Access control guards work for all 74 EPIC-003 operations.
- [ ] Integration testing passes for both skills.
- [ ] SKILL.md documentation is complete for both skills with operation catalog and examples.

## Related documentation

- `.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md`
- `.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md`
- `.ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md`
- `.ept/docs/deliverables/architecture/adr/ADR-002-call-timeout-defaults.md`
- `.ept/docs/deliverables/architecture/adr/ADR-004-format-auto-algorithm.md`
- `.ept/docs/deliverables/architecture/adr/ADR-005-log-format.md`
- `.ept/docs/deliverables/architecture/canonical-env-var-reference.md`
- `.ept/docs/deliverables/architecture/metadata-allow-list.md`

## Notes

Ontology namespace is the largest EPIC-003 skill. Functions is smaller and should follow the same common-layer pattern once ontology scope is settled.
