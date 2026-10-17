---
id: QUESTION-152
type: question
title: May offline Foundry skills ship linked local reference parts?
status: Closed
addressed_to: project-owner
created: 2026-10-03
updated: 2026-10-03
priority: Medium
assignee: project-owner
reporter: architect
time_spent_hours: 0.1
---

# Decision requested
May FEATURE-012 distribute each skill as SKILL.md plus linked, packaged local Markdown reference parts when full operation semantics exceed one file? Recommended: yes. SKILL.md must navigate to each required local part; every part must ship in the copied skill folder; an offline review must prove every link resolves and full operation coverage is available. Command execution stays in the installed pal-found-* CLI.

Alternative: require exactly one SKILL.md per skill with full semantic coverage in that file. This requires an approved exception to the 300-line composition rule or another approved layout that still keeps all required content offline. Neither choice may reduce coverage.

## Research Done
FEATURE-012 requires offline meaning for every supported operation and parameter. The current pal_found_cli_skills/.agents/skills tree has 19 SKILL.md files and no part files; the general skill lists 351 implemented operations. SA-DES-009 sections 1, 3, and 6 allow linked parts when a skill exceeds 300 lines. SA-DES-011 sections 2.1 and 3 say every namespace folder contains exactly one file, SKILL.md. Both designs are linked in .ept/docs/document_index.md. FEATURE-011 forbids skill-side Python scripts; local Markdown parts would preserve documentation-only execution.

## Acceptance criteria
- Project Owner selects a content model and states whether locally linked Markdown parts count as a self-contained distributed skill.
- The decision reconciles full offline coverage and the 300-line composition rule.
- The decision identifies which files must ship with each skill and what an offline agent may rely on.
