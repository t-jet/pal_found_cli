Subject: python-developer: New->Open DoD and test plan (offline Ontology actions and rich properties content)
Created: 2026-10-12T00:55:58
Updated: 2026-10-12T00:55:58
---
## New -> Open DoD and test plan

**Documentation reviewed**: `.ept/docs/document_index.md`; parent DEV-STORY-047 (offline Ontology actions and rich properties content); BA-ANA-013, BA-DES-013, SA-DES-012. DEV-047 Closed; CODEREVIEW-047 Closed (approved).

**Readiness**: assignee python-developer; priority High; dates set; parent Story context reviewed; no open QUESTION sub-tasks; no blockers identified; Development sub-task Closed so content is ready for tests.

**Scope**: Ontologies actions/rich properties, 39 ops (action, attachments, interface, object_set, transaction, query, media/time-series/cipher properties).

**Test plan (offline)**
1. `python -m pytest tests/test_offline_skill_gate.py tests/test_documented_examples.py -q` from `pal_found_cli_skills/`.
2. Independent probe `.ept/tmp/verify_wave.py` over ['pal-found-ontologies'] for frozen-register reachability, one record per op, example parse, leaf-line limit, relative local-link resolution, install block.
