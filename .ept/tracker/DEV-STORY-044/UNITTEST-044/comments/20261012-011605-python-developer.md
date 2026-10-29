Subject: python-developer: Open->In Progress DoD and test plan (offline Datasets operations content)
Created: 2026-10-12T01:16:05
Updated: 2026-10-12T01:16:05
---
## Open -> In Progress DoD and test plan

**Documentation reviewed**: `.ept/docs/document_index.md` (BA-ANA-013, BA-DES-013, SA-DES-012 entries); parent DEV-STORY-044 scope and acceptance criteria; linked QUESTION-187 (Closed). Predecessors DESIGN-044, DEV-044, CODEREVIEW-044 all Closed.

**Critical thinking**: this ticket verifies documentation content, not executable Python, so the applicable quality gates are the offline skill-gate checks (frozen-register reachability, exactly one record per frozen operation, parseable example per record, <=300-line leaves, in-folder relative links resolve, install-prerequisite block present) plus the independent per-namespace probe. Verification is re-run now because the ticket was previously only blocked, never completed.

**Questions**: linked QUESTION-187 is terminal (Closed, answer: proceed to closure; parent returned to Development). No other question sub-tasks open.

**Prerequisites**: DEV-044 Closed; CODEREVIEW-044 Closed (approved); authored content ready for tests.

**Scope**: Datasets, 33 ops across `references/01-dataset.md` (11), `02-branch.md` (5), `03-file.md` (5), `04-transaction.md` (6), `05-view.md` (6); `SKILL.md` (95 lines).

**Test plan (offline, no network)**
1. `python -m pytest tests/test_offline_skill_gate.py tests/test_documented_examples.py tests/test_skill_documentation.py tests/test_repository_hygiene.py -q` from `pal_found_cli_skills/`.
2. Independent probe `python .ept/tmp/verify_wave.py pal-found-datasets` for frozen-register reachability, one record per frozen op, example parse, leaf-line limit (<=300), relative local-link resolution, install block presence.

**Related documentation**: `.ept/docs/deliverables/business_analysis/BA-ANA-013-offline-foundry-knowledge.md`, `.ept/docs/deliverables/business_design/BA-DES-013-offline-foundry-skill-guidance.md`, `.ept/docs/deliverables/architecture/SA-DES-012-offline-foundry-skill-technical-design.md`.
