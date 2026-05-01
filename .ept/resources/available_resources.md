# Available Custom Agents Registry

Last Updated: January 18, 2026

## Human Stakeholders (Special Cases)

### Project Owner

**Type**: Human Stakeholder (NOT an AI agent)  
**Role**: Product Owner, Requirements Authority, Decision Maker  
**Identifier**: `project-owner`

**Important**: The Project Owner is a human and cannot be invoked like an agent. All interactions must go through the tracking system.

**How to Interact**:

1. **For Questions**: Create a `QUESTION` ticket with `addressed_to: project-owner`
   - Use when requirements are unclear or ambiguous
   - Use for approval requests (Feature definitions, architectural decisions, resource requests)
   - Use when business priorities need clarification
   - Project Owner will respond by updating the ticket with answers

2. **For Approvals**: Specific ticket types have approval stages where Project Owner review is required
   - Feature Requests in "Waiting for Approval" status
   - Resource Requests in "Pending Approval" status
   - Major architectural decisions requiring stakeholder sign-off

3. **Response Protocol**:
   - Question tickets addressed to project-owner will be answered by the human stakeholder
   - Check ticket status and comments for responses
   - Never assume or proceed without clarity - always create a Question ticket when uncertain

**Authority**:

- Final decision maker on feature priorities and business requirements
- Approves resource allocation and team composition changes
- Validates acceptance criteria and definition of done
- Provides domain expertise and business context

---

## Tracking System Agents

### Agent: Project Tracking Manager

**Name**: `tracking-mgr`  
**File**: `.github/agents/tracking-mgr.agent.md`  
**Status**: Active  
**Specialization**: Issue Tracking System Management, Quality Control, Status Reporting, Workflow Coordination

**Responsibilities**:

- Validate tracking system consistency and enforce standards
- Request ticket execution from appropriate team members
- Monitor workflow progression and identify blockers
- Generate status reports (weekly, epic progress, burndown data)
- Escalate Project Owner questions to expert
- Search tracking system and create ad-hoc reports
- Coordinate dependencies and track DoR/DoD compliance
- Maintain tracking system documentation

**Skills**:

- File System Navigation & Management: Expert
- Issue Tracking Workflows: Expert
- Data Validation & Quality Control: Advanced
- Report Generation & Analysis: Advanced
- Communication & Coordination: Advanced
- Markdown & CSV Manipulation: Advanced
- Requirements Interpretation: Advanced
- Search & Query Capabilities: Intermediate
- Agile Methodology: Intermediate

**Tools**: read, edit, search, agent, ditrix.ask-me-copilot-tool/*, malaksedarous.copilot-context-optimizer/*

**Handoffs**:

- Can request work from ALL agents (automatic)
- Can escalate questions to expert via ditrix ask tool

---

## Domain & Requirements Agents

## Organizational & Resource Management Agents

### Agent: Architect

**Name**: `Architect`  
**File**: `.github/agents/architect.agent.md`  
**Status**: Active  
**Specialization**: Solution Architecture, Business Analysis, Enterprise Development

**Responsibilities**:

- Analyze and document business requirements
- Design scalable, maintainable, and secure system architectures
- Plan implementation strategies and development roadmaps
- Guide development teams through implementation challenges
- Conduct code and architecture reviews
- Ensure adherence to best practices and coding standards
- **Evaluate task fit and delegate to specialized agents when appropriate**
- **Create resource requests when new specialized capabilities are needed**

**Skills**:

- Solution Architecture: Expert
- Business Analysis: Expert
- Python Development: Advanced
- Database Design: Advanced
- AI/ML Application Development: Advanced
- Security Best Practices: Advanced
- Technical Documentation: Expert
- Code Review: Expert
- Resource Delegation: Expert

**Tools**: read, search, fetch, githubRepo, usages, execute, edit, web, agent, terminal, LSP, todo

---

### Agent: HR (Agents Resource Manager)

**Name**: `HR`  
**File**: `.github/agents/hr.agent.md`  
**Status**: Active  
**Specialization**: Custom Agent Lifecycle Management, Requirements Analysis, Agent Registry

**Responsibilities**:

- Manage agent request index and track completion status
- Create and maintain agent registry documentation
- Process agent requirement specifications (including direct prompt requests)
- Design and create custom agent configurations
- Synchronize agent registry with actual agents folder
- Collaborate with Architect agent for clarifications

**Skills**:

- Requirements Analysis: Expert
- Documentation Management: Expert
- Agent Configuration: Expert
- Process Management: Expert
- Collaboration & Coordination: Advanced
- Quality Assurance: Advanced
- Handoff Orchestration: Expert

**Tools**: read, edit, search, agent

---

## Development & Engineering Agents

