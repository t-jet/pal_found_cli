---
id: EPIC-006
type: epic
title: Data Pipeline Skills
status: In Progress
created: 2026-04-13
updated: 2026-05-18
priority: High
assignee: architect
reporter: architect
---

# EPIC-006: Data Pipeline Skills

## Description

Implement four data pipeline namespace skills for the Foundry CLI Agentic Toolset, covering orchestration, SQL queries, streaming data, and connectivity management. This epic corresponds to **Phase 4 (Sprint 7-8)** of the implementation roadmap defined in SAD-001.

## Scope

This epic encompasses the following four Developer Stories:

| Story | Skill | Operations | Priority |
|---|---|---|---|
| DEV-STORY-014 | oundry-orchertation | 20 operations | High |
| DEV-STORY-015 | oundry-sql-queries | 5 operations | High |
| DEV-STORY-016 | oundry-streams | 17 operations (batch strategy per ADR-003) | High |
| DEV-STORY-017 | oundry-connectivity | 15 operations | Medium |

**Total: 57 operations across 4 skills**

## Acceptance Criteria

- [ ] All 4 DEV-STORYs (014-017) implemented and in Done/Closed status
- [ ] oundry-orchestration skill exposes 20 Foundry SDK orchestration operations via CLI
- [ ] oundry-sql-queries skill exposes 5 SQL query operations via CLI
- [ ] oundry-streams skill exposes 17 streaming operations via CLI, implementing batch-response pattern per ADR-003
- [ ] oundry-connectivity skill exposes 15 connectivity operations via CLI
- [ ] All skills follow common patterns: ConfigLoader, AuthProvider, RetryHandler, ErrorSerializer, OutputFormatter (per SAD-001)
- [ ] All skills follow exit code taxonomy (ADR-001), timeout defaults (ADR-002), log format (ADR-005)
- [ ] oundry-streams implements --max-records (default 100, max 10,000) and FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S (default 120s) per ADR-003
- [ ] Unit tests cover all 57 operations
- [ ] Integration tests validate end-to-end CLI behavior for each skill
- [ ] SKILL.md documentation produced for each skill

## Dependencies

- EPIC-001 (Core CLI Infrastructure) must be complete — provides _foundry_cli_common.py, RetryHandler, ErrorSerializer, OutputFormatter, AccessControlGuard
- ADR-003 (Streams Batch Strategy) defines batch-response pattern for oundry-streams skill

## Related Documentation

- SAD-001 §10 (Implementation Roadmap, Phase 4): .ept/docs/deliverables/architecture/SAD-001-foundry-cli.md
- ADR-003 (Streams Batch Strategy): .ept/docs/deliverables/architecture/adr/ADR-003-streams-batch-strategy.md
- ADR-001 (Exit Code Taxonomy): .ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md
- ADR-002 (Call Timeout Defaults): .ept/docs/deliverables/architecture/adr/ADR-002-call-timeout-defaults.md
- ADR-005 (Log Format): .ept/docs/deliverables/architecture/adr/ADR-005-log-format.md
- SRS-001 (Software Requirements Specification): .ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md

## Notes

- Phase 4 of implementation roadmap (Sprint 7-8)
- Blocks: none identified at this stage
