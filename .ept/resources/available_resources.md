# Available Custom Agents Registry

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

## Domain & Requirements Agents

### Agent: Business Analyst (BA)

**Name**: `ba`  
**File**: `.github/agents/ba.agent.md`  
**Status**: Active  
**Specialization**: Requirements Analysis, Acceptance Criteria Authoring, Business Design Documentation, Requirements Traceability

**Responsibilities**:

- Execute BA-DES sub-tasks under feature tickets: produce detailed business design specifications aligned to approved requirements documents
- Author and refine acceptance criteria in Given/When/Then (BDD) format for user stories and DEV-STORYs, ensuring full traceability to source requirements
- Review and validate DEV-STORY scope during Grooming: confirm scope boundaries, identify gaps, ensure acceptance criteria are testable and unambiguous
- Maintain requirements traceability matrices linking business requirements to user stories, acceptance criteria, and test cases
- Collaborate with Solution Architect to ensure alignment between business requirements and technical architecture
- Support QA with user acceptance testing criteria and assist with defect triage from a business perspective

**Skills**:

- Business Requirements Analysis: Expert
- User Story Writing (Given/When/Then): Expert
- Technical Writing & Documentation: Advanced
- Stakeholder Communication: Advanced
- Requirements Traceability: Advanced
- CLI / Developer Tooling Domain Knowledge: Intermediate
- Python/API Conceptual Understanding: Intermediate

**Tools**: vscode/memory, read, search, edit, agent, todo

---

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

## Organizational & Resource Management Agents

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

### Agent: Tech Lead / Senior Python Developer

**Name**: `tech-lead`
**File**: `.github/agents/tech-lead.agent.md`
**Status**: Active
**Specialization**: Python async CLI implementation, code review, technical design, shared infrastructure, coding standards

**Responsibilities**:

- Implement the shared infrastructure layer (`_foundry_cli_common.py`) — DEV-STORY-001 through DEV-STORY-004 (ConfigLoader, AuthProvider, AsyncClientFactory, RetryHandler, ErrorSerializer, OutputFormatter, LogSetup, AccessControlGuard, PaginationHelper, BinaryDownloadHandler, SessionManager, TracingProvider)
- Execute all DESIGN sub-tasks (23 total) during the Grooming stage: technical planning, effort estimation, and detailed implementation specifications
- Execute all CODEREVIEW sub-tasks (23 total) during the Development stage: review code quality, security, performance, and adherence to coding standards
- Define and enforce coding standards and patterns for namespace skill implementations (tool schema, Pydantic models, async HTTP client usage)
- Provide technical direction and mentoring to Python Developer agents executing namespace skill DEV and UNITTEST sub-tasks
- Collaborate with Architect on architectural decisions and ADRs impacting implementation

**Skills**:

- Python 3.x: Expert
- AsyncIO / aiohttp: Expert
- REST API Client Development: Expert
- Code Review & Quality Standards: Expert
- CLI Framework Development (Click/Typer): Advanced
- Testing (pytest, pytest-asyncio): Advanced
- Security Best Practices (OWASP Top-10): Advanced
- Technical Leadership & Mentoring: Advanced
- Git / GitHub Workflows: Advanced

**Tools**: execute, read, edit, search, agent, web, browser, pylance, lsp, python, todo

---

### Agent: Python Developer

**Name**: `python-developer`
**File**: `.github/agents/python-developer.agent.md`
**Status**: Active
**Specialization**: Namespace skill implementation, unit testing, defect resolution, async REST API client development

**Responsibilities**:

- Implement namespace skill Python files (DEV sub-tasks, one per namespace DEV-STORY from DEV-STORY-005 to DEV-STORY-023) following patterns established by the Tech Lead and approved architecture documentation
- Write unit test suites for all implemented namespace skills (UNITTEST sub-tasks), achieving minimum coverage thresholds defined in DESIGN specifications
- Fix defects identified in TESTEXEC sub-tasks and BUG-SUB tickets within agreed SLA
- Follow coding standards defined by the Tech Lead: tool schema structure, Pydantic model conventions, async HTTP client patterns, error handling, and logging
- Address CODEREVIEW feedback from the Tech Lead within the same sprint
- Self-review code against OWASP Top-10 security checklist before submitting for code review

**Skills**:

- Python 3.x: Advanced
- AsyncIO / aiohttp: Intermediate
- REST API Client Development: Advanced
- Testing (pytest, pytest-asyncio): Advanced
- Pydantic Data Validation: Intermediate
- Git / GitHub Workflows: Advanced
- CLI Tool Development: Intermediate
- OWASP Top-10 Security Awareness: Intermediate

**Tools**: execute, read, edit, search, agent, web, pylance, lsp, python, todo

---

## QA & Testing Agents

### Agent: QA Engineer

**Name**: `qa-engineer`
**File**: `.github/agents/qa-engineer.agent.md`
**Status**: Active
**Specialization**: Test case design, API test execution, defect management, QA sign-off for Foundry CLI Agentic Toolset

**Responsibilities**:

- Design TESTCASE sub-tasks for all 23 DEV-STORYs: test scenarios, input/output specifications, edge cases, negative cases, and boundary conditions for all Foundry API operations in scope
- Execute TESTEXEC sub-tasks: run tests against the target environment, validate actual vs. expected behavior, record pass/fail results with evidence
- Create BUG-SUB tickets for defects found during test execution, with full reproduction steps, expected vs. actual behavior, severity classification, and affected version
- Validate that all DEV-STORY acceptance criteria (Given/When/Then from SRS-001) are demonstrably met before issuing QA sign-off
- Maintain test coverage metrics across all 23 DEV-STORYs; flag coverage gaps proactively
- Collaborate with Tech Lead and Python Developer agents to resolve ambiguous acceptance criteria via QUESTION sub-tasks

**Skills**:

- QA/Testing Methodology: Expert
- Test Case Design & Documentation: Expert
- API Testing (REST/JSON): Advanced
- Python Scripting (test automation): Intermediate
- Defect Management & Bug Reporting: Expert
- Given/When/Then / BDD Testing: Advanced
- CLI Tool Testing: Intermediate
- Test Coverage Analysis: Advanced

**Tools**: execute, read, edit, search, agent, web, todo

---

## DevOps & Infrastructure Agents

### Agent: DevOps Engineer

**Name**: `devops-engineer`  
**File**: `.github/agents/devops-engineer.agent.md`  
**Status**: Active  
**Specialization**: CI/CD Pipeline Design, Python Packaging Infrastructure, DEVOPS Sub-task Execution, Secrets Management, Deployment Automation

**Responsibilities**:

- Design and implement GitHub Actions CI/CD workflows for the Foundry CLI source repository: lint (ruff/flake8), type checking (mypy), unit test execution (pytest/pytest-asyncio), security scanning (bandit/safety), and release publishing
- Execute DEVOPS sub-tasks for all 23 DEV-STORYs during the Deployment stage: deploy skill packages to target environments, verify successful operation via smoke tests, and document deployment results as ticket comments
- Configure Python packaging infrastructure: `pyproject.toml`, build system (poetry-core or hatchling), version tagging, changelog generation, and release publishing workflows
- Manage environment configuration and secrets: Foundry API token handling, `.env.example` templates, environment variable schemas, and GitHub Actions Secrets integration
- Establish rollback procedures and deployment health checks for each namespace skill deployment
- Collaborate with the Tech Lead on performance and scalability requirements relevant to deployment configuration

**Skills**:

- CI/CD Pipeline Design (GitHub Actions): Expert
- Python Packaging (poetry/setuptools/PyPI): Advanced
- Secrets Management & Environment Config: Advanced
- Docker / Containerization: Advanced
- Infrastructure as Code: Intermediate
- Git / Release Management: Expert
- Security Scanning (bandit, safety, SAST): Advanced
- Shell Scripting (Bash/PowerShell): Advanced
- Monitoring & Observability: Intermediate

**Tools**: execute, read, edit, search, agent, web, todo

---
