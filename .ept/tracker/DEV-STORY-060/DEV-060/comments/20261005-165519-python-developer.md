Subject: Internal SDK shorthand regression gate
Created: 2026-10-05T16:55:19
Updated: 2026-10-05T16:55:19
---
Extended pal_found_cli_skills/tests/test_foundry_development_skill.py negative scan to reject distributed docs/v2/... SDK authoring paths. Read-only scan found these in multiple existing skill pages; DEV-STORY-056 cleanup owner is correcting content. REST source-review matrix disposition now states Mapped; SDK contract verified, with evidence from local SDK Dataset.md, public Get Dataset and Paging pages, and DEV-059 comment 20261005-163139-project-manager. No skill content files edited. This post-commit test change requires central follow-up commit and rerun before closure.
