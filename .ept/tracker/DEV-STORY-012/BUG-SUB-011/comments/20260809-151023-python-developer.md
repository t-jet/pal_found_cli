Subject: Root cause and fix plan
Created: 2026-08-09T15:10:23
Updated: 2026-08-09T15:10:23
---
Root cause: ConfigLoader did not expose the global enabled setting, and AccessControlGuard started at namespace and operation controls. Plan: add ENV_ENABLED and global_enabled with a true default and canonical false-token parsing, then enforce global enablement as absolute precedence step 0 before narrower controls. Namespace or operation true must never bypass global false. Add real ConfigLoader/guard regressions for both Language Models operations plus Datasets and Audit, asserting AccessControlError before any client call. The QA report linked in the ticket contains the failing environment and application evidence. Implement and validate in commit a74d3f4; no question or external blocker remains.
