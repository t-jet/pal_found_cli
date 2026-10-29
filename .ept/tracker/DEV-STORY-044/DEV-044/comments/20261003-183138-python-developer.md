Subject: python-developer: New->Open DoD + implementation plan (Datasets 33 ops)
Created: 2026-10-03T18:31:38
Updated: 2026-10-03T18:31:38
---
TRIAGE (New->Open DoD MET):
- Docs studied: document_index, BA-DES-013 sec8, SA-DES-012 sec1/3/4, parent DEV-STORY-044, frozen register 20261003-174735-tech-lead (5 clients, 33 ops), TESTCASE-003.
- Assignee python-developer; DESIGN-044 Closed; parent in Development. No open QUESTIONs; Blocked=No.
- Critical thinking: hand-rolled CLI parser (pal_found_datasets_cli.py, no OP_SPECS). 33 ops across dataset(11)/branch(5)/file(5)/transaction(6)/view(6). get_schema_batch/put_schema use JSON body. Preserve FEATURE-008/009 (capability+source, JSON formats), FEATURE-011 install block.

IMPLEMENTATION PLAN (Open->In Progress):
1. Rewrite .agents/skills/pal-found-datasets/SKILL.md as entry+nav/index linking refs.
2. Author references/*.md per operation cluster: 01-dataset.md(11), 02-branch.md(5), 03-file.md(5), 04-transaction.md(6), 05-view.md(6). Each record: class/precondition/effect/inputs/success/failure/example/evidence.
3. Leaf<=300, relative links offline, install block + JSON variants preserved.
4. Verify + pytest + commit + time_spent + Resolved (NOT closed; CODEREVIEW-044 handoff).
DELIVERABLE: datasets SKILL.md + references/01-05.md (33 ops).
