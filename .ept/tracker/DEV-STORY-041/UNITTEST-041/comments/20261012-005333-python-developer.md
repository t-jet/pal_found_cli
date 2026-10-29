Subject: python-developer: New->Open DoD and test plan (pal-found primer and navigation)
Created: 2026-10-12T00:53:33
Updated: 2026-10-12T00:53:33
---
## New -> Open DoD and test plan

**Documentation reviewed**
- `.ept/docs/document_index.md`; parent DEV-STORY-041 (offline Foundry primer and navigation); BA-ANA-013, BA-DES-013, SA-DES-012.
- DEV-041 Closed, CODEREVIEW-041 Closed (approved).
- Ticket body: markdown validity, <=300-line leaf rule, offline local-link and anchor resolution, install-prerequisite block, 19-folder copy integrity.

**Readiness**
- Assignee python-developer; priority High; created/updated dates set.
- Parent Story context reviewed; no open QUESTION sub-tasks; no blockers identified.
- Development sub-task DEV-041 is Closed, so the authored content is ready for tests.

**Test plan (offline, no network)**
1. `python -m pytest tests/test_skill_documentation.py tests/test_skill_tree_migration.py tests/test_distribution_commands.py tests/test_offline_skill_gate.py -q` from `pal_found_cli_skills/`.
2. Independent probe `.ept/tmp/verify_wave.py pal-found` for leaf-line limit, relative local-link resolution inside the pal-found folder, and install-prerequisite block in `SKILL.md`.
3. Confirm the 19-folder copy integrity checks in `test_distribution_commands.py` pass (PowerShell copy completeness and atomicity).
4. Record results and coverage as a Resolved comment.
