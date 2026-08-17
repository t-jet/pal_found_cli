Subject: Resolved evidence
Created: 2026-08-13T19:10:12
Updated: 2026-08-13T19:10:12
---
Implemented in commit 2d96c2f. Files: src/foundry_cli package tree renamed to src/pal_found_cli with pal_found_* modules; pyproject.toml, conda.recipe/meta.yaml, .github/workflows/ci.yml, .env.example, .gitmodules, README.md, and .ept/docs updated; all tests renamed or updated. Protected pre-existing src/foundry_cli/_version.py was not changed. Full pytest passed 1370 tests at 86.40% branch coverage; ruff, mypy, compileall, and clean wheel check passed. Clean wheel contains no foundry_cli/ entries.
