Subject: UNITTEST-023 test plan — content-accuracy verification
Created: 2026-08-11T04:08:55
Updated: 2026-08-11T04:08:55
---
# UNITTEST-023 test plan

## Scope
Content-accuracy verification of the authored `.claude/skills/foundry/SKILL.md` against authoritative sources. No code under test — this is a documentation story.

## Verification checklist (mapped to ACs)
1. All 20 namespace entries + operation counts match canonical env-var reference (ENV-REF-001), metadata allow-list (META-ALLOW-001), and test-asserted OP_SPECS counts (verified via source AST). geo/core documented as zero-op.
2. Auth guide correctness: UserTokenAuth from FOUNDRY_TOKEN; FOUNDRY_HOSTNAME via AsyncClientFactory; ADR-006 search order (explicit override → git-root discovery → env-var-only; no home-dir fallback); load_dotenv override=False.
3. Access control guide correctness: 8-step precedence per ADR-007; control variable naming patterns (global/namespace/operation; _ENABLED/_READONLY/_METADATA_ONLY); exit code 8.
4. TOON explanation matches ADR-004 rule (list + uniform field set → TOON; else JSON; --format json|toon|auto; FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT default auto).
5. Exit-code taxonomy matches ADR-001 (0-9 mapping).
6. widgets known-limitation statement matches QUESTION-043 decision (12 design vs 8 runtime; DevModeSettingsV2 out of scope; runtime authoritative).
7. Markdown lint clean on all authored files.
8. References resolve to real documents (SRS-001, SAD-001, ADR-001..007, ENV-REF-001, META-ALLOW-001 paths verified).
9. .env variable names match ADR-006/canonical reference.

## Deliverables
Verification report comment on this ticket (this is the UNITTEST-023 deliverable per ticket body).

## Approach
Run automated checks where possible (source AST count script, regex extraction of tables), manual cross-reference for section content, then document all results.

Requesting transition UNITTEST-023 Open → In Progress.
