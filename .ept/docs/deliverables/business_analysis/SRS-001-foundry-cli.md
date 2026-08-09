# Software Requirements Specification  
## Foundry CLI — Agentic Toolset for Palantir Foundry API v2

| Field | Value |
|---|---|
| **Document ID** | SRS-001 |
| **Version** | 1.1.0 |
| **Status** | Approved by BA |
| **Date** | 2026-04-13 |
| **Last updated** | 2026-07-27 |
| **BA Sign-off** | 2026-05-02 (Business Analyst) |
| **Author** | Solution Architect (acting on behalf of BA role) |
| **Reviewers** | Product Owner, Business Analyst |
| **Traceability** | FEATURE-001, BA-ANA-001, SA-ANA-001 |
| **Source Q&A** | open_questions.md, open_questions_2.md, open_questions_3.md (47 questions, 80+ sub-answers) |

---

## Table of Contents

1. [Introduction](#1-introduction)  
2. [Overall Description](#2-overall-description)  
3. [Functional Requirements](#3-functional-requirements)  
4. [Access Control Requirements](#4-access-control-requirements)  
5. [Configuration Reference](#5-configuration-reference)  
6. [Non-Functional Requirements](#6-non-functional-requirements)  
7. [Acceptance Criteria](#7-acceptance-criteria)  
8. [Constraints and Assumptions](#8-constraints-and-assumptions)  
9. [Open Items](#9-open-items)  

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) defines the complete set of functional and non-functional requirements for the **Foundry CLI Agentic Toolset** — a purpose-designed command-line interface optimised for AI-agent consumption of the Palantir Foundry API v2, packaged as Claude Code skills for VS Code.

### 1.2 Scope

The toolset provides 20 namespace-specific CLI skill packages and one general Foundry knowledge skill, totalling 21 skills. Each namespace skill exposes every operation available in the corresponding `foundry-platform-python` SDK v2 namespace via a subprocess-invocable Python CLI.

**In scope:**
- All 355 API v2 operations across 20 namespaces
- 21 Claude Code skill packages (20 namespace + 1 knowledge)
- Shared common utility module
- Configuration and access control system
- Session management for AIP Agents stateful interactions

**Out of scope:**
- Foundry API v1 endpoints
- OAuth2 / OIDC authentication flows
- Graphical user interfaces
- Direct SDK wrapping of `foundry_sdk_v2` CLI

### 1.3 Definitions and Abbreviations

| Term | Definition |
|---|---|
| **CLI** | Command-Line Interface |
| **Skill** | Claude Code skill package (`.claude/skills/{name}/SKILL.md` + scripts) |
| **Namespace** | A top-level API grouping in the `foundry-platform-python` SDK v2 |
| **Operation** | An individual SDK method (e.g., `datasets.dataset.get`) |
| **TOON** | Tabular Object Output Notation — columnar text format for uniform arrays |
| **RID** | Resource Identifier — Palantir's universal object identifier scheme |
| **Agent** | An AI agent invoking CLI tools via subprocess |
| **UserTokenAuth** | SDK authentication mechanism using a static bearer token |
| **Tier** | Access control level: Full / Read-only / Metadata-only |

### 1.4 References

| Document | Location |
|---|---|
| Initial Task Brief | `.ept/docs/customer_input/initial_task.md` |
| Requirements Q&A Round 1 | `.ept/docs/customer_input/open_questions.md` |
| Requirements Q&A Round 2 | `.ept/docs/customer_input/open_questions_2.md` |
| Requirements Q&A Round 3 | `.ept/docs/customer_input/open_questions_3.md` |
| Requirements Completeness Assessment | `.ept/docs/customer_input/task_description.md` |
| Solution Architecture Document | `.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md` |
| Common Components Design | `.ept/docs/deliverables/architecture/DESIGN-005-common-components.md` |
| Canonical Env Var Reference | `.ept/docs/deliverables/architecture/canonical-env-var-reference.md` |
| Metadata Allow-list | `.ept/docs/deliverables/architecture/metadata-allow-list.env` |
| foundry-platform-python SDK | `.ept/docs/customer_input/foundry-platform-python/` |

---

## 2. Overall Description

### 2.1 Product Perspective

The Foundry CLI is a new agentic interface layer sitting between AI agents and the Palantir Foundry platform. It is built *on top of* the `foundry-platform-python` SDK (not a wrapper around the existing `foundry_sdk_v2` CLI). The CLI provides a structured, consistent subprocess interface that AI agents can call programmatically.

```
AI Agent (Claude / Custom Orchestrator)
    │
    │  subprocess call: python foundry_datasets_cli.py dataset get --dataset-rid ri.foundry...
    ▼
Foundry CLI (foundry_datasets_cli.py)
    │  _foundry_cli_common.py (auth, retry, output, access control)
    │
    ▼
foundry-platform-python SDK (AsyncFoundryClient)
    │
    ▼
Palantir Foundry API v2 (HTTP/REST)
    │
    ▼
Palantir Foundry Platform
```

### 2.2 Product Functions (High-Level)

| Function | Description |
|---|---|
| F-EXEC | Execute all Foundry API v2 operations via CLI subprocess |
| F-AUTH | Authenticate to Foundry using UserTokenAuth with env vars |
| F-OUT | Format and emit structured output (JSON / TOON / auto) |
| F-PAG | Handle API pagination with per-call and batch modes |
| F-ERR | Serialize all errors to structured JSON on stdout |
| F-RETRY | Retry transient failures with configurable exponential backoff |
| F-DL | Download binary content with size limits and integrity checks |
| F-SESSION | Persist AIP Agents session state for multi-turn interactions |
| F-ACL | Enforce three-tier access control with 8-step precedence |
| F-ATTR | Inject attribution headers on supported operations |
| F-TRACE | Propagate SDK-native B3 distributed trace context |
| F-SKILL | Package CLI as Claude Code skills for VS Code agent consumption |
| F-KNOW | Provide pre-authored Foundry knowledge skill (static content) |

### 2.3 User Classes

| User Class | Description | Usage Pattern |
|---|---|---|
| **AI Agent (Claude)** | Primary consumer; invokes CLI via VS Code skill runner | Subprocess calls per tool use |
| **Custom Orchestrator** | Internal agent framework (under development) | Subprocess calls, exit code inspection |
| **Developer** | Human configuring credentials and access controls via `.env` | Manual CLI invocation for testing |

### 2.4 Operating Environment

- **Platforms:** Windows 11, macOS, Linux
- **Python:** 3.11.x and 3.12.x (3.13+ requires compatibility review)
- **SDK dependency:** `foundry-platform-python` (in-repo copy at `.ept/docs/customer_input/foundry-platform-python/`)
- **TOON library:** `toon-python >=0.9,<1.0` (`pip install git+https://github.com/toon-format/toon-python.git`)
- **Config source:** `.env` file at repo root; overridable by environment variables
- **Data paths:** relative to repository root (not user home directory)

### 2.5 Design Constraints

- DCC-1: Must not modify or wrap the existing `foundry_sdk_v2` CLI
- DCC-2: Distribution via file copy only (no package registry)
- DCC-3: Each namespace skill is self-contained (with copied common module)
- DCC-4: CLI contract: exit 0 on success, non-zero on error; result on stdout; metadata/diagnostics on stderr
- DCC-5: v1 API endpoints are excluded
- DCC-6: `.foundry-data/` directory must be gitignored

---

## 3. Functional Requirements

### FR-AUTH: Authentication

| ID | Requirement | Source |
|---|---|---|
| FR-AUTH-1 | The CLI SHALL authenticate using `UserTokenAuth` only, reading `FOUNDRY_TOKEN` and `FOUNDRY_HOSTNAME` from the environment | Q&A R1: A3.1, A3.2 |
| FR-AUTH-2 | When `FOUNDRY_TOKEN` or `FOUNDRY_HOSTNAME` is absent, the CLI SHALL exit with code 9 (configuration error) and return a JSON error on stdout | Q&A R1: A3.1 |
| FR-AUTH-3 | OAuth2 authentication (`ConfidentialClientAuth`, `PublicClientAuth`) SHALL NOT be implemented | Q&A R1: A3.1 |
| FR-AUTH-4 | The SDK-native variable names (`FOUNDRY_TOKEN`, `FOUNDRY_HOSTNAME`) SHALL be used without renaming or prefixing | Q&A R1: A3.2 |

**Acceptance Criteria — FR-AUTH-1:**
- **Given** `FOUNDRY_TOKEN=abc` and `FOUNDRY_HOSTNAME=my.palantircloud.com` are set  
- **When** any CLI operation is invoked  
- **Then** the SDK client is initialised with `UserTokenAuth(token="abc")` and `hostname="my.palantircloud.com"`

**Acceptance Criteria — FR-AUTH-2:**
- **Given** `FOUNDRY_TOKEN` is not set  
- **When** any CLI operation is invoked  
- **Then** stdout contains `{"error": {"type": "ConfigurationError", "message": "FOUNDRY_TOKEN is required", ...}}` and exit code is 9

---

### FR-OUT: Output Format

| ID | Requirement | Source |
|---|---|---|
| FR-OUT-1 | Primary result data SHALL be emitted to stdout | Q&A R1: A4.1 |
| FR-OUT-2 | Pagination metadata (cursor, total count, status) SHALL be emitted to stderr as compact JSON | Q&A R2: A(Q2(R2).3-C) |
| FR-OUT-3 | Binary download results SHALL emit a JSON envelope to stdout (file_path, file_size, checksum_md5, checksum_sha256, mime_type, truncated) | Q&A R2: A(Q2(R2).7) |
| FR-OUT-4 | All errors SHALL be emitted as JSON to stdout regardless of the `--format` setting | Q&A R1: A4.1 |
| FR-OUT-5 | The `--format` flag SHALL accept `json`, `toon`, or `auto`; default is `auto` | Q&A R2: A(Q2(R2).2) |
| FR-OUT-6 | The `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT` environment variable SHALL set the default format | Q&A R2: A(Q2(R2).2) |

**TOON Applicability Rule (FR-OUT-7):**  
The CLI SHALL use TOON format when ALL of the following are true:
1. The top-level result is a list/array
2. All items in the list share a uniform set of fields
3. The format is `toon` or `auto`

The CLI SHALL use JSON format in all other cases:
- Single objects
- Heterogeneous arrays
- Empty arrays
- Errors
- Pagination metadata (always on stderr)

**Acceptance Criteria — FR-OUT-7 (TOON selection):**
- **Given** format is `auto` and the API returns `{"items": [{"id": "1", "name": "A"}, {"id": "2", "name": "B"}]}`  
- **When** the CLI formats the result  
- **Then** stdout is TOON-formatted with columns `id` and `name`

- **Given** format is `auto` and the API returns a single object `{"dataset": {...}}`  
- **When** the CLI formats the result  
- **Then** stdout is JSON-formatted

---

### FR-ASYNC: Async Client

| ID | Requirement | Source |
|---|---|---|
| FR-ASYNC-1 | The CLI SHALL use `AsyncFoundryClient` internally | Q&A R2: A(Q1(R2).2-B) |
| FR-ASYNC-2 | The CLI surface SHALL be synchronous — the async event loop SHALL be entered via `asyncio.run()` | Q&A R2: A(Q1(R2).2-B) |
| FR-ASYNC-3 | Each API call SHALL be wrapped in `asyncio.wait_for()` to enforce per-call timeouts | Q&A R2: A(Q1(R2).2-B) |
| FR-ASYNC-4 | On `SIGINT` or `SIGTERM`, the CLI SHALL cancel the current operation and exit with a structured JSON error on stdout | Q&A R2: A(Q1(R2).2-B) |

---

### FR-PAG: Pagination

| ID | Requirement | Source |
|---|---|---|
| FR-PAG-1 | For list/search operations, the CLI SHALL by default return the first page only | Q&A R1: A4.2 |
| FR-PAG-2 | When a next page token is available, it SHALL be emitted to stderr as part of the metadata JSON object | Q&A R1: A4.2 |
| FR-PAG-3 | The CLI SHALL expose `--page-size`, `--page-token`, and `--batch-pages` arguments on all paginated operations | Q&A R1: A4.2 |
| FR-PAG-4 | When `--batch-pages N` is specified, the CLI SHALL retrieve up to N pages and aggregate results before emitting | Q&A R1: A4.2 |
| FR-PAG-5 | The maximum value for `--batch-pages` SHALL be 40 | Q&A R1: A4.2 |

**Acceptance Criteria — FR-PAG-3:**
- **Given** `--batch-pages 3` and `--page-size 10` are specified  
- **When** the API returns 3 pages of 10 items each  
- **Then** stdout contains a combined array of 30 items (TOON or JSON per format rules) and stderr contains the next cursor (or null if no more pages)

---

### FR-ERR: Error Handling

| ID | Requirement | Source |
|---|---|---|
| FR-ERR-1 | All errors (user, auth, permission, system, timeout) SHALL be serialized to JSON on stdout | Q&A R1: A4.3 |
| FR-ERR-2 | The JSON error envelope SHALL contain: `type`, `message`, `http_status` (if applicable), `details` (if applicable), `attempt` (retry count) | Q&A R1: A4.3 |
| FR-ERR-3 | HTTP 429 and 503 responses SHALL trigger exponential backoff retry | Q&A R1: A4.3 |
| FR-ERR-4 | Retry behaviour SHALL be fully configurable via env vars: `FOUNDRY_AGENTIC_CLI_RETRY_INITIAL_DELAY_MS`, `FOUNDRY_AGENTIC_CLI_RETRY_MAX_DELAY_MS`, `FOUNDRY_AGENTIC_CLI_RETRY_MULTIPLIER`, `FOUNDRY_AGENTIC_CLI_RETRY_MAX_ATTEMPTS` | Q&A R1: A4.3 |
| FR-ERR-5 | SDK typed exceptions (`PalantirRPCException`, `PermissionDeniedError`, etc.) SHALL be mapped to their corresponding exit codes (see ADR-001) | Q&A R1: A4.3 |

**Error JSON Schema:**
```json
{
  "error": {
    "type": "string",            // e.g. "AuthenticationError", "PermissionDeniedError"
    "message": "string",
    "http_status": 403,          // optional
    "details": {},               // optional, SDK-provided details
    "attempt": 1,                // retry attempt number (1 = first attempt)
    "operation": "datasets.dataset.get",
    "call_id": "uuid"
  }
}
```

---

### FR-DL: Binary Downloads

| ID | Requirement | Source |
|---|---|---|
| FR-DL-1 | Binary content SHALL be written to disk at `<repo-root>/.foundry-data/downloads/{uuid}/{original_file_name}` | Q&A R2: A(Q2(R2).7) |
| FR-DL-2 | If the original filename is unavailable, the fallback name SHALL be `{namespace}_{operation}_{timestamp}.{ext}` | Q&A R2: A(Q2(R2).7) |
| FR-DL-3 | The default file size limit SHALL be 1.5 MB (1,572,864 bytes); configurable via `FOUNDRY_AGENTIC_CLI_MAX_DOWNLOAD_BYTES` | Q&A R3: A(Q3(R3).1) |
| FR-DL-4 | When the size limit is exceeded, the CLI SHALL write partial content up to the limit, read at most one probe byte, close the stream, and set `truncated: true` | Q&A R3: A(Q3(R3).1); DESIGN-005 |
| FR-DL-5 | The JSON envelope on stdout SHALL include `file_path`, `file_size`, `checksum_md5`, `checksum_sha256`, `mime_type`, `truncated`, nullable `source_size`, and nullable `source_size_at_least`; readers SHALL accept older envelopes where the two source-size fields are absent | Q&A R2: A(Q2(R2).7); DESIGN-005 |
| FR-DL-6 | The CLI SHALL NOT consume the remaining response solely to calculate an exact source size after the configured limit is crossed | DESIGN-005 |

**Acceptance Criteria — FR-DL-3 (partial download):**
- **Given** `FOUNDRY_AGENTIC_CLI_MAX_DOWNLOAD_BYTES=1048576` (1 MB) and the API returns a 3 MB file  
- **When** the download operation is invoked  
- **Then** a 1 MB file is written to disk and stdout JSON contains `"truncated": true, "file_size": 1048576`
- **And** when a valid applicable `Content-Length` is available, `source_size` and the warning report that exact size
- **And** when exact source size is unknown, `source_size` is `null`, `source_size_at_least` is `1048577`, and the warning reports the lower bound instead of an invented exact size

---

### FR-SESSION: Session Management

| ID | Requirement | Source |
|---|---|---|
| FR-SESSION-1 | Session state SHALL be persisted to `<repo-root>/.foundry-data/sessions/` | Q&A R1: A4.4 |
| FR-SESSION-2 | Sessions SHALL be identified by a named alias provided by the agent | Q&A R2: A(Q2(R2).8) |
| FR-SESSION-3 | If a session alias already exists for an active session, creation SHALL fail with a structured error | Q&A R3: A(Q3(R3).5) |
| FR-SESSION-4 | Session state SHALL persist `session_id` from SDK `Session.rid`, `agent_rid`, nullable `session_token`, `created_at`, `last_used_at`, `status`, and `tool_history`; readers SHALL accept a missing, null, or string `session_token` | Q&A R1: A4.4; DESIGN-005 |
| FR-SESSION-5 | Sessions older than 7 days SHALL be automatically cleaned up on any tool invocation | Q&A R3: A(Q3(R3).5) |
| FR-SESSION-6 | An explicit `session purge` command SHALL be available to delete all sessions | Q&A R3: A(Q3(R3).5) |
| FR-SESSION-7 | A warning SHALL be logged (not enforced) when a single agent has more than 5 concurrent active sessions | Q&A R3: A(Q3(R3).5) |

---

### FR-ATTR: Attribution

| ID | Requirement | Source |
|---|---|---|
| FR-ATTR-1 | Attribution SHALL be opt-in, disabled by default | Q&A R2: A(Q1(R2).1) |
| FR-ATTR-2 | Attribution IS enabled by setting `FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION=true` | Q&A R2: A(Q1(R2).1) |
| FR-ATTR-3 | Attribution RIDs SHALL be supplied via `FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS` (comma-separated) | Q&A R3: A(Q2(R3).1) |
| FR-ATTR-4 | Attribution SHALL be injected on: `functions.query.*`, `ontologies.query.*`, `media_sets.media_set.*`, `language_models.*` | Q&A R2: A(Q1(R2).1) |

---

### FR-TRACE: Distributed Tracing

| ID | Requirement | Source |
|---|---|---|
| FR-TRACE-1 | Tracing SHALL be opt-in, disabled by default | Q&A R2: A(Q1(R2).1) |
| FR-TRACE-2 | Tracing IS enabled by setting `FOUNDRY_AGENTIC_CLI_ENABLE_TRACING=true` | Q&A R3: A(Q2(R3).1) |
| FR-TRACE-3 | When enabled, SDK-native B3 multi-header context SHALL be generated and propagated for each CLI call | Q&A R3: A(Q2(R3).1); DESIGN-005 |
| FR-TRACE-4 | SDK vars `FOUNDRY_TRACE_ID`, `FOUNDRY_SPAN_ID`, and `FOUNDRY_SAMPLED` SHALL map to `X-B3-TraceId`, `X-B3-SpanId`, and `X-B3-Sampled` respectively | Q&A R3: A(Q2(R3).1); DESIGN-005 |
| FR-TRACE-5 | The CLI SHALL NOT claim W3C `traceparent` or `tracestate` propagation unless a separate supported implementation is added | DESIGN-005 |

---

### FR-SKILL: Skill Packaging

| ID | Requirement | Source |
|---|---|---|
| FR-SKILL-1 | Each namespace SHALL have a skill package under `.claude/skills/foundry-{namespace}/` | Q&A R1: A2.4 |
| FR-SKILL-2 | Each namespace skill SHALL contain: `SKILL.md` and `scripts/` directory with `foundry_{namespace}_cli.py` and `_foundry_cli_common.py` | Q&A R3: A(Q3(R3).7-B) |
| FR-SKILL-3 | The general Foundry knowledge skill SHALL be at `.claude/skills/foundry/SKILL.md` | Q&A R1: A2.4 |
| FR-SKILL-4 | The general knowledge skill SHALL have `user-invocable: false` and be auto-loaded on Foundry context detection | Q&A R2: A(Q2(R2).9) |
| FR-SKILL-5 | All 21 skills SHALL follow Claude Code skill format | Q&A R1: A2.2 |

---

### FR-KNOW: General Knowledge Skill

| ID | Requirement | Source |
|---|---|---|
| FR-KNOW-1 | The knowledge skill SHALL contain pre-authored static markdown (no runtime web fetch) | Q&A R2: A(Q2(R2).9) |
| FR-KNOW-2 | Content SHALL cover: Foundry core concepts, cross-namespace workflow recipes, auth/config guidance, skill catalog, Palantir Ontology, PySpark pipeline development | Q&A R2: A(Q2(R2).9) |
| FR-KNOW-3 | Content SHALL be reviewed and updated on every `foundry-platform-python` minor release | Q&A R3: A(Q3(R3).6) |

---

## 4. Access Control Requirements

### FR-ACL: Three-Tier Access Model

| ID | Requirement | Source |
|---|---|---|
| FR-ACL-1 | The CLI SHALL support three access tiers: Full (default), Read-only, Metadata-only | Q&A R3: A(Q3(R3).3) |
| FR-ACL-2 | Tier 2 (Read-only) SHALL block all write operations; all read operations SHALL be permitted | Q&A R3: A(Q3(R3).3) |
| FR-ACL-3 | Tier 3 (Metadata-only) SHALL block data content reads and all write operations; only metadata reads SHALL be permitted | Q&A R3: A(Q3(R3).3) |
| FR-ACL-4 | `METADATA_ONLY=true` SHALL imply `READONLY=true` — writes are BLOCKED | Q&A R3: A(Q3(R3).3) |
| FR-ACL-5 | Access control SHALL be evaluated using an 8-step precedence model (see below) | Q&A R3: A(Q3(R3).3) |
| FR-ACL-6 | The metadata allow-list SHALL use a **deny-by-default** stance for tier-3 unclassified operations | Q&A R3: A(Q3(R3).8) |

### 8-Step Precedence Model

Evaluated in order; first matching rule wins:

| Step | Condition | Effect |
|---|---|---|
| 1 | `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_ENABLED=false` | BLOCKED |
| 2 | `FOUNDRY_AGENTIC_CLI_{NS}_ENABLED=false` | BLOCKED |
| 3 | `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_READONLY=false` (overrides global READONLY=true) | WRITE PERMITTED for this op |
| 4 | `FOUNDRY_AGENTIC_CLI_{NS}_READONLY=false` (overrides global READONLY=true) | WRITE PERMITTED for this namespace |
| 5 | `FOUNDRY_AGENTIC_CLI_READONLY=true` | ALL WRITES BLOCKED |
| 6 | `FOUNDRY_AGENTIC_CLI_{NS}_METADATA_ONLY=false` (overrides global METADATA_ONLY=true) | CONTENT READS PERMITTED for this namespace |
| 7 | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` | CONTENT READS BLOCKED + ALL WRITES BLOCKED |
| 8 | Default | FULL ACCESS |

**Acceptance Criteria — FR-ACL-5 (step 3 override):**
- **Given** `FOUNDRY_AGENTIC_CLI_READONLY=true` and `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_PUT_SCHEMA_READONLY=false`  
- **When** `datasets dataset put-schema` is invoked  
- **Then** the operation proceeds (step 3 grants write permission for this specific operation)

**Acceptance Criteria — FR-ACL-6 (deny-by-default):**
- **Given** `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` and `datasets.file.content` is NOT in the metadata allow-list  
- **When** `datasets file content` is invoked  
- **Then** exit code is 8 and stdout contains `{"error": {"type": "AccessControlError", "message": "Operation blocked: not in metadata allow-list"}}`

---

## 5. Configuration Reference

### 5.1 Loading Order

1. `.env` file at repo root (primary)
2. Environment variables override `.env` (highest precedence)

### 5.2 Variable Naming Convention

| Scope | Pattern | Example |
|---|---|---|
| SDK-native | Original SDK names (no prefix) | `FOUNDRY_TOKEN`, `FOUNDRY_HOSTNAME` |
| Global project | `FOUNDRY_AGENTIC_CLI_{KEY}` | `FOUNDRY_AGENTIC_CLI_READONLY` |
| Namespace-level | `FOUNDRY_AGENTIC_CLI_{NAMESPACE}_{CONTROL}` | `FOUNDRY_AGENTIC_CLI_DATASETS_READONLY` |
| Operation-level | `FOUNDRY_AGENTIC_CLI_{NAMESPACE}_{CLASS}_{OP}_{CONTROL}` | `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_PUT_SCHEMA_ENABLED` |

Transformation rule: uppercase entire SDK path, replace dots and underscores with single underscores, prefix with `FOUNDRY_AGENTIC_CLI_`.

### 5.3 Core Variables with Defaults

| Variable | Default | Description |
|---|---|---|
| `FOUNDRY_TOKEN` | *(required)* | Palantir bearer token |
| `FOUNDRY_HOSTNAME` | *(required)* | Foundry instance hostname |
| `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT` | `auto` | Output format: `json` / `toon` / `auto` |
| `FOUNDRY_AGENTIC_CLI_READONLY` | `false` | Global read-only mode |
| `FOUNDRY_AGENTIC_CLI_METADATA_ONLY` | `false` | Global metadata-only mode |
| `FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION` | `false` | Enable attribution header injection |
| `FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS` | *(empty)* | Comma-separated attribution RIDs |
| `FOUNDRY_AGENTIC_CLI_ENABLE_TRACING` | `false` | Enable SDK-native B3 multi-header propagation |
| `FOUNDRY_AGENTIC_CLI_RETRY_INITIAL_DELAY_MS` | `500` | Retry initial delay (ms) |
| `FOUNDRY_AGENTIC_CLI_RETRY_MAX_DELAY_MS` | `30000` | Retry maximum delay (ms) |
| `FOUNDRY_AGENTIC_CLI_RETRY_MULTIPLIER` | `2.0` | Retry backoff multiplier |
| `FOUNDRY_AGENTIC_CLI_RETRY_MAX_ATTEMPTS` | `4` | Maximum retry attempts |
| `FOUNDRY_AGENTIC_CLI_TIMEOUT_S` | `30` | Per-call timeout in seconds |
| `FOUNDRY_AGENTIC_CLI_DEFAULT_PAGE_SIZE` | `100` | Default page size for list operations |
| `FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES` | `40` | Maximum pages in one batch call |
| `FOUNDRY_AGENTIC_CLI_MAX_DOWNLOAD_BYTES` | `1572864` | Max binary download size (1.5 MB) |
| `FOUNDRY_AGENTIC_CLI_DOWNLOAD_PATH` | `.foundry-data/downloads` | Base path for binary downloads |
| `FOUNDRY_AGENTIC_CLI_SESSION_PATH` | `.foundry-data/sessions` | Base path for session state |
| `FOUNDRY_AGENTIC_CLI_LOG_LEVEL` | `WARNING` | Log verbosity (DEBUG / INFO / WARNING / ERROR) |
| `FOUNDRY_AGENTIC_CLI_ENV_FILE` | *(none)* | Explicit path to `.env` file |

> Canonical per-namespace and per-operation variables: see [Canonical Env Var Reference](../architecture/canonical-env-var-reference.md) (~415+ entries)

---

## 6. Non-Functional Requirements

### NFR-PLAT: Platform Compatibility

| ID | Requirement | Source |
|---|---|---|
| NFR-PLAT-1 | The CLI SHALL run on Python 3.11.x and Python 3.12.x | Q&A R1: A5.1 |
| NFR-PLAT-2 | The CLI SHALL run on Windows 11, macOS, and Linux | Q&A R1: A5.2 |
| NFR-PLAT-3 | Data paths SHALL be relative to repository root (not user home directory) | Q&A R2: A(Q2(R2).10-D) |

### NFR-DIST: Distribution

| ID | Requirement | Source |
|---|---|---|
| NFR-DIST-1 | Distribution SHALL be via file copy of skill folders to target repository | Q&A R1: A5.2 |
| NFR-DIST-2 | `_foundry_cli_common.py` SHALL be copied alongside each namespace CLI file | Q&A R3: A(Q3(R3).7-B) |
| NFR-DIST-3 | `.foundry-data/` SHALL be excluded from git via `.gitignore` | Q&A R2: A(Q2(R2).10-D) |

### NFR-IFACE: CLI Interface Contract

| ID | Requirement | Source |
|---|---|---|
| NFR-IFACE-1 | Exit 0 on success; non-zero on error (see ADR-001 for taxonomy) | Q&A R2: A(Q2(R2).3) |
| NFR-IFACE-2 | Structured result on stdout; diagnostics and metadata on stderr | Q&A R2: A(Q2(R2).3) |
| NFR-IFACE-3 | The CLI SHALL be compatible with VS Code Claude skills and custom subprocess-based orchestrators | Q&A R1: A2.2 |

### NFR-MAINT: Maintainability

| ID | Requirement | Source |
|---|---|---|
| NFR-MAINT-1 | All shared utilities SHALL reside in `_foundry_cli_common.py` (single source of truth) | Q&A R3: A(Q3(R3).7-B) |
| NFR-MAINT-2 | The metadata allow-list and knowledge skill content SHALL be reviewed on every `foundry-platform-python` minor release | Q&A R3: A(Q3(R3).6, Q3(R3).8) |

---

## 7. Acceptance Criteria

### AC-SMOKE: End-to-End Smoke Test

- **Given** a configured `.env` with valid `FOUNDRY_TOKEN` and `FOUNDRY_HOSTNAME`
- **When** `python foundry_datasets_cli.py dataset list` is invoked
- **Then** stdout is valid JSON (or TOON if auto selects it), stderr contains metadata JSON with `page_token` field, exit code is 0

### AC-ERR-AUTH: Authentication Failure

- **Given** `FOUNDRY_TOKEN` is set to an invalid value
- **When** `python foundry_datasets_cli.py dataset list` is invoked
- **Then** stdout contains `{"error": {"type": "AuthenticationError", ...}}`, exit code is 2

### AC-RETRY: Exponential Backoff

- **Given** `FOUNDRY_AGENTIC_CLI_RETRY_MAX_ATTEMPTS=3` and the API returns 429 on the first two calls
- **When** `python foundry_datasets_cli.py dataset get --dataset-rid ri.foundry...` is invoked
- **Then** the operation is retried twice with increasing delay, and on the third attempt (if 200) succeeds with exit code 0

### AC-ACL-BLOCK: Access Control Blocking

- **Given** `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_PUT_SCHEMA_ENABLED=false`
- **When** `datasets dataset put-schema` is invoked
- **Then** exit code is 8, stdout contains `{"error": {"type": "AccessControlError", ...}}`

### AC-FMT-TOON: TOON Format Selection

- **Given** `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT=auto` and the result is a uniform array
- **When** any list operation is invoked
- **Then** stdout is valid TOON-formatted output with column headers

### AC-SESS: Session Collision

- **Given** an active session with alias `my-session` exists
- **When** `aip-agents session create --alias my-session` is invoked
- **Then** exit code is 1, stdout contains `{"error": {"type": "SessionAliasConflictError", "message": "Session alias 'my-session' is already in use"}}`

---

## 8. Constraints and Assumptions

| # | Type | Description |
|---|---|---|
| C-1 | Technical | SDK version pinned to in-repo copy; upgrade requires re-enumeration of operations |
| C-2 | Technical | TOON library pinned `>=0.9,<1.0`; air-gap environments require private mirror |
| C-3 | Security | UserTokenAuth tokens are long-lived; rotation and revocation are user responsibility |
| C-4 | Operational | `.foundry-data/` is local-only; no shared/remote session storage |
| C-5 | Performance | 1.5 MB default download limit is intentionally conservative; large binary workflows require explicit limit increase |
| A-1 | Assumption | All 355 SDK operations are accessible via API v2; no operations require SDK version >0.0.0 in-repo copy |
| A-2 | Assumption | Agent callers are trusted to supply valid argument types; input validation is at CLI boundary only |
| A-3 | Assumption | Python 3.13+ is not a target until the compatibility review reports no breaking changes |

---

## 9. Open Items

| # | Item | Owner | Target |
|---|---|---|---|
| OI-1 | BA sign-off on SRS completeness and acceptance criteria | Business Analyst | Before design freeze |
| OI-2 | Confirm 7 ADR decisions are accepted | Product Owner | Before implementation sprint |
| OI-3 | Confirm retry defaults (500ms initial, 2x multiplier, 30s cap, 4 attempts) | Product Owner | Before implementation |
| OI-4 | Confirm `geo` namespace has 0 public methods (no CLI entry required) | Developer | During implementation |
| OI-5 | Confirm `core` namespace has 0 public methods (no CLI entry required) | Developer | During implementation |
| OI-6 | TOON library installation in air-gapped environments | DevOps | Before deployment |

---

*SRS-001 v1.1.0 | Generated 2026-04-13 | Updated 2026-07-27 | Foundry CLI Agentic Toolset*
