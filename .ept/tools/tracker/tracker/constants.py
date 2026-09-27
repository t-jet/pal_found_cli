"""Constants, exit codes, templates, and field-name lists."""

from __future__ import annotations

# ── Exit codes ───────────────────────────────────────────────────────────────

EXIT_OK: int = 0
EXIT_VALIDATION_ERROR: int = 2
EXIT_CONFIG_ERROR: int = 3
EXIT_FILE_ERROR: int = 4
EXIT_UNEXPECTED_ERROR: int = 5

# ── File names ───────────────────────────────────────────────────────────────

TICKET_CONTENT_FILE: str = "ticket.md"
METADATA_SEPARATOR: str = "---"

# ── Index CSV field names ────────────────────────────────────────────────────

INDEX_FIELDNAMES: list[str] = [
    "id",
    "type",
    "title",
    "status",
    "priority",
    "assignee",
    "reporter",
    "parent",
    "addressed_to",
    "path",
    "created",
    "updated",
]

LINK_INDEX_FIELDNAMES: list[str] = [
    "link_id",
    "source_ticket",
    "target_ticket",
    "link_type",
    "source_role",
    "target_role",
    "created",
    "created_by",
    "comment",
]

# ── Templates ────────────────────────────────────────────────────────────────

TICKET_TEMPLATE: str = """---
{frontmatter}
---

# {ticket_id}: {title}

## Description

{description}

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
"""

COMMENT_TEMPLATE: str = """Subject: {subject}
Created: {created}
Updated: {updated}
---
{text}
"""
