Subject: Corrected committed unit-test evidence and test plan
Created: 2026-08-13T22:11:58
Updated: 2026-08-13T22:11:58
---
Commit: 5746815a0d57115048bbea1e0d1009addf2612d2 — docs: complete rename migration verification.

Committed test plan and coverage: tests/test_rename_migration.py:32-42 verifies the public mapping and approved migration guide content, including each old/new namespace pair; :45-53 verifies pyproject package metadata, all 18 public entry points, and absence of legacy command entries; :56-70 executes every direct renamed launcher with --help and requires exit 0 plus usage output. Supporting paths are .ept/docs/deliverables/development/DEV-037-rename-migration.md:9-32 (mapping), :71-85 (rollback and verification), README.md:35-36, and .ept/docs/document_index.md:119.

Results: focused pytest 15 passed (exit 0); 18/18 direct launcher --help probes passed (exit 0); Ruff, mypy, compileall, scoped diff, and index checks each exited 0. Full suite was intentionally skipped. Coverage includes mapping, package/entry-point, and launcher behavior cases.

External limitation: git submodule status exits 128 because .ept/docs/customer_input/foundry-platform-python is stale and unmapped; installed pal-found commands are absent. Direct launchers pass, but installed-distribution verification remains unavailable.
