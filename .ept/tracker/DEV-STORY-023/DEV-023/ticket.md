---
id: DEV-023
type: development
title: 'DEV-023: Author the foundry/ knowledge skill markdown content'
status: Closed
created: 2026-08-11
updated: 2026-08-11
priority: High
resolution: Done
assignee: python-developer
reporter: architect
estimated_hours: 16
time_spent_hours: 16
---

# DEV-023: DEV-023: Author the foundry/ knowledge skill markdown content

## Description

# DEV-023: Author the foundry/ knowledge skill markdown content

## Description

Author the static markdown content for the `foundry/` general knowledge skill under `.claude/skills/foundry/` per DESIGN-023. Documentation story — no executable code, no console entry points, no pyproject packaging changes.

## Acceptance Criteria

- [x] Create `.claude/skills/foundry/SKILL.md` with frontmatter (name: foundry, concise description of the general knowledge it provides)
- [x] Content covers all 8 sections per the story body and DESIGN-023: Foundry platform concept primer, namespace overview table (20 namespaces + operation counts), operation catalogue reference, authentication setup guide (UserTokenAuth + .env per ADR-006), access control configuration guide (8-step precedence per ADR-007), TOON format explanation (ADR-004), troubleshooting reference (exit codes ADR-001, retry ADR-002, NDJSON logging ADR-005), known limitations and open items
- [x] Operation counts cross-verified against the canonical env-var reference and test-asserted OP_SPECS counts (355 total; geo/core documented as zero-op)
- [x] widgets runtime drift (12 design vs 8 installed per QUESTION-043) recorded in the known limitations section
- [x] Content references authoritative documents (SRS-001, SAD-001, ADR-001..007, ENV-REF-001, META-ALLOW-001) rather than re-deriving facts
- [x] Markdown lint-clean (space-padded table separators per established convention)
- [x] All content files listed in a comment on this ticket
- [x] Related documents in `.ept/docs/document_index.md` updated (skill registration)

## Deliverables

- `.claude/skills/foundry/SKILL.md`
- Optional supporting reference documents under `.claude/skills/foundry/references/`

## Notes

Static markdown only. No executable scripts inside this skill.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
