Subject: Completion evidence
Created: 2026-07-29T15:59:05
Updated: 2026-07-29T15:59:05
---
Completion evidence: foundry-functions CLI implemented with 7 operations; Query, ValueType, and ValueType.VersionId routing; JSON args; boolean flags; FUNCTIONS ACL; no pagination; bytes envelope; console entry and launcher. Verification evidence: targeted functions tests 36 passed; ruff passed; mypy passed; full suite 622 passed; coverage 81.75%; compileall passed; module help exit 0; launcher help exit 0. Non-fatal RequestsDependencyWarning and pytest_asyncio deprecation warning observed. Deliverables changed: src/foundry_cli/functions/__init__.py, src/foundry_cli/functions/scripts/__init__.py, src/foundry_cli/functions/scripts/foundry_functions_cli.py, .claude/skills/foundry-functions/SKILL.md, .claude/skills/foundry-functions/scripts/foundry_functions_cli.py, tests/test_foundry_functions_cli.py, tests/test_functions_console_wrapper.py, pyproject.toml.
