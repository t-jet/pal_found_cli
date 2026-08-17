Subject: Evidence: JSON and parameter documentation
Created: 2026-08-13T20:16:04
Updated: 2026-08-13T20:16:04
---
Implementation plan and acceptance evidence:
- Document JSON schemas and parameter variants derived from argparse and JSON handling in src/foundry_cli; include flags, choices, short forms, and positional variants; keep each file <=300 lines.
- Evidence: parser audit all 18 build_parser functions missing=-; all 18 capability sections/files <=300 lines; 19 Source lines; official URLs HTTP 200.
- Quality checks: targeted pytest 8 passed; latest focused pytest 1,092 passed, 5 warnings; ruff, mypy, compileall exit 0.
