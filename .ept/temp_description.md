---

# Approval Request: SRS-001

The Business Analyst has completed and formally signed off on **SRS-001** (Software Requirements Specification — Foundry CLI Agentic Toolset for Palantir Foundry API v2).

## Document Summary

- **Document ID**: SRS-001
- **Document Title**: Software Requirements Specification — Foundry CLI Agentic Toolset for Palantir Foundry API v2
- **Status**: Approved by BA (2026-05-02)
- **Location**: [SRS-001-foundry-cli.md](.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md)
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

## Acceptance Criteria

**Given** the Project Owner has received this approval request with links to all deliverable documents  
**When** the Project Owner reviews SRS-001 and provides an approval decision  
**Then** the decision must be one of: Approved, Approved with comments, or Rejected  
**And** any rejection must include specific concerns and required changes  
**And** any approval with comments must specify what follow-up actions are required  

## Related Documentation

### Primary Deliverable
- [SRS-001 — Software Requirements Specification](.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md)

### Supporting Architecture Documents
- [SAD-001 — Solution Architecture Document](.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md)
- [Canonical Environment Variable Reference](.ept/docs/deliverables/architecture/canonical-env-var-reference.md)
- [Metadata Allow-list](.ept/docs/deliverables/architecture/metadata-allow-list.md)

### Architecture Decision Records
- [ADR-001 — Exit Code Taxonomy](.ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md)
- [ADR-002 — Call Timeout Defaults](.ept/docs/deliverables/architecture/adr/ADR-002-call-timeout-defaults.md)
- [ADR-003 — Streams Batch Strategy](.ept/docs/deliverables/architecture/adr/ADR-003-streams-batch-strategy.md)
- [ADR-004 — Format Auto-Selection Algorithm](.ept/docs/deliverables/architecture/adr/ADR-004-format-auto-algorithm.md)
- [ADR-005 — Log Format](.ept/docs/deliverables/architecture/adr/ADR-005-log-format.md)
- [ADR-006 — .env File Search Path](.ept/docs/deliverables/architecture/adr/ADR-006-env-file-search-path.md)
- [ADR-007 — Operation-Level READONLY Independence](.ept/docs/deliverables/architecture/adr/ADR-007-operation-level-readonly.md)

### Source Requirements and Q&A
- [Initial Task](.ept/docs/customer_input/initial_task.md)
- [Task Description / Requirements Completeness Assessment](.ept/docs/customer_input/task_description.md)
- [Open Questions — Round 1](.ept/docs/customer_input/open_questions.md) (25 questions, all answered)
- [Open Questions — Round 2](.ept/docs/customer_input/open_questions_2.md) (12 questions, all answered)
- [Open Questions — Round 3](.ept/docs/customer_input/open_questions_3.md) (10 questions, all answered via QUESTION-001)

### Related Tickets
- **Parent Feature**: FEATURE-001 (Foundry CLI: Requirements Analysis and Open Questions)
- **BA Design Sub-Task**: BA-DES-001 (this request originates from BA-DES-001 Resolved stage)
- **SA Design Sub-Task**: SA-DES-001 (parallel work, in progress)
- **Previous Approval Request**: QUESTION-001 (Round 3 Open Questions, Closed 2026-04-10)

## Deadline

Please provide approval decision by: **2026-05-09** (7 days from BA sign-off)

## Notes

**BA Sign-off Summary**:
- All 60+ functional requirements traced to source customer input
- All 12 non-functional requirements validated for feasibility
- All 47 Q&A questions (3 rounds) incorporated into requirements
- Requirements internally consistent and unambiguous
- All acceptance criteria testable and measurable
- Implementation roadmap complete (8 EPICs, 23 DEV-STORYs)
- Requirements approved by BA as ready for implementation

**Next Steps Upon Approval**:
1. BA-DES-001 transitions to Closed
2. SA-DES-001 completes final architecture validation
3. FEATURE-001 transitions to Waiting for Implementation
4. Tech Lead begins implementation planning based on SRS-001

---
