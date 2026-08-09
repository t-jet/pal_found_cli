---
id: EPIC-001
type: epic
title: Core CLI Infrastructure
status: Done
created: 2026-04-13
updated: 2026-07-30
priority: Critical
resolution: Done
assignee: architect
reporter: architect
---

# EPIC-001: Core CLI Infrastructure

## Description

Implement the shared `_foundry_cli_common.py` module — the single source of truth for all 21 namespace CLI skills. This module provides the foundational infrastructure for authentication, configuration, error handling, output formatting, access control, pagination, session management, and tracing.

This epic represents Phase 1 (Sprint 1-2) of the implementation roadmap defined in SAD-001 and is Critical priority as all subsequent namespace skills depend on this infrastructure.

## Acceptance Criteria

### Functional Requirements
- [ ] `_foundry_cli_common.py` module implemented with all required components
- [ ] ConfigLoader: Load and validate configuration from .env file and environment variables (per ADR-006)
- [ ] AuthProvider: Handle OAuth2 token acquisition and validation
- [ ] AsyncClientFactory: Create configured foundry-platform-python SDK client instances
- [ ] RetryHandler: Implement exponential backoff with configurable timeout defaults (per ADR-002)
- [ ] ErrorSerializer: Structured error output with typed exit codes (per ADR-001)
- [ ] OutputFormatter: Support both JSON and TOON output formats with auto-selection algorithm (per ADR-004)
- [ ] LogSetup: Structured logging to stderr (per ADR-005)
- [ ] AccessControlGuard: Implement 8-step precedence evaluation (per SAD-001 §9.2)
- [ ] PaginationHelper: Handle multi-page API responses
- [ ] BinaryDownloadHandler: Stream large binary responses efficiently
- [ ] SessionManager: Manage session state files for stateful operations
- [ ] TracingProvider: Optional distributed tracing support

### Non-Functional Requirements
- [ ] All 4 linked Developer Stories (DEV-STORY-001 through DEV-STORY-004) reach Closed status
- [ ] Unit tests achieve ≥80% code coverage
- [ ] Integration tests cover all public interfaces
- [ ] Module conforms to Python 3.11+ type hints
- [ ] No external dependencies beyond foundry-platform-python SDK and toon-python library
- [ ] Performance: Configuration load <50ms, auth token acquisition <200ms
- [ ] Security: No credentials logged or written to stdout

### Documentation Requirements
- [ ] API documentation generated from docstrings
- [ ] Usage examples provided for each major component
- [ ] Deployment guide updated with installation instructions
- [ ] All ADRs (ADR-001 through ADR-007) rationale verified in implementation

## Related Documentation

### Requirements & Architecture
- [SRS-001 — Software Requirements Specification](.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md) — FR-SKILL-2, NFR-DIST-2, NFR-MAINT-1
- [SAD-001 — Solution Architecture Document](.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md) — §10 Implementation Roadmap (Phase 1)
- [Canonical Environment Variable Reference](.ept/docs/deliverables/architecture/canonical-env-var-reference.md)

### Architecture Decision Records
- [ADR-001 — Exit Code Taxonomy](.ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md)
- [ADR-002 — Call Timeout Defaults](.ept/docs/deliverables/architecture/adr/ADR-002-call-timeout-defaults.md)
- [ADR-004 — Format Auto-Selection Algorithm](.ept/docs/deliverables/architecture/adr/ADR-004-format-auto-algorithm.md)
- [ADR-005 — Log Format](.ept/docs/deliverables/architecture/adr/ADR-005-log-format.md)
- [ADR-006 — .env File Search Path](.ept/docs/deliverables/architecture/adr/ADR-006-env-file-search-path.md)

## Notes

**Dependencies**: None — this is the foundational epic that all other epics depend on.

**Linked Stories**: This epic comprises 4 developer stories:
- DEV-STORY-001: ConfigLoader, AuthProvider, AsyncClientFactory (Critical)
- DEV-STORY-002: RetryHandler, ErrorSerializer, OutputFormatter, LogSetup (Critical)
- DEV-STORY-003: AccessControlGuard, PaginationHelper (Critical)
- DEV-STORY-004: BinaryDownloadHandler, SessionManager, TracingProvider (High)

**Technical Constraints**:
- Must be compatible with foundry-platform-python SDK (version TBD during implementation)
- Must support toon-python library >=0.9,<1.0
- Must be copyable to each namespace skill directory (single-file distribution model per NFR-DIST-2)
- Must have zero runtime dependencies beyond SDK and toon library

**Risk Mitigation** (from SAD-001 §11):
- TOON library API breaks: Version pin >=0.9,<1.0; fallback to JSON on TOON failure
- SDK update breaks CLI: SDK version locked in-repo; explicit review required for upgrades
