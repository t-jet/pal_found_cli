Subject: Fix, verification, and security review
Created: 2026-10-14T09:28:43
Updated: 2026-10-14T09:28:43
---
## Fix (2026-10-14)
_page_data now keeps every non-item, non-cursor SDK page field in page_metadata for ontology_object_set.load, .load_multiple_object_types, and .load_objects_or_interfaces. PaginationHelper emits one corresponding object per fetched page in stderr esponse_metadata; stdout remains the ordered item list. Three Ontology skill records now name this key and the model's page fields, including interface mappings.

## Verification
- Ontology CLI tests: 54 passed. Single-page cases cover all three operations; a two-page case checks item order, mapping order, count, and cursor completion.
- Offline skill gate and documented examples: 10 passed. Ruff and git diff --check: passed.
- Independent Ontology QA reported two-page probes for all three operations with items, fields, counts, and cursors preserved.

## Security review
No access guard, credentials, shell execution, network-on-import, or logging changes. Metadata comes from SDK response fields and stays on stderr with the existing separator. Caller-controlled page input is not evaluated as code. This change only adds page fields to the success metadata envelope.
