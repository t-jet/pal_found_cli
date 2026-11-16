---
id: QUESTION-195
type: question
title: 'How should the three un-merged FEATURE-015 bug fixes reach skills main: merge integration
  or cherry-pick?'
status: Closed
addressed_to: architect
created: 2026-10-25
updated: 2026-10-27
priority: High
assignee: architect
reporter: project-manager
time_spent_hours: 2
---

# QUESTION-195: How should the three un-merged FEATURE-015 bug fixes reach skills main: merge integration or cherry-pick?

## Description

## Question

Three of the four open bug fixes are absent from the deployable pal_found_cli_skills main (716a85b). They live on origin/feature015/integration. What is the correct way to land them?

## Evidence

- BUG-035 fix: commit 65430e9. Audit SKILL.md SHA at main = c040dd592980bf28a93285171a541211e8871b0879b7fc83f293b3e09c5d74ba (original broken hash); at integration = 90f95b408320c92cf389d03f648785cde7ed623dedd7d268087bbc5b40b9ae4d (recorded corrected hash). Zero api:audit-read matches at main.
- BUG-SUB-027/028 fix: commit 27b147f. GroupMembershipExpirationPolicy/replace.py, Group/get_batch.py, User/get_batch.py all differ between main and 27b147f.
- BUG-SUB-025 fix: d2ce40a IS on main.
- Parent gitlink pins skills 716a85b, so none of the corrected audit/admin content is in the deployable bundle.

## Topology

- merge-base(main, integration) = 04e860f. Integration is 100 ahead, 1 behind main.
- main's 1 unique commit is 716a85b (QUESTION-189 merge: strengthened whole-tree .py gate, pre-ruling examples/ removed).
- integration does NOT contain main's QUESTION-189 fix; its gate uses whole-tree rglob and its data-health folder is doc-only, so semantically adjacent.
- git merge-tree main integration = exactly ONE conflict: tests/test_skill_tree_migration.py.
- integration carries 443 files / ~601k insertions (FEATURE-015 REST authoring stream).

## Options

A. Merge origin/feature015/integration into skills main now, resolving the single gate conflict to main's strengthened whole-tree form. Lands all three fixes; matches DEV-STORY-070 publish ownership.
B. Cherry-pick only 65430e9 and 27b147f onto main, leaving the rest of the integration stream for later.
C. Other.

## Requested answer

State the ruling (A, B, or other), the correct gate-conflict resolution, whether the parent gitlink re-pin rides with it, and which ticket/role owns the execution.

## Research Done

Read-only investigation of the pal_found_cli_skills submodule (origin remote `t-jet/pal_found_cli_skills`) plus tracker governance. No repository was modified.

### Ref state

- skills main = 716a85b (parents 419b261, 04e860f)
- origin/feature015/integration HEAD = 2190c40
- `git rev-list --left-right --count main...integration` = `1  100`

### Topology correction: TWO merge bases

`git merge-base --all main integration` returns both 04e860f and 419b261 (criss-cross). `git merge-tree --write-tree` uses stage-1 blob 8f3ed81 and reports exactly ONE conflicted path: tests/test_skill_tree_migration.py.

### BUG-035 fix (65430e9) does not reproduce the accepted hash alone

sha256 of .agents/skills/pal-found-audit/SKILL.md:

| Ref | sha256 |
| --- | --- |
| main | c040dd592980bf28a93285171a541211e8871b0879b7fc83f293b3e09c5d74ba |
| 65430e9 | f648831f0e7ad577ec4500645f63feada5d0b3214e61ec786f6f446ef30ba1d5 |
| 1ece38f | 90f95b408320c92cf389d03f648785cde7ed623dedd7d268087bbc5b40b9ae4d |
| integration HEAD | 90f95b408320c92cf389d03f648785cde7ed623dedd7d268087bbc5b40b9ae4d |

The accepted corrected hash 90f95b40 is reproducible only from the integration lineage. 1ece38f (2026-10-17, "Remove CLI installation prose from distributed skills") is the last commit touching the file and removed 15 lines (5215 to 4923 bytes). A cherry-pick of 65430e9 lands the superseded f648831f content and reinstates the CLI install prose the distribution rules removed.

### BUG-SUB-027/028 fix (27b147f) is content-stable to integration HEAD

All 9 touched files (7 examples, 2 reference markdown) equal the integration HEAD blob, and main equals the pre-fix parent blob. Sample:

| File | main | 27b147f | integration HEAD |
| --- | --- | --- | --- |
| examples/rest/071/v2/admin/Group/replace.py | 245615880460 | e91403986966 | e91403986966 |
| examples/rest/071/v2/admin/Group/get_batch.py | e7c6a9f3d26e | 3b7e44db0c6f | 3b7e44db0c6f |
| references/rest/v2/admin/Group.md | 1cfa6258b326 | 5ac37a2ac3e4 | 5ac37a2ac3e4 |

### BUG-SUB-025 fix (d2ce40a)

Already on main (ancestor check exit 0). Ticket premise correct.

### Gate strength: the ticket premise is inverted

- main gate blob d1478545 (introduced by 9bf8771): bans scripts/; bans any .py anywhere in the namespace skill folder (rglob); bans "python pal_found_" in SKILL.md; requires the backticked command name.
- integration gate blob 9a82c8cf (introduced by addc228): bans scripts/; ALSO bans an examples/ dir; bans 8 suffixes (.py .pyi .sh .ps1 .bat .cmd .js .mjs) anywhere excluding __pycache__; same SKILL.md assertions; its own comment already cites QUESTION-189.

The integration gate is a strict superset of main's. It is stronger, not merely adjacent, and already implements the QUESTION-189 doc-only ruling.

### Compliance measurement

| Ref | namespace files | executable-suffix matches | examples/ paths |
| --- | --- | --- | --- |
| main | 146 | 0 | 0 |
| integration | 146 | 0 | 0 |
| merged tree 6bbb032 | 146 | 0 | 0 |

The 3 files present in integration but absent from main under .agents/skills/pal-found-dev are inside pal-found-dev, which both gate variants exclude from the namespace loop. The data-health fixture sits at tests/fixtures/offline/data-health/ on both refs, not in the distributed folder. No gate risk on either side.

### Governance

- DEV-STORY-070 "Verify offline semantic development completeness and publish reviewed skills" (Development, assignee qa-engineer) owns publish and the parent pin. Children: DESIGN-066 Closed, DEV-066 In Progress, UNITTEST-065 In Progress, CODEREVIEW-066 New (architect), TESTCASE-065 In Progress, TESTEXEC-065 Open, DEVOPS-047 Open (devops-engineer).
- DEVOPS-047 "Publish accepted offline skills to existing GitHub repository" is the executing sub-task (Contains LINK-01697 from DEV-STORY-070).
- QUESTION-189 Closed: distributed namespace skills must be doc-only.
- Parent repo gitlink 160000 commit 716a85b pal_found_cli_skills, last bumped by 2bc017bb.

## Answer

Ruling: Option A. Merge origin/feature015/integration into skills main, resolve the single gate conflict to the integration side, then publish and re-pin. Option B (cherry-pick 65430e9 and 27b147f) is rejected on evidence, not preference.

### Rationale

1. Option B cannot deliver BUG-035 as accepted. 65430e9 alone yields f648831f, not the accepted 90f95b40. The accepted artifact exists only in the integration lineage via 1ece38f. Cherry-picking the fix commit re-opens BUG-035 and re-introduces removed CLI install prose. Landing BUG-035 correctly would require cherry-picking an unbounded tail of the integration stream, which is Option A with worse provenance.
2. The gate conflict is a merge artifact, not a real disagreement. Both variants enforce the same QUESTION-189 rule; integration's is strictly stronger. Both sides measure 0 executable and 0 examples/ paths in namespace skills.
3. git merge-tree shows one conflicted file and nothing else, so a merge loses nothing from either side, preserves main's 716a85b content, and lands the reviewed FEATURE-015 REST authoring stream as one auditable unit.
4. Option B leaves main un-publishable: three ad-hoc fixes without the 443-file stream the reviews and QA evidence actually cover, so main would not be the reviewed bundle DEV-STORY-070 owns.

### Gate conflict resolution

Resolve tests/test_skill_tree_migration.py to the INTEGRATION (theirs) variant 9a82c8cf. It is the strict superset and already implements QUESTION-189, so it satisfies both branches' intent. Taking main's variant would be a silent gate regression: it drops the examples/ ban and 7 of the 8 banned suffixes, re-opening the QUESTION-189 defect class. Do not hand-merge into a third form; the integration blob is the reviewed version.

Post-resolution verification: `python -m pytest tests/test_skill_tree_migration.py -q` must pass, and the namespace audit on the merge result must show 0 executable-suffix matches and 0 examples/ paths under .agents/skills/pal-found-* excluding pal-found and pal-found-dev.

### Parent gitlink re-pin

The re-pin does NOT ride with this question, and this ruling does not perform it. It follows the merge, in the parent repository, as its own commit. DEV-STORY-070 owns the publish and the parent pin; DEVOPS-047 executes the publication. The parent currently pins 716a85b and must be re-pointed to the merge commit after the merge lands and its gate passes.

### Ownership and sequencing

1. python-developer executes the merge and gate-conflict resolution in pal_found_cli_skills, under a merge task owned by DEV-STORY-070. Approver: architect (CODEREVIEW-066).
2. devops-engineer performs the publish and the parent gitlink re-pin under DEVOPS-047.
3. qa-engineer verifies BUG-035 acceptance (audit SKILL.md sha256 = 90f95b40) and the BUG-SUB-027/028 admin file hashes on the merge result before DEVOPS-047 closes.

Nothing in this ruling authorizes a push or merge by this question.

## Acceptance Criteria

- [x] Ruling stated, with gate-conflict resolution, pin ownership, and executing role/ticket identified.

## Related Documentation

- `.ept/docs/document_index.md` (governance context).
- Governance tickets: DEV-STORY-070, DEVOPS-047, QUESTION-189.

## Notes

Evidence is read-only git output from the pal_found_cli_skills submodule plus tracker queries. Key refs: main 716a85b; integration HEAD 2190c40; merge bases 04e860f and 419b261; fixes 65430e9 and 27b147f and d2ce40a; superseding commit 1ece38f; merged-tree probe 6bbb0323a2c350669c1e4f0a132da5b3d0f75341.
