Subject: Fix plan
Created: 2026-08-17T13:03:45
Updated: 2026-08-17T13:03:45
---
Estimate: 4-6 hours.

1. Classify tool, skill, root, documentation, CI, and test paths against BA-DES-004, SA-DES-003, and the DEV-024 split manifest.
2. In temporary working copies only, use git-filter-repo to build separate tool and skills histories. Keep the current checkouts untouched during the dry run.
3. Merge each filtered lineage into its destination main branch with allow-unrelated-histories. Preserve published commits and require a fast-forward result before any push.
4. Adapt destination documentation, CI, packaging, launchers, and tests to their new repository boundaries.
5. Verify moved-path history, clean tool installation, launchers, tool tests, skill inventory and discovery, CI configuration, and secret/security checks.
6. Commit each destination repository. Remove moved ownership from root, then update root references and gitlinks.
7. Run root tests, public URL probes, and a clean recursive clone. Review every diff and test result before pushing.
8. Push destination and root branches only when the dry run proves each update is fast-forward and reproducible.

Main risks are overlapping CI/test ownership and root tests that still assume the old layout. Resolve ownership from the design records first; update or relocate affected tests without weakening coverage.
