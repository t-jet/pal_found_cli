Subject: python-developer: New->Open DoD + implementation plan (Orchestration/SQL 25 ops)
Created: 2026-10-03T18:46:26
Updated: 2026-10-03T18:46:26
---
TRIAGE (New->Open DoD MET):
- Docs studied: document_index, BA-DES-013 sec8, SA-DES-012 sec1/3/4, parent DEV-STORY-051, frozen register 20261003-174908-tech-lead (orchestration20+sql_queries5=25), TESTCASE-014/015.
- Assignee python-developer; DESIGN-051 Closed; parent in Development. No open QUESTIONs; Blocked=No.
- Critical thinking: build cancel/create, schedule create/delete/pause/replace/run/unpause, sql_query cancel/execute are write/execute with compute cost; async build/schedule status requires follow-up check (never presumed final). SQL CLI subcommand is query (alias). Preserve FEATURE-008/009 + FEATURE-011 install blocks.

IMPLEMENTATION PLAN:
1. orchestration SKILL.md+refs (build6/job2/schedule10/schedule_version2 = 20).
2. sql-queries SKILL.md+refs (sql_query5 incl Arrow downloads) CLI resource subcommand query.
3. Leaf<=300, install block each. Verify+pytest+commit+time_spent+Resolved (NOT closed; CODEREVIEW-051 handoff).
