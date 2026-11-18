Subject: Release acceptance blocked by BUG-051; prior In Progress
Created: 2026-11-18T08:23:30
Updated: 2026-11-18T08:23:30
---
BUG-050 is blocked by active BUG-051 through existing LINK-02096 (BUG-051 Blocks BUG-050). Prior BUG-050 status: In Progress. BUG-051 is High priority, assigned devops-engineer and currently Blocked by Open QUESTION-198.

Exact-head CI run 44247425711 at tool commit 54dfbdefe54820d0722474b7bd2b0095f2eb232e passed six checks: Ruff, mypy and four test jobs. Security Scan failed; Build Package was skipped. DevOps reproduced Safety 3.8.1 introducing filelock through its >=3.16.1,<4.0 constraint, selecting vulnerable 3.32.7. Runtime/dev installation introduces no filelock. Safety exits 64; forcing patched filelock >=4.2.1 conflicts with the published Safety constraint. QUESTION-198 seeks a supported scanner remediation decision.

Retained CI proof .ept/tmp/feature015_tool_bug050_corrected_ci_20261118.json SHA256 a74b8cfddc129464cfe70db2bfcc154a692ba3917ddec49b4195a0f3578a87c8; failure log .ept/tmp/task022_tool_bug050_corrected_security_failure_20261118.log SHA256 c9775c20f3675bcc89073d24dfb5b3b5b5f8de2d6903987d108c69aa7cd7ba0a. DevOps reproduction is documented in BUG-051 comment 20261118-080957-@devops-engineer.

This dependency block concerns publication acceptance. The accepted 197 offline runtime checks and reviewed typing correction remain valid within their recorded scope. External publication, all required CI checks, merged revision and parent-pin acceptance remain pending. No source, resolution or other link changes.
