---
id: EPIC-004
type: epic
title: Admin & Security Skills
status: Open
created: 2026-04-13
updated: 2026-05-05
priority: High
assignee: architect
reporter: architect
---

# EPIC-004: Admin & Security Skills

## End-to-End Business Scenario

**Actor**: AI Agent (Claude or custom orchestrator) operating on behalf of a Foundry system administrator or security auditor

**Scenario**: Administrative Operations & Security Audit Lifecycle

### User Journey

1. **Stimulus**: Administrator agent receives a request to perform administrative operations (user management, group provisioning, permission audits, workspace configuration) or conduct security audits (access reviews, activity logging).

2. **Administrative Operations Path** (foundry-admin skill):
   - **User Management**: Query user details, list users by criteria, update user profiles, manage user status
   - **Group Management**: Create/update groups, manage group membership, query group hierarchies, handle nested groups
   - **Permission Management**: Grant/revoke permissions, audit permission assignments, validate access levels, manage role-based access
   - **Workspace Administration**: Configure workspace settings, manage workspace resources, handle workspace metadata
   - **Organization Management**: Query org structure, manage org-level settings, handle multi-tenant configurations
   - **Resource Provisioning**: Provision new resources, configure resource access, manage resource lifecycle
   
3. **Security Audit Path** (foundry-audit skill):
   - **Access Reviews**: Query access logs, identify permission assignments, validate authorization decisions
   - **Activity Auditing**: Retrieve audit trails, analyze user activities, generate compliance reports
   
4. **Output**: Agent receives structured administrative data or audit reports, enabling downstream analysis, compliance verification, or automated remediation actions.

5. **Quality Attributes**:
   - **Auditability**: All admin operations logged with actor, timestamp, and action details
   - **Security**: Access control guards prevent unauthorized administrative actions
   - **Reliability**: Retry logic handles transient API failures
   - **Traceability**: Structured errors with exit codes enable diagnostics
   - **Performance**: Pagination support for large result sets (user lists, audit logs)

### Business Value

This epic enables AI agents to perform enterprise-grade administrative and security audit operations on Foundry, supporting:
- **Automated Compliance**: Agents can audit permissions and generate compliance reports automatically
- **Self-Service Administration**: Agents can perform routine admin tasks (user provisioning, group management) without human intervention
- **Security Posture Management**: Agents can continuously monitor access patterns and identify anomalies
- **Operational Efficiency**: Reduces manual administrative overhead through agentic automation

## Technical Scope

- **DEV-STORY-009**: `foundry-admin` skill (66 operations covering user, group, permission, workspace, and organization management)
- **DEV-STORY-010**: `foundry-audit` skill (2 operations for access review and activity auditing)

## Implementation Context

- **Phase**: Phase 3 — Platform & Admin Skills (Sprint 5-6)
- **Priority**: High (foundry-admin), Medium (foundry-audit)
- **Dependencies**: Requires EPIC-001 (Core CLI Infrastructure) completed for shared common module (`_foundry_cli_common.py`) with ConfigLoader, AuthProvider, AccessControlGuard, RetryHandler, ErrorSerializer, OutputFormatter
- **Related Documentation**: SAD-001 §10 (Implementation Roadmap), SRS-001 (NFR-SEC, NFR-AUD requirements)

## Acceptance Criteria

- [ ] `foundry-admin` skill deployed with all 66 operations functional
- [ ] `foundry-audit` skill deployed with 2 audit operations functional
- [ ] Access control guards enforce READONLY restrictions per operation
- [ ] All operations support JSON and TOON output formats
- [ ] Pagination implemented for list operations (user lists, audit logs)
- [ ] Retry logic handles transient API failures (503, rate limits)
- [ ] Structured errors with exit codes per ADR-001
- [ ] Integration tests validate end-to-end administrative workflows
- [ ] Security audit operations capture required metadata for compliance reporting
- [ ] Documentation updated with admin/audit skill usage examples

## Related Documentation

- [SAD-001 — Solution Architecture Document](../.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md) §10 Implementation Roadmap
- [SRS-001 — Software Requirements Specification](../.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md) NFR-SEC, NFR-AUD
- [ADR-001 — Exit Code Taxonomy](../.ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md)
- [Canonical Environment Variable Reference](../.ept/docs/deliverables/architecture/canonical-env-var-reference.md)

## Notes

This epic is part of the overall Foundry CLI Agentic Toolset initiative (FEATURE-001) and represents one of 8 epics covering the 21 skill packages with 355 operations total.
