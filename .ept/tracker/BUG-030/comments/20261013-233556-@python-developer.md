Subject: Root cause and output contract
Created: 2026-10-13T23:35:56
Updated: 2026-10-13T23:35:56
---
## Root cause
_page_data reduces each SDK object-set response to data and 
ext_page_token. The three load response models also return count, mapping, compute, security, or transaction fields, so those fields disappear before PaginationHelper emits metadata.

## Output contract
Keep loaded items on stdout. For the three affected operations, pass all response fields other than items and cursor as page_metadata. PaginationHelper will emit them as ordered esponse_metadata entries on stderr, one per fetched page. This preserves pagination and page-specific meaning without merging distinct page values.
