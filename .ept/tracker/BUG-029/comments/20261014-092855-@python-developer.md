Subject: Checkpoint batch example corrected
Created: 2026-10-14T09:28:55
Updated: 2026-10-14T09:28:55
---
Root cause: record.get_batch described RID strings although SDK get_batch body requires GetRecordsBatchRequestElement objects with recordRid. Updated input guidance, output interpretation, and example to use object array. Local SDK Pydantic validation accepts the corrected example. Offline skill gate and documented-example suite: 10 passed. Scoped git diff --check passed. Ready for independent semantic recheck.
