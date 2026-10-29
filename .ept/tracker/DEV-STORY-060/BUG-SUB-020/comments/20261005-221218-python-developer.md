Subject: Root cause, fix, and regression
Created: 2026-10-05T22:12:18
Updated: 2026-10-05T22:12:18
---
Root cause: source matrix citations were selected from the public coverage register without checking exact URL presence in each mapped skill section. PM corrected the three affected rows: 5.1 now cites Developer Console create-application; 6 Widget lifecycle cites custom-widgets/create; 7.2 cites Code Repositories navigation. These are the exact public URLs used in the mapped skill text. Independent read-only Python check parsed all 37 matrix rows and found 0 URL mismatches (exit 0); python -m pytest -q tests in pal_found_cli_skills passed 31/31 in 3.22s. The matrix exists and remains indexed. No skill content changed for this defect. Time spent on developer triage and verification: 0.25 hours. Ready for QA verification.
