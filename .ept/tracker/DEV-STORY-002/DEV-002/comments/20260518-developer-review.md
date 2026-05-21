Subject: Parent Context Review — DEV-002

**Author**: developer | **Date**: 2026-05-18 | **Action**: New → Open transition

## 1. Parent Story Context Review (DEV-STORY-002)

### 1.1 Scope
DEV-STORY-002 requires implementation of **four critical components** in the `_foundry_cli_common.py` module (note: DESIGN-001 splits these into separate files under `src/foundry_cli/utils/`, which is an acceptable modularization):

| Component | Purpose | Key Requirements |
|---|---|---|
| **RetryHandler** | Exponential backoff with jitter for HTTP 429/503 | Configurable env vars, wraps SDK async calls, logs to stderr |
| **ErrorSerializer** | SDK exception → exit code mapping + JSON error envelope | Per ADR-001 taxonomy (codes 0-9), always JSON on stdout |
| **OutputFormatter** | Intelligent format selection (JSON/TOON/auto) | Per ADR-004 algorithm, pagination metadata to stderr |
| **LogSetup** | NDJSON structured logging to stderr | Per ADR-005, configurable log level, metadata separator |

### 1.2 Dependencies
- **DEV-STORY-001** (ConfigLoader, AuthProvider, AsyncClientFactory) — **prerequisite**. Config and auth must be operational before RetryHandler can wrap SDK calls.

### 1.3 Acceptance Criteria Summary
- RetryHandler: 4 env vars, exponential backoff, ±10% jitter, asyncio.wait_for, SIGINT/SIGTERM handling
- ErrorSerializer: Exit codes 0-9 per ADR-001, JSON error envelope with all 7 fields
- OutputFormatter: Full ADR-004 algorithm (7-step), TOON integration, pagination metadata to stderr
- LogSetup: NDJSON formatter to stderr, ISO 8601 UTC, configurable level (default WARNING), metadata separator

---

## 2. Related Documentation Review

### 2.1 SAD-001 — Solution Architecture Document
- **§4 (Component Diagram)**: Confirms `_foundry_cli_common.py` as the shared module for all skills; RetryHandler and ErrorSerializer sit at the core of the call pipeline.
- **§6.2 (Retry Sequence)**: Retry behavior diagram matches the exponential backoff + jitter approach specified in AC1.

### 2.2 ADR-001 — Exit Code Taxonomy
- Defines codes **0-9** for all CLI error categories.
- Key mappings relevant to DEV-002:
  - `5` → TimeoutError (`asyncio.wait_for` timeout)
  - `6` → ServerError (HTTP 5xx excluding 503)
  - `7` → RateLimitExhausted (HTTP 429 after max retries)
- All errors produce JSON on stdout regardless of `--format`.

### 2.3 ADR-002 — Call Timeout Defaults
- Default `FOUNDRY_AGENTIC_CLI_TIMEOUT_S` = **30 seconds**
- Range: 1-3600 seconds
- Streams namespace has separate `FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S` = 120s
- Timeout breach → `asyncio.CancelledError` → exit code 5

### 2.4 ADR-004 — Format Auto-Selection Algorithm
- **7-step algorithm** (explicit > errors > non-list > empty > field-set extraction > uniformity check)
- Special cases: error envelopes → JSON, binary downloads → JSON, pagination metadata → JSON to stderr
- TOON only for uniform arrays of dicts

### 2.5 ADR-005 — Log Format
- **NDJSON** on stderr — each line independently parseable
- Required fields: `ts`, `level`, `logger`, `msg`
- Optional: `op`, `call_id`, `attempt`, `delay_ms`, `http_status`
- Metadata separator: `# ---metadata-start---`

### 2.6 DESIGN-001 — Technical Design
- Status: **Closed** (ready for implementation)
- Maps all ACs from DEV-STORY-002 to implementation plan
- Suggests splitting components into separate files under `src/foundry_cli/utils/`

---

## 3. Blockers Identified

### 3.1 Blocker: DEV-STORY-001 Not Yet Complete
- **Severity**: Medium-High
- **Impact**: RetryHandler wraps SDK async calls; ErrorSerializer maps SDK exceptions — both depend on the async client and SDK exception types established in DEV-STORY-001.
- **Mitigation**: Implementation can proceed with mock/stub dependencies for DEV-STORY-001 components. Unit tests should isolate each component; integration tests will require DEV-STORY-001.
- **Recommendation**: Track DEV-STORY-001 status; coordinate with architect on completion timeline.

### 3.2 Blocker: `toon-python` Dependency
- **Severity**: Low
- **Impact**: OutputFormatter depends on `toon-python >=0.9,<1.0`. Must be added to project dependencies.
- **Mitigation**: Add to `requirements.txt`/`pyproject.toml` during setup.

### 3.3 Clarification: File Location Discrepancy
- **Issue**: DEV-STORY-002 references `_foundry_cli_common.py` module; DESIGN-001 suggests separate files under `src/foundry_cli/utils/`.
- **Resolution**: DESIGN-001 (technical design) takes precedence — use separate files. A consolidated `_foundry_cli_common.py` can re-export from the individual modules if desired for backward compatibility.

---

## 4. Critical Thinking Summary

### 4.1 Alignment Assessment
The implementation plan in DESIGN-001 is **well-aligned** with DEV-STORY-002 acceptance criteria and all referenced ADRs. Key observations:

1. **RetryHandler** correctly implements exponential backoff per the sequence diagram in SAD-001 §6.2. The ±10% jitter requirement is met.
2. **ErrorSerializer** covers all 10 exit codes (0-9) from ADR-001. The mapping table in DESIGN-001 should be verified against the final ADR-001 taxonomy (minor naming differences in exception types).
3. **OutputFormatter** implements the full ADR-004 7-step algorithm. The "errors always JSON" rule is correctly enforced.
4. **LogSetup** implements ADR-005 NDJSON format. The metadata separator `# ---metadata-start---` is included.

### 4.2 Risks
1. **Integration complexity**: All four components must work together seamlessly. E.g., RetryHandler logs via LogSetup and may trigger ErrorSerializer on timeout.
2. **TOON library version pinning**: `toon-python >=0.9,<1.0` is strict; ensure no transitive dependency pulls a conflicting version.
3. **stderr/stdout contract**: The CLI contract is strict — errors always JSON to stdout, logs/metadata always to stderr. Careful stream management is required.

### 4.3 Recommendations
1. Implement components **in order**: LogSetup → RetryHandler → ErrorSerializer → OutputFormatter (each builds on the previous).
2. Write **unit tests first** (TDD approach) for each component, achieving ≥80% coverage as required.
3. Use **dependency injection** for the SDK client in RetryHandler to enable mocking.
4. Create a **shared test fixtures module** for common mock objects (SDK exceptions, HTTP responses).

---

## 5. Status Update: New → Open

| Field | Before | After |
|---|---|---|
| status | New | **Open** |
| updated | 2026-05-17 | **2026-05-18** |
| assignee | developer | developer (unchanged) ✓ |

### Pre-conditions Met:
- [x] Parent Story (DEV-STORY-002) context reviewed ✓
- [x] Related documentation reviewed (SAD-001, ADR-001, ADR-002, ADR-004, ADR-005, DESIGN-001) ✓
- [x] Critical thinking applied (alignment assessment, risks, recommendations) ✓
- [x] Blockers identified and recorded ✓
- [x] ParentChild link established (DEV-STORY-002 → DEV-002) ✓
- [x] Required fields validated ✓

### Actions Completed:
1. ✅ ParentChild link from DEV-STORY-002 to DEV-002 created (link_type=ParentChild)
2. ✅ Parent story context reviewed
3. ✅ All related documentation reviewed (SAD-001, ADR-001, ADR-002, ADR-004, ADR-005, DESIGN-001)
4. ✅ Parent context documented in this comment
5. ✅ Blockers identified: DEV-STORY-001 dependency, toon-python dependency, file location discrepancy
6. ✅ Status updated to Open
