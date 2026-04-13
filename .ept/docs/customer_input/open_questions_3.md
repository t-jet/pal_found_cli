# Open Questions — Foundry CLI Agent Skill (Round 3)

**Purpose:** Follow-up questions arising from analysis of answers in `open_questions_2.md`.  
**Date:** 2026-04-10  
**Author:** Solution Architect  
**Predecessor:** [open_questions_2.md](open_questions_2.md)

---

## Background Context

All 12 questions from Round 2 were reviewed against inline answers. This document contains:

1. **One unanswered sub-question** left incomplete in Round 2.
2. **One direct contradiction** between two answers in the same document that must be reconciled.
3. **Eight new questions** arising from ambiguities or design conflicts in the provided answers.

No external research was required for this round — all gaps stem solely from the Round 2 answers themselves.

---

## Section 1 — Incomplete Answer from Round 2

### Q1(R3).1 — TOON adoption decision: sub-question A was not answered  *(from Q2(R2).1)*

Question Q2(R2).1 had two distinct sub-questions:

- **A)** Which adoption option should be taken — Accept the beta dependency / Implement a minimal internal encoder / Defer until v1.0?
- **B)** If the beta is accepted, pin by commit SHA or by semver range?

The provided answer addressed only **B)** ("Pin to semver range"), leaving **A)** completely unanswered. Answering B implies accepting the beta, but this has not been explicitly confirmed.

This matters because:

- **Accept beta**: Take a dependency on `pip install git+https://github.com/toon-format/toon-python.git` with `>=0.9,<1.0`. Fastest to implement but introduces an install-from-GitHub dependency that may require air-gap / private mirror handling in restricted environments.
- **Minimal internal encoder**: Implement ~100–200 lines of Python covering uniform-array tabular encoding only. No external beta dependency; immune to upstream API changes; covers the primary Foundry list-response pattern. Adds ~1 sprint of implementation effort.
- **Defer**: Use JSON for all outputs until `toon_format` reaches v1.0.0. Zero risk but misses the token-efficiency benefit specified in A4.1.

**Required answer:** Please select one of the three options above explicitly.

**Answer:**

Accept the beta dependency — take a dependency on `pip install git+https://github.com/toon-format/toon-python.git` and pin to the `>=0.9,<1.0` semver range. Air-gap / private mirror handling (if required in restricted environments) is acknowledged as a future operational concern.

---

## Section 2 — Contradiction Requiring Reconciliation

### Q2(R3).1 — Environment variable prefix conflict  *(Q1(R2).1 answers vs Q2(R2).6-A answer)*

Two answers in `open_questions_2.md` use different prefixes for the same project's environment variables:

| Source | Env vars referenced | Prefix used |
| --- | --- | --- |
| Q1(R2).1 answer (attribution/tracing) | `FOUNDRY_CLI_ATTRIBUTION_RIDS`, `FOUNDRY_CLI_ENABLE_ATTRIBUTION`, `FOUNDRY_CLI_ENABLE_TRACING` | `FOUNDRY_CLI_` |
| Q2(R2).6 answer A (naming convention) | `FOUNDRY_AGENTIC_CLI_` mandated as the standard prefix for all project-specific variables | `FOUNDRY_AGENTIC_CLI_` |

These are directly contradictory. Q1(R2).1 was answered before Q2(R2).6, so the attribution/tracing variable names need to be updated to use the agreed prefix.

**Proposed resolution (requires confirmation):**

The following variable names should use the `FOUNDRY_AGENTIC_CLI_` prefix established in Q2(R2).6:

| Old name (from Q1R2.1 answer) | Corrected name |
| --- | --- |
| `FOUNDRY_CLI_ATTRIBUTION_RIDS` | `FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS` |
| `FOUNDRY_CLI_ENABLE_ATTRIBUTION` | `FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION` |
| `FOUNDRY_CLI_ENABLE_TRACING` | `FOUNDRY_AGENTIC_CLI_ENABLE_TRACING` |

The SDK's own tracing context variables (`FOUNDRY_TRACE_ID`, `FOUNDRY_SPAN_ID`, `FOUNDRY_SAMPLED`) retain their SDK-defined names and are not renamed.

**Is this correction acceptable?**

**Answer:**

Yes — the proposed renaming is confirmed. All three attribution/tracing environment variables must use the `FOUNDRY_AGENTIC_CLI_` prefix: `FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS`, `FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION`, `FOUNDRY_AGENTIC_CLI_ENABLE_TRACING`. The SDK's own variables (`FOUNDRY_TRACE_ID`, `FOUNDRY_SPAN_ID`, `FOUNDRY_SAMPLED`) retain their SDK-defined names without modification.

---

## Section 3 — New Questions Arising from Round 2 Answers

### Q3(R3).1 — Default file size limit of 1.5 MB appears too low  *(from Q2(R2).7-D)*

The answer specifies a **default maximum file size of 1.5 MB** for binary downloads.

This limit is very likely to be exceeded in normal Foundry usage:

| Operation | Typical file size |
| --- | --- |
| Parquet dataset export (`read_table`) | 50 MB – 10 GB+ |
| Compressed Arrow file | 5 MB – 1 GB+ |
| Media item (image/video) | 1 MB – 500 MB+ |
| Pipeline output artifact | 10 MB – 1 GB+ |

At 1.5 MB, nearly every real-world binary download would return an error rather than content.

**Questions:**

- **A)** Was the intended limit **1.5 GB** rather than 1.5 MB? If so, please confirm.
- **B)** If 1.5 MB is intentional, what is the use case for such a restrictive limit — and should agent operators routinely be expected to increase it via env var for most operations?
- **C)** When the limit is exceeded, should the tool:
  - Return an error immediately with the actual file size and the configured limit?
  - Return partial content up to the limit with a truncation warning?
  - Provide a streaming / chunked mode where the agent can read in segments?

**Answers:**

- **A)** The 1.5 MB default limit is **intentional** — it is a default security setting for the default environment for single dataset file downloads. Agent operators are expected to increase this limit via env var for production use cases requiring larger file transfers.
- **B)** Use case: the 1.5 MB limit acts as a conservative safe default to prevent accidental large data transfers in environments where the limit has not been explicitly reviewed and raised.
- **C)** When the limit is exceeded: **return partial content up to the configured limit with a truncation warning**, indicating that the response was truncated, the configured limit, and the actual file size.

---

### Q3(R3).2 — Response envelope schema: TOON and JSON cannot both be the top-level output format  *(from Q2(R2).2-B, Q2(R2).3-C, Q2(R2).7-C)*

Multiple answers reference a **response envelope** containing metadata fields, but none define its format in relation to TOON output:

| Answer | Field(s) mentioned |
| --- | --- |
| Q2(R2).2-B | `"format": "toon"` or `"format": "json"` field in envelope |
| Q2(R2).3-C | Optional `"status"`, `"result"`, `"error"` wrapper |
| Q2(R2).7-C | File path, file size, checksum (MD5/SHA-256), MIME type in envelope |

A JSON envelope is a JSON object. TOON is a distinct text format. These cannot both be the literal `stdout` output of a single command without a defined nesting strategy.

The three possible resolution strategies (each has different trade-offs):

**Option A — JSON envelope always, TOON/JSON result nested as a string field:**

```json
{
  "format": "toon",
  "status": "success",
  "result": "users[3]{id,name,role}:\n  1,Alice,admin\n  2,Bob,user\n  3,Carol,viewer"
}
```

- Pro: Always parseable as JSON; format field is unambiguous.
- Con: The TOON content must be string-escaped (newlines as `\n`, etc.), removing its human-readability advantage. Agents must parse JSON then decode the inner TOON string manually.

**Option B — TOON or JSON raw output (no envelope), format indicated by exit code and content-type header on stderr:**

```text
users[3]{id,name,role}:
  1,Alice,admin
  2,Bob,user
  3,Carol,viewer
```

- Pro: Maximum token efficiency; no escaping overhead.
- Con: Metadata (format, pagination cursor, status) cannot be conveyed in the same stream.

**Option C — Split stdout / stderr: structured result on stdout, metadata JSON envelope on stderr:**

- stdout: raw TOON or JSON result.
- stderr: `{"format":"toon","status":"success","page_token":"abc","total_count":42}`.
- Pro: Preserves raw format efficiency; metadata available on separate channel.
- Con: Many subprocess wrappers merge stdout and stderr; orchestration frameworks must support separate capture.

**Questions:**

- **A)** Which option (A, B, C, or another approach) should be used?
- **B)** For binary downloads specifically (Q2(R2).7-C): the response must include both a file path and a JSON envelope with checksum/MIME type. Given the file content is written to disk, the CLI only outputs the envelope to stdout — confirming this is always JSON (not TOON) regardless of which option above is chosen?

**Answers:**

- **A)** Option B — raw TOON or JSON output on stdout with no envelope. The format is determined by the `--format` flag or `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT` env var. Metadata (pagination cursor, total count, status) is conveyed on stderr as a compact JSON object. This maximises token efficiency and avoids double-escaping TOON content inside a JSON string field.
- **B)** Yes — binary downloads always output a JSON envelope to stdout (containing file path, file size, checksum, and MIME type), regardless of the output format setting. The file content itself is written to disk only and never emitted to stdout.

---

### Q3(R3).3 — Access control precedence: global vs. namespace override interaction  *(from Q2(R2).6-D)*

The answer to Q2(R2).6-D establishes a two-level hierarchy:

- Level 1 (global): `FOUNDRY_AGENTIC_CLI_READONLY=true` / `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true`
- Level 2 (namespace): `FOUNDRY_AGENTIC_CLI_{NAMESPACE}_READONLY=false` (override to re-enable writes)

Combined with Q2(R2).4-A's hierarchical enable/disable:

- `FOUNDRY_AGENTIC_CLI_{NAMESPACE}_ENABLED=false` — disables entire namespace
- `FOUNDRY_AGENTIC_CLI_{NAMESPACE}_{OPERATION}_ENABLED=false` — disables a single operation

The interactions between these four dimension types (ENABLED, READONLY, METADATA\_ONLY at global, namespace, and operation levels) create up to 12 independent control variables per namespace. The effective access state for any operation under conflicting settings is undefined.

**Proposed precedence model (requires confirmation):**

Evaluated in this order (first match wins):

1. Operation-level `ENABLED=false` → **BLOCKED**
2. Namespace-level `ENABLED=false` → **BLOCKED**
3. Operation-level `READONLY=false` overrides global `READONLY=true` → **WRITE PERMITTED** for this operation
4. Namespace-level `READONLY=false` overrides global `READONLY=true` → **WRITE PERMITTED** for this namespace
5. Global `READONLY=true` → **ALL WRITES BLOCKED**
6. Namespace-level `METADATA_ONLY=false` overrides global `METADATA_ONLY=true` → **CONTENT READS PERMITTED** for this namespace
7. Global `METADATA_ONLY=true` → **CONTENT READS BLOCKED**
8. Default → **FULL ACCESS**

**Questions:**

- **A)** Is the proposed precedence model correct?
- **B)** Should it be possible to set `READONLY=true` at the namespace level independently of the global setting (i.e., lock a specific namespace to read-only while the global default is full access)?
- **C)** What is the effective mode when `METADATA_ONLY=true` is set but the operation is a write? Is it **BLOCKED** (write denied) or **METADATA\_ONLY** (content reads blocked but structure writes permitted)? The combination is logically ambiguous.

**Answers:**

- **A)** Confirmed — the proposed 8-step precedence model is correct as specified.
- **B)** Yes — `FOUNDRY_AGENTIC_CLI_{NAMESPACE}_READONLY=true` can be set independently at the namespace level to lock a specific namespace to read-only, regardless of the global setting.
- **C)** BLOCKED — when `METADATA_ONLY=true` is in effect and the operation is a write, the write is denied. `METADATA_ONLY` implies read-only across all content operations in that scope.

---

### Q3(R3).4 — Operation-level env var naming: SDK method path transformation rule  *(from Q2(R2).4-B)*

The answer recommends using the SDK method path (e.g., `datasets.Dataset.upload_file`) as the operation identifier for env vars. However, the SDK uses a mixed-case path (`Namespace.ClassName.method_name`) that must be transformed into a valid env var name.

**Example transformation options:**

| SDK path | Option 1 (flatten) | Option 2 (class + method) | Option 3 (method only) |
| --- | --- | --- | --- |
| `datasets.Dataset.upload_file` | `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_UPLOAD_FILE_ENABLED` | `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_UPLOAD_FILE_ENABLED` | `FOUNDRY_AGENTIC_CLI_DATASETS_UPLOAD_FILE_ENABLED` |
| `datasets.Branch.list` | `FOUNDRY_AGENTIC_CLI_DATASETS_BRANCH_LIST_ENABLED` | `FOUNDRY_AGENTIC_CLI_DATASETS_BRANCH_LIST_ENABLED` | `FOUNDRY_AGENTIC_CLI_DATASETS_LIST_ENABLED` |
| `ontologies.OntologyObject.list` | `FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ONTOLOGY_OBJECT_LIST_ENABLED` | `FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ONTOLOGY_OBJECT_LIST_ENABLED` | `FOUNDRY_AGENTIC_CLI_ONTOLOGIES_LIST_ENABLED` |

Note: Option 3 (method only) creates naming collisions — `datasets.Dataset.list` and `datasets.Branch.list` would both map to `FOUNDRY_AGENTIC_CLI_DATASETS_LIST_ENABLED`.

Some SDK class names (`OntologyObject`, `LinkedObjectType`, `ActionTypeV2`) produce very long env var names under Option 1/2 (e.g., `FOUNDRY_AGENTIC_CLI_ONTOLOGIES_LINKED_OBJECT_TYPE_GET_LINKED_OBJECT_ENABLED` = 68 characters).

**Questions:**

- **A)** Which transformation rule should be applied? (Option 1 includes the class name segment, Option 3 uses method name only.)
- **B)** Is there a character limit for env var names in the target environments (Windows CMD has a 32,767-character total environment size limit, but individual names can be very long)? Is human-readability of long names a concern?
- **C)** Should a canonical reference table (namespace → class → operation → env var name) be generated and published as part of the project documentation to avoid ambiguity?

**Answers:**

- **A)** Full path flattened (Option 1/2) — include the class name segment. Transformation rule: uppercase the entire SDK path, replace dots with underscores, prefix with `FOUNDRY_AGENTIC_CLI_`. Example: `datasets.Dataset.upload_file` → `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_UPLOAD_FILE_ENABLED`. Long names from complex class names (e.g., `OntologyObject`) are an accepted trade-off.
- **B)** No specific character limit concern; human-readability of long names is acknowledged but not a blocker. Full path naming is accepted.
- **C)** Yes — a canonical reference table (namespace → class → operation → env var name) must be generated and published as part of the project documentation.

---

### Q3(R3).5 — "Per agent" session limit: agent identity and alias uniqueness  *(from Q2(R2).8-B and Q2(R2).8-C)*

Two related ambiguities in the session answers:

**5A — Agent identity for the "5 concurrent sessions per agent" limit:**

Sessions are identified by a **named alias** (per Q2(R2).8-C). The "5 concurrent sessions per agent" limit (per Q2(R2).8-B) requires defining what constitutes one "agent" for counting purposes.

Options:

- **By `CLAUDE_SESSION_ID`** — one Claude Code session = one agent; the agent can have up to 5 Foundry sessions active within one Claude session.
- **By Foundry agent RID** — sessions belong to a specific AIP Agent resource; each AIP Agent can have up to 5 concurrent CLI sessions.
- **Unlimited per creator; total cap** — global cap of N sessions regardless of creator (simpler to implement).
- **No enforced limit; only warning logged** — limit is advisory.

Which definition should be used?

**5B — Named alias uniqueness scope:**

A named alias is a string the agent provides at session creation. If two different Claude sessions (or two different agent invocations) create sessions with the same alias:

- **Collision = error**: The second creation attempt fails; the agent must choose a different name.
- **Collision = overwrite**: The second creation replaces the first.
- **Collision = scoped by `CLAUDE_SESSION_ID`**: Aliases are unique only within the same Claude session, so two sessions from different Claude sessions can share the same alias without conflict.

Which rule applies?

**Answers:**

- **5A)** Advisory only — the "5 concurrent sessions per agent" limit is not enforced programmatically. The CLI logs a warning when the advisory limit is exceeded but does not block session creation.
- **5B)** Collision = error — if a second session creation attempt uses an alias already held by an active session (regardless of which Claude session created it), the creation fails. The agent must choose a different alias.

---

### Q3(R3).6 — General Foundry skill: live web fetch vs. pre-authored static content  *(from Q2(R2).9-C)*

The answer specifies nine Palantir documentation URLs as the authoritative content source. This raises the question of **how Claude accesses this content** at skill invocation time.

| Approach | Mechanism | Trade-offs |
| --- | --- | --- |
| **Live fetch** | Claude uses its `WebFetch` tool during skill invocation to read the URLs | Always current; requires internet access at runtime; adds latency; Palantir docs may require login or throttle automated requests |
| **Pre-authored static** | SA reads the URLs, distils the key concepts, and writes static markdown content into supplementary files inside the skill folder | No runtime dependency; may become stale as Foundry evolves; requires manual maintenance |
| **Hybrid** | SKILL.md includes pre-authored summaries + reference URLs; Claude can optionally fetch for detail if connectivity is available | Best of both; more complex to maintain |

**Questions:**

- **A)** Which approach is required?
- **B)** If live fetch is used: the Palantir documentation at the provided URLs is publicly accessible without authentication — is this confirmed? (Some Palantir doc pages require a Palantir account login.)
- **C)** If pre-authored static: what is the acceptable staleness threshold — how often should the content be reviewed and updated (e.g., per SDK release, quarterly)?

**Answers:**

- **A)** Pre-authored static — the Solution Architect reads the nine Palantir documentation URLs, distils the key concepts, and writes static markdown content into supplementary files inside the skill folder. No runtime web fetch is required or used.
- **B)** Confirmed — all nine Palantir documentation URLs are publicly accessible without authentication.
- **C)** Content must be reviewed and updated on every `foundry-sdk` minor release (any bump in the minor version segment). The Solution Architect is responsible for triggering the review.

---

### Q3(R3).7 — Single-file per namespace: explicit acceptance of duplicated shared logic  *(from Q2(R2).10-C)*

The answer mandates self-contained single-file modules per namespace, with no shared utility library.

The following logic is **common to every namespace wrapper** and would be duplicated across all 20 files under this constraint:

| Shared concern | Estimated lines of code | Duplicated in N files |
| --- | --- | --- |
| Auth client initialization (`UserTokenAuth + FoundryClient`) | ~30 | 20 |
| Async client setup (`AsyncFoundryClient + asyncio.run`) | ~50 | 20 |
| Exponential backoff retry decorator | ~80 | 20 |
| TOON / JSON output formatter with envelope | ~60 | 20 |
| Structured JSON error serializer | ~40 | 20 |
| Pagination argument handling | ~50 | 20 |
| Binary download path + UUID folder + checksum | ~70 | 20 |
| `.env` file loader (`python-dotenv`) | ~15 | 20 |
| Access control guard (ENABLED / READONLY / METADATA\_ONLY) | ~60 | 20 |
| **Total duplicated lines** | **~455 lines × 20 = ~9,100 lines** | — |

This is approximately **9,100 lines of identical code** across 20 files, which creates 20 independent locations requiring the same bug fix whenever any shared logic changes.

Are there alternative interpretations that could avoid this while still meeting "self-contained and easy to distribute"?

**Option A — Confirmed duplication accepted**: All 20 files duplicate the shared logic. Acknowledged trade-off: every shared bug fix must be applied in 20 places.

**Option B — Thin shared module bundled with each skill**: A single `_foundry_cli_common.py` file is distributed alongside each namespace file and imported locally. When copying skills to a target repo, both files are copied together. Each namespace file remains the entry point. The common module is not a "package" — it is a local relative import.

**Option C — Namespace files import from a single shared location under `.claude/skills/foundry-common/`**: A `foundry-common` skill folder contains only the shared utilities (no SKILL.md, or a non-user-invocable SKILL.md). Namespace scripts import from it using a path relative to the repo root.

**Questions:**

- **A)** Is the duplication in Option A explicitly accepted by the product owner / technical lead?
- **B)** If not, which alternative (B or C) is preferred?

**Answers:**

- **A)** No — the duplication in Option A is not accepted by the product owner.
- **B)** Option B — a thin shared module `_foundry_cli_common.py` is distributed alongside each namespace file. When copying skills to a target repository, both the namespace file and the common module are copied together. Each namespace file remains the single entry point. The common module uses a local relative import; it is not packaged or installed separately.

---

### Q3(R3).8 — Metadata-only allow-list: ownership and timing  *(from Q2(R2).5-B)*

The answer specifies the metadata/data classification should be **maintained in configuration** and that *"a detailed review of all operations should be conducted to ensure accurate classification."*

This review has not been performed yet (there are hundreds of operations across 20 namespaces). The allow-list is a security-critical artefact — incorrect classification of a content-returning operation as "metadata" causes a data access control bypass.

**Questions:**

- **A)** Who is responsible for performing the detailed operation-by-operation review — the Solution Architect as part of the architecture deliverable, or the development team during implementation?
- **B)** Should the allow-list be delivered as a structured configuration file (e.g., YAML/TOML), a Python constant in the shared utility code, or an external `.env`-compatible configuration?
- **C)** Should the **default stance** for unclassified operations in tier-3 (metadata-only) mode be:
  - **Allow** (new operations are permitted unless explicitly added to a deny list)?
  - **Deny** (new operations are blocked unless explicitly added to an allow list) — more secure but requires list update with every SDK version upgrade?

> A "deny by default" stance for unclassified operations is strongly recommended from an OWASP data exposure perspective, as it prevents accidental data access in restricted mode.

**Answers:**

- **A)** Solution Architect — the operation-by-operation metadata allow-list review is part of the architecture deliverable, not deferred to the development team.
- **B)** `.env`-compatible configuration file — the allow-list is delivered in `.env` format so operators can inspect and override it without modifying Python source code.
- **C)** Deny by default — unclassified operations in tier-3 (metadata-only) mode are blocked unless explicitly added to the allow-list. The allow-list must be reviewed and updated with each `foundry-sdk` minor release.

---

## Summary Priority Matrix

| # | Type | Question | Impact if not answered |
| --- | --- | --- | --- |
| Q1(R3).1 | Incomplete answer | TOON adoption option A (accept/encoder/defer) | Cannot start output layer implementation |
| Q2(R3).1 | Contradiction | Env var prefix: `FOUNDRY_CLI_` vs `FOUNDRY_AGENTIC_CLI_` | Inconsistent variable names in 21 skills |
| Q3(R3).1 | Likely typo | 1.5 MB download limit | Every real binary download silently blocked |
| Q3(R3).2 | Architecture conflict | Response envelope schema vs TOON raw output | Inconsistent output across all 20 CLI tools; potentially unparseable by agents |
| Q3(R3).3 | Design gap | Access control precedence matrix | Undefined behaviour under mixed global/namespace settings |
| Q3(R3).4 | Naming rule | Operation env var transformation convention | Cannot generate the 500+ operation-level env var reference table |
| Q3(R3).5 | Ambiguity × 2 | Per-agent session limit identity + alias uniqueness scope | Incorrect session isolation; possible alias collision failures |
| Q3(R3).6 | Design decision | General skill: live fetch vs pre-authored | Skill may fail at runtime (no internet) or become stale |
| Q3(R3).7 | Architecture trade-off | Single-file duplication: explicit acceptance required | 9,100 lines of duplicated code; 20-file bug fix scope per shared change |
| Q3(R3).8 | Security gap | Metadata allow-list ownership + default stance | Data access control bypass risk from unclassified operations |
