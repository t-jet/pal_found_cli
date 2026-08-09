---
id: EPIC-002
type: epic
title: Datasets & Filesystem Skills
status: Done
created: 2026-04-13
updated: 2026-07-30
priority: Critical
resolution: Done
assignee: architect
reporter: architect
---

# EPIC-002: Datasets & Filesystem Skills

## Description

Implement foundry-datasets skill (26 operations) and foundry-filesystem skill (31 operations). These are the highest-priority namespace skills consumed by agents for data I/O operations and are critical enablers for any data-centric workflows.

This epic encompasses the end-to-end implementation of the two highest-priority namespace skills that enable AI agents to interact with Foundry's core data storage and file management capabilities:

**foundry-datasets skill (DEV-STORY-005):**
- 26 operations covering dataset CRUD, branch management, schema inspection
- File upload/download capabilities
- Transaction management
- Critical priority

**foundry-filesystem skill (DEV-STORY-006):**
- 31 operations for file/folder navigation, management, and transfer
- Foundry Compass filesystem operations (upload, download, stat, move, copy)
- High priority

**Phase 2 of Implementation Roadmap** (Sprint 3-4) as defined in SAD-001.

**Dependencies:**
- Requires DEV-STORY-001 through DEV-STORY-004 complete (Phase 1 foundation)
- Builds on _foundry_cli_common.py shared module
- Follows architecture patterns from SAD-001

## Acceptance Criteria

- [ ] DEV-STORY-005 (foundry-datasets skill) completed and transitioned to Done status
- [ ] DEV-STORY-006 (foundry-filesystem skill) completed and transitioned to Done status
- [ ] Both skills tested and validated for agent consumption via subprocess calls
- [ ] Both skills follow architecture patterns defined in SAD-001 (auth, retry, output formatting, access control)
- [ ] Integration with _foundry_cli_common.py module validated
- [ ] Skills packaged according to Claude Code skill format (.claude/skills/ structure with SKILL.md)
- [ ] All acceptance criteria in child DEV-STORYs met
- [ ] Access control and configuration subsystems functioning correctly for both skills
- [ ] JSON/TOON output formatting validated per requirements in SRS-001

## Related Documentation

- [SAD-001 — Solution Architecture Document](../deliverables/architecture/SAD-001-foundry-cli.md) — See Section 10 (Implementation Roadmap), Phase 2: EPIC-002
- [SRS-001 — Software Requirements Specification](../deliverables/business_analysis/SRS-001-foundry-cli.md) — Functional requirements for datasets and filesystem operations
- FEATURE-001 — Parent feature request for Foundry CLI implementation
- DEV-STORY-005 — foundry-datasets skill (26 operations)
- DEV-STORY-006 — foundry-filesystem skill (31 operations)

## Notes

TODO: Add any additional notes
