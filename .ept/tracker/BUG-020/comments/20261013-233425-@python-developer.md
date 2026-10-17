Subject: Paging flag omission root cause
Created: 2026-10-13T23:34:25
Updated: 2026-10-13T23:34:25
---
# Root cause
Four Models records listed operation-specific paging inputs but omitted common parser flags --all and --max-pages. Models _common_parser(paginated=True) adds both to exactly the four PAGINATED_OPS. _resolve_pagination_flags fetches one page by default, uses --max-pages as requested batch count, and makes --all take precedence by requesting the hard page cap; PaginationHelper also enforces configured maximum.
# Correction
Add both flags and their effects to each of four records. Retest the gate and scoped diff.
