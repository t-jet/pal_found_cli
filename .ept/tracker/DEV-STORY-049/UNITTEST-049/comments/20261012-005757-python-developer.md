Subject: python-developer: New->Open DoD and test plan (offline AIP Agents Functions and Language Models operations content)
Created: 2026-10-12T00:57:57
Updated: 2026-10-12T00:57:57
---
## New -> Open DoD and test plan

**Documentation reviewed**: `.ept/docs/document_index.md`; parent DEV-STORY-049 (offline AIP Agents Functions and Language Models operations content); BA-ANA-013, BA-DES-013, SA-DES-012. DEV-049 Closed; CODEREVIEW-049 Closed (approved).

**Readiness**: assignee python-developer; priority High; dates set; parent Story context reviewed; no open QUESTION sub-tasks; no blockers identified; Development sub-task Closed so content is ready for tests.

**Scope**: AIP Agents, 15 ops; Functions, 7 ops; Language Models, 2 ops.

**Test plan (offline)**
1. `python -m pytest tests/test_offline_skill_gate.py tests/test_documented_examples.py -q` from `pal_found_cli_skills/`.
2. Independent probe `.ept/tmp/verify_wave.py` over ['pal-found-aip-agents', 'pal-found-functions', 'pal-found-language-models'] for frozen-register reachability, one record per op, example parse, leaf-line limit, relative local-link resolution, install block.
