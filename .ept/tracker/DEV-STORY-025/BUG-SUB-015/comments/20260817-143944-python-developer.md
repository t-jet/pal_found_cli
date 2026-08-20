Subject: Fix plan
Created: 2026-08-17T14:39:44
Updated: 2026-08-17T14:39:44
---
Apply the same policy in root, tool, and skills: ignore .env and .env.*, preserve !.env.example and !.env.template, and ignore *.pem, *.key, *.p12, and *.pfx. Add an isolated pytest regression in each repository that runs git ignore checks for protected patterns, confirms the approved exceptions remain usable, and audits the tracked inventory for live credential files. Run each repository's full pytest, Ruff, mypy, and security checks where applicable. Commit and push in dependency order skills, then tool, then root; update tool and skills gitlinks in root to the verified commits. Preserve tracker and workflow data unchanged.
