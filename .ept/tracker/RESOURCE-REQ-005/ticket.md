---
id: RESOURCE-REQ-005
type: resource_req
title: Provision DevOps Engineer agent for Foundry CLI packaging and deployment pipeline
status: Closed
reporter: architect
created: 2026-05-01
updated: 2026-05-01
priority: High
resolution: Fulfilled
assignee: hr
---

# RESOURCE-REQ-005: Provision DevOps Engineer agent for Foundry CLI packaging and deployment pipeline

## Description

﻿## Role Definition

**Role**: DevOps Engineer  
**Project**: Foundry CLI Agentic Toolset — 21 Claude Code skills exposing 355 Palantir Foundry API v2 operations

## Context / Business Need

Each of the 23 DEV-STORYs includes a DEVOPS sub-task in the Deployment stage. A DEV-STORY cannot be marked Resolved without DEVOPS sub-task completion. The DevOps Engineer is responsible for CI/CD pipeline setup, Python package distribution infrastructure, and environment configuration.

The project structure requires:
- A `pyproject.toml`/packaging configuration for distribution as a Claude Code MCP toolset
- CI/CD automation for testing, linting, security scanning, and release publishing
- Integration with Palantir Foundry authentication infrastructure (token management, environment configuration)
- Potential containerization for isolated test environments

No DevOps Engineer role is currently provisioned. Without one, all 23 DEV-STORYs will stall at the Deployment stage.

## Responsibilities

1. Design and implement the CI/CD pipeline (GitHub Actions) to automate: linting (ruff/flake8), type checking (mypy), unit test execution (pytest), security scanning (bandit/safety), and package builds
2. Execute DEVOPS sub-tasks for all 23 DEV-STORYs during the Deployment stage: deploy skill updates, verify successful operation in the target environment, and document deployment results
3. Configure Python packaging infrastructure: `pyproject.toml`, `poetry` or `setuptools` build system, release publishing workflow (version tagging, changelog generation)
4. Manage environment configuration and secrets: Foundry API token handling, environment variable schemas, `.env` templates, and integration with secrets managers
5. Establish rollback procedures and deployment health checks for each namespace skill deployment
6. Collaborate with Tech Lead on performance and scalability requirements relevant to deployment configuration

## Required Skills

| Skill | Proficiency Level |
|---|---|
| CI/CD Pipeline Design (GitHub Actions) | Expert |
| Python Packaging (poetry/setuptools/PyPI) | Advanced |
| Secrets Management & Environment Config | Advanced |
| Docker / Containerization | Advanced |
| Infrastructure as Code | Intermediate |
| Git / Release Management | Expert |
| Security Scanning (bandit, safety, SAST) | Advanced |
| Shell Scripting (Bash/PowerShell) | Advanced |
| Monitoring & Observability | Intermediate |

## Expected Deliverables

- GitHub Actions CI/CD pipeline (`.github/workflows/`) covering lint, test, security scan, and publish stages
- `pyproject.toml` with full packaging configuration (dependencies, entry points, metadata)
- Environment configuration templates (`.env.example`, configuration schema documentation)
- DEVOPS sub-tasks (23 total): deployment execution records for each DEV-STORY
- Release runbook and rollback procedures

## References

- SAD-001: `.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md` (Technology Stack section, ADR-002 Claude Code skill packaging)
- All 23 DEV-STORY tickets (deployment targets)


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
