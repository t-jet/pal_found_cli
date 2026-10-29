Subject: python-developer: New->Open DoD + implementation plan (Admin identity/access 38 ops + Admin SKILL nav)
Created: 2026-10-03T18:26:48
Updated: 2026-10-03T18:26:48
---
TRIAGE (New->Open DoD MET):
- Docs studied: document_index, BA-DES-013 sec8, SA-DES-012 sec1/3, BA-ANA-013, parent DEV-STORY-042, frozen register 20261003-174711-tech-lead (11 owned clients, 38 ops), TESTCASE-009.
- Assignee python-developer; DESIGN-042 Closed; parent story DEV-STORY-042 in Development. No open QUESTIONs; Blocked=No.
- Fields valid: status Open, High, estimated_hours (20).
- Critical thinking: Admin split 042/043 disjoint; 042 owns Admin SKILL.md navigation + identity part; 043 owns governance part + Audit skill. Preserve FEATURE-008/009 capability+JSON content, FEATURE-011 install block, and Admin capability/source block from existing SKILL.md.

IMPLEMENTATION PLAN (Open->In Progress):
1. Rewrite .agents/skills/pal-found-admin/SKILL.md as entry+nav/index linking both identity (042) and governance (043) parts + audit skill.
2. Author references/01-identity-and-access.md with 38 operation records (auth provider, enrollment, enrollment-role-assignment, group, group-member, group-membership, group-membership-expiration-policy, group-provider-info, role, user, user-provider-info) each: preconditions/effect/inputs/success/failure/example/evidence locators.
3. Leaf<=300 lines, relative links resolve offline, install block + FEATURE-008/009 preserved.
4. Verify + run skills pytest + commit + time_spent + Resolved (NOT closed; CODEREVIEW-042 architect handoff).
DELIVERABLE: admin SKILL.md (nav) + references/01-identity-and-access.md (042 identity part). 043 adds governance part + Audit skill separately.
