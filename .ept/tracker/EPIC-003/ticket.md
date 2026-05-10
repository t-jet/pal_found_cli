---
id: EPIC-003
type: epic
title: Ontology & Functions Skills
status: Blocked
created: 2026-04-13
updated: 2026-05-02
priority: Critical
assignee: architect
reporter: architect
---

# EPIC-003: Ontology & Functions Skills

## Description

Implement two Claude Code skills that expose Foundry API v2 Ontology and Functions namespaces to AI agents. These are Phase 2 high-priority skills (Sprint 3-4) that enable agents to interact with Foundry's knowledge graph and data transformation services.

**Scope:**
- **`foundry-ontologies` skill** (DEV-STORY-007): 55 operations — Largest namespace covering:
  - Object type CRUD operations
  - Link types, action types, query types
  - Interface types, shared property types
  - Special attention to TOON output for list operations
  - Attribution headers required for `ontologies.query.*` operations (FR-ATTR-4)

- **`foundry-functions` skill** (DEV-STORY-008): 7 operations covering:
  - Function versioning
  - Function execution
  - Relatively small scope; completes quickly after EPIC-001 foundation

**Dependencies:**
- EPIC-001 (Core Infrastructure & Templates) must be complete — provides `_foundry_cli_common.py`, skill templates, test framework, and common patterns

**Technical Requirements:**
- Both skills must implement 8-step access control precedence model (SRS §4.2)
- TOON format auto-selection per ADR-004
- Structured error handling with typed exit codes per ADR-001
- Retry logic and timeouts per ADR-002
- NDJSON logging to stderr per ADR-005
- Attribution injection for ontology query operations per FR-ATTR-4

## Acceptance Criteria

- [ ] DEV-STORY-007 (`foundry-ontologies` skill) in Done status with all 55 operations implemented, tested, and validated
- [ ] DEV-STORY-008 (`foundry-functions` skill) in Done status with all 7 operations implemented, tested, and validated
- [ ] Both skills deployed to `.claude/skills/foundry-{namespace}/` structure
- [ ] All operations follow common patterns from EPIC-001
- [ ] Attribution headers correctly injected for `ontologies.query.*` operations
- [ ] TOON format rendering works correctly for list operations
- [ ] Access control guards function correctly for all 62 operations
- [ ] Integration testing passes for both skills
- [ ] SKILL.md documentation complete for both skills with operation catalog and examples

## Related Documentation

- [SAD-001 §10 Implementation Roadmap](e:\learn\GenAI_Foundations_DA\git\foundry_cli\.ept\docs\deliverables\architecture\SAD-001-foundry-cli.md) — Phase 2 planning
- [SRS-001 §3.2 FR-ATTR-4](e:\learn\GenAI_Foundations_DA\git\foundry_cli\.ept\docs\deliverables\business_analysis\SRS-001-foundry-cli.md) — Attribution requirements for ontologies.query.*
- [ADR-004](e:\learn\GenAI_Foundations_DA\git\foundry_cli\.ept\docs\deliverables\architecture\adr\ADR-004-format-auto-algorithm.md) — Format auto-selection for TOON rendering
- [ADR-001](e:\learn\GenAI_Foundations_DA\git\foundry_cli\.ept\docs\deliverables\architecture\adr\ADR-001-exit-code-taxonomy.md) — Exit code taxonomy
- [ADR-002](e:\learn\GenAI_Foundations_DA\git\foundry_cli\.ept\docs\deliverables\architecture\adr\ADR-002-call-timeout-defaults.md) — Timeout and retry configuration
- [ADR-005](e:\learn\GenAI_Foundations_DA\git\foundry_cli\.ept\docs\deliverables\architecture\adr\ADR-005-log-format.md) — Structured logging format

## Notes

- Largest combined operation count in a single epic (62 operations)
- Ontologies namespace is the largest single namespace in Foundry API v2
- Functions skill is relatively straightforward; ontologies skill requires careful attention to complex query operations
