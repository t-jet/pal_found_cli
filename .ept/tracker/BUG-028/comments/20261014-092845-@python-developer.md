Subject: Connectivity guidance corrected
Created: 2026-10-14T09:28:45
Updated: 2026-10-14T09:28:45
---
Root cause: five operation records copied SDK result or input details without checking CLI presentation and SDK security notes. Updated connection.create JDBC example with required jdbcProperties and explained temporary plaintext handling. Explained exportEnabledWithoutMarkingsValidation responsibility and update_secrets processing. File/table import list records now describe item-list stdout, cursor metadata on stderr, and all four paging flags. Local SDK Pydantic validation accepts JDBC example. Offline skill gate and documented-example suite: 10 passed. Scoped git diff --check passed. Ready for independent semantic recheck.
