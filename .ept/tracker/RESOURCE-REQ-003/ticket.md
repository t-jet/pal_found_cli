---
id: RESOURCE-REQ-003
type: resource_req
title: Provision Python Developer agent(s) for Foundry CLI namespace skill implementation
status: Closed
reporter: architect
created: 2026-05-01
updated: 2026-05-01
priority: Critical
resolution: Done
assignee: hr
---

# RESOURCE-REQ-003: Provision Python Developer agent(s) for Foundry CLI namespace skill implementation

## Description

﻿## Role Definition

**Role**: Python Developer (1–2 agents recommended for parallel execution)  
**Project**: Foundry CLI Agentic Toolset — 21 Claude Code skills exposing 355 Palantir Foundry API v2 operations

## Context / Business Need

The project has 19 namespace skill DEV-STORYs (DEV-STORY-005 through DEV-STORY-023), each implementing a specific Foundry API namespace as a Claude Code MCP skill. The workload is:

| Category | DEV-STORYs | Operations |
|---|---|---|
| Datasets & Filesystem Skills | DEV-STORY-005, 006 | 57 ops |
| Ontology & Functions Skills | DEV-STORY-007, 008 | 62 ops |
| Admin & Security Skills | DEV-STORY-009, 010 | 68 ops |
| AI & Models Skills | DEV-STORY-011, 012, 013 | 38 ops |
| Data Pipeline Skills | DEV-STORY-014, 015, 016 | 42 ops |
| Remaining Namespace Skills | DEV-STORY-017 through 022 | 73 ops |
| Knowledge Skill | DEV-STORY-023 | N/A (content authoring) |

Each DEV-STORY requires DEV and UNITTEST sub-tasks. The work is highly parallelizable by namespace. No Python Developer role is currently provisioned; the Tech Lead will handle shared infrastructure (DEV-STORY-001 to 004), but cannot execute all 19 namespace skills.

## Responsibilities

1. Implement namespace skill Python files (e.g., `foundry_datasets.py`, `foundry_ontologies.py`, `foundry_admin.py`) following patterns established by the Tech Lead and SAD-001 architecture specifications
2. Write unit tests for all implemented operations (UNITTEST sub-tasks using pytest/pytest-asyncio), achieving minimum 80% code coverage per skill
3. Fix defects identified in TESTEXEC sub-tasks and BUG-SUB tickets within agreed SLA
4. Follow coding standards defined by the Tech Lead: tool schema structure, Pydantic model conventions, async client patterns, error handling
5. Participate in code review processes: address CODEREVIEW feedback from Tech Lead within the same sprint
6. Self-review code against OWASP Top-10 security checklist before submitting for code review

## Required Skills

| Skill | Proficiency Level |
|---|---|
| Python 3.x | Advanced |
| AsyncIO / aiohttp | Intermediate |
| REST API Client Development | Advanced |
| Testing (pytest, pytest-asyncio) | Advanced |
| Pydantic Data Validation | Intermediate |
| Git / GitHub Workflows | Advanced |
| CLI Tool Development | Intermediate |
| OWASP Top-10 Security Awareness | Intermediate |

## Expected Deliverables

- 19 namespace skill implementation files (DEV sub-tasks, one per DEV-STORY from DEV-STORY-005 to DEV-STORY-023)
- Unit test suites for all namespace skills (UNITTEST sub-tasks, >=80% code coverage)
- Defect fixes for BUG-SUB tickets raised during QA

## Staffing Recommendation

**1 agent minimum** to unblock the Development stage. **2 agents recommended** to enable parallel execution across namespace groups, targeting 9-sprint delivery as per SAD-001 roadmap. Sprints 3-7 are the peak development period requiring parallel capacity.

## References

- SAD-001: `.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md` (Implementation Phases, Tech Stack)
- DEV-STORY-005 through DEV-STORY-023 (namespace skill stories)


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
