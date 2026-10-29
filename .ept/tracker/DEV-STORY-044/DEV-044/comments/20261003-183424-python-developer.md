Subject: python-developer: Implementation complete + Resolve evidence (Datasets 33 ops)
Created: 2026-10-03T18:34:24
Updated: 2026-10-03T18:34:24
---
IMPLEMENTED (SA-DES-012 sec3/4 + DEV-044 ACs, frozen register 174735):
DELIVERABLE FILES (committed 082764d in pal_found_cli_skills@main):
- .agents/skills/pal-found-datasets/SKILL.md (86) - entry+nav, index to 5 refs, install block, JSON variants retained.
- references/01-dataset.md (131, dataset 11) includes put_schema/get_schema_batch JSON body + read-table data-volume cues.
- references/02-branch.md (69) - branch 5.
- references/03-file.md (73) - file 5, binary upload/download bounds.
- references/04-transaction.md (91) - transaction 6, abort/build/commit/create/get/job; async build requires status check.
- references/05-view.md (86) - view 6.

Total 33 ops matches frozen register (TESTCASE-003 counts: Dataset 11/Branch 5/File 5/Transaction 6/View 6). Each record: class/precondition/effect/inputs/success/failure/example + evidence locators (CLI parser pal_found_datasets_cli path, SDK paths, pinned commit 2da67907, reviewer architect, QA TESTCASE-003 + migration TESTCASE-039/040).

VERIFICATION: leaf<=300 (max 131); relative links resolve offline; install block conda/pip/uv; FEATURE-008 source + FEATURE-009 JSON variants retained; hygiene test (no stale _cli.py/scripts in SKILL.md) passed after removing parser path from SKILL.md. regression python -m pytest => 16 passed. time_spent 3/20. CODEREVIEW-044 bidir RelatesTo.

RESOLVED DoD: files exist+committed, leaf+links+install OK, tests pass, standards met. NOT Closed - pending CODEREVIEW-044 architect review.
