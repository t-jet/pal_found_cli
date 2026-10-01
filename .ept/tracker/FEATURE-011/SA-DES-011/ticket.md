---
id: SA-DES-011
type: sa_subtask_design
title: 'Architecture design: remove python scripts from skills, retire launcher layer, migrate
  datasets/ontologies implementations to tool, packaging'
status: Closed
created: 2026-09-30
updated: 2026-10-01
priority: Medium
assignee: solution-architect
reporter: ba
component: skills
time_spent_hours: 1.5
---

# SA-DES-011: Architecture design: remove python scripts from skills, retire launcher layer, migrate datasets/ontologies implementations to tool, packaging

## Description

FEATURE-011 (PO change request 2026-09-30) requires that the skills use only the
CLI interface and contain no separate Python scripts. This sub-task produces the
architecture/technical design for FEATURE-011: sweep the 18 namespace skills to
the doc-only model (single SKILL.md invoking an installed pal-found-<ns>
command), retire the launcher layer (16 thin wrappers + datasets/ontologies
standalone copies), migrate the datasets/ontologies implementations to the tool
(verify the tool superset and operation parity 33/67, no net-new command), and
cover infrastructure, packaging, and onboarding implications.

## Acceptance Criteria

1. **AC-1** Repository-level and interface changes designed for both the skills
   repo (doc-only SKILL.md, no scripts/) and the tool repo (canonical commands
   kept, no new command).
2. **AC-2** Launcher-layer retirement approach defined (16 thin wrappers).
3. **AC-3** Datasets/ontologies migration approach defined: remove stale skill
   copies; verify tool command superset and operation parity (33/67).
4. **AC-4** Non-functional requirements defined for developers.
5. **AC-5** Infrastructure and packaging changes identified and communicated
   (distribution + onboarding).
6. **AC-6** Step-by-step migration procedure described.
7. **AC-7** Risks and mitigations listed.
8. **AC-8** Traceability to FEATURE-011 / EPIC-011 and mapping to the DEV-STORYs
   the BA creates under FEATURE-011.

## Related Documentation

- `.ept/docs/deliverables/architecture/SA-ANA-012-doc-only-skills-architecture-analysis.md`
- `.ept/docs/deliverables/business_analysis/BA-ANA-012-doc-only-skills.md`
- `SA-DES-011-doc-only-skills-technical-design.md` (deliverable, this sub-task)
- `.ept/docs/document_index.md`

## Notes

BA-DES-012 is the BA design sibling. The BA creates the DEV-STORYs under
FEATURE-011 during BA-DES-012.
