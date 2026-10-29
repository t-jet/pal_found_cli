Subject: Correction applied: admin op-count labels 20/18 verified + PM parameter gaps closed
Created: 2026-10-11T23:04:11
Updated: 2026-10-11T23:04:11
---
## Correction cycle - CODEREVIEW-042 (implementer: python-developer)

### Sources reviewed
- Reviewer verdict (architect): comment 20261003-190838-architect - HIGH defect, admin per-part op-count labels 15/23 swapped.
- DEV-042 defect record: comment 20261003-190847-architect.
- PM (DEV-STORY-042): comment 20261004-102755-project-manager - Admin parameter gaps.
- Design baseline: SA-DES-012 (admin 66); frozen register identity 38 = 20 (part 01) + 18 (part 02).

### Defect 1 (HIGH): per-part labels swapped
Reviewer assessed commit b37bc3a (DEV-042, 2026-10-03). Confirmed at that commit: SKILL.md index row 01 = 15 (expected 20), row 02 = 23 (expected 18); references/01 header said (15 operations); references/02 header said (23 operations).

Corrective action (delivered): the current content carries the correct labels.
- Fix commit: 45bc51d (2026-10-05).
- pal-found-admin/SKILL.md lines 47-48: 20 and 18.
- references/01-identity-auth-users.md and 02-identity-groups-roles.md headers no longer state an inline count; the index table is the single count source.
- git -C pal_found_cli_skills status --short shows no uncommitted change in the pal-found-admin folder.

Independent verification (counted from actual ### resource.op record headings, not copied from the 66 total):

| Part | File | Records | Index label |
| --- | --- | ---: | ---: |
| 01 identity auth/user | 01-identity-auth-users.md | 20 | 20 |
| 02 identity groups/roles | 02-identity-groups-roles.md | 18 | 18 |
| 03 governance classification | 03-governance.md | 12 | 12 |
| 04 governance access | 04-governance-access.md | 16 | 16 |
| Total | | 66 | 66 |

Matches SA-DES-012 baseline (admin 66) and the frozen identity split 38 = 20 + 18.

### Defect 2: PM parameter gaps (DEV-STORY-042 comment 20261004-102755)
Verified against pinned SDK docs under .ept/docs/customer_input/foundry-platform-python/docs/v2/Admin/:
- group_membership_expiration_policy (references/02 lines 105, 113): maximum_duration = seconds into the future from the time a member is added; maximum_value = absolute latest expiration timestamp; returns GroupMembershipExpirationPolicy. Matches SDK models/GroupMembershipExpirationPolicy.md.
- group_member list (references/02 lines 81, 83): --include-expirations and --transitive are mutually exclusive (cannot both be true). Matches GroupMember.md includeExpirations semantics.
- Fix commit: 1855d29 (2026-10-08).

### Gate verification
python -m pytest pal_found_cli_skills/tests/ -q -> 606 passed, exit 0. (Reviewer expected 23; that was the suite size at review time.)

### Questions
None created. No child QUESTION sub-tasks exist (list --parent CODEREVIEW-042 -> 0). No clarification was needed.

### Residual observation (reviewer awareness; no action taken)
The frozen gate checks per-namespace totals and per-operation record presence/duplicates, but not the per-part index labels this defect touched. Strengthening the gate would change the frozen harness, which is a reviewer/tech-lead decision.

### Result
All requested corrections are implemented and verified. Moving Correction -> Corrected and reassigning to architect. DEV-042 remains Resolved.
