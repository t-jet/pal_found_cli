Subject: DEV-023 implementation plan — 8-section foundry/ knowledge skill
Created: 2026-08-11T04:10:31
Updated: 2026-08-11T04:10:31
---
# DEV-023 implementation plan

## Deliverable
`.claude/skills/foundry/SKILL.md` — static markdown knowledge skill (frontmatter `name: foundry` + concise description; no executable scripts, no pyproject changes).

## Acceptance criteria prepared (from ticket body)
- All 8 content sections per DESIGN-023 and the story body: platform concept primer; 20-namespace overview table; operation catalogue reference; auth setup guide (UserTokenAuth + .env per ADR-006); access control configuration guide (8-step precedence per ADR-007); TOON format explanation (ADR-004); troubleshooting reference (exit codes ADR-001, retry ADR-002, NDJSON logging ADR-005); known limitations and open items.
- Operation counts cross-verified against the canonical env-var reference and test-asserted OP_SPECS counts.
- widgets runtime drift (12 design vs 8 installed per QUESTION-043) recorded in known limitations.
- References authoritative documents (SRS-001, SAD-001, ADR-001..007, ENV-REF-001, META-ALLOW-001) rather than re-deriving facts.
- Markdown lint-clean (space-padded table separators per established convention).
- document_index.md updated (knowledge skill registration).

## Ground-truth operation counts (verified from source AST, 2026-08-11)
admin 66, aip_agents 15, audit 2, checkpoints 3, connectivity 20, data_health 6, datasets 33, filesystem 31, functions 7, language_models 2, media_sets 19, models 23, ontologies 67, orchestration 20, sql_queries 5, streams 15, third_party_applications 9, widgets 8 → implemented total 351. Documented total 355 = 351 + 4 widgets design rows not implemented (disable/get/pause/set_widget_set). geo/core 0 ops per SAD-001 AA-3.

## Related documentation (linked)
- DESIGN-023-knowledge-skill.md (content specification)
- DEV-STORY-023 scope/triage/analysis/grooming comments
- SRS-001, SAD-001, ADR-001..007, ENV-REF-001, META-ALLOW-001
- 18 implemented namespace skills under .claude/skills/foundry-*/

## Approach
1. Author SKILL.md with frontmatter + 8 sections, space-padded table separators, kebab-case CLI names with snake_case SDK paths.
2. Verify file exists; run markdown lint; check counts against canonical references.
3. Update .ept/docs/document_index.md with the knowledge skill entry.
4. Document files + verification as a comment; set time_spent_hours; transition to Resolved (blocks on CODEREVIEW-023 per LINK-00696/697).

Requesting transition DEV-023 Open → In Progress.
