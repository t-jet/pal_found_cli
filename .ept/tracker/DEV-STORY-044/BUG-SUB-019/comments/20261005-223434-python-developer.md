Subject: Developer root cause and verification plan
Created: 2026-10-05T22:34:34
Updated: 2026-10-05T22:34:34
---
## Root cause
SDK v2 paged methods return AsyncResourceIterator; awaiting them raises before records are emitted. Raw-response wrappers return a single decodable page with data and 
ext_page_token, allowing bounded cursor requests. Current clean checkout already contains a raw-page fix.

## Verification
Check all six paged Datasets operations against SDK signatures, then add regression coverage for initial cursor, empty page, batch limits, and avoidance of ordinary iterator methods. Run focused and full tests before resolving.
