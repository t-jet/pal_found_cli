Subject: DEV-023 implementation complete — files, verification, commit
Created: 2026-08-11T04:19:09
Updated: 2026-08-11T04:19:09
---
# DEV-023 implementation complete

## Files created/modified
- Created: `.claude/skills/foundry/SKILL.md` — the foundry/ general knowledge skill (frontmatter `name: foundry` + description; 8 sections; 226 lines committed). MANDATORY VERIFICATION: file exists on disk (18778 bytes), confirmed via file search.
- Modified: `.ept/docs/document_index.md` — Architecture Documentation entry for the knowledge skill + footer Implementation Change note.
- Committed: `a4d48ab` — docs(foundry): add foundry/ knowledge skill - 8 sections (DEV-023, UNITTEST-023).

## Content delivered (8 sections per DESIGN-023)
1. Foundry platform concept primer (concept-to-skill mapping table)
2. Namespace overview — all 20 namespaces with operation counts (18 implemented + geo/core zero-op per SAD-001 AA-3)
3. Operation catalogue reference — per-namespace resource client -> operation lists (kebab-case CLI / snake_case SDK)
4. Authentication setup guide — UserTokenAuth from FOUNDRY_TOKEN, FOUNDRY_HOSTNAME via AsyncClientFactory, .env search order per ADR-006 (explicit override → git-root → env-only; no home-dir fallback), load_dotenv override=False
5. Access control configuration guide — 8-step precedence per ADR-007, control variable naming patterns, _ENABLED/_READONLY/_METADATA_ONLY, metadata-only 162/193 default-deny (META-ALLOW-001), exit code 8
6. TOON format explanation — ADR-004 rule (top-level list + uniform field set → TOON; else JSON), --format json|toon|auto, FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT
7. Troubleshooting reference — exit-code taxonomy ADR-001 (0-9), retry ADR-002 (exp backoff + jitter, 4 attempts, 30s/120s timeouts), NDJSON logging ADR-005, common failure modes
8. Known limitations — geo/core zero-op; widgets 12-design vs 8-runtime drift (QUESTION-043, DevModeSettingsV2 out of scope, runtime authoritative); SDK snapshot 0.0.0 vs installed 1.102.0; binary bounds 1.5 MiB download / 16 MiB upload; preview params excluded; attribution scope per FR-ATTR-4

## Verification
- Operation counts cross-verified from source (AST over OP_SPECS + datasets subparsers): 351 implemented across 18 namespaces; 355 documented = 351 + 4 widgets design rows not implemented; overview table matches both.
- Markdown lint: VS Code markdown.validate reports no errors on SKILL.md and document_index.md. Space-padded table separators per convention.
- Full content verification performed by UNITTEST-023 (separate ticket) — 46 checks, 0 failures.

Requesting transition DEV-023 In Progress → Resolved (blocks on CODEREVIEW-023 via LINK-00696/697).
