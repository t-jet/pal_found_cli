Subject: P1 fix applied — Claude skill and launcher added (CODEREVIEW-019)
Created: 2026-08-10T19:28:57
Updated: 2026-08-10T19:28:57
---
## P1 corrective action — missing skill deliverable (2026-08-10)

### Root cause
`.claude/skills/foundry-checkpoints/` did not exist — no `SKILL.md`, no launcher. DESIGN-019 Component breakdown lists "Claude skill and launcher for `foundry-checkpoints`" as a deliverable, and every prior namespace ships `.claude/skills/<ns>/SKILL.md` + thin launcher in its DEV commit (e.g. `62c269f` for connectivity/media-sets). The DEV-019 commit `b0df380` shipped the CLI but omitted the skill deliverable.

### Fix applied (commit f63a12c)
- Created `.claude/skills/foundry-checkpoints/SKILL.md` — documents the exact 3-op catalog (`record get` / `record get-batch` / `record search`), the `--records-json` / `--where-json` flags, cursor pagination on `record search` only (`--page-size`/`--page-token`/`--all`/`--max-pages`, max 40 pages), the all-read ACL classification with metadata-only permitting exactly 3/3, `include_attribution=False`, ADR-002 retry policy (all ops safe to retry), and privacy rules.
- Created `.claude/skills/foundry-checkpoints/scripts/foundry_checkpoints_cli.py` — thin launcher re-exporting `build_parser`, `console_main`, `main` from `foundry_cli.checkpoints.scripts.foundry_checkpoints_cli` (mirrors the connectivity launcher pattern).
- Added `tests/test_checkpoints_console_wrapper.py` — launcher delegation test (importlib: launcher re-exports packaged interfaces, no business logic) and launcher `--help` exit 0 subprocess test.

### Verification
- Launcher `--help` exits 0 and lists `record`.
- `compileall -q src` exit 0; ruff clean; mypy source 0 errors.
- Focused suites: `tests/test_foundry_checkpoints_cli.py` (25) + wrapper (3) = 28 passed.
- Full suite: **1276 passed, 0 failed** (was 1267 before this correction).

### Impact
No CLI surface change; no changes to `src/foundry_cli/checkpoints/`. Only the missing skill deliverable and its coverage were added.

Requesting re-review. Moving CODEREVIEW-019 Correction → Corrected, reassigned to tech-lead.
