Subject: Ontology record corrections implemented
Created: 2026-10-13T11:31:39
Updated: 2026-10-13T11:31:39
---
## Source and changes
- Compared Ontology CLI OP_SPECS, _invoke, _invoke_paginated, and PaginationHelper with local Foundry SDK models and methods.
- Corrected selector preconditions, metadata/value failures, linked-object missing-link behavior, interface-search map example, stream encoding flag, and media-upload header guidance.
- Corrected 15 BUG-011 paginated operation result descriptions to distinguish CLI stdout item lists and stderr cursor metadata from SDK page models. The get_edits_history section remains under the separate BUG-013 owner.
- Corrected Ontology SKILL.md index: attribution is a scalar string; object-primary-key is JSON.
## Verification
- python -m pytest tests/test_offline_skill_gate.py -q: 9 passed, exit 0.
- git diff --check on Ontology references: exit 0.
- Independent semantic QA and BUG-011 runtime retest remain pending; no status transition requested.
