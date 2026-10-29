Subject: python-developer: New->Open DoD + implementation plan (Integration review harness + copied-bundle gate)
Created: 2026-10-03T18:53:47
Updated: 2026-10-03T18:53:47
---
TRIAGE (New->Open DoD MET):
- Docs studied: document_index, BA-DES-013 sec7/8 (DEV-STORY-055 owns reusable coverage/local-link/offline exercise checks + final copied-bundle gate, audits 351-op register), SA-DES-012 sec5 (verification gates: inventory/syntax, semantic, local distribution, offline usability, release integration), parent DEV-STORY-055 (DependsOn all), TESTCASE-* set.
- Assignee python-developer; DESIGN-055 Closed; parent in Development. No open QUESTIONs; Blocked=No.
- Critical thinking: 055 builds REUSABLE content-verification tests in pal_found_cli_skills/tests/ (real unit tests, no external calls): operation-coverage (each frozen op key reachable), local-link resolution within copied folder, 300-line leaf limit, install-block presence, relative-link structural checks, widgets 4 negatives not callable. UNITTEST-055 owns running/validating; DEV may implement harness + claim tests pass only once UNITTEST-equivalent verified (I will run and verify the suite myself).

IMPLEMENTATION PLAN:
1. Add .agents/skills/pal-found self-check OR reuse tests; author pal_found_cli_skills/tests/test_offline_skill_gate.py implementing reusable checks: (a) every namespace SKILL.md has install block exact strings; (b) leaf files (SKILL.md + references/*.md) <=300 lines; (c) relative links in SKILL.md resolve within the folder; (d) each frozen op key appears as a documented record across refs (summary counts per namespace match register); (e) widgets 4 legacy negatives NOT documented as callable.
2. Run full skills pytest; confirm all pass.
3. Commit + time_spent + Resolved (NOT closed; CODEREVIEW-055 handoff). UNITTEST-055 runs same harness as authoritative unit-test gate; DEV only claims pass after verified run.
