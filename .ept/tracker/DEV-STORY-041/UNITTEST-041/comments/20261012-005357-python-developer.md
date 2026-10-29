Subject: python-developer: In Progress->Resolved evidence and coverage (pal-found primer and navigation)
Created: 2026-10-12T00:53:57
Updated: 2026-10-12T00:53:57
---
## In Progress -> Resolved evidence

All checks run offline from `pal_found_cli_skills/`; no network or Foundry calls.

### 1. Skills test suite (authoritative)
`python -m pytest tests -q` -> **606 passed in 127.99s** (exit 0).
Relevant files individually:
- `tests/test_skill_documentation.py` -> 3 passed (capability and parameters, JSON surfaces, media-set variant flags).
- `tests/test_skill_tree_migration.py` -> 4 passed (canonical 20-skill tree, doc-only namespace skills, legacy pointer, README onboarding).
- `tests/test_distribution_commands.py` -> 5 passed (19-folder PowerShell copy completeness and atomicity/sentinel checks).
- `tests/test_offline_skill_gate.py` -> 9 passed (leaf limit, install block, relative links, frozen ops, per-op records and examples, counts, widgets negatives).
- `tests/test_documented_examples.py` -> 1 passed (all documented examples parse with their namespace CLI).

### 2. Independent probe (`.ept/tmp/verify_wave.py pal-found`)
```
=== pal-found ===
  max_leaf_lines=113 (SKILL.md) limit=300 ok=True
  unresolved_local_links=[]
  install_block_missing=[]
```
`pal-found` has no frozen operation register (it is the general navigation/primer skill), so the operation-record checks do not apply. Its 5 Markdown parts resolve their relative links inside the folder and `SKILL.md` carries the FEATURE-011 install block (`conda install -c t-jet pal_found_cli`, `pip install pal_found_cli`, `uv tool install pal_found_cli`).

### 3. Copy integrity
`tests/test_skill_tree_migration.py::test_canonical_skill_tree_has_one_renamed_skill_set` confirms exactly 20 skill folders with matching frontmatter names; `test_distribution_commands.py` confirms the published copy is complete, idempotent, and refuses to mutate on a bad source.

### Coverage
All acceptance criteria for the pal-found content map to an offline passing check. Coverage threshold: 100% of the ticket scope is exercised by the cited tests; the probe adds per-file line and link checks that the suite asserts only in aggregate.

### Time
`time_spent_hours` recorded as **untracked** (contributor hours not measured).

**Result: all tests written/executed and passing (100% pass rate). Ready to advance to Resolved.**
