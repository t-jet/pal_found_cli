Subject: Evidence: JSON and parameter validation
Created: 2026-08-13T20:16:09
Updated: 2026-08-13T20:16:09
---
Test plan and evidence:
- Audit JSON formats and parameter variants against all 18 build_parser functions; check examples, choices, short forms, positional variants, line limits, and referenced parts.
- Coverage: parser audit all 18 build_parser functions missing=-; all 18 capability sections/files <=300 lines; official URLs HTTP 200.
- Checks: targeted pytest 8 passed; latest focused pytest 1,092 passed, 5 warnings; ruff, mypy, compileall exit 0.
