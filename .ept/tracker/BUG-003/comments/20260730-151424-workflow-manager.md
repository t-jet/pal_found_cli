Subject: Implementation and verification evidence
Created: 2026-07-30T15:14:24
Updated: 2026-07-30T15:14:24
---
Root cause: ticket frontmatter and CSV index can diverge; frontmatter is canonical. Implementation adds reconcile-index --author ROLE [--apply]. Check mode reports mismatches; apply mode writes canonical ticket-file statuses to the index while preserving ticket timestamps, comments, links, and content. Changed paths: .ept/skills/tracking-system/references/REFERENCE.md; tracker/index.py; tracker/tickets.py; tracker/build_queue.py; tracker/automations.py; tracker/argument_parser.py; tracker/cli.py; tracker/handlers/__init__.py; tracker/handlers/index_handlers.py; tests/test_status_reconciliation.py. Verification: 5 targeted reconciliation tests passed; 424 full tracker tests passed; focused Ruff and diff checks passed. Full Ruff still reports unrelated pre-existing cli_test_handler.py errors. No live tracker state was changed during implementation or testing.
