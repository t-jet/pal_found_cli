---
id: RESOURCE-REQ-002
type: resource_req
title: Provision Tech Lead / Senior Python Developer agent for Foundry CLI project
status: Closed
reporter: architect
created: 2026-05-01
updated: 2026-05-01
priority: Critical
resolution: Tech Lead / Senior Python Developer agent provisioned. Agent file created at \.github/agents/tech-lead.agent.md\. Registered in \.ept/resources/available_resources.md\ under Development & Engineering Agents.
assignee: hr
---

# RESOURCE-REQ-002: Provision Tech Lead / Senior Python Developer agent for Foundry CLI project

## Description

﻿## Role Definition

**Role**: Tech Lead / Senior Python Developer  
**Project**: Foundry CLI Agentic Toolset — 21 Claude Code skills exposing 355 Palantir Foundry API v2 operations

## Context / Business Need

The Foundry CLI project has 23 DEV-STORYs. DEV-STORY-001 through DEV-STORY-004 implement the critical shared infrastructure layer (`_foundry_cli_common.py`), which all 20 namespace skills depend on. This layer includes:

- `ConfigLoader`, `AuthProvider`, `AsyncClientFactory` (DEV-STORY-001)
- `RetryHandler`, `ErrorSerializer`, `OutputFormatter`, `LogSetup` (DEV-STORY-002)
- `AccessControlGuard`, `PaginationHelper` (DEV-STORY-003)
- `BinaryDownloadHandler`, `SessionManager`, `TracingProvider` (DEV-STORY-004)

A Tech Lead is also required to execute the DESIGN sub-task (Grooming stage) and CODEREVIEW sub-task (Development stage) for all 23 DEV-STORYs. Without a Tech Lead, the Grooming stage cannot complete and no DEV-STORY can transition to Development.

No senior developer role is currently provisioned. The Architect role covers architecture but not hands-on implementation or code review at scale.

## Responsibilities

1. Implement DEV-STORY-001 through DEV-STORY-004: the complete shared infrastructure layer (`_foundry_cli_common.py`) including all common components (ConfigLoader, AuthProvider, AsyncClientFactory, RetryHandler, ErrorSerializer, OutputFormatter, LogSetup, AccessControlGuard, PaginationHelper, BinaryDownloadHandler, SessionManager, TracingProvider)
2. Execute all DESIGN sub-tasks across 23 DEV-STORYs during the Grooming stage: technical planning, effort estimation, and detailed implementation specifications
3. Execute all CODEREVIEW sub-tasks across 23 DEV-STORYs during the Development stage: review code quality, security, performance, and adherence to coding standards
4. Define and enforce coding standards and patterns for namespace skill implementations (tool schema, Pydantic models, async HTTP client usage)
5. Provide technical direction and mentoring to Python Developers executing namespace skill DEV and UNITTEST sub-tasks
6. Collaborate with Architect on architectural decisions and ADRs impacting implementation

## Required Skills

| Skill | Proficiency Level |
|---|---|
| Python 3.x | Expert |
| AsyncIO / aiohttp | Expert |
| CLI Framework Development (Click/Typer) | Advanced |
| REST API Client Development | Expert |
| Code Review & Quality Standards | Expert |
| Technical Leadership & Mentoring | Advanced |
| Testing (pytest, pytest-asyncio) | Advanced |
| Security Best Practices (OWASP Top-10) | Advanced |
| Git / GitHub Workflows | Advanced |

## Expected Deliverables

- Complete `_foundry_cli_common.py` shared infrastructure layer (DEV-STORY-001 to DEV-STORY-004)
- DESIGN sub-tasks (23 total) with technical planning, estimation, and implementation specs
- CODEREVIEW sub-tasks (23 total) with review comments and approval sign-off
- Coding standards document / architecture guidelines for namespace skill development

## References

- SAD-001: `.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md`
- DEV-STORY-001: Implement ConfigLoader, AuthProvider, AsyncClientFactory
- DEV-STORY-002: Implement RetryHandler, ErrorSerializer, OutputFormatter, LogSetup
- DEV-STORY-003: Implement AccessControlGuard, PaginationHelper
- DEV-STORY-004: Implement BinaryDownloadHandler, SessionManager, TracingProvider


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
