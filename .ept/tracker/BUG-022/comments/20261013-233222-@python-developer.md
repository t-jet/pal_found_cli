Subject: Root cause and correction scope
Created: 2026-10-13T23:32:22
Updated: 2026-10-13T23:32:22
---
# Root cause
The Orchestration records copied SDK response-model names and SDK parameter prose without accounting for CLI pagination and request semantics. uild.jobs, uild.search, and schedule.runs run through _paginate_operation: the formatter writes collected items to stdout; PaginationHelper.emit_metadata() writes cursor and page count to stderr. uild.create copied the SDK's schedule-target wording for a one-time build. schedule.create and schedule.replace copied SDK trigger visibility prose into request-input guidance. Read-only schedule records also inherited a mutation permission precondition.
# Correction
Update the six failed operation records and read-only prerequisites in the two owned reference files. Validate against local parser, SDK model/signatures, offline gate, and Orchestration tests.
