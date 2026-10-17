Subject: python-developer: New->Open DoD and test plan (offline integration review harness and coverage register)
Created: 2026-10-12T01:00:12
Updated: 2026-10-12T01:00:12
---
## New -> Open DoD and test plan

**Documentation reviewed**: `.ept/docs/document_index.md`; parent DEV-STORY-055 (offline integration review harness and coverage register); BA-ANA-013, BA-DES-013, SA-DES-012. DEV-055 Closed; CODEREVIEW-055 Closed (approved).

**Readiness**: assignee python-developer; priority High; dates set; parent Story context reviewed; no open QUESTION sub-tasks; no blockers identified; Development sub-task Closed so content is ready for tests.

**Scope**: reusable coverage/link/mock harness + signed 351-operation register; 19 skill folders.

**Test plan (offline)**
1. `python -m pytest tests/test_offline_skill_gate.py tests/test_offline_topic_acceptance.py tests/test_offline_topic_acceptance_guards.py tests/test_offline_rest_wave1.py tests/test_offline_rest_acceptance.py -q` from `pal_found_cli_skills/`.
2. Independent probe `.ept/tmp/verify_wave.py` over ['(harness only)'] for frozen-register reachability, one record per op, example parse, leaf-line limit, relative local-link resolution, install block.
