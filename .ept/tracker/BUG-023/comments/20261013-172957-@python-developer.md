Subject: Root cause and fix scope
Created: 2026-10-13T17:29:57
Updated: 2026-10-13T17:29:57
---
## Root cause
OP_SPECS lists SDK-required keyword inputs under optional. uild_parser() creates flags without requiredness, and _invoke() omits absent values. SDK signature binding then raises before network.

## Scope
Reconcile the 18 listed operations with installed SDK signatures, preserve valid empty JSON objects/lists, update CLI tests and matching offline records. Attachment upload inference stays unchanged.
