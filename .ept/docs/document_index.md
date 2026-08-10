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
- [DESIGN-005 — Binary Downloads, Sessions, and Tracing](deliverables/architecture/DESIGN-005-common-components.md) — Approved component contracts for bounded binary streaming, atomic session persistence, and SDK-native B3 propagation. Includes integration order, security controls, test matrix, and estimates.
- [DESIGN-008 — Foundry Functions CLI](deliverables/architecture/DESIGN-008-functions-cli.md) — Design for DEV-STORY-008 covering the 7-operation Functions namespace CLI, client routing, JSON arguments, tests, and packaging.
- [DESIGN-009 — Foundry Admin CLI](deliverables/architecture/DESIGN-009-admin-cli.md) — Design for DEV-STORY-009 covering the 66-operation Admin namespace CLI, security controls, pagination, JSON arguments, tests, and packaging.
- [DESIGN-010 — Foundry Audit CLI](deliverables/architecture/DESIGN-010-audit-cli.md) — Design for DEV-STORY-010 covering two Audit operations, exact-page pagination, bounded streamed log downloads, access control, B3 tracing, tests, and packaging.
- [DESIGN-011 — Foundry AIP Agents CLI](deliverables/architecture/DESIGN-011-aip-agents-cli.md) — Implementation-ready design for DEV-STORY-011 covering 15 SDK v2 operations, local session purge, aliases, exact-page pagination, eager-byte persistence, ACL, B3-only tracing, no-attribution behavior, tests, and packaging.
- [DESIGN-012 — Foundry Language Models CLI](deliverables/architecture/DESIGN-012-language-models-cli.md) — Completed design for DEV-STORY-012 covering two inference operations, structured JSON inputs, write and Tier-3 controls, attribution restoration, B3 tracing, retry cost, privacy, tests, and packaging.
- [DESIGN-013 — Foundry Models CLI](deliverables/architecture/DESIGN-013-models-cli.md) — Completed design for DEV-STORY-013 covering the 23-operation Models namespace CLI, nested client dispatch, cursor pagination, streamed downloads, ACL write classification, the 12/11 metadata-only policy, B3 tracing, no-attribution behavior, tests, and packaging.
- [DESIGN-014 — Foundry Orchestration CLI](deliverables/architecture/DESIGN-014-orchestration-cli.md) — Completed design for DEV-STORY-014 covering the 20-operation Orchestration namespace CLI, nested client dispatch (Build/Job/Schedule/ScheduleVersion/ScheduleRun), cursor pagination, the 12/8 metadata-only policy, B3 tracing, no-attribution behavior, tests, and packaging.
- [DESIGN-015 — Foundry SQL Queries CLI](deliverables/architecture/DESIGN-015-sql-queries-cli.md) — Completed design for DEV-STORY-015 covering the 5-operation SqlQueries namespace CLI, Arrow byte-result downloads, the 1/4 metadata-only policy, B3 tracing, no-attribution behavior, tests, and packaging.
- [DESIGN-016 — Foundry Streams CLI](deliverables/architecture/DESIGN-016-streams-cli.md) — Completed design for DEV-STORY-016 covering the 15-operation Streams namespace CLI (Dataset/Stream/Subscriber client paths), the ADR-003 batch-response pattern, the 3/12 metadata-only policy, B3 tracing, no-attribution behavior, tests, and packaging.
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
  - `access_control_guard.py` — `AccessControlGuard`: 8-step precedence access-control model and metadata allow-list (SRS §4.2 FR-ACL, ADR-007, exit code 8)
  - `pagination_helper.py` — `PaginationHelper`: page-size/page-token/batch-pages management with stderr metadata emission (SRS §4 FR-PAG, ADR-005)
- **Namespace Skill Scripts** (`.claude/skills/<namespace>/scripts/`) — CLI entry points that wire the common library into SDK operations per namespace:
  - `foundry-datasets/scripts/foundry_datasets_cli.py` — Datasets CLI (33 operations) integrating AccessControlGuard, PaginationHelper, RetryHandler, OutputFormatter, and ErrorSerializer

### CI/CD & Infrastructure (DEVOPS-002 / DEVOPS-003)

- **GitHub Actions CI Pipeline** (`.github/workflows/ci.yml`) — Six-stage pipeline: lint (ruff) → type-check (mypy) → test (pytest + coverage, Python 3.11/3.12 matrix) → security-scan (bandit + safety) → build (PEP 517). Third-party actions are pinned to full SHA digests.
- **GitHub Actions Publish Pipeline** (`.github/workflows/publish.yml`) — Tag-triggered (`v*`) PyPI publication workflow with twine validation; uses `PYPI_API_TOKEN` from GitHub secrets.
- **Coverage Configuration** (`pyproject.toml` `[tool.coverage.*]`) — Branch coverage, 80% repository-wide minimum threshold, XML output for CI reporting. DEVOPS-002 evidence on 2026-07-26 measured 81.65% with 262 tests passing; older 90% checklist wording is treated as aspirational/new-code guidance unless the quality standard is formally raised.
- **Environment Template** (`.env.example`) — Lists all required and optional environment variables per ADR-006 with inline documentation; `.env` is gitignored.
- **pyproject.toml** — Package metadata uses `README.md` as the PyPI long description. Runtime dependencies: `foundry-platform-sdk>=1.0.0`, `python-dotenv>=1.0.0`. Dev dependencies: pytest, pytest-asyncio, pytest-cov, mypy, ruff, bandit. Ruff per-file ignores are scoped to tests for import-order and intentionally unused test scaffolding patterns.
- [DEVOPS-010 - Foundry Audit packaging and deployment report](deliverables/devops/DEVOPS-010-deployment-report.md) - Clean-archive build, wheel/editable installation, entry-point smoke, security gates, and rehearsed rollback evidence for DEV-STORY-010 at commit `87d817c6`.
- [DEVOPS-011 - Foundry AIP Agents packaging and deployment report](deliverables/devops/DEVOPS-011-aip-agents-deployment-report.md) - Clean-archive build, wheel/editable installation, Python 3.11/3.12 gates, packaged policy, and rehearsed rollback evidence for DEV-STORY-011 at commit `4bc449c`.
- [DEVOPS-012 - Foundry Language Models packaging and deployment report](deliverables/devops/DEVOPS-012-language-models-deployment-report.md) - Clean-archive build, wheel/editable installation, Python 3.11/3.12 gates, blocked policy, and rehearsed rollback evidence for DEV-STORY-012 at commit `cb8e8d2`.
- [DEVOPS-013 - Foundry Models packaging and deployment report](deliverables/devops/DEVOPS-013-deployment-report.md) - Clean-archive build, wheel/editable installation, entry-point smoke, packaged 12/11 metadata policy, Python 3.11/3.12 gates, security gates, and rehearsed rollback evidence for DEV-STORY-013 at commit `bd13955`.
- [DEVOPS-014 - Foundry Orchestration packaging and deployment report](deliverables/devops/DEVOPS-014-deployment-report.md) - Clean-archive build, wheel/editable installation, entry-point smoke, packaged 12/8 metadata policy, Python 3.11/3.12 gates, security gates, and rehearsed rollback evidence for DEV-STORY-014 at commit `bd13955`.
- [DEVOPS-015 - Foundry SQL Queries packaging and deployment report](deliverables/devops/DEVOPS-015-deployment-report.md) - Clean-archive build, wheel/editable installation, entry-point smoke, packaged 1/4 metadata policy, Python 3.11/3.12 gates, security gates, and rehearsed rollback evidence for DEV-STORY-015 at commit `0c88063`.
- [DEVOPS-016 - Foundry Streams packaging and deployment report](deliverables/devops/DEVOPS-016-deployment-report.md) - Clean-archive build, wheel/editable installation, entry-point smoke, packaged 3/12 metadata policy, Python 3.11/3.12 gates, security gates, and rehearsed rollback evidence for DEV-STORY-016 at commit `0c88063`.

### QA Deliverables

- [TESTCASE-004 — AccessControlGuard and PaginationHelper QA Test Cases](deliverables/qa/TESTCASE-004-test-cases.md) — Test case design for DEV-STORY-003 covering ACL precedence, metadata-only allow-list behavior, pagination controls, stderr metadata, parser exposure, and smoke/environment labels.
- [TESTCASE-005 — Binary Downloads, Sessions, and Tracing QA Test Cases](deliverables/qa/TESTCASE-005-test-cases.md) — Test case design for DEV-STORY-004 covering bounded binary streaming, atomic session persistence, B3 tracing, retry-in-scope behavior, and error serialization.
- [TESTEXEC-005 — Binary Downloads, Sessions, and Tracing Test Execution Log](deliverables/qa/TESTEXEC-005-execution-log.md) — Execution evidence for DEV-STORY-004 targeted suites; 95/95 tests passed on 2026-07-28.
- [TESTCASE-006 — Foundry Ontologies CLI QA Test Cases](deliverables/qa/TESTCASE-006-test-cases.md) — Test case design for DEV-STORY-007 covering the 67-operation ontology catalog, parser, dispatch, pagination, binary upload/download, ACL, retry, error serialization, JSON/TOON output, console entry point, and B3-only tracing.
- [TESTEXEC-006 — Foundry Ontologies CLI Test Execution Log](deliverables/qa/TESTEXEC-006-execution-log.md) — Execution evidence for DEV-STORY-007 targeted ontology suite; 184/184 targeted tests passed on clean committed HEAD `19c297b`, with separate green full-suite archive and local-worktree counts documented.
- [TESTCASE-007 — Foundry Filesystem CLI QA Test Cases](deliverables/qa/TESTCASE-007-test-cases.md) — Test case design for DEV-STORY-006 covering the 31-operation filesystem catalog, parser, dispatch, nested Resource.Role routing, pagination, ACL, exit codes, output formats, console entry point, and `.claude` skill launcher.
- [TESTEXEC-007 — Foundry Filesystem CLI Test Execution Log](deliverables/qa/TESTEXEC-007-execution-log.md) — Execution evidence for DEV-STORY-006 targeted filesystem tests and full regression suite; 586/586 tests passed with 81.96% coverage on 2026-07-29.
- [TESTCASE-008 — Foundry Functions CLI QA Test Cases](deliverables/qa/TESTCASE-008-test-cases.md) — Test case design for DEV-STORY-008 covering the 7-operation functions catalog, parser, dispatch, JSON arguments, boolean flags, FUNCTIONS ACL namespace, output formats, byte streaming response envelope, exit codes, console entry point, and `.claude` skill launcher.
- [TESTEXEC-008 — Foundry Functions CLI Test Execution Log](deliverables/qa/TESTEXEC-008-execution-log.md) — Execution evidence for DEV-STORY-008 targeted functions tests, packaging checks, help checks, and full regression suite; 622/622 tests passed with 81.75% coverage on 2026-07-29.
- [TESTCASE-009 — Foundry Admin CLI QA Test Cases](deliverables/qa/TESTCASE-009-test-cases.md) — Test case design for DEV-STORY-009 covering the 66-operation admin catalog, parser, SDK routing, JSON arguments, ACL, pagination, byte handling, packaging, and regression checks.
- [TESTCASE-010 — Foundry Audit CLI QA Test Cases](deliverables/qa/TESTCASE-010-test-cases.md) — Test case design for DEV-STORY-010 covering both Audit operations, exact-page pagination, bounded streamed downloads, ACL precedence, ADR exit codes, B3 transport, packaging, and regression checks.
- [TESTEXEC-010 — Foundry Audit CLI Test Results](deliverables/qa/TESTEXEC-010-test-results.md) — Execution evidence for DEV-STORY-010: all 26 QA cases passed, with 83 targeted tests, 933 full-suite tests on Python 3.11 and 3.12, 82.66% branch coverage, and clean static, security, compile, and packaging gates.
- [TESTCASE-013 — Foundry Models CLI QA Test Cases](deliverables/qa/TESTCASE-013-test-cases.md) — Test case design for DEV-STORY-013 covering all 23 foundry-models operations: exact catalog and nested routing, JSON validation, four cursor-paged commands, service slicing, three streamed downloads, ACL write classification, the 12/11 metadata-only policy, B3 tracing, retry, output, privacy, packaging, and regression gates.
- [TESTCASE-014 — Foundry Orchestration CLI QA Test Cases](deliverables/qa/TESTCASE-014-test-cases.md) — Test case design for DEV-STORY-014 covering all 20 foundry-orchestration operations across Build, Job, Schedule, ScheduleVersion, and ScheduleRun client paths: exact catalog, nested routing, three cursor-paged commands, single-call batches, the 8-operation write set, the 12/8 metadata-only policy, B3 tracing, retry, output, privacy, packaging, and regression gates.
- [TESTCASE-015 — Foundry SQL Queries CLI QA Test Cases](deliverables/qa/TESTCASE-015-test-cases.md) — Test case design for DEV-STORY-015 covering all 5 foundry-sql-queries operations through the single SqlQuery client path (cancel, execute, execute_ontology, get_results, get_status): exact catalog, nested routing, JSON validation, bounded Arrow byte-result downloads, the 3-operation write set, the 1/4 metadata-only policy, B3 tracing, retry, output, privacy, packaging, and regression gates.
- [TESTCASE-016 — Foundry Streams CLI QA Test Cases](deliverables/qa/TESTCASE-016-test-cases.md) — Test case design for DEV-STORY-016 covering all 15 foundry-streams operations (Dataset 1, Stream 7, Subscriber 7; corrected from the stale 17-operation count): exact catalog, nested routing, JSON validation, the ADR-003 batch-read pattern with bounded --max-records, the 10-operation write set including reset classification, the 3/12 metadata-only policy, streams timeout, B3 tracing, retry, output, privacy, packaging, and regression gates.
- [TESTEXEC-016 — Foundry Streams CLI Execution Log](deliverables/qa/TESTEXEC-016-execution-log.md) — Execution evidence for DEV-STORY-016: all 24 QA cases passed (STR-TC-001..024), 57 focused SQL+Streams tests, 1148 full-suite tests, 86.06% branch coverage (streams 90%), and clean static, compile, and packaging gates on 2026-08-10. No defects opened.
- [TESTEXEC-013 — Foundry Models CLI Execution Log](deliverables/qa/TESTEXEC-013-execution-log.md) — Execution evidence for DEV-STORY-013: all 28 QA cases passed (MDL-TC-001..028), 33 focused Models tests, 1089 full-suite tests, 85.50% branch coverage, and clean static, compile, and packaging gates on 2026-08-10. No defects opened.
- [TESTEXEC-014 — Foundry Orchestration CLI Execution Log](deliverables/qa/TESTEXEC-014-execution-log.md) — Execution evidence for DEV-STORY-014: all 23 QA cases passed (ORC-TC-001..023), 32 focused Orchestration tests, 1089 full-suite tests, 85.50% branch coverage, and clean static, compile, and packaging gates on 2026-08-10. No defects opened.
- [TESTEXEC-015 — Foundry SQL Queries CLI Execution Log](deliverables/qa/TESTEXEC-015-execution-log.md) — Execution evidence for DEV-STORY-015: all 22 QA cases passed (SQL-TC-001..022), 57 focused SQL+Streams tests, 1148 full-suite tests, 86.06% branch coverage (sql_queries 89%), and clean static, compile, and packaging gates on 2026-08-10. No defects opened.

### Work Instructions (Team Member Guides)

(not yet introduced)

## Tools

(not yet introduced)

## Resources

- [Available Resources](resources/available_resources.md) - Registry of available agents and capabilities
- [Agent Definition Template](resources/agent_definition_template.md) - Template for defining new agent roles and capabilities

---

**Last Updated:** 2026-08-10
**Architecture Change:** SAD-001 DEV-STORY-007 ontology scope corrected from 55 to 67 operations to match the approved allow-list.
**Major Change:** Added DEVOPS-015-deployment-report.md and DEVOPS-016-deployment-report.md — packaging and deployment verification evidence for DEV-STORY-015/016 (foundry-sql-queries and foundry-streams CLIs) at commit `0c88063`: clean-archive build, wheel/editable install, entry-point smoke, packaged metadata policies (1/4 and 3/12), Python 3.11/3.12 gates (1148 passed, 86.06% branch), security gates, and rehearsed rollback (2026-08-10).
