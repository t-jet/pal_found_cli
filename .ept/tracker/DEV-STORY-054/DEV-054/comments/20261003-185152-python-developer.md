Subject: python-developer: New->Open DoD + implementation plan (Apps/Widgets 17 ops)
Created: 2026-10-03T18:51:52
Updated: 2026-10-03T18:51:52
---
TRIAGE (New->Open DoD MET):
- Docs studied: document_index, BA-DES-013 sec8, SA-DES-012 sec1/3/4 (17 ops + 4 unsupported widgets negatives), parent DEV-STORY-054, frozen register 20261003-174943-tech-lead (third_party_applications9 + widgets8), TESTCASE-021/022.
- Assignee python-developer; DESIGN-054 Closed; parent in Development. No open QUESTIONs; Blocked=No.
- Critical thinking: website deploy/undeploy, version upload/upload_snapshot/delete, repository publish write with material effects; 4 legacy widgets (dev-mode-settings disable/get/pause/set-widget-set) NEGATIVE-only, must be documented unsupported NOT callable. Widgets runtime 8-op surface. Preserve FEATURE-008/009 + FEATURE-011 install blocks.

IMPLEMENTATION PLAN:
1. third-party-applications SKILL.md+refs (third_party_application1/website3/version5 = 9).
2. widgets SKILL.md+refs (dev_mode_settings2/release3/repository2/widget_set1 = 8) + explicit Unsupported section for 4 legacy negatives.
3. Leaf<=300, install block each. Verify+pytest+commit+time_spent+Resolved (NOT closed; CODEREVIEW-054 handoff).
