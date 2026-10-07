Subject: python-developer: New->Open DoD + implementation plan (Connectivity/Checkpoints/DataHealth 29 ops)
Created: 2026-10-03T18:40:11
Updated: 2026-10-03T18:40:11
---
TRIAGE (New->Open DoD MET):
- Docs studied: document_index, BA-DES-013 sec8, SA-DES-012 sec1/3/4, parent DEV-STORY-048, frozen register 20261003-174840-tech-lead (connectivity20 + checkpoints3 + data_health6 = 29), TESTCASE-017/019/020.
- Assignee python-developer; DESIGN-048 Closed; parent in Development. No open QUESTIONs; Blocked=No.
- Critical thinking: update_secrets/upload_custom_jdbc_drivers/import execute write; secrets never logged; check_report routed through nested Check.CheckReport. 3 skills (connectivity/checkpoints/data-health). Preserve FEATURE-008/009 + FEATURE-011 install blocks.

IMPLEMENTATION PLAN:
1. connectivity SKILL.md entry+nav + references (connection7/file_import6/table_import6/virtual_table1).
2. checkpoints SKILL.md + references (record3).
3. data-health SKILL.md + references (check4/check_report2).
4. Each leaf<=300, install block in each SKILL.md (each has its own block normally - preserve). Verify+pytest+commit+time_spent+Resolved (NOT closed; CODEREVIEW-048 handoff).
DELIVERABLE: 3 skills (connectivity/checkpoints/data-health) SKILL.md+refs, 29 ops.
