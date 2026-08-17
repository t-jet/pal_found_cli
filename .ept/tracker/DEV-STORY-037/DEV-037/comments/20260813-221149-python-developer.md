Subject: Corrected committed implementation evidence and plan
Created: 2026-08-13T22:11:49
Updated: 2026-08-13T22:11:49
---
Commit: 5746815a0d57115048bbea1e0d1009addf2612d2 — docs: complete rename migration verification.

Implemented deliverables: .ept/docs/deliverables/development/DEV-037-rename-migration.md:3-5 confirms runtime behavior remains unchanged; :9-32 maps the 18 public commands; :34-47 covers existing clones and redirects; :49-69 covers install and skill migration; :71-85 covers rollback and verification; :87-92 preserves SDK/runtime and historical-name exceptions. README.md:35-36 links this migration guide. .ept/docs/document_index.md:119 registers the deliverable. tests/test_rename_migration.py:32-42 checks the mapping, :45-53 checks package and entry-point names, and :56-70 runs all 18 direct launcher --help probes.

Plan and acceptance evidence: retain approved SDK and historical names; document the final mapping, migration, rollback, and validation route; prove mappings and launcher reachability with committed regression tests; list changed paths above. Results: focused pytest 15 passed (exit 0); 18/18 direct launcher --help probes passed (exit 0); Ruff, mypy, compileall, scoped diff, and index checks each exited 0. Full suite was intentionally skipped.

External limitation: git submodule status exits 128 because .ept/docs/customer_input/foundry-platform-python is a stale unmapped submodule; installed pal-found commands are absent. This does not invalidate the direct launcher probes, but remote/installed-distribution verification remains unavailable.
