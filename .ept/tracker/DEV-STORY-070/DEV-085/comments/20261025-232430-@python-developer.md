Subject: Verification: gate test, audit SHA256 90f95b40 match, namespace scan, full suite
Created: 2026-10-25T23:24:30
Updated: 2026-10-25T23:24:30
---
# Verification (DEV-085)

All commands run in `pal_found_cli_skills` at merge commit cee3d98.

## 1. Gate test
- `python -m pytest tests/test_skill_tree_migration.py -q` -> **4 passed** (20.21s).
- Re-run on committed tree together with the other suites: `python -m pytest tests/test_skill_tree_migration.py tests/test_skill_documentation.py tests/test_offline_skill_gate.py tests/test_repository_hygiene.py -q` -> **22 passed** (6.07s).

## 2. Audit fix present and hash matches (BUG-035)
- `Get-FileHash .agents/skills/pal-found-audit/SKILL.md -Algorithm SHA256` = `90f95b408320c92cf389d03f648785cde7ed623dedd7d268087bbc5b40b9ae4d`.
- MATCHES the accepted hash 90f95b40 exactly. This is the artifact the architect ruling (QUESTION-195) required; cherry-picking 65430e9 alone would have produced f648831f.
- Required strings present:
  - line 22: `Create datasets with audit logs for the organization`
  - line 25: `api:audit-read`
- Fix commits are ancestors of HEAD: `git merge-base --is-ancestor` exit 0 for 65430e9, 1ece38f, and 27b147f.

## 3. Namespace skill folders clean
- 18 `pal-found-*` folders (excluding pal-found, pal-found-dev).
- Executable scan over `.py .pyi .sh .ps1 .bat .cmd .js .mjs` (excluding `__pycache__`): **0 files**.
- No `examples/` dir, no `scripts/` dir in any of the 18.

## 4. Full suite
- `python -m pytest tests -q` -> **729 passed, 1 failed** in 125.30s.
- The single failure is `tests/test_documented_examples.py::test_every_operation_example_parses_with_its_namespace_cli`: `ModuleNotFoundError: No module named toon_format` (raised from `pal_found_cli/common/output_formatter.py:24`).
- Classification: PRE-EXISTING and ENVIRONMENTAL, not a merge regression. Proven by checking out pristine `main` (716a85b) into a throwaway worktree and running the same test there: it fails identically (1 failed in 0.25s). `toon-format==1.2.0` is declared in the tool `pyproject.toml` but is not installed in this environment (`python -m pip show toon-format` -> not found). The merge does not touch `test_documented_examples.py` (same blob 84e7d27 on main and integration).

## 5. Admin fixes (BUG-SUB-027/028)
- `27b147f` is an ancestor of HEAD. Its nine changed files under `.agents/skills/pal-found-dev/examples/rest/071/v2/admin/**` and `references/rest/v2/admin/**` are present in the merged tree.
- BUG-SUB-025 (`d2ce40a`) was already on main; unchanged.

## 6. Notable deliberate content change (not a loss)
- `.agents/skills/pal-found-admin/SKILL.md` drops the `## Install requirement` prose block. That removal comes from integration commit `1ece38f` ("Remove CLI installation prose from distributed skills"), the same commit the ruling cited as trimming the audit page. Merge deleted 0 files overall.
