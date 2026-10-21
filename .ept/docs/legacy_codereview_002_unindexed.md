---
id: CODEREVIEW-002
type: codereview
title: 'CODE REVIEW: RetryHandler, ErrorSerializer, OutputFormatter, LogSetup implementation'
status: New
parent: DEV-STORY-002
created: 2026-05-18
updated: 2026-05-18
priority: Medium
assignee: architect
reporter: architect
---

# CODEREVIEW-002: CODE REVIEW: RetryHandler, ErrorSerializer, OutputFormatter, LogSetup

## Description

Code review for DEV-STORY-002 implementation of RetryHandler, ErrorSerializer, OutputFormatter, LogSetup in `_foundry_cli_common.py`.

Review checklist:
- [ ] RetryHandler implements exponential backoff with jitter (ADR-002)
- [ ] RetryHandler respects RETRY_* env vars with correct defaults (500ms initial, 8000ms max, 2.0 multiplier, 4 attempts)
- [ ] RetryHandler applies ±10% jitter to prevent thundering herd
- [ ] RetryHandler wraps SDK calls in asyncio.wait_for() with correct timeout
- [ ] RetryHandler logs retry attempts to stderr in NDJSON format
- [ ] RetryHandler handles HTTP 429 and 503 specifically
- [ ] RetryHandler returns exit code 5 on timeout
- [ ] ErrorSerializer maps SDK exceptions to exit codes 0-9 per ADR-001 taxonomy
- [ ] ErrorSerializer emits JSON error envelope regardless of --format setting
- [ ] ErrorSerializer includes all required fields: type, message, http_status, details, attempt, operation, call_id
- [ ] ErrorSerializer handles PalantirRPCException subclasses and Python built-ins
- [ ] OutputFormatter implements ADR-004 auto-selection algorithm in correct order
- [ ] OutputFormatter respects --format json|toon|auto and FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT
- [ ] OutputFormatter TOON rule: uniform array of dicts → TOON; all other → JSON
- [ ] OutputFormatter integrates with toon-python >=0.9,<1.0
- [ ] OutputFormatter emits primary data to stdout; pagination metadata to stderr
- [ ] OutputFormatter binary downloads always use JSON
- [ ] LogSetup configures logging with NDJSON formatter to stderr (ADR-005)
- [ ] LogSetup uses correct log record schema: {ts, level, logger, msg, op, call_id, attempt, delay_ms}
- [ ] LogSetup default level is WARNING via FOUNDRY_AGENTIC_CLI_LOG_LEVEL
- [ ] LogSetup includes # ---metadata-start--- separator before metadata JSON
- [ ] No hardcoded secrets or credentials
- [ ] All components follow SAD-001 code structure conventions
- [ ] Type hints compatible with Python 3.11+

## Acceptance Criteria

- [ ] All review items checked
- [ ] Code approved or change requests logged
- [ ] Reviewer signs off with status Approved/ChangesRequested
- [ ] Specific file paths and line numbers cited in review findings
- [ ] Review findings reference actual code snippets (not generic descriptions)

## Related Documentation

- [SRS-001 §3.5 (FR-ERR)](../DEV-STORY-002/ticket.md) — Error handling requirements
- [SRS-001 §3.2 (FR-OUT)](../DEV-STORY-002/ticket.md) — Output format requirements
- [SAD-001 §4 (Component Diagram)](../docs/deliverables/architecture/SAD-001-foundry-cli.md) — Component interaction design
- [ADR-001 — Exit Code Taxonomy](../docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md) — Exit code mapping (0-9)
- [ADR-002 — Call Timeout Defaults](../docs/deliverables/architecture/adr/ADR-002-call-timeout-defaults.md) — Timeout configuration (30s default)
- [ADR-004 — Format Auto-Selection Algorithm](../docs/deliverables/architecture/adr/ADR-004-format-auto-algorithm.md) — TOON vs JSON selection logic
- [ADR-005 — Log Format](../docs/deliverables/architecture/adr/ADR-005-log-format.md) — NDJSON structured logging format

## Notes

**Dependencies:**
- Parent: DEV-STORY-002 (Implement RetryHandler, ErrorSerializer, OutputFormatter, LogSetup)
- Depends on DEV-STORY-001 for ConfigLoader, AuthProvider, AsyncClientFactory

**Technical Scope:**
- All four components live in `_foundry_cli_common.py`
- Exit codes 5, 6, 7 specifically implemented per ADR-001
- Error output always JSON on stdout regardless of --format
- Pagination metadata on stderr with # ---metadata-start--- separator
