Subject: UNITTEST-023 verification results — 46 checks, 0 failures
Created: 2026-08-11T04:19:28
Updated: 2026-08-11T04:19:28
---
# UNITTEST-023 verification results

## Subject under verification
`.claude/skills/foundry/SKILL.md` (committed a4d48ab) — content accuracy against authoritative sources. No code under test.

## Automated checks: 46 checks, 0 failures (misc_dos/verify_skill_023.py)

### 1. Namespace overview + operation counts (AC-1) — PASS
- All 20 namespaces present in the overview table (18 implemented + geo/core zero-op).
- Table counts match both the canonical documented counts (355 total) and the implemented source surface (351): verified by AST over OP_SPECS tuples + datasets subparser expansion. Per-namespace: admin 66, aip_agents 15, audit 2, checkpoints 3, connectivity 20, data_health 6, datasets 33, filesystem 31, functions 7, language_models 2, media_sets 19, models 23, ontologies 67, orchestration 20, sql_queries 5, streams 15, third_party_applications 9, widgets 8, geo 0, core 0.
- Implemented total from source = 351; skill states both 355 (documented, incl. 4 widgets design rows not implemented) and 351 (implemented) with the reconciliation explained.

### 2. Auth guide (AC-2) — PASS
- UserTokenAuth constructed from FOUNDRY_TOKEN only; FOUNDRY_HOSTNAME consumed by AsyncClientFactory (verified against src/foundry_cli/common/async_client_factory.py L79-89).
- ADR-006 search order stated: explicit FOUNDRY_AGENTIC_CLI_ENV_FILE override (no fallback on missing file) → git-root .env discovery → env-vars-only; home directory deliberately never searched; load_dotenv override=False semantics.
- .env.example referenced in setup steps.

### 3. Access control guide (AC-3) — PASS
- 8-step precedence model per ADR-007 (operation ENABLED → namespace ENABLED → op READONLY override → ns READONLY override → global READONLY → ns METADATA_ONLY → global METADATA_ONLY → permit).
- Control variable naming patterns per ENV-REF-001: global FOUNDRY_AGENTIC_CLI_{KEY}, namespace FOUNDRY_AGENTIC_CLI_{NS}_{CONTROL}, operation FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_{CONTROL}; _ENABLED/_READONLY/_METADATA_ONLY suffixes.
- Operation-level _READONLY=true not supported as independent setting (ADR-007); metadata-only 162/193 permitted/blocked default-deny (META-ALLOW-001); blocked ops exit code 8 (AccessControlError).

### 4. TOON explanation (AC-4) — PASS
- ADR-004 rule stated exactly: TOON only when top-level result is a list AND all items share an identical field set; JSON otherwise (errors, single objects, empty lists, mixed-type arrays, heterogeneous-field arrays, binary envelopes, pagination metadata).
- --format json|toon|auto, FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT default auto; toon-python rendering; data on stdout, metadata on stderr with # ---metadata-start--- separator (ADR-005).

### 5. Exit-code taxonomy (AC-5) — PASS
- All 10 codes 0-9 present with names matching ADR-001: 0 Success, 1 user input, 2 auth, 3 permission, 4 not found, 5 timeout, 6 server, 7 rate limit, 8 access control, 9 configuration.
- Refined nuance verified against implementation: missing FOUNDRY_TOKEN/FOUNDRY_HOSTNAME raises ConfigurationError before client construction → exit 9; token rejected at request time (SDK auth failure) → exit 2.

### 6. Widgets known limitation (AC-6) — PASS
- Matches QUESTION-043 decision: DESIGN-022 documents 12 ops from vendored snapshot; installed SDK 1.102.0 exposes 8; runtime surface authoritative; DevModeSettingsV2 out of scope. Recorded as known limitation, not corrected in content.

### 7. Markdown lint (AC-7) — PASS
- VS Code markdown.validate: no errors on SKILL.md or document_index.md. Space-padded table separators per established convention. All 8 section headings present; frontmatter name+description valid.

### 8. References resolve (AC-8) — PASS
- All cited documents exist on disk: SRS-001, SAD-001, ADR-001..007, ENV-REF-001, META-ALLOW-001, DESIGN-023. All cited in the skill text.

### 9. Env var names (AC-9) — PASS
- All env var names in the skill exist in the canonical reference (ENV-REF-001): FOUNDRY_TOKEN, FOUNDRY_HOSTNAME, FOUNDRY_AGENTIC_CLI_ENV_FILE, _READONLY, _METADATA_ONLY, _TIMEOUT_S, _STREAMS_TIMEOUT_S, _LOG_LEVEL, _DEFAULT_FORMAT, _MAX_DOWNLOAD_BYTES, _ENABLE_ATTRIBUTION, _ATTRIBUTION_RIDS.

## Verification findings (non-blocking)
- During verification, SRS-001 (FR-ACL) and ADR-003 (streams batch strategy) citations were added to the skill to complete the authoritative-source coverage; content unchanged otherwise.
- Verification script artifacts: misc_dos/count_ops_023.py, misc_dos/dump_ops_023.py, misc_dos/verify_skill_023.py (working notes, not deliverables).

Requesting transition UNITTEST-023 In Progress → Resolved.
