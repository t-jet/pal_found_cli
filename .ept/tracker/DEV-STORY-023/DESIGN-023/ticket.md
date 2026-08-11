---
id: DESIGN-023
type: design
title: 'DESIGN-023: foundry/ knowledge skill — design and grooming'
status: Closed
created: 2026-08-11
updated: 2026-08-11
priority: High
assignee: tech-lead
reporter: architect
estimated_hours: 6
---

# DESIGN-023: DESIGN-023: foundry/ knowledge skill — design and grooming

## Description

# DESIGN-023: foundry/ knowledge skill — design and grooming

## Description

Grooming, estimation, and technical design for the DEV-STORY-023 documentation story: author the static markdown `foundry/` general knowledge skill content.

## Acceptance Criteria

- [x] Produce the DESIGN-023 deliverable `.ept/docs/deliverables/architecture/DESIGN-023-knowledge-skill.md` mirroring the DESIGN-022 document style (Field/Value table, Technical summary, Evidence and governing references, section-by-section content specification)
- [x] Define the content outline for all 8 knowledge skill sections (platform primer, namespace overview, operation catalogue, auth setup, access control, TOON, troubleshooting, known limitations)
- [x] Cross-verify operation counts from three authoritative sources (test-asserted OP_SPECS counts, canonical env-var reference, metadata allow-list) and record the widgets 12-vs-8 runtime drift (QUESTION-043) as a known limitation
- [x] Identify responsible persons for all sub-tasks from `.ept/docs/resources/available_resources.md`
- [x] Provide estimates (story points + hours for each sub-task)
- [x] Register the deliverable in `.ept/docs/document_index.md` (Last Updated + Major Change footer)
- [x] Document all changes as comments on this ticket

## Deliverables

- `.ept/docs/deliverables/architecture/DESIGN-023-knowledge-skill.md`

## Estimates

| Sub-task | Assignee | Estimated hours |
| --- | --- | --- |
| DEV-023 | python-developer | 16 |
| UNITTEST-023 | python-developer | 12 |
| CODEREVIEW-023 | tech-lead | 6 |
| TESTCASE-023 | qa-engineer | 8 |
| TESTEXEC-023 | qa-engineer | 8 |
| DEVOPS-023 | devops-engineer | 3 |

## Notes

Documentation story — no code, no console entry points, no pyproject packaging changes.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
