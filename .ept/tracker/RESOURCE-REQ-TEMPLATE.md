# RESOURCE-REQ Template

Use this template when creating Resource/Agent Request tickets in the file-based issue tracking system.

**Folder Location**: `tracker/RESOURCE-REQ-XXX/` (where XXX is the sequential number from ID counter)

**Main File**: `resource-request.md`

---

## File Structure

### resource-request.md

````markdown
---
id: RESOURCE-REQ-001
type: resource-request
title: [Agent Name] - [Brief Role Description]
status: New
priority: Medium
resolution: null
created: 2026-01-11T12:00:00Z
updated: 2026-01-11T12:00:00Z
assignee: null
reporter: architect
component: resources
labels: []
due_date: null
---

# RESOURCE-REQ-001: [Agent Name] - [Brief Role Description]

## Role Definition

[Clear description of the agent's role and purpose. What problem does this agent solve? What domain expertise does it provide?]

**Example:**
This agent specializes in database query optimization and schema design for large-scale applications. The agent provides expert guidance on indexing strategies, query performance tuning, and database architecture decisions.

## Responsibilities

1. [Primary responsibility - the main function of this agent]
2. [Secondary responsibility - additional key function]
3. [Additional responsibilities as needed]

**Example:**
1. Analyze and optimize slow-running database queries
2. Design and review database schemas for performance and scalability
3. Provide guidance on indexing strategies and query execution plans
4. Review database-related code changes for performance implications
5. Recommend database technology choices based on use case requirements

## Required Skills

| Skill | Proficiency Level | Description |
|-------|-------------------|-------------|
| [Skill 1] | Expert/Advanced/Intermediate/Basic | [Why this proficiency level is needed] |
| [Skill 2] | Expert/Advanced/Intermediate/Basic | [Why this proficiency level is needed] |
| [Skill 3] | Expert/Advanced/Intermediate/Basic | [Why this proficiency level is needed] |

**Proficiency Level Definitions:**
- **Expert**: Deep mastery, can handle complex edge cases, provide guidance to others
- **Advanced**: Strong capability, handles most scenarios independently
- **Intermediate**: Solid foundation, may need guidance on complex scenarios
- **Basic**: Foundational understanding, requires support for advanced tasks

**Example:**
| Skill | Proficiency Level | Description |
|-------|-------------------|-------------|
| SQL Query Optimization | Expert | Must identify performance bottlenecks and recommend fixes for complex queries |
| Database Schema Design | Advanced | Should design normalized schemas with appropriate indexing strategies |
| Python | Intermediate | Needs to understand ORM patterns and query generation code |
| Databricks Unity Catalog | Advanced | Must understand catalog structure and security models |
| Performance Profiling | Advanced | Should analyze query execution plans and identify optimization opportunities |

## Expected Deliverables

- [Deliverable 1 - e.g., "Database query optimization recommendations"]
- [Deliverable 2 - e.g., "Performance analysis reports"]
- [Deliverable 3 - e.g., "Schema design documentation"]

**Example:**
- Query optimization reports with before/after performance metrics
- Database schema design documents with entity-relationship diagrams
- Index recommendation reports based on query patterns
- Performance tuning guidelines and best practices documentation
- Code review feedback on database-related implementations

## Special Requirements

[Any specific constraints, tools, integrations, or considerations needed for this agent]

**Examples:**
- Must have access to database connection tools
- Requires read-only access to production database metadata (not data)
- Should integrate with monitoring dashboards for query performance metrics
- Needs specialized MCP servers for database analysis
- Requires access to query execution plan visualization tools

**Example:**
This agent requires:
- Access to Databricks SQL API for query analysis
- Read access to Unity Catalog metadata
- Integration with query profiling tools
- Ability to execute EXPLAIN PLAN commands
- No access to PII or sensitive data (metadata only)

## Context

[Why this resource is needed now. What problem or gap does it address? What work cannot be completed without this agent?]

**Example:**
The current project requires extensive database optimization to meet performance requirements (15-second query response time). The existing team lacks deep expertise in Databricks-specific optimization techniques and Unity Catalog performance tuning. Without this specialized agent, the project risks missing performance targets and incurring significant refactoring costs later in development.

**Current Blockers:**
- EPIC-005 (Databricks Connector) needs query optimization guidance
- FEATURE-022 (Performance and Scalability) requires database performance expertise
- Multiple stories experiencing slow query performance in development environment

## Related Documentation

- [Available Resources Registry](../../.ept/docs/resources/available_resources.md)
- [Architecture Document](../../.ept/docs/deliverables/architecture/software_architecture_document.md)
- [Requirements Specification](../../.ept/docs/deliverables/requirements/requirements_specification.md)

---

## Comments

### Comment by architect on 2026-01-11T12:00:00Z

Created resource request for [Agent Name].

**Justification**: [Brief explanation of why this resource is critical]

**Expected Impact**: [What will improve once this resource is available]

**Timeline**: [When this resource is needed by]

---
````

### Optional: links.md (if related to specific tickets)

````markdown
# Links for RESOURCE-REQ-001

## Blocks (Tickets waiting for this resource)

- [EPIC-005](../EPIC-005/epic.md) - Databricks Connector optimization
- [FEATURE-022](../FEATURE-022/feature-request.md) - Performance and Scalability

## Relates To

- [ADR-003](../../docs/deliverables/architecture/adr/ADR-003-database-access-pattern.md) - Database Access Pattern
````

---

## Usage Workflow

### 1. Create Request

```bash
# Create folder
mkdir tracker/RESOURCE-REQ-001

# Create ticket file
# Copy template above and fill in all sections
```

### 2. Submit for Review

```yaml
# Update frontmatter
status: New → Under Review
assignee: hr-agent  # or architect
updated: <current-timestamp>
```

### 3. Review Process

**Architect Review:**

- Validates technical requirements
- Confirms skills and proficiency levels
- Checks for duplicate or overlapping resources
- Approves or requests clarification

**HR Agent Review:**

- Validates completeness of request
- Confirms deliverables are measurable
- Checks resource availability
- Creates agent if approved

### 4. Approval and Implementation

```yaml
# If approved
status: Under Review → Approved → In Progress
assignee: hr-agent
```

**Implementation Checklist:**

- [ ] Agent configuration created
- [ ] Skills and capabilities validated
- [ ] Handoffs configured for all relevant agents
- [ ] Agent registered in available_resources.md
- [ ] Documentation updated
- [ ] Requester notified

### 5. Completion

```yaml
# Mark as complete
status: In Progress → Resolved → Closed
resolution: Done
```

---

## Definition of Ready (DoR)

Before submitting request (status: New):

- [ ] Clear role definition provided
- [ ] Primary responsibilities listed (minimum 3)
- [ ] Required skills with proficiency levels specified
- [ ] Expected deliverables defined
- [ ] Context explaining why resource is needed
- [ ] Special requirements identified (tools, access, integrations)

## Definition of Done (DoD)

Before closing request (status: Closed):

- [ ] Agent/resource created and configured
- [ ] Skills and capabilities validated
- [ ] Handoffs configured for all relevant agents
- [ ] Resource registered in available_resources.md
- [ ] Documentation updated (if applicable)
- [ ] Requester notified of resource availability

---

## Status Transitions

```text
New → Under Review → Approved → In Progress → Resolved → Closed
                  ↘ Rejected (terminal)
```

**Status Definitions:**

- **New**: Request submitted, waiting for review
- **Under Review**: HR agent or Architect reviewing requirements
- **Approved**: Request approved, ready for implementation
- **In Progress**: Resource being created/configured
- **Resolved**: Resource ready and deployed
- **Closed**: Request fulfilled and archived
- **Rejected**: Request denied (not needed or infeasible)

---

## Best Practices

1. **Be Specific**: Clearly define the role and responsibilities
2. **Justify Need**: Explain the problem this resource solves
3. **Define Success**: Specify measurable deliverables
4. **Right-Size Skills**: Request appropriate proficiency levels
5. **Check Existing**: Review available_resources.md before requesting
6. **Link Blockers**: Reference tickets that are blocked by this resource
7. **Set Timeline**: Indicate urgency and when resource is needed

---

## Example: Database Specialist Request

See the example content in the template above for a complete sample of a Database Specialist agent request.

---

**For questions about resource requests, contact the HR agent or Solution Architect.**
