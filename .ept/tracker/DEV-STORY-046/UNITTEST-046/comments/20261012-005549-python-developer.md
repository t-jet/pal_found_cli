Subject: python-developer: New->Open DoD and test plan (offline Ontology discovery operations content)
Created: 2026-10-12T00:55:49
Updated: 2026-10-12T00:55:49
---
## New -> Open DoD and test plan

**Documentation reviewed**: `.ept/docs/document_index.md`; parent DEV-STORY-046 (offline Ontology discovery operations content); BA-ANA-013, BA-DES-013, SA-DES-012. DEV-046 Closed; CODEREVIEW-046 Closed (approved).

**Readiness**: assignee python-developer; priority High; dates set; parent Story context reviewed; no open QUESTION sub-tasks; no blockers identified; Development sub-task Closed so content is ready for tests.

**Scope**: Ontologies discovery, 28 ops (action_type, action_type_full_metadata, linked_object, object_type, ontology, ontology_object, ontology_value_type, query_type).

**Test plan (offline)**
1. `python -m pytest tests/test_offline_skill_gate.py tests/test_documented_examples.py -q` from `pal_found_cli_skills/`.
2. Independent probe `.ept/tmp/verify_wave.py` over ['pal-found-ontologies'] for frozen-register reachability, one record per op, example parse, leaf-line limit, relative local-link resolution, install block.
