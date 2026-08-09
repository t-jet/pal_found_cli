Subject: Post-resolution error-envelope fix
Created: 2026-08-01T20:16:25
Updated: 2026-08-01T20:16:25
---
Post-resolution unit testing exposed an unexpected/HTTP 503 error-envelope mismatch. The production path was corrected in isolated commit b4e241c94fb5305fa480615c49b23965151b5376 by classifying the exception once with ErrorSerializer and reusing that classification for both the deterministic exit code and serialized envelope, preventing divergent error identities. The commit modifies only src/foundry_cli/audit/scripts/foundry_audit_cli.py; the file was physically verified and is clean against the commit. This fix is included in CODEREVIEW-010 scope together with implementation commit 0c705b8928a5a7792dfb1f0df2e13fae131b9376 and test commit af5b4e326c808618a9846b5479a61dd8d0a2e62f. DEV-010 remains Resolved pending review approval; no Closed transition is claimed.
