# DESIGN-023 — foundry/ Knowledge Skill

| Field | Value |
| --- | --- |
| Story | DEV-STORY-023 |
| Status | Completed; ready for content authoring |
| Date | 2026-08-11 |
| Scope | Static markdown `foundry/` general knowledge skill, 8 content sections |

## Technical summary

Author the static markdown content for the `foundry/` general knowledge skill under `.claude/skills/foundry/`. The skill is a documentation-only artifact: it provides cross-cutting Foundry platform knowledge used by all 18 namespace CLI skills. It contains no executable scripts, adds no console entry points, and makes no `pyproject.toml` packaging changes. Content is authored from authoritative project documents and cross-verified against the implemented namespace skills rather than re-derived.

The skill frontmatter follows the established skill convention: `name: foundry` with a concise `description` of the general knowledge it provides. The body is organized into eight sections matching the story body: Foundry platform concept primer, namespace overview table, operation catalogue reference, authentication setup guide, access control configuration guide, TOON format explanation, troubleshooting reference, and known limitations / open items.

## Evidence and governing references

This design follows:

- SRS-001 functional requirements (F-OUT output formats, F-ACL access control, FR-PAG pagination, FR-TRACE tracing, configuration model, exit codes) and non-functional constraints (DCC-3 self-contained skills, DCC-6 environment configuration);
- SAD-001 architecture sections: 20 namespaces / 355 operations, skill packaging layout (`foundry-{namespace}/` skills), SKILL.md frontmatter template, EPIC-008 entry, assumption AA-3 (geo and core have 0 public CLI-callable operations);
- ADR-001 exit-code taxonomy (0-9), ADR-002 call timeout defaults and retry policy, ADR-003 streams batch strategy, ADR-004 format auto-selection algorithm (TOON vs JSON), ADR-005 NDJSON log format, ADR-006 `.env` file search path order, ADR-007 operation-level READONLY independence and the 8-step precedence model;
- the canonical environment-variable reference (ENV-REF-001), which defines global, namespace-level (20-var × 3 controls) and 355 operation-level variables;
- the canonical metadata allow-list (META-ALLOW-001), which classifies all 355 operations for Tier-3 metadata-only access (162 permitted / 193 blocked, default-deny);
- the vendored SDK sources under `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/` (20 catalog namespaces: 18 client namespaces plus `geo` and `core`, which expose only `errors.py` and `models.py`);
- the 18 implemented namespace skills under `.claude/skills/` and their test-asserted `OP_SPECS` counts.

## Content specification (8 sections)

### 1. Foundry platform concept primer

Plain-language introduction to the Palantir Foundry platform concepts surfaced by the CLI skills: projects and folders, datasets, branches and transactions, schemas, files, views; ontologies, object types, object sets, links; functions (queries and value types); AIP agents and sessions; media sets; streams; models; and platform administration (enrollment, groups, markings, organizations, roles). Each concept lists the namespace skill(s) that operate on it.

### 2. Namespace overview table

A single table listing all 20 SDK v2 catalog namespaces with their CLI operation counts. The 18 CLI-implemented namespaces use test-asserted `OP_SPECS` counts; `geo` and `core` are documented explicitly as zero-operation namespaces (SAD-001 AA-3).

| Namespace | CLI skill | Operations |
| --- | --- | --- |
| admin | foundry-admin | 66 |
| aip_agents | foundry-aip-agents | 15 |
| audit | foundry-audit | 2 |
| checkpoints | foundry-checkpoints | 3 |
| connectivity | foundry-connectivity | 20 |
| data_health | foundry-data-health | 6 |
| datasets | foundry-datasets | 33 |
| filesystem | foundry-filesystem | 31 |
| functions | foundry-functions | 7 |
| language_models | foundry-language-models | 2 |
| media_sets | foundry-media-sets | 19 |
| models | foundry-models | 23 |
| ontologies | foundry-ontologies | 67 |
| orchestration | foundry-orchestration | 20 |
| sql_queries | foundry-sql-queries | 5 |
| streams | foundry-streams | 15 |
| third_party_applications | foundry-third-party-applications | 9 |
| widgets | foundry-widgets | 12* |
| geo | — | 0 |
| core | — | 0 |

*widgets: DESIGN-022 baseline 12 operations; installed SDK 1.102.0 exposes 8 (QUESTION-043 decision). Total implemented = 355.

### 3. Operation catalogue reference

Per-namespace resource client paths and operation lists. Format follows the implemented skill files: resource grouped tables with kebab-case CLI command names and the snake_case SDK dispatch paths. Cross-verified against the canonical env-var reference and metadata allow-list row counts. For the full authoritative catalogue, readers are directed to the individual `foundry-*` skill files; this section summarizes the complete inventory (355 operations across 18 namespaces).

### 4. Authentication setup guide

- `FOUNDRY_TOKEN` (required): Palantir bearer token; `UserTokenAuth` is constructed from the token only.
- `FOUNDRY_HOSTNAME` (required): Foundry instance hostname; consumed by `AsyncClientFactory` at client construction.
- `.env` loading per ADR-006: explicit `FOUNDRY_AGENTIC_CLI_ENV_FILE` override (no fallback on missing file) → git-root `.env` discovery (walk up from CWD to first `.git`) → env-vars-only mode. Home directory is deliberately never searched.
- `python-dotenv` `load_dotenv()` with `override=False`: pre-set shell environment variables take precedence over `.env` values.
- Setup steps: copy `.env.example` to `.env`, fill token and hostname, verify with any read-only command.

### 5. Access control configuration guide

- 8-step precedence model per ADR-007: (1) operation-level ENABLED → (2) namespace-level ENABLED → (3) operation-level READONLY override (`false` = permit write) → (4) namespace-level READONLY override → (5) global READONLY → (6) namespace METADATA_ONLY → (7) global METADATA_ONLY → (8) permit.
- Control variable naming patterns from ENV-REF-001: global `FOUNDRY_AGENTIC_CLI_{KEY}`, namespace `FOUNDRY_AGENTIC_CLI_{NS}_{CONTROL}`, operation `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_{CONTROL}`; control suffixes `_ENABLED`, `_READONLY`, `_METADATA_ONLY`.
- Tier-3 metadata-only policy: default-deny; 162 operations permitted, 193 blocked (META-ALLOW-001). Policy is packaged per namespace as `metadata-allow-list.md`.
- Violations exit with code 8 (AccessControlError).

### 6. TOON format explanation

- ADR-004 rule: TOON (Tabular Object Output Notation) is used only when the top-level result is a list AND all items share a uniform field set; otherwise JSON.
- Selection via `--format {json,toon,auto}` flag or `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT` (default `auto`).
- TOON rendering uses `toon-python >=0.9,<1.0`; data on stdout, metadata on stderr separated by `# ---metadata-start---`.

### 7. Troubleshooting reference

- Exit-code taxonomy (ADR-001): 0 success, 1 user input, 2 authentication, 3 permission denied, 4 not found, 5 timeout, 6 server error, 7 rate limit exhausted, 8 access control, 9 configuration.
- Retry policy (ADR-002): exponential backoff with jitter; 4 max attempts; per-call timeout 30 s default (120 s streams).
- NDJSON structured logging to stderr (ADR-005); `FOUNDRY_AGENTIC_CLI_LOG_LEVEL`.
- Common failure modes: missing token/hostname (exit 2/9), ACL block in read-only or metadata-only mode (exit 8), oversized binary (1.5 MiB download / 16 MiB upload bounds), HTTP 429 rate limiting (exit 7), JSON argument validation errors (exit 1).

### 8. Known limitations and open items

- `geo` and `core` namespaces expose no public CLI-callable operations (SAD-001 AA-3); no skill folders exist for them.
- widgets SDK drift: DESIGN-022 documents 12 operations from the vendored snapshot; installed SDK 1.102.0 exposes 8 (DevModeSettingsV2 out of scope per QUESTION-043). The runtime surface is authoritative.
- Vendored SDK snapshot is version `0.0.0` (git-derived); installed runtime is `foundry-platform-sdk 1.102.0`. Operation counts must be re-verified on every SDK minor release (ENV-REF-001 review cycle).
- Binary download bound 1.5 MiB and upload bound 16 MiB apply per operation; large media must be handled outside the CLI.
- Preview-mode SDK parameters are excluded from the CLI surface.
- Attribution (`FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION` / `_ATTRIBUTION_RIDS`) applies only to namespaces within FR-ATTR-4 scope (media_sets currently); other namespaces set `include_attribution=False`.

## Component breakdown

- `.claude/skills/foundry/SKILL.md` — the single deliverable skill file (frontmatter + 8 sections). Optional supporting reference documents may live under `.claude/skills/foundry/references/` if content volume warrants.
- No changes to `src/foundry_cli/`, no console entry points, no `pyproject.toml` package data changes.
- Registration in `.ept/docs/document_index.md` (knowledge skill entry).

## Estimates and sprint fit

| Sub-task | Assignee | Estimated hours |
| --- | --- | --- |
| DESIGN-023 | tech-lead | 6 |
| DEV-023 | python-developer | 16 |
| UNITTEST-023 | python-developer | 12 |
| CODEREVIEW-023 | tech-lead | 6 |
| TESTCASE-023 | qa-engineer | 8 |
| TESTEXEC-023 | qa-engineer | 8 |
| DEVOPS-023 | devops-engineer | 3 |
| **Total** | | **59** |

The story fits within one sprint (single static markdown artifact, 8 sections, one reviewer, no packaging changes). No split into additional stories is required.

## Risks

Operation-count drift between the vendored SDK snapshot and the installed runtime (mitigated by three-source verification and a documented review cycle); widgets 12-vs-8 discrepancy (recorded as a known limitation rather than corrected in the content, per QUESTION-043); content duplication with the namespace skill files (mitigated by referencing authoritative sources instead of re-deriving); markdown lint consistency (space-padded table separators per established convention).
