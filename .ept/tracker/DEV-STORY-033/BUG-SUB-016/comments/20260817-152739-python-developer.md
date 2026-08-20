Subject: Regression and validation evidence
Created: 2026-08-17T15:27:39
Updated: 2026-08-17T15:27:39
---
The executable regression test extracts the real PowerShell block from the published README and runs it with workspace-path substitution. It verifies all 19 exact skill names, paths containing spaces, source and destination sentinels, stale-target removal, overwrite of corrupted content, no nested skill directories, preservation of unrelated destination directories, and an 18-source failure before mutation. Results: 2 focused tests passed; full skills suite 12 passed; Ruff passed; markdownlint exited 0; documentation link check passed. A clean anonymous clone of the published skills repository passed the same 2 executable tests. No blocking test failure remains; independent QA is still required before closure.
