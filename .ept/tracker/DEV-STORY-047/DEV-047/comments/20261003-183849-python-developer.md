Subject: python-developer: New->Open DoD + implementation plan (Ontology actions/rich props 39 ops)
Created: 2026-10-03T18:38:49
Updated: 2026-10-03T18:38:49
---
TRIAGE (New->Open DoD MET):
- Docs studied: document_index, BA-DES-013 sec8 (Ontology actions/rich props), SA-DES-012 sec1/3/4 (split 046/047), parent DEV-STORY-047, frozen register 20261003-174831-tech-lead (12 clients, 39 ops), TESTCASE-006.
- Assignee python-developer; DESIGN-047 Closed; parent in Development. DependsOn DEV-STORY-046 (nav). No open QUESTIONs; Blocked=No.
- Critical thinking: 047 owns only the action/property local part (references/03-actions-rich-properties.md) replacing the 046 placeholder. apply*/create_temporary/post_edits/upload are write/execute; attachment/media/streaming binary semantics verified.

IMPLEMENTATION PLAN:
1. Rewrite references/03-actions-rich-properties.md (placeholder->full) with 39 op records. Split into two parts if >300 lines: 03-actions-rich-properties.md (action/attachment/interface/object_set/transaction/query) + 04-time-series-media.md (cipher/geotemporal/media/time_series). Must align with SKILL.md index.
2. Update ontologies SKILL.md index if part naming changes.
3. Leaf<=300, relative links, install block preserved. Verify+pytest+commit+time_spent+Resolved (NOT closed; CODEREVIEW-047 handoff).
DELIVERABLE: ontologies references 03 (and 04 if split) - 39 action/rich-prop ops.
