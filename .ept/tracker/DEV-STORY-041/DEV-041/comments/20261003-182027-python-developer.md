Subject: python-developer: New->Open DoD + implementation plan (general pal-found primer + navigation)
Created: 2026-10-03T18:20:27
Updated: 2026-10-03T18:20:27
---
TRIAGE (New->Open DoD MET):
- Docs studied: document_index, BA-DES-013, SA-DES-012, BA-ANA-013, parent DEV-STORY-041, FEATURE-008/009/011.
- Assignee set to python-developer (creator). Parent story DEV-STORY-041 in Development; DESIGN-041 Closed.
- Questions: none open (no QUESTION links). Blockers: none (Blocked=No).
- Required fields validated: status Open, assignee python-developer, priority High, estimated_hours 20.
- Critical thinking: doc-only; verbatim re-use of existing general-skills content pitfalls reviewed; QA baseline for general skill is derive-from-namespace SKILL.md counts (18 namespace skills, 351 ops).

IMPLEMENTATION PLAN (Open->In Progress):
1. Rewrite .agents/skills/pal-found/SKILL.md as platform primer + navigation map (retain FEATURE-008 platform description, FEATURE-009 stage baselines, FEATURE-011 install block).
2. Author references/*.md local parts: references/01-platform-and-resources.md, references/02-identifiers-and-auth.md, references/03-output-errors.md, references/04-shared-options.md (extract Sections 4-8 content).
3. Each leaf <=300 lines; relative links only; no namespace presented callable unless documented.
4. Verify install block exact strings + local links resolve offline + leaf limits.
5. Run skills pytest; commit; set time_spent; Resolved (do NOT close; CODEREVIEW-041 architect handoff).
DELIVERABLE: pal-found/SKILL.md + references/*.md (general platform primer)
