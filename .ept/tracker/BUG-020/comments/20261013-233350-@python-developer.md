Subject: Models reference correction and verification
Created: 2026-10-13T23:33:50
Updated: 2026-10-13T23:33:50
---
# Changes
Corrected all 14 failed Models records in eight reference files. Four paged commands now describe list stdout and stderr next_page_token; three downloads describe filename under configured root; studio create/get, trainer get/list, latest config null, JSON series failure, and resources example now match source.
# Evidence
Models CLI tests: 33 passed. SDK ResourceConfiguration.model_validate with memory=4G, cpu=2, gpu=V100 passed. Skill suite: 18 passed, 1 deselected; full run 18 passed, 1 failed in unrelated pal-found-orchestration build.jobs guidance for --page-size. Scoped git diff --check passed. Source checked Models CLI _paginate_operation/_download_operation/main, PaginationHelper.emit_metadata, BinaryDownloadHandler._safe_filename, and local SDK models. No code, access control, credentials, or network behavior changed; OWASP review finds no new exposure.
# Follow-up
Independent QA should retest 14 rows and refresh review hashes. Manager should track orchestration gate failure separately. Keep BUG-020 In Progress pending that QA.
