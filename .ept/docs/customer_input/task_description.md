# Foundry CLI Agent Skill — Requirements & Architecture Findings

**Document type:** Requirements Completeness Assessment  
**Date:** 2026-04-10  
**Author:** Solution Architect  
**Status:** Ready to proceed — all customer questions answered  

---

## Tracking References

| Ticket | Title | Status |
| --- | --- | --- |
| [FEATURE-001] | Foundry CLI: Requirements Analysis and Open Questions | Open |
| [QUESTION-001] | Foundry CLI Round 3: 10 open questions requiring Product Owner answers | Closed |

## Source Documents

| Document | Purpose |
| --- | --- |
| [initial_task.md](initial_task.md) | Original task brief — FR-01, FR-02 (blank), NFR-01–03 |
| [open_questions.md](open_questions.md) | Round 1 — 25 questions and answers (Q1.1–Q6.5) |
| [open_questions_2.md](open_questions_2.md) | Round 2 — 12 questions and answers (Q1(R2).1–Q2(R2).10) |
| [open_questions_3.md](open_questions_3.md) | Round 3 — 10 questions and answers (Q1(R3).1–Q3(R3).8) |

---

## 1. Project Goal

Build a new, purpose-designed CLI toolset optimised for AI-agent consumption of the Palantir Foundry API v2, packaged as Claude agent skills for VS Code. The toolset is **not** a wrapper around the existing SDK CLI (`foundry_sdk_v2`), but a new agentic interface built on top of the `foundry-platform-python` SDK.

---

## 2. Deliverable Scope

### 2.1 Skills

| Skill | Description |
| --- | --- |
| `foundry` | General Foundry knowledge skill — auto-loaded, non-user-invocable |
| `foundry-admin` | Wraps `admin` namespace |
| `foundry-aip-agents` | Wraps `aip_agents` namespace |
| `foundry-audit` | Wraps `audit` namespace |
| `foundry-checkpoints` | Wraps `checkpoints` namespace |
| `foundry-connectivity` | Wraps `connectivity` namespace |
| `foundry-core` | Wraps `core` namespace |
| `foundry-data-health` | Wraps `data_health` namespace |
| `foundry-datasets` | Wraps `datasets` namespace |
| `foundry-filesystem` | Wraps `filesystem` namespace |
| `foundry-functions` | Wraps `functions` namespace |
| `foundry-geo` | Wraps `geo` namespace |
| `foundry-language-models` | Wraps `language_models` namespace |
| `foundry-media-sets` | Wraps `media_sets` namespace |
| `foundry-models` | Wraps `models` namespace |
| `foundry-ontologies` | Wraps `ontologies` namespace |
| `foundry-orchestration` | Wraps `orchestration` namespace |
| `foundry-sql-queries` | Wraps `sql_queries` namespace |
| `foundry-streams` | Wraps `streams` namespace |
| `foundry-third-party-applications` | Wraps `third_party_applications` namespace |
| `foundry-widgets` | Wraps `widgets` namespace |

**Total: 21 skills** (20 namespace skills + 1 general knowledge skill).  
Source: [open_questions.md](open_questions.md) A1.3, A2.4; [open_questions_2.md](open_questions_2.md) A(Q2(R2).10-A).

### 2.2 API Coverage

- All v2 operations across all 20 namespaces (every SDK method exposed).
- v1 endpoints are **excluded**.
- No operations are excluded by default; access control is runtime-configurable.

Source: [open_questions.md](open_questions.md) A1.1, A1.3.

### 2.3 Folder Structure

```text
<repo-root>/
├── .claude/
│   └── skills/
│       ├── foundry/                        # General knowledge skill
│       │   └── SKILL.md
│       ├── foundry-{namespace}/            # One per namespace (×20)
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       ├── foundry_{namespace}_cli.py   # Namespace entry point
│       │       └── _foundry_cli_common.py       # Shared utility module (copied alongside)
│       └── ...
├── .foundry-data/                          # Runtime data (gitignored)
│   ├── downloads/                          # Binary downloads
│   └── sessions/                          # Session state files
└── .env                                   # Primary configuration source
```

Source: [open_questions_2.md](open_questions_2.md) A(Q2(R2).10); [open_questions_3.md](open_questions_3.md) A(Q3(R3).7-B).

---

## 3. Functional Requirements

### 3.1 Authentication

- **Method:** `UserTokenAuth` only (agents invoked by developers).
- **Credentials:** Environment variables `FOUNDRY_TOKEN` and `FOUNDRY_HOSTNAME` (SDK-native variables, not prefixed).
- OAuth2 (`ConfidentialClientAuth`, `PublicClientAuth`) is **not** used.

Source: [open_questions.md](open_questions.md) A3.1, A3.2.

### 3.2 Output Format

- **Primary result:** stdout — raw TOON (for uniform arrays) or JSON (all other cases).
- **Metadata (pagination cursor, total count, status):** stderr — compact JSON object.
- **Binary downloads:** stdout — JSON envelope (file path, file size, checksum MD5/SHA-256, MIME type); file content written to disk only.
- **Errors:** always JSON on stdout regardless of format setting.
- **Format selection:** `--format` flag or `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT` env var (`json` / `toon` / `auto`).

**TOON applicability rule:**  
Use TOON when the top-level result is a list/array AND all items share a uniform field set.  
Use JSON in all other cases (single objects, heterogeneous arrays, errors, pagination metadata).

Source: [open_questions.md](open_questions.md) A4.1; [open_questions_2.md](open_questions_2.md) A(Q2(R2).2), A(Q2(R2).3-C); [open_questions_3.md](open_questions_3.md) A(Q3(R3).2-A, Q3(R3).2-B).

### 3.3 TOON Library

- Dependency: `toon-python` from `pip install git+https://github.com/toon-format/toon-python.git`.
- Version pin: semver range `>=0.9,<1.0`.
- Air-gap / private mirror handling acknowledged as a future operational concern.

Source: [open_questions_3.md](open_questions_3.md) A(Q1(R3).1).

### 3.4 Async Client

- Internal client: `AsyncFoundryClient`.
- CLI boundary: `asyncio.run()` — synchronous surface, async internals.
- Enables per-call `asyncio.wait_for()` timeouts and `SIGINT`/`SIGTERM` graceful exit reporting.

Source: [open_questions_2.md](open_questions_2.md) A(Q1(R2).2-B).

### 3.5 Pagination

- Default: return first page only with `page_token` on stderr metadata.
- Caller (agent) manages pagination using the returned cursor.
- Batch mode: agent specifies number of pages to retrieve in one call (maximum 40 pages per batch).
- Arguments exposed: `--page-size`, `--page-token`, `--batch-pages`.

Source: [open_questions.md](open_questions.md) A4.2.

### 3.6 Error Handling

- All errors returned as structured JSON on stdout.
- Transient errors (429, 503): exponential backoff retry, fully configurable via env vars:
  - `FOUNDRY_AGENTIC_CLI_RETRY_INITIAL_DELAY_MS`
  - `FOUNDRY_AGENTIC_CLI_RETRY_MAX_DELAY_MS`
  - `FOUNDRY_AGENTIC_CLI_RETRY_MULTIPLIER`
  - `FOUNDRY_AGENTIC_CLI_RETRY_MAX_ATTEMPTS`
- SDK typed exceptions (`PalantirRPCException`, `PermissionDeniedError`, etc.) serialised to JSON with type, message, and HTTP status.

Source: [open_questions.md](open_questions.md) A4.3.

### 3.7 Binary Downloads

- Default path: `<repo-root>/.foundry-data/downloads/{uuid}/{original_file_name}`
- Fallback name (if original unavailable): `{namespace}_{operation}_{timestamp}.{ext}`
- Default file size limit: **1.5 MB** (intentional conservative safe default; increase via `FOUNDRY_AGENTIC_CLI_MAX_DOWNLOAD_BYTES`).
- Behaviour when limit exceeded: return **partial content up to limit** with truncation warning (includes actual file size and configured limit).
- Stdout output: JSON envelope with `file_path`, `file_size`, `checksum_md5`, `checksum_sha256`, `mime_type`, `truncated` flag.

Source: [open_questions_2.md](open_questions_2.md) A(Q2(R2).7); [open_questions_3.md](open_questions_3.md) A(Q3(R3).1).

### 3.8 Session Management (Multi-turn / Stateful)

- Session state persisted to `<repo-root>/.foundry-data/sessions/` (gitignored).
- Session identified by **named alias** provided by the agent at creation time.
- Alias collision rule: **error** — if alias already held by an active session (regardless of creator), creation fails.
- Persisted fields: `session_id`, `agent_rid`, `session_token`, `created_at`, `last_used_at`, `status`, `tool_history`.
- Retention: **7 days** maximum age; auto-cleanup triggered on tool invocation; explicit `session purge` command also available.
- Concurrent session advisory limit: **5 per agent** (logged as warning only; not enforced programmatically).

Source: [open_questions.md](open_questions.md) A4.4; [open_questions_2.md](open_questions_2.md) A(Q2(R2).8); [open_questions_3.md](open_questions_3.md) A(Q3(R3).5).

### 3.9 Attribution and Distributed Tracing

Both features are **opt-in**, disabled by default.

| Feature | Enable variable | Config variable |
| --- | --- | --- |
| Attribution | `FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION=true` | `FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS` (comma-separated RIDs) |
| Tracing | `FOUNDRY_AGENTIC_CLI_ENABLE_TRACING=true` | SDK vars: `FOUNDRY_TRACE_ID`, `FOUNDRY_SPAN_ID`, `FOUNDRY_SAMPLED` |

Attribution is injected as per-call parameter on operations that accept it (`functions.query.*`, `ontologies.query.*`, `media_sets.media_set.*`, `language_models.*`).  
Tracing generates and propagates W3C/B3 trace context for each CLI call.

Source: [open_questions_2.md](open_questions_2.md) A(Q1(R2).1); [open_questions_3.md](open_questions_3.md) A(Q2(R3).1).

---

## 4. Access Control Model

### 4.1 Three-tier Access Mode

| Tier | Mode | Description |
| --- | --- | --- |
| 1 | Full access | All read and write operations enabled (default) |
| 2 | Read-only | Write operations disabled; all reads permitted |
| 3 | Metadata-only | Only metadata reads permitted; data content reads and all writes blocked |

`METADATA_ONLY=true` implies read-only — writes are **BLOCKED** (not permitted even for structure writes).

### 4.2 8-Step Precedence Model

Evaluated in order (first match wins):

1. Operation-level `ENABLED=false` → **BLOCKED**
2. Namespace-level `ENABLED=false` → **BLOCKED**
3. Operation-level `READONLY=false` overrides global `READONLY=true` → **WRITE PERMITTED** for this operation
4. Namespace-level `READONLY=false` overrides global `READONLY=true` → **WRITE PERMITTED** for this namespace
5. Global `READONLY=true` → **ALL WRITES BLOCKED**
6. Namespace-level `METADATA_ONLY=false` overrides global `METADATA_ONLY=true` → **CONTENT READS PERMITTED** for this namespace
7. Global `METADATA_ONLY=true` → **CONTENT READS BLOCKED** + **ALL WRITES BLOCKED**
8. Default → **FULL ACCESS**

Namespace-level `READONLY=true` can also be set independently (not only as an override of global setting).

Source: [open_questions_3.md](open_questions_3.md) A(Q3(R3).3).

### 4.3 Metadata Allow-list

- Classification of operations as "metadata" vs. "data" is maintained in a `.env`-format configuration file.
- **Default stance: deny** — unclassified operations in tier-3 are blocked unless explicitly listed.
- Allow-list is an **architecture deliverable** (SA responsibility, not deferred to development).
- Must be reviewed and updated on every `foundry-sdk` minor release.

**Proposed classification (to be confirmed in allow-list deliverable):**

| Category | Tier-3 permitted? |
| --- | --- |
| Resource descriptors (`Dataset.get()`, `Branch.list()`) | Yes |
| Schema / stats (`Dataset.get_schema()`) | Yes |
| File/content reads (`read_table()`, `File.get_content()`) | No |
| Media content reads (`get_media_item_content()`) | No |
| Function results (`functions.query.*`) | No |
| AIP agent sessions (`continue_session()`) | No |
| Any write operation | No |
| Unclassified operations | No (deny by default) |

Source: [open_questions_2.md](open_questions_2.md) A(Q2(R2).5); [open_questions_3.md](open_questions_3.md) A(Q3(R3).8).

---

## 5. Configuration Reference

### 5.1 Environment Variable Naming Convention

- **SDK-native variables** (not renamed): `FOUNDRY_TOKEN`, `FOUNDRY_HOSTNAME`, `FOUNDRY_TRACE_ID`, `FOUNDRY_SPAN_ID`, `FOUNDRY_SAMPLED`
- **Project-specific prefix:** `FOUNDRY_AGENTIC_CLI_`
- **Namespace-level pattern:** `FOUNDRY_AGENTIC_CLI_{NAMESPACE}_{CONTROL}`
- **Operation-level pattern:** `FOUNDRY_AGENTIC_CLI_{NAMESPACE}_{CLASS}_{OPERATION}_{CONTROL}`
- **Transformation rule:** uppercase entire SDK path, replace dots with underscores, prefix with `FOUNDRY_AGENTIC_CLI_`
  - Example: `datasets.Dataset.upload_file` → `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_UPLOAD_FILE_ENABLED`

Source: [open_questions_2.md](open_questions_2.md) A(Q2(R2).6); [open_questions_3.md](open_questions_3.md) A(Q2(R3).1, Q3(R3).4).

### 5.2 Configuration Loading Order

1. `.env` file (primary configuration source; relative to repo root)
2. Environment variables (override; highest precedence)

### 5.3 Core Environment Variables

| Variable | Default | Description |
| --- | --- | --- |
| `FOUNDRY_TOKEN` | *(required)* | Palantir user token |
| `FOUNDRY_HOSTNAME` | *(required)* | Foundry instance hostname |
| `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT` | `auto` | Output format: `json` / `toon` / `auto` |
| `FOUNDRY_AGENTIC_CLI_READONLY` | `false` | Global read-only mode |
| `FOUNDRY_AGENTIC_CLI_METADATA_ONLY` | `false` | Global metadata-only mode |
| `FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION` | `false` | Enable attribution header injection |
| `FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS` | *(empty)* | Comma-separated attribution RIDs |
| `FOUNDRY_AGENTIC_CLI_ENABLE_TRACING` | `false` | Enable W3C/B3 trace propagation |
| `FOUNDRY_AGENTIC_CLI_RETRY_INITIAL_DELAY_MS` | TBD | Retry backoff initial delay |
| `FOUNDRY_AGENTIC_CLI_RETRY_MAX_DELAY_MS` | TBD | Retry backoff cap |
| `FOUNDRY_AGENTIC_CLI_RETRY_MULTIPLIER` | TBD | Retry backoff multiplier |
| `FOUNDRY_AGENTIC_CLI_RETRY_MAX_ATTEMPTS` | TBD | Maximum retry attempts |
| `FOUNDRY_AGENTIC_CLI_DEFAULT_PAGE_SIZE` | TBD | Default page size for list operations |
| `FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES` | 40 | Maximum pages in one batch call |
| `FOUNDRY_AGENTIC_CLI_MAX_DOWNLOAD_BYTES` | 1,572,864 (1.5 MB) | Maximum binary download size |
| `FOUNDRY_AGENTIC_CLI_DOWNLOAD_PATH` | `.foundry-data/downloads` | Base path for binary downloads |
| `FOUNDRY_AGENTIC_CLI_SESSION_PATH` | `.foundry-data/sessions` | Base path for session state |
| `FOUNDRY_AGENTIC_CLI_LOG_LEVEL` | TBD | Log verbosity |
| `FOUNDRY_AGENTIC_CLI_{NAMESPACE}_ENABLED` | `true` | Enable/disable entire namespace |
| `FOUNDRY_AGENTIC_CLI_{NAMESPACE}_READONLY` | *(inherits global)* | Namespace-level read-only override |
| `FOUNDRY_AGENTIC_CLI_{NAMESPACE}_METADATA_ONLY` | *(inherits global)* | Namespace-level metadata-only override |
| `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_ENABLED` | `true` | Enable/disable individual operation |

A canonical reference table mapping every SDK path to its full env var name (~500+ entries) is a required architecture deliverable.

---

## 6. General Foundry Skill

- **Format:** Claude Code skill, `user-invocable: false`, auto-loaded on Foundry context detection.
- **Content:** Pre-authored static markdown files — no runtime web fetch.
- **Scope:** Foundry core concepts, cross-namespace workflow recipes, authentication/configuration guidance, skill catalog, Palantir Ontology, PySpark pipeline development.
- **Authoritative source examples, the whole https://www.palantir.com site can be crawled if needed (to be distilled at authoring time):**
  - <https://www.palantir.com/docs>
  - <https://www.palantir.com/docs/foundry/building-pipelines/overview>
  - <https://www.palantir.com/docs/foundry/transforms-python-spark/overview/>
  - <https://www.palantir.com/docs/foundry/object-link-types/object-types-overview>
  - <https://www.palantir.com/docs/foundry/security/securing-a-data-foundation>
  - <https://www.palantir.com/docs/foundry/data-integration/source-type-overview>
  - <https://www.palantir.com/docs/foundry/integrate-models/integrate-overview>
  - <https://www.palantir.com/docs/foundry/ontologies/ontologies-overview/>
  - <https://www.palantir.com/docs/foundry/functions/overview>
- **Maintenance:** Content reviewed on every `foundry-sdk` minor release.

Source: [open_questions.md](open_questions.md) A2.1, A2.4; [open_questions_2.md](open_questions_2.md) A(Q2(R2).9); [open_questions_3.md](open_questions_3.md) A(Q3(R3).6).

---

## 7. Non-Functional Requirements

### 7.1 Python Version

- **Targets:** Python 3.11.x and Python 3.12.x
- Python 3.13+ requires compatibility review (deprecated features removed).

Source: [open_questions.md](open_questions.md) A5.1.

### 7.2 Deployment

- Distribution: file copy of skill folders to target repository.
- Platforms: Windows 11, macOS, Linux.
- Data paths: relative to repository root (not user home directory).
- `.foundry-data/` excluded from git via `.gitignore`.

Source: [open_questions.md](open_questions.md) A5.2; [open_questions_2.md](open_questions_2.md) A(Q2(R2).10-D).

### 7.3 Target Agent Platforms

1. VS Code with Claude agents (Claude Code skills format).
2. Custom internal agent orchestration framework (subprocess invocation, under development).

CLI interface contract: exit 0 on success, non-zero on error; structured result on stdout; diagnostics and metadata on stderr.

Source: [open_questions.md](open_questions.md) A2.2; [open_questions_2.md](open_questions_2.md) A(Q2(R2).3).

### 7.4 Code Structure

Each namespace skill has two files:

1. `foundry_{namespace}_cli.py` — namespace-specific entry point.
2. `_foundry_cli_common.py` — shared utility module (auth, async client, retry, output formatter, error serialiser, pagination, binary download, `.env` loader, access control guard) — **copied alongside each namespace file** when distributing.

Source: [open_questions_3.md](open_questions_3.md) A(Q3(R3).7-B).

---

## 8. Architecture-Phase Decisions Required (No Further Customer Input)

The following items are architect-level decisions to be recorded as ADRs:

| # | Topic | Decision needed |
| --- | --- | --- |
| 1 | Exit code taxonomy | Non-zero codes per error type (auth, permission, user error, system error, timeout) |
| 2 | Call timeout defaults | Default `asyncio.wait_for()` duration; `FOUNDRY_AGENTIC_CLI_TIMEOUT_S` value |
| 3 | Streams namespace | Batch-response vs. streaming handle strategy |
| 4 | `--format auto` logic | Exact algorithm for selecting TOON vs. JSON when format is auto |
| 5 | Log format | Structured JSON fields required on stderr log entries |
| 6 | `.env` search path order | File paths probed and priority (local dir → repo root → home dir?) |
| 7 | Op-level `READONLY=true` | Whether independent operation-level READONLY (not override) is supported |

---

## 9. Architecture Deliverables

| Deliverable | Description | Owner |
| --- | --- | --- |
| Requirements Document | Full SRS tracing all decisions to source Q&A | Architect |
| Architecture Design Document (SAD) | C4/C5 diagrams, component design, sequence diagrams | Architect |
| ADRs | One per major technology/design decision (items above) | Architect |
| Canonical env var reference table | ~500+ entries: SDK path → env var name | Architect |
| Metadata allow-list | `.env`-format operation classification for all 20 namespaces | Architect |

---

## 10. Completeness Assessment

**Status: Ready to proceed with Requirements Document and Architecture Design.**

All three rounds of open questions (25 + 12 + 10 = 47 questions, 80+ sub-questions) have been fully answered by the Product Owner. No blocking ambiguities remain. Architecture-phase decisions listed in Section 8 are resolvable by the Solution Architect without further customer input.

| Round | Document | Questions | Status |
| --- | --- | --- | --- |
| 1 | [open_questions.md](open_questions.md) | 25 | All answered |
| 2 | [open_questions_2.md](open_questions_2.md) | 12 | All answered |
| 3 | [open_questions_3.md](open_questions_3.md) | 10 | All answered (QUESTION-001 closed 2026-04-10) |

See ticket **FEATURE-001**, comment `20260410-013318-architect` for the assessment log entry.
