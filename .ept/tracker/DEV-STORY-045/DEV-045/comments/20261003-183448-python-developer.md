Subject: python-developer: New->Open DoD + implementation plan (Filesystem 31 ops)
Created: 2026-10-03T18:34:48
Updated: 2026-10-03T18:34:48
---
TRIAGE (New->Open DoD MET):
- Docs studied: document_index, BA-DES-013 sec8, SA-DES-012 sec1/3/4, parent DEV-STORY-045, frozen register 20261003-174742-tech-lead (5 clients, 31 ops), TESTCASE-007.
- Assignee python-developer; DESIGN-045 Closed; parent in Development. No open QUESTIONs; Blocked=No.
- Critical thinking: get_by_path(_batch) vs get/get_batch routing; permanently_delete/restore destructive; resource add/remove markings write. Preserve FEATURE-008/009 + FEATURE-011 install block.

IMPLEMENTATION PLAN:
1. Rewrite pal-found-filesystem/SKILL.md as entry+nav.
2. references/01-folder-project.md(12), 02-resource.md(11), 03-resource-role-space.md(8).
3. Leaf<=300, relative links, install block. Verify+pytest+commit+time_spent+Resolved (NOT closed; CODEREVIEW-045 handoff).
