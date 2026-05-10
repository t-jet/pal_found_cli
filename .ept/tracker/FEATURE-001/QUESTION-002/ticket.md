---
id: QUESTION-002
type: question
title: 'Approval Request: SRS-001 (Software Requirements Specification for Foundry CLI)'
status: Closed
addressed_to: project-owner
created: 2026-05-02
updated: 2026-05-05
priority: Critical
reporter: ba
---

# QUESTION-002: Approval Request: SRS-001 (Software Requirements Specification for Foundry CLI)

## Description

﻿# Approval Request: SRS-001

The Business Analyst has completed and formally signed off on **SRS-001** (Software Requirements Specification — Foundry CLI Agentic Toolset for Palantir Foundry API v2).

## Document Summary

- **Document ID**: SRS-001
- **Status**: Approved by BA (2026-05-02)
- **Location**: `.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md`
- **Size**: ~1000 lines (9 comprehensive sections)

## Scope Overview

**Functional Requirements**: 60+ requirements covering:
- Authentication (UserTokenAuth, env vars)
- Output format (JSON/TOON auto-selection)
- Async client with timeouts
- Pagination (per-page and batch modes)
- Error handling and retry (exponential backoff)
- Binary downloads (1.5 MB default limit, integrity checks)
- Session management (AIP Agents, 7-day TTL)
- Attribution and tracing (opt-in)
- Skill packaging (21 Claude Code skills)

**Non-Functional Requirements**: 12 NFRs covering:
- Platform compatibility (Python 3.11/3.12, Windows/macOS/Linux)
- Distribution model (file copy, no package registry)
- CLI interface contract (exit codes, stdout/stderr separation)
- Maintainability (single-source common module)

**Access Control**: Complete 3-tier model (Full / Read-only / Metadata-only) with 8-step precedence

**Configuration**: Comprehensive taxonomy (20+ core vars, 415+ namespace/operation vars)

**Traceability**: All requirements traced to Initial Task and 47 Q&A questions across 3 rounds

**Implementation Artifacts**: 8 EPICs (EPIC-001 through EPIC-008), 23 DEV-STORYs (DEV-STORY-001 through DEV-STORY-023)

## Key Decisions Documented

1. **Authentication**: UserTokenAuth only (no OAuth2/OIDC)
2. **Output Format**: Auto-selection algorithm for JSON vs TOON (ADR-004)
3. **Access Control**: 3-tier model with 8-step precedence, deny-by-default metadata allow-list
4. **Binary Downloads**: 1.5 MB default limit, partial write with truncation flag
5. **Session Management**: Named aliases, 7-day TTL, 5-session warning threshold
6. **Exit Code Taxonomy**: Structured exit codes per ADR-001
7. **Distribution**: File copy only, self-contained skills with copied common module

## Approval Request

**Question**: Do you approve SRS-001 as the authoritative requirements specification for the Foundry CLI Agentic Toolset project?

**Required Response**: 
- ✅ **Approved** — Proceed with implementation per SRS-001
- ⚠️ **Approved with comments** — Approval granted; address comments in follow-up
- ❌ **Rejected** — Specify concerns and required changes

**Impact of Approval**: 
Approval authorizes the development team to proceed with implementation of all 8 EPICs and 23 DEV-STORYs based on SRS-001 requirements. Any changes to requirements after approval will require formal change control.

## Related Tickets

- Parent Feature: FEATURE-001
- BA Design Sub-Task: BA-DES-001 (this request originates from BA-DES-001 Resolved stage)
- SA Design Sub-Task: SA-DES-001 (parallel work, in progress)

## Deadline

Please provide approval decision by: **2026-05-09** (7 days from sign-off)

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
