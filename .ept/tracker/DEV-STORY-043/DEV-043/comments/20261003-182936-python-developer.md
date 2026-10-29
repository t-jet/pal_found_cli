Subject: python-developer: New->Open DoD + implementation plan (Admin governance 28 + Audit 2 ops)
Created: 2026-10-03T18:29:36
Updated: 2026-10-03T18:29:36
---
TRIAGE (New->Open DoD MET):
- Docs studied: document_index, BA-DES-013 sec8 (Admin governance+Audit 28+2), SA-DES-012 sec1/3, parent DEV-STORY-043, frozen register 20261003-174720-tech-lead, TESTCASE-009/010.
- Assignee python-developer; DESIGN-043 Closed; parent in Development. DependsOn DEV-STORY-042 (Admin nav). No open QUESTIONs; Blocked=No.
- Critical thinking: 043 owns governance local part (refs/03-governance.md in admin folder, replacing DEV-042 placeholder) + pal-found-audit skill (2 ops: log_file content, list). Worst-effect writers (create/replace/add/remove) documented with permission/side-effect cues.

IMPLEMENTATION PLAN (Open->In Progress):
1. Rewrite .agents/skills/pal-found-admin/references/03-governance.md with 28 governance operation records (cbac_banner, cbac_marking_restrictions, host, marking, marking_category, marking_member, marking_role_assignment, organization, organization_guest_member, organization_role_assignment), preserving the placeholder->full transition.
2. Rewrite .agents/skills/pal-found-audit/SKILL.md as audit entry + record for log_file content(list/config/content) (2 ops: content, list).
3. Leaf<=300; relative links; install block preserved; FEATURE-008/009 retained.
4. Verify + pytest + commit + time_spent + Resolved (NOT closed; CODEREVIEW-043 handoff).
DELIVERABLE: admin/references/03-governance.md (28 ops) + pal-found-audit/SKILL.md (2 ops).
