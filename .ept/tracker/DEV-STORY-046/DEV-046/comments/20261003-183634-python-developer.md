Subject: python-developer: New->Open DoD + implementation plan (Ontology discovery 28 ops + SKILL nav)
Created: 2026-10-03T18:36:34
Updated: 2026-10-03T18:36:34
---
TRIAGE (New->Open DoD MET):
- Docs studied: document_index, BA-DES-013 sec8 (Ontology discovery group), SA-DES-012 sec1/3/4 (split 046 nav/discovery vs 047 actions/rich, Q-161/Q-162), parent DEV-STORY-046, frozen register 20261003-174821-tech-lead (8 clients, 28 ops), TESTCASE-006.
- Assignee python-developer; DESIGN-046 Closed; parent in Development. DependsOn DEV-STORY-041. No open QUESTIONs; Blocked=No.
- Critical thinking: 046 owns Ontologies SKILL.md navigation to 047's action/property part + discovery local part. Discovery ops are read/query classes (reads never write). Preserve FEATURE-008/009 + FEATURE-011 install block.

IMPLEMENTATION PLAN:
1. Rewrite pal-found-ontologies/SKILL.md as entry+nav/index linking discovery(046) + action/property(047) parts.
2. references/01-discovery-keyed.md(18: action_type4, action_type_full_metadata2, linked_object2, object_type7, ontology4... wait, 8 clients 28) - split into 01-discovery-metadata.md + 02-discovery-objects.md to stay <=300.
3. Leaf<=300, relative links, install block. Verify+pytest+commit+time_spent+Resolved (NOT closed; CODEREVIEW-046 handoff).
DELIVERABLE: ontologies SKILL.md (nav to both parts), discovery references, placeholder link to 047's action/property part.
