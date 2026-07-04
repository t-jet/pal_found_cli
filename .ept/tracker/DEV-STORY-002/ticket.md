---
id: DEV-STORY-002
type: dev_story
title: Implement RetryHandler, ErrorSerializer, OutputFormatter, LogSetup
status: Blocked
feature_request: FEATURE-001
epic: EPIC-001
created: 2026-04-13
updated: 2026-07-04
priority: Critical
assignee: architect
reporter: architect
release_notes: Implementation of RetryHandler (exponential backoff with jitter for HTTP 429/503), ErrorSerializer (SDK exception to exit code mapping per ADR-001), OutputFormatter (JSON/TOON auto-selection per ADR-004), and LogSetup (NDJSON structured logging to stderr per ADR-005). Exit codes 5 (TimeoutError), 6 (ServerError), 7 (RateLimitExhausted) implemented per ADR-001. All error output as JSON on stdout regardless of --format setting.
---

﻿# DEV-STORY-002: Implement RetryHandler, ErrorSerializer, OutputFormatter, LogSetup

## Description

Implement four critical components of the `_foundry_cli_common.py` module that handle resilience, error handling, output formatting, and observability for all CLI operations:

### Components

1. **RetryHandler**: Exponential back-off retry logic with jitter for transient failures (HTTP 429, 503)
   - Configurable via `FOUNDRY_AGENTIC_CLI_RETRY_*` environment variables
   - Wraps SDK async calls in `asyncio.wait_for()` with configurable timeout (ADR-002)
   - Implements exponential backoff: delay_ms = initial_delay * (multiplier ^ attempt) + jitter
   - Logs retry attempts to stderr using structured JSON format (ADR-005)

2. **ErrorSerializer**: Maps SDK exceptions to structured JSON error envelopes and typed exit codes
   - Implements exit code taxonomy per ADR-001 (codes 0-9)
   - Maps `foundry-platform-python` SDK exceptions to exit codes
   - Emits all errors as JSON to stdout regardless of `--format` setting
   - Error schema: `{type, message, http_status, details, attempt, operation, call_id}`

3. **OutputFormatter**: Intelligent output format selection and rendering
   - Implements format auto-selection algorithm per ADR-004
   - Supports JSON, TOON, and auto modes via `--format` flag or `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT`
   - TOON selection rule: uniform array of dicts → TOON; all other cases → JSON
   - Integrates with `toon-python >=0.9,<1.0` library
   - Emits primary result to stdout; pagination metadata to stderr

4. **LogSetup**: Structured JSON logging configuration
   - Configures Python `logging` with NDJSON formatter directed to stderr (ADR-005)
   - Log level control via `FOUNDRY_AGENTIC_CLI_LOG_LEVEL` (default: WARNING)
   - Log record schema: `{ts, level, logger, msg, op, call_id, attempt, delay_ms, ...}`
   - Metadata separator: `# ---metadata-start---` precedes metadata JSON on stderr

## Acceptance Criteria

### RetryHandler (FR-ERR-3, FR-ERR-4, FR-ASYNC-3, ADR-002)

- [ ] Implements exponential backoff retry for HTTP 429 and 503 responses
- [ ] Configurable via environment variables:
  - `FOUNDRY_AGENTIC_CLI_RETRY_INITIAL_DELAY_MS` (default: 500ms)
  - `FOUNDRY_AGENTIC_CLI_RETRY_MAX_DELAY_MS` (default: 8000ms)
  - `FOUNDRY_AGENTIC_CLI_RETRY_MULTIPLIER` (default: 2.0)
  - `FOUNDRY_AGENTIC_CLI_RETRY_MAX_ATTEMPTS` (default: 4)
- [ ] Adds random jitter (±10%) to prevent thundering herd
- [ ] Wraps SDK calls in `asyncio.wait_for()` with timeout from `FOUNDRY_AGENTIC_CLI_TIMEOUT_S` (default: 30s)
- [ ] Logs retry attempts to stderr with structured JSON format
- [ ] Returns structured error JSON on timeout (exit code 5)
- [ ] Respects `SIGINT`/`SIGTERM` signals and cancels operations gracefully

### ErrorSerializer (FR-ERR-1, FR-ERR-2, FR-ERR-5, ADR-001)

- [ ] Maps all SDK exceptions to exit codes 0-9 per ADR-001 taxonomy:
  - 0: Success
  - 1: UserInputError (invalid CLI args, validation failure)
  - 2: AuthenticationError (missing/invalid FOUNDRY_TOKEN)
  - 3: PermissionDeniedError (HTTP 403)
  - 4: NotFoundError (HTTP 404)
  - 5: TimeoutError (asyncio timeout, SIGINT/SIGTERM)
  - 6: ServerError (HTTP 5xx excluding 503)
  - 7: RateLimitExhausted (HTTP 429, max retries exhausted)
  - 8: AccessControlError (blocked by CLI access control)
  - 9: ConfigurationError (missing required env var)
- [ ] Emits JSON error envelope to stdout with fields: `{error: {type, message, http_status, details, attempt, operation, call_id}}`
- [ ] All errors emitted as JSON regardless of `--format` setting
- [ ] Includes retry attempt number in error output
- [ ] Handles SDK `PalantirRPCException` subclasses and Python built-in exceptions

### OutputFormatter (FR-OUT-1 through FR-OUT-7, ADR-004)

- [ ] Implements format auto-selection algorithm per ADR-004:
  1. Explicit format (json/toon) always wins
  2. Errors always use JSON
  3. Non-list top-level always uses JSON
  4. Empty list uses JSON
  5. Extract field sets from all items
  6. Any non-dict item → JSON
  7. All items share identical field set → TOON; otherwise → JSON
- [ ] Supports `--format json|toon|auto` CLI argument
- [ ] Respects `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT` environment variable (default: auto)
- [ ] Integrates with `toon-python` library for TOON rendering
- [ ] Emits primary result data to stdout
- [ ] Emits pagination metadata to stderr as compact JSON (with `# ---metadata-start---` separator)
- [ ] Binary download envelopes always use JSON (never TOON)
- [ ] Fallback to JSON if TOON library fails

### LogSetup (NFR-IFACE-2, ADR-005)

- [ ] Configures Python `logging` module with custom JSON formatter
- [ ] Directs all logs to stderr
- [ ] Implements NDJSON format (newline-delimited JSON)
- [ ] Log record schema includes required fields: `{ts, level, logger, msg}`
- [ ] Log record includes optional context fields: `{op, call_id, attempt, delay_ms, access_decision, http_status}`
- [ ] ISO 8601 timestamps in UTC
- [ ] Log level control via `FOUNDRY_AGENTIC_CLI_LOG_LEVEL` (default: WARNING)
- [ ] Supported levels: DEBUG, INFO, WARNING, ERROR
- [ ] Metadata separator `# ---metadata-start---` precedes metadata JSON object

### Integration & Quality

- [ ] All four components integrated into `_foundry_cli_common.py` module
- [ ] Unit tests achieve ≥80% code coverage
- [ ] Integration tests verify correct interaction between components
- [ ] Type hints compatible with Python 3.11+
- [ ] No external dependencies beyond `foundry-platform-python` SDK and `toon-python`
- [ ] Performance: error serialization <5ms, format selection <10ms, log setup <10ms

## Related Documentation

### Requirements
- [SRS-001 §3.5 (FR-ERR)](../../deliverables/business_analysis/SRS-001-foundry-cli.md#fr-err-error-handling) — Error handling requirements
- [SRS-001 §3.2 (FR-OUT)](../../deliverables/business_analysis/SRS-001-foundry-cli.md#fr-out-output-format) — Output format requirements
- [SRS-001 §3.3 (FR-ASYNC)](../../deliverables/business_analysis/SRS-001-foundry-cli.md#fr-async-async-client) — Async client requirements
- [SRS-001 §6.2 (NFR-IFACE-2)](../../deliverables/business_analysis/SRS-001-foundry-cli.md#nfr-iface-interface-standards) — Structured logging requirement

### Architecture
- [SAD-001 §4 (Component Diagram)](../../deliverables/architecture/SAD-001-foundry-cli.md#4-c4-level-3--component-diagram-common-module) — Component interaction design
- [SAD-001 §6.2 (Retry Sequence)](../../deliverables/architecture/SAD-001-foundry-cli.md#62-retry-on-429) — Retry behavior sequence diagram

### Architecture Decision Records
- [ADR-001 — Exit Code Taxonomy](../../deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md) — Exit code mapping (0-9)
- [ADR-002 — Call Timeout Defaults](../../deliverables/architecture/adr/ADR-002-call-timeout-defaults.md) — Timeout configuration (30s default)
- [ADR-004 — Format Auto-Selection Algorithm](../../deliverables/architecture/adr/ADR-004-format-auto-algorithm.md) — TOON vs JSON selection logic
- [ADR-005 — Log Format](../../deliverables/architecture/adr/ADR-005-log-format.md) — NDJSON structured logging format

## Notes

**Dependencies:**
- Depends on DEV-STORY-001 (ConfigLoader, AuthProvider, AsyncClientFactory) for configuration and client initialization
- No external dependencies beyond project scope

**Technical Constraints:**
- Must be compatible with `foundry-platform-python` SDK async client
- Must integrate with `toon-python >=0.9,<1.0` (version pinned)
- Must handle all SDK exception types from `foundry_sdk._errors/`
- Logging must not interfere with stdout/stderr CLI contract

**Risk Mitigation:**
- TOON library API breaks: Version pin + fallback to JSON on failure
- SDK exception hierarchy changes: Exception mapping table with catch-all fallback
