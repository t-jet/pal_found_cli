Subject: Root cause and implementation evidence
Created: 2026-10-12T11:05:40
Updated: 2026-10-12T11:05:40
---
## 2026-10-12 implementation
- Reproduced defect with frozen-clock fixture: first service_001 comment read back as service; focused suite failed 1 of 20 before fix.
- Root cause: legacy filename parser treats any trailing _NNN as collision suffix, though sanitized author names may contain that suffix. Filename alone cannot resolve old ambiguous records.
- Updated tracker/comments.py: new IDs use timestamp-@author with optional ~NNN collision sequence. Both markers lie outside sanitized author alphabet. Exclusive file creation still protects concurrent writes. Legacy filenames remain readable and updateable under prior interpretation.
- Added focused tests in tests/test_comments.py for service and service_001 mixed names, duplicate same-second writes, legacy references and update. Existing concurrent writer test remains active.
- Verification: focused suite 20 passed; full tracker suite 434 passed in 9.12s; compileall exit 0; CRLF-aware diff check exit 0. Independent QA readback remains pending.
- Scope: old filename service_001 may represent author service_001 or collision 001 for service; historic author cannot be recovered without separate metadata.
