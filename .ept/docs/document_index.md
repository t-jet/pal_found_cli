# Project Documentation Index

## Documentation Structure

This project follows a structured documentation approach organized into logical folders:

```text
.ept/
└── docs/
    ├── customer_input/          # Original requirements and constraints from stakeholders
    │
    ├── deliverables/            # Project deliverables organized by discipline
    │   ├── requirements/        # Requirements analysis, specifications, and use cases
    │   ├── architecture/        # Architecture designs, decisions, and security assessments
    │   │   └── adr/            # Architecture Decision Records (ADRs)
    │   ├── development/         # Implementation plans and deployment guides
    │   └── work_instructions/   # Role-specific workflow and process guides
    │
    ├── resources/               # Agent and resource management
    │
    └── document_index.md        # This file - navigation hub for all documentation
```

---

## Customer Input Documents

- [Initial Task](customer_input/initial_task.md) - Core task description and basic requirements
- [Task Description / Requirements Completeness Assessment](customer_input/task_description.md) - Full requirements specification including all decisions resolved during Q&A
- [Open Questions — Round 1](customer_input/open_questions.md) - 25 questions across 6 domains; all answered
- [Open Questions — Round 2](customer_input/open_questions_2.md) - 12 follow-up questions on attribution, async, TOON stability; all answered
- [Open Questions — Round 3](customer_input/open_questions_3.md) - 10 critical/high/medium questions; all answered by Product Owner (QUESTION-001 Closed)

## Deliverables

### Requirements Documentation

- [SRS-001 — Software Requirements Specification](deliverables/business_analysis/SRS-001-foundry-cli.md) — Complete functional and non-functional requirements for the Foundry CLI Agentic Toolset. Status: Draft — Pending BA Sign-off. Traceable to FEATURE-001, BA-ANA-001, SA-ANA-001 and all 3 Q&A rounds.

### Architecture Documentation

- [SAD-001 — Solution Architecture Document](deliverables/architecture/SAD-001-foundry-cli.md) — Full architectural design including C4 L1–L4 diagrams, sequence flows, technology stack, deployment topology, and implementation roadmap (8 EPICs, 23 DEV-STORYs). Status: Draft.
- [DESIGN-012 — Foundry Language Models CLI](deliverables/architecture/DESIGN-012-language-models-cli.md) — Completed design for DEV-STORY-012 covering two inference operations, structured JSON inputs, write and Tier-3 controls, attribution restoration, B3 tracing, retry cost, privacy, tests, and packaging.
- [Canonical Environment Variable Reference](deliverables/architecture/canonical-env-var-reference.md) — Complete reference table for all environment variables used across the 21 CLI skills (500+ entries).
- [Metadata Allow-list](deliverables/architecture/metadata-allow-list.md) — Approved metadata field allow-list for the access control subsystem. Defines which dataset/object metadata fields may be exposed per access tier.

#### Architecture Decision Records (ADRs)

- [ADR-001 — Exit Code Taxonomy](deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md) — Defines the structured exit-code scheme for all CLI operations.
- [ADR-002 — Call Timeout Defaults](deliverables/architecture/adr/ADR-002-call-timeout-defaults.md) — Default and configurable timeout values for API calls.
- [ADR-003 — Streams Batch Strategy](deliverables/architecture/adr/ADR-003-streams-batch-strategy.md) — Batch vs. streaming approach for the `foundry-streams` namespace skill (17 operations).
- [ADR-004 — Format Auto-Selection Algorithm](deliverables/architecture/adr/ADR-004-format-auto-algorithm.md) — Rules for auto-selecting JSON vs. TOON output format based on response shape.
- [ADR-005 — Log Format](deliverables/architecture/adr/ADR-005-log-format.md) — Structured logging format for stderr output across all skills.
- [ADR-006 — .env File Search Path](deliverables/architecture/adr/ADR-006-env-file-search-path.md) — Search path order for `.env` file loading.
- [ADR-007 — Operation-Level READONLY Independence](deliverables/architecture/adr/ADR-007-operation-level-readonly.md) — Decision on per-operation READONLY flag independence from namespace-level control.

### Development Documentation

- **Common Error Handling Library** (`src/foundry_cli/common/`) — Shared infrastructure components implemented per DESIGN-001 and DEV-002:
  - `retry.py` — `RetryHandler`: Exponential backoff with jitter for retryable operations (ADR-002)
  - `error_serializer.py` — `ErrorSerializer`: Exception-to-exit-code mapping per ADR-001 taxonomy
  - `output_formatter.py` — `OutputFormatter`: JSON/TOON output with auto-selection per ADR-004 algorithm
  - `log_setup.py` — `LogSetup`: NDJSON structured logging to stderr per ADR-005

### CI/CD & Infrastructure (DEVOPS-003)

- **GitHub Actions CI Pipeline** (`.github/workflows/ci.yml`) — Six-stage pipeline: lint (ruff) → type-check (mypy) → test (pytest + coverage, Python 3.9–3.12 matrix) → security-scan (bandit + safety) → build (PEP 517) → All third-party actions pinned to full SHA digest (supply-chain integrity).
- **GitHub Actions Publish Pipeline** (`.github/workflows/publish.yml`) — Tag-triggered (`v*`) PyPI publication workflow with twine validation; uses `PYPI_API_TOKEN` from GitHub secrets.
- **Coverage Configuration** (`pyproject.toml` `[tool.coverage.*]`) — Branch coverage, 80% minimum threshold, XML output for CI reporting.
- **Environment Template** (`.env.example`) — Lists all required and optional environment variables per ADR-006 with inline documentation; `.env` is gitignored.
- **pyproject.toml** — Dependencies: `foundry-platform-python>=2.0.0`, `python-dotenv>=1.0.0`. Dev: pytest, pytest-asyncio, pytest-cov, mypy, ruff, bandit.
- [DEVOPS-011 - Foundry AIP Agents packaging and deployment report](deliverables/devops/DEVOPS-011-aip-agents-deployment-report.md) - Clean-archive build, wheel/editable installation, Python 3.11/3.12 gates, packaged policy, and rehearsed rollback evidence for DEV-STORY-011 at commit `4bc449c`.
- [DEVOPS-012 - Foundry Language Models packaging and deployment report](deliverables/devops/DEVOPS-012-language-models-deployment-report.md) - Clean-archive build, wheel/editable installation, Python 3.11/3.12 gates, blocked policy, and rehearsed rollback evidence for DEV-STORY-012 at commit `cb8e8d2`.

### Work Instructions (Team Member Guides)

(not yet introduced)

## Tools

(not yet introduced)

## Resources

- [Available Resources](resources/available_resources.md) - Registry of available agents and capabilities
- [Agent Definition Template](resources/agent_definition_template.md) - Template for defining new agent roles and capabilities

---

**Last Updated:** 2026-05-19
**Major Change:** Added CI/CD & Infrastructure documentation (DEVOPS-003): GitHub Actions CI pipeline (lint, type-check, test matrix, security scan, build), publish workflow, coverage configuration, `.env.example` template, and infrastructure dependencies in pyproject.toml.
