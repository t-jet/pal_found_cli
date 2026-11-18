Subject: Open DoD and investigation
Created: 2026-10-29T10:43:50
Updated: 2026-10-29T10:43:50
---
## 2026-10-29 source investigation
- Reviewed indexed DESIGN-013, ticket reproduction, related comments and links. No unresolved QUESTION sub-task.
- SDK 1.101.0 receives integer path version; its URL encoder calls quote on that integer and raises TypeError before HTTP. Independent probe records exit 1 and zero requests at a3a38ec.
- Expected GET configVersions/1 with typed ModelStudioConfigVersion. Actual standard TypeError envelope, no request. Synthetic denied-network transport limits evidence to CLI serialization.
- Implement narrow compatibility bridge in Models CLI and verify real SDK 1.101.0 and 1.111.0 wire behavior, guard, timeout, retry, errors and cleanup.
