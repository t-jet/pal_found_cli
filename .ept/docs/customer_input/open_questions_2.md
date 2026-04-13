# Open Questions — Foundry CLI Agent Skill (Round 2)

**Purpose:** Follow-up questions arising from analysis of answers in `open_questions.md` and additional SDK/format research.  
**Date:** 2026-04-09  
**Author:** Solution Architect  
**Predecessor:** [open_questions.md](open_questions.md)

---

## Background Context

All 25 questions from Round 1 were reviewed against the provided answers (A1.1–A6.5). This document captures:

1. **Section 1** — Two items from Round 1 that remain explicitly open or uncertain.
2. **Section 2** — New questions arising from the answers and supporting research performed on the SDK source and referenced formats/libraries.

Supporting research performed before authoring this document:

- SDK analysis of `ATTRIBUTION_VAR`, `TRACE_ID_VAR`, `SPAN_ID_VAR` in `foundry_sdk/_core/context_and_environment_vars.py` and `foundry_sdk/v2/core/models.py`.
- Review of the official TOON Python implementation (`toon-format/toon-python`) and its PyPI/stability status.
- Review of Claude Code Skills specification at `code.claude.com/docs/en/skills`.

---

## Section 1 — Carry-Over: Still-Open Items from Round 1

### Q1(R2).1 — Attribution and distributed-trace context injection  *(follows up on Q3.4)*

**Research findings since Q3.4:**

From the SDK source:

| Variable | Type | Purpose |
| --- | --- | --- |
| `ATTRIBUTION_VAR` | `ContextVar[Optional[list[str]]]` | Holds a list of Foundry resource RIDs joined into a comma-separated HTTP request header that Foundry uses to attribute API calls for billing/cost allocation. |
| `TRACE_ID_VAR` / `SPAN_ID_VAR` / `SAMPLED_VAR` | `ContextVar[Optional[str]]` | Standard distributed-tracing propagation headers (B3/W3C-compatible). Forwarded by the SDK to Foundry's backend for internal observability. |

`Attribution` itself is `str` (a RID or comma-separated RIDs). The `InvalidAttributionHeader` error is raised if the value cannot be parsed to a valid RID.  
Attribution is accepted as a **per-call parameter** (not global) in: `functions.query.*`, `ontologies.query.*`, `media_sets.media_set.*`, `language_models.*`.

**Questions requiring an answer:**

- **A)** Should CLI-wrapped API calls inject attribution headers to identify them as agent-initiated? If yes, what RID(s) should be used?
  - *Implication:* Requires a Foundry project or resource RID to be provided at configuration time, adding a new required/optional environment variable.
- **B)** Should the CLI generate and propagate W3C/B3 trace context (`TRACE_ID`, `SPAN_ID`) for operations, or is trace propagation out of scope?
  - *Implication:* If enabled, the tool would emit structured trace metadata on stderr/stdout for each call, enabling correlation in Foundry audit logs.
- **C)** If attribution or tracing is required, should it be opt-in (disabled by default, enabled via env var) or opt-out?

> Attribution and tracing are orthogonal to NFR-01–03 requirements but affect compliance, cost visibility, and auditability of agent-initiated Foundry API calls. A deliberate decision is needed before finalising the CLI's HTTP call layer.


**Answers:**
- A) Attribution should be injected to identify agent-initiated calls if the RID(s) used for attribution is provided via a new environment variable, e.g., `FOUNDRY_CLI_ATTRIBUTION_RIDS`, which can accept a comma-separated list of RIDs.
- B) Trace context propagation should be implemented to enable correlation in Foundry audit logs. The CLI should generate and propagate W3C/B3 trace context (`TRACE_ID`, `SPAN_ID`) for operations.
- C) Both attribution and tracing should be opt-in features, disabled by default and enabled via environment variables (e.g., `FOUNDRY_CLI_ENABLE_ATTRIBUTION=true`, `FOUNDRY_CLI_ENABLE_TRACING=true`), to allow users to choose based on their compliance and observability needs.


---

### Q1(R2).2 — `AsyncFoundryClient` adoption decision  *(follows up on Q5.3)*

A5.3 acknowledges uncertainty: *"Not sure about it. There are no benefit from performance point of view, but calling async interfaces can help with setting timeouts for tools which can be useful and with supporting graceful exit in case of forced termination to report correct status."*

**A clear architectural decision is required** because the choice determines the internal client type, signal-handling approach, and timeout enforcement throughout all 20 namespace wrappers.

- **A)** Use **synchronous `FoundryClient` only**: Simpler implementation; subprocess timeout enforced externally by the agent/shell. No graceful-exit reporting from within the tool.
- **B)** Use **`AsyncFoundryClient` internally** with `asyncio.run()` at the CLI boundary: Enables per-call `asyncio.wait_for()` timeouts, clean `SIGINT`/`SIGTERM` handlers, and structured status reporting on forced termination. Adds moderate complexity.
- **C)** Expose **both** sync and async paths (one CLI, two internal execution modes, selectable via env var/flag): Maximally flexible but doubles testing burden for 20 namespaces.

> **Recommended default to evaluate**: Option B — async internally, sync CLI surface — for timeout enforcement and graceful shutdown without agent-side complexity.

**Answer:**
- B) The CLI should use `AsyncFoundryClient` internally with `asyncio.run()` at the CLI boundary. This approach allows for better timeout management and graceful exit handling, which can improve the robustness of the tools when integrated with agents that may enforce time limits on tool execution. While it adds some complexity compared to a purely synchronous implementation, the benefits in terms of reliability and user experience are significant.

---

## Section 2 — New Questions Arising from Answers

### Q2(R2).1 — TOON Python library stability and adoption risk  *(from A4.1)*

A4.1 specifies TOON as the preferred output format with JSON fallback.

**Research finding:** The official Python library `toon-python` (PyPI package `toon_format`) is currently at **v0.9.0-beta.1**:

- Status: beta — *"working towards spec compliance; API may change before 1.0.0 release."*
- Install: only via `pip install git+https://github.com/toon-format/toon-python.git` (not a stable PyPI release yet).
- Coverage: 91%, 792 tests; roadmap targets v1.0.0-rc for production readiness.

**Questions:**

- **A)** Given the beta status, should the project:
  - **Accept the beta dependency** (fastest to implement, risk of breaking API changes before 1.0)?
  - **Implement a minimal internal TOON encoder** covering TOON's most useful pattern (uniform arrays of objects → tabular notation)? This covers the primary Foundry list-operation output shape and avoids external beta dependency.
  - **Defer TOON support until the library reaches 1.0.0**, using JSON for all outputs in the interim?
- **B)** If the beta library is accepted, should it be pinned to an exact commit SHA (for reproducibility) and updated manually, or accepted with a semver range `>=0.9,<1.0`?

**Answer:**
- B) Pin to semver range.

---

### Q2(R2).2 — TOON output applicability criteria  *(from A4.1)*

A4.1 says TOON "where applicable or JSON if TOON doesn't match." The applicability boundary must be defined explicitly so all 20 namespace wrappers apply it consistently.

TOON's own documentation identifies three structural patterns:

| Data structure | TOON suitability | Recommendation |
| --- | --- | --- |
| Uniform arrays of objects (list API responses) | Excellent (30–60% token saving) | TOON |
| Single objects / deeply nested structures (get API responses) | Marginal (JSON compact may be smaller) | JSON |
| Binary / streaming data (returned as file path) | N/A | Plain text path only |
| Error/exception objects | Must be parseable JSON for agent interpretation (Q4.3) | Always JSON |

**Proposed rule (requires confirmation):**

> Use TOON when: the top-level result is a list/array AND all items share a uniform field set.  
> Use JSON in all other cases (single objects, heterogeneous arrays, errors, pagination metadata).

- **A)** Is the proposed rule acceptable?
- **B)** Should the chosen format be declared in a response envelope field (e.g., `"format": "toon"` / `"format": "json"`) so consuming agents know which decoder to use?

**Answers:**
- A) The proposed rule is acceptable and provides a clear guideline for when to use TOON versus JSON, ensuring consistency across all namespace wrappers.
- B) Yes, including a `"format"` field in the response envelope is a good practice as it allows consuming agents to easily determine which decoder to use for the output, improving robustness and flexibility in handling different response formats.

---

### Q2(R2).3 — Custom internal agent orchestration framework interface  *(from A2.2)*

A2.2 names two target platforms: **VS Code with Claude agents** (Claude Code skills — format confirmed from documentation) and **custom internal agent orchestration framework** (unspecified).

The CLI tool interface — argument style, exit codes, stdout/stderr split, streaming vs. batch output, authentication credential handoff — must be designed to work with both platforms.

**Questions:**

- **A)** What is the name or reference documentation for the custom internal orchestration framework?
- **B)** How does it invoke CLI tools? (subprocess call, Python import, REST endpoint, other?)
- **C)** Does it impose any specific contracts on:
  - Exit codes (0 = success, 1 = user error, 2 = system error — or different convention)?
  - stdout vs. stderr usage (structured result on stdout, diagnostics on stderr)?
  - Response envelope schema (is a wrapper with `"status"`, `"result"`, `"error"` fields required)?
  - Maximum response size or streaming requirements?

> Without this information, the CLI interface may need to be redesigned after implementation.

**Answers:**
- A) The custom internal orchestration framework is currently under development and does not have publicly available documentation. It is designed to invoke CLI tools via subprocess calls, similar to how agents typically execute external commands.
- B) The framework invokes CLI tools using subprocess calls, allowing for language-agnostic integration and flexibility in how tools are implemented.
- C) No specific conventions. However, it is recommended to follow common CLI practices:
  - Exit codes: 0 for success, non-zero for errors (with specific codes for different error types if needed).
  - stdout for structured results (in TOON or JSON format), stderr for logging and diagnostics.
  - A consistent response envelope with fields like `"status"`, `"result"`, and `"error"` can improve clarity and ease of parsing for consuming agents, but is not strictly required by the framework.

---

### Q2(R2).4 — Enable/disable granularity for wrappers  *(from A1.3)*

A1.3 specifies: *"CLI Wrappers should support configuration provided in .env files or environment variables which will enable/disable specific wrappers."*

The 20 SDK namespaces contain hundreds of individual operations (e.g., `datasets` alone has ~25 operations). The schema of control environment variables needs to be defined.

**Questions:**

- **A)** What is the granularity level?
  - **Namespace-level only** (e.g., `FOUNDRY_CLI_DATASETS_ENABLED=false` disables all dataset operations)?
  - **Operation-level** (e.g., `FOUNDRY_CLI_DATASETS_UPLOAD_FILE_ENABLED=false` disables a specific call)?
  - **Both hierarchical** (namespace default with per-operation override)?
- **B)** If operation-level control is required, can the operation identifier use the SDK method path (e.g., `datasets.Dataset.upload_file`) or should a shorter alias be defined?

**Answers:**

- A) Both hierarchical: a namespace-level variable can enable/disable the entire namespace, while individual operation-level variables can override the namespace default for specific operations.
- B) Using the SDK method path (e.g., `datasets.Dataset.upload_file`) is recommended for clarity and direct mapping to the underlying SDK calls, but shorter aliases can be supported for convenience if they are well-documented and consistently applied.

---

### Q2(R2).5 — "Metadata-only" read-only mode: boundary definition  *(from A1.4)*

A1.4 introduces a three-tier access control model:

1. **Full access** — all read and write operations enabled.
2. **Read-only** — write operations disabled; all reads permitted.
3. **Metadata-only read** — only metadata reads permitted; no binary/dataset content reads.

The boundary between "metadata" and "data" must be defined unambiguously for each namespace, as it determines which operations are blocked in tier 3.

**Proposed classification (requires confirmation):**

| Category | Examples | Tier-3 permitted? |
| --- | --- | --- |
| Resource descriptors | `datasets.Dataset.get()`, `datasets.Branch.list()` | Yes |
| Schema / stats | `datasets.Dataset.get_schema()` | Yes |
| File/content reads | `datasets.Dataset.read_table()`, `datasets.File.get_content()` | **No** |
| Media content reads | `media_sets.MediaSet.get_media_item_content()` | **No** |
| Function results | `functions.query.*` | **No** (data output) |
| AIP agent sessions | `aip_agents.Agent.Session.continue_session()` | **No** (live inference) |

**Questions:**

- **A)** Is the proposed classification correct?
- **B)** Should the list be defined once centrally (allow-list maintained in configuration or code) or inferred automatically from operation naming conventions (e.g., any operation whose name contains `get_content`, `read_table`, `download`, `stream`)?

**Answers:**
- A) The proposed classification is generally correct, but it may require adjustments based on specific operations within each namespace. A detailed review of all operations should be conducted to ensure accurate classification.
- B) It should be maintained in configuration. Automatic inference based on naming conventions can be error-prone and may not capture all edge cases, whereas a centrally maintained allow-list can be explicitly reviewed and updated as needed to ensure accuracy and security.

---

### Q2(R2).6 — Environment variable naming convention  *(from multiple answers)*

The following categories of environment variables have been identified based on all answers:

| Category | Example variables | Count estimate |
| --- | --- | --- |
| Auth | `FOUNDRY_TOKEN`, `FOUNDRY_HOSTNAME` | 2 |
| Namespace enable/disable | `FOUNDRY_CLI_DATASETS_ENABLED` | 20 |
| Namespace read-only mode | `FOUNDRY_CLI_DATASETS_READONLY` | 20 |
| Metadata-only mode | `FOUNDRY_CLI_DATASETS_METADATA_ONLY` | 20 |
| Attribution (if required) | `FOUNDRY_CLI_ATTRIBUTION_RIDS` | 1 |
| Tracing (if required) | `FOUNDRY_TRACE_ID` (already SDK standard) | 3 |
| Retry policy | `FOUNDRY_CLI_RETRY_INITIAL_DELAY_MS`, `FOUNDRY_CLI_RETRY_MAX_DELAY_MS`, `FOUNDRY_CLI_RETRY_MULTIPLIER`, `FOUNDRY_CLI_RETRY_MAX_ATTEMPTS` | 4 |
| Pagination defaults | `FOUNDRY_CLI_DEFAULT_PAGE_SIZE`, `FOUNDRY_CLI_MAX_BATCH_PAGES` | 2 |
| Binary output | `FOUNDRY_CLI_DOWNLOAD_PATH` | 1 |
| Session storage | `FOUNDRY_CLI_SESSION_PATH` | 1 |
| Logging | `FOUNDRY_CLI_LOG_LEVEL` | 1 |

**Total: ~75+ environment variables.**

**Questions:**

- **A)** Is the prefix `FOUNDRY_CLI_` acceptable for all project-specific variables (distinguishing them from the SDK's own `FOUNDRY_TOKEN`/`FOUNDRY_HOSTNAME`/`FOUNDRY_TRACE_ID`)?
- **B)** For namespace-specific variables, is the pattern `FOUNDRY_CLI_{NAMESPACE}_{CONTROL}` (e.g., `FOUNDRY_CLI_DATASETS_READONLY=true`) acceptable?
- **C)** Should a `.env` file be the **primary** configuration source with environment variables as override, or should both be treated as equally primary?
- **D)** Should a single env var enable all-namespace read-only (e.g., `FOUNDRY_CLI_READONLY=true`) which can then be overridden per namespace?

**Answers:**

- A) Use the more specific prefix `FOUNDRY_AGENTIC_CLI_` to clearly distinguish from SDK environment variables and avoid potential naming conflicts.
- B) The pattern `FOUNDRY_AGENTIC_CLI_{NAMESPACE}_{CONTROL}` is acceptable and provides a clear, consistent naming convention for namespace-specific configuration.
- C) A `.env` file should be the primary configuration source for ease of use in development environments, with environment variables taking precedence as overrides for flexibility in different deployment contexts (e.g., CI/CD pipelines, production environments).
- D) Yes, a single env var like `FOUNDRY_AGENTIC_CLI_READONLY=true` can enable read-only mode globally, with the ability to override it for specific namespaces using `FOUNDRY_AGENTIC_CLI_{NAMESPACE}_READONLY=false` for exceptions. The same should apply for metadata-only mode with `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` and per-namespace overrides.

---

### Q2(R2).7 — Binary download path and file naming convention  *(from A1.5)*

A1.5 states binary/streaming data should be written to *"a safe dedicated local path inside the repository excluded from source tracking using .gitignore."*

**Questions:**

- **A)** What should the default download path be? Proposed: `<repo-root>/.foundry-data/downloads/` (excluded via `.gitignore`). Acceptable?
- **B)** How should downloaded files be named to avoid collisions across concurrent agent sub-tasks?
  - Proposed: `{namespace}_{operation}_{resource-rid}_{timestamp}.{ext}` (e.g., `datasets_read_table_ri.foundry.main.dataset.abc123_20260409T123456.parquet`).
  - Is the RID-based naming acceptable, or should UUIDs be preferred?
- **C)** Should the tool return **only the file path** on stdout, or also include file size, checksum (MD5/SHA-256), and MIME type in the response envelope for the agent to validate the download?
- **D)** Is there a maximum file size limit beyond which the tool should refuse to download and return an error instead?

**Answers:**

- A) The proposed default download path of `<repo-root>/.foundry-data/downloads/` is acceptable, ensuring it is excluded from source tracking via `.gitignore`.
- B) Use folders with UUID names to distinguish between downloads. The file name should be the original file name provided by Foundry, or a sanitized version of it, to preserve context about the content. For example: `<repo-root>/.foundry-data/downloads/{uuid}/{original_file_name}`. This approach avoids collisions while maintaining traceability to the original content. If the original file name is not available, a fallback naming convention can be used: `{namespace}_{operation}_{timestamp}.{ext}`.
- C) The tool should return the file path on stdout, and include file size, checksum (MD5/SHA-256), and MIME type in the response envelope for validation purposes.
- D) A maximum file size limit should be configurable, and the tool should return an error if the limit is exceeded. Default limit should be 1.5 MB .

---

### Q2(R2).8 — Multi-turn session state: persistence model and lifecycle  *(from A4.4)*

A4.4 states sessions should be stored in files in a dedicated folder excluded from source tracking.

**Questions:**

- **A)** What state must be persisted to resume a session?
  - *Proposed minimum:* `session_id`, `agent_rid` (for AIP Agents), `session_token` or context handle returned by the SDK, `created_at`, `last_used_at`, tool invocation log.
  - Are there additional fields required (e.g., pagination cursors, intermediate results)?
- **B)** What is the session **retention policy**?
  - Maximum age before automatic cleanup (e.g., 24 h, 7 days)?
  - Maximum number of concurrent sessions per agent?
  - Should cleanup be triggered automatically on tool invocation, or only via an explicit `session purge` command?
- **C)** How are sessions identified from the CLI? By:
  - **Auto-generated UUID** returned on session creation (agent must remember it)?
  - **Named alias** provided by the agent at creation time?
  - **${CLAUDE_SESSION_ID}** from the Claude Code skill environment variable?
- **D)** What should the default session storage path be? Proposed: `<repo-root>/.foundry-data/sessions/`. Acceptable?

**Answers:**

- A) The proposed minimum fields for session persistence are appropriate. Additionally, it may be beneficial to include a `status` field to indicate whether the session is active, completed, or expired, and a `tool_history` field to log the sequence of tool invocations and their outcomes within the session.
- B) The session retention policy should include a maximum age of 7 days before automatic cleanup, and a maximum of 5 concurrent sessions per agent. Cleanup should be triggered automatically on tool invocation to ensure stale sessions do not accumulate, with an additional explicit `session purge` command available for manual cleanup.
- C) Sessions should be identified by a **named alias** provided by the agent at creation time, as this allows for easier reference and management by the agent. The alias can be mapped to the underlying `session_id` in the storage layer for retrieval.
- D) The proposed default session storage path of `<repo-root>/.foundry-data/sessions/` is acceptable, ensuring it is excluded from source tracking via `.gitignore`.

---

### Q2(R2).9 — General Foundry knowledge skill: content scope and invocation mode  *(from A2.4)*

A2.4 specifies: *"one general skill which covers general knowledge about Foundry and aware about other skills and how to combine them to solve questions."*

**Questions:**

- **A)** What **domain knowledge** should the general skill contain?
  - Foundry core concepts (datasets, ontologies, pipelines, resources, RIDs, branches)?
  - Cross-namespace workflow recipes (e.g., "to query an ontology object, use `ontologies` to get the type, then `sql_queries` to run a query")?
  - Authentication and configuration guidance?
  - Skill catalog (names, descriptions, and usage hints for the other 20 namespace skills)?
  - All of the above?
- **B)** Should this skill be **auto-loaded by Claude** when any Foundry-related context is detected (`user-invocable: false`, no `disable-model-invocation`), or should it require explicit invocation via `/foundry` or similar?
- **C)** Is there an existing Foundry platform documentation source (internal wiki, Confluence, README) that should be used as the authoritative content for this skill, or should it be authored from scratch based on the SDK and public API docs?

**Answers:**

- A) The general skill should contain all of the above domain knowledge to provide comprehensive support for users interacting with Foundry. This includes core concepts, cross-namespace workflow recipes, authentication and configuration guidance, and a catalog of the other namespace skills with descriptions and usage hints. In addition it should be supplemented with knowledge about Palantir Ontology concepts and PySpark pipelines development, as these are common areas of user inquiry that can be addressed with the CLI tools.
- B) The skill should be auto-loaded by Claude when any Foundry-related context is detected, with `user-invocable: false` and no `disable-model-invocation`, to ensure that users have access to this foundational knowledge whenever they are working with Foundry-related tasks. This allows for seamless support without requiring explicit invocation, while still making the information readily available when needed.
- C) Use publicly available documentation sources as the authoritative content for this skill, such as the official Foundry API documentation, SDK documentation, and any relevant public resources. Example pages are:
  - https://www.palantir.com/docs 
  - https://www.palantir.com/docs/foundry/building-pipelines/overview
  - https://www.palantir.com/docs/foundry/transforms-python-spark/overview/
  - https://www.palantir.com/docs/foundry/object-link-types/object-types-overview
  - https://www.palantir.com/docs/foundry/security/securing-a-data-foundation
  - https://www.palantir.com/docs/foundry/data-integration/source-type-overview
  - https://www.palantir.com/docs/foundry/integrate-models/integrate-overview
  - https://www.palantir.com/docs/foundry/ontologies/ontologies-overview/
  - https://www.palantir.com/docs/foundry/functions/overview

---

### Q2(R2).10 — Skill repository structure and placement  *(from A6.3)*

A6.3 states: *"Toolset code should reside inside the skills folders in the repository."*  
A2.1 confirms the format is Claude Code skills (`.claude/skills/<skill-name>/SKILL.md`).

**Questions:**

- **A)** Confirm the following target folder structure is acceptable:

  ```text
  <repo-root>/
  └── .claude/
      └── skills/
          ├── foundry/                   # General Foundry knowledge skill
          │   └── SKILL.md
          ├── foundry-admin/             # admin namespace
          │   ├── SKILL.md
          │   └── scripts/
          │       └── foundry_admin_cli.py
          ├── foundry-datasets/          # datasets namespace
          │   ├── SKILL.md
          │   └── scripts/
          │       └── foundry_datasets_cli.py
          ├── ...                        # (one per namespace — 20 total)
          └── foundry-widgets/           # widgets namespace
              ├── SKILL.md
              └── scripts/
                  └── foundry_widgets_cli.py
  ```

- **B)** Should each namespace skill's `SKILL.md` embed the installation instructions for `foundry-platform-sdk` (from PyPI), or should a shared `CLAUDE.md` or `foundry/SKILL.md` file handle SDK installation once?
- **C)** Should the Python CLI scripts be self-contained single-file modules per namespace, or share a common utility library (`foundry_cli_shared/`)? If shared, where does the shared code live within the `.claude/skills/` hierarchy?
- **D)** When distributed to target repositories via file copy, should the `.foundry-data/` path (for downloads and sessions) be relative to the repository root (where the agent checks out), or should it default to a user home directory path (`~/.foundry-data/`) to be shared across repositories?


**Answers:**

- A) The proposed folder structure is acceptable and provides a clear organization for the skills and their associated CLI scripts. Each namespace has its own subfolder under `.claude/skills/`, which allows for modular development and maintenance.
- B) Each `SKILL.md` file should handle the installation instructions for `foundry-platform-sdk` to ensure that each skill is self-contained and can be easily understood and set up by users who may only be interested in specific namespaces.
- C) They should be self-contained single-file modules per namespace to minimize coupling and simplify distribution.
- D) The `.foundry-data/` path should be relative to the repository root to ensure that all data generated by the CLI tools is contained within the context of the specific repository and can be easily managed and cleaned up as part of the repository's lifecycle. This also avoids potential conflicts and security concerns that could arise from sharing a common directory across multiple repositories.
---

## Summary Priority Matrix

| # | Question | Blocks | Impact if not answered |
| --- | --- | --- | --- |
| Q1(R2).1 | Attribution / trace injection | Architecture of HTTP call layer | Compliance/audit gap in agent-initiated calls |
| Q1(R2).2 | Async vs. sync client decision | Internal client architecture | Wrong choice doubles refactoring cost across 20 namespaces |
| Q2(R2).1 | TOON library stability | Output format implementation | Build dependency on unstable beta, or unexpected re-implementation work |
| Q2(R2).2 | TOON applicability criteria | Output format contract | Inconsistent output across namespace skills |
| Q2(R2).3 | Orchestration framework interface | CLI interface design | Interface incompatible with consumer after implementation |
| Q2(R2).4 | Enable/disable granularity | Env-var schema design | Either too coarse (namespace only) or impractical (hundreds of vars) |
| Q2(R2).5 | Metadata-only mode boundary | Access control implementation | Incorrect classification causes data leaks or over-blocking |
| Q2(R2).6 | Env-var naming convention | All configuration | 75+ vars with no consistent naming leads to unusable config surface |
| Q2(R2).7 | Binary download path/naming | File I/O for binary ops | Filename collisions in parallel agent runs; missing checksum validation |
| Q2(R2).8 | Session persistence model | Multi-turn session implementation | Unresumable sessions, unbounded session storage growth |
| Q2(R2).9 | General skill content scope | General skill authoring | Under-specified skill provides no value; over-specified wastes context budget |
| Q2(R2).10 | Skill repository structure | Project scaffolding | Wrong structure requires redistribution to all target repos |
