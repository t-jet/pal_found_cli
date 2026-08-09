---
id: UNITTEST-004
type: unittest
title: Add unit coverage for ACL and pagination common components
status: Closed
created: 2026-07-22
updated: 2026-07-26
priority: Critical
assignee: python-developer
reporter: architect
estimated_hours: 6
time_spent_hours: 1
---

## Scope
Add pytest coverage for AccessControlGuard and PaginationHelper.

## Acceptance criteria
- Cover each ACL precedence step and conflict, including ENABLED=false precedence, READONLY=false overrides, global READONLY blocking writes, and default full access.
- Cover namespace METADATA_ONLY=false overriding global METADATA_ONLY=true and global metadata-only blocking writes.
- Verify datasets.file.content is denied under global metadata-only, datasets.dataset.get is permitted by the allow-list, and read_table is denied.
- Assert AccessControlError exit code 8 and blocked-rule details.
- Cover invalid and zero page sizes, max batch cap, missing next token, null/no-more-pages metadata, stderr metadata separator, and SDK page-token propagation.
- Prove the allow-list parser accepts only canonical backticked SDK paths with PERMITTED status from metadata-allow-list.md.
- Keep tests isolated from external services.
