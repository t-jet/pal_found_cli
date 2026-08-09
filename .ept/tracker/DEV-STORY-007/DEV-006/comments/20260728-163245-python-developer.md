Subject: Implementation evidence
Created: 2026-07-28T16:32:45
Updated: 2026-07-28T16:32:45
---
Implementation completed by python-developer. Files changed: .claude/skills/foundry-ontologies/SKILL.md; .claude/skills/foundry-ontologies/scripts/foundry_ontologies_cli.py; src/foundry_cli/ontologies/**; tests/test_foundry_ontologies_cli.py; tests/test_ontologies_console_wrapper.py; pyproject.toml. Scope covers all 67 canonical ontology ops, binary handling, pagination, ACL/read-only/metadata-only guards, retry, error serialization, JSON/TOON output, and B3-only tracing. Test evidence: python -m pytest tests	est_foundry_ontologies_cli.py tests	est_ontologies_console_wrapper.py -q -> 153 passed; python -m pytest -q -> 468 passed. Next: keep DEV-006 In Progress until commit/time-report DoD is satisfied, then move to Resolved for code review.
