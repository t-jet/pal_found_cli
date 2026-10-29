Subject: Admin search page records fixed
Created: 2026-10-14T09:33:29
Updated: 2026-10-14T09:33:29
---
Root cause: Admin page collector read items, but SDK SearchGroupsResponse and SearchUsersResponse put records in data. Both search operations now read data and retain the existing items fallback. Two-page batches emit three flat records with pages_fetched=2 and total_items=3; one-page batches keep the page-2 cursor. Verified with the reported repro, four SDK-model regression cases, and the 238-test Admin suite. Scoped diff check is clean. Independent QA remains pending.
