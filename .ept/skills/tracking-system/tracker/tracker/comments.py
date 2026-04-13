"""Comment CRUD operations."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from .config import get_paths
from .constants import COMMENT_TEMPLATE, METADATA_SEPARATOR
from .exceptions import FileOperationError, ValidationError
from .index import get_ticket
from .utils import now_timestamp, sanitize_author


# ── Path helpers ─────────────────────────────────────────────────────────────


def _comments_dir(ticket_id: str) -> Path:
    """Return (and create) the comments directory for *ticket_id*."""
    ticket = get_ticket(ticket_id)
    raw = Path(ticket["path"])
    base = raw if raw.is_absolute() else get_paths().tracker_root / raw
    path = base / "comments"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _comment_file_path(ticket_id: str, comment_id: str) -> Path:
    """Resolve and validate a comment file path."""
    comments_dir = _comments_dir(ticket_id)
    normalized = comment_id if comment_id.endswith(".md") else f"{comment_id}.md"
    file_path = comments_dir / normalized
    if not file_path.exists():
        raise ValidationError(
            f"Comment '{comment_id}' not found for ticket {ticket_id}. "
            "Fix: run 'comment list' and use an existing comment ID"
        )
    return file_path


def _parse_comment_metadata(file_path: Path) -> dict[str, str]:
    """Parse the fixed-header comment format into a dict."""
    try:
        with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
            raw = f.read().replace("\r\n", "\n").replace("\r", "\n")
            lines = raw.splitlines()
    except Exception as e:
        raise FileOperationError(f"Failed to read comment file {file_path}: {e}")

    if len(lines) < 4:
        raise ValidationError(
            f"Comment format invalid in {file_path.name}. "
            "Fix: use CLI comment commands to manage comments"
        )

    subject_line, created_line, updated_line, separator_line = lines[:4]

    if not subject_line.startswith("Subject: "):
        raise ValidationError(
            f"Comment '{file_path.name}' missing 'Subject:' metadata line"
        )
    if not created_line.startswith("Created: "):
        raise ValidationError(
            f"Comment '{file_path.name}' missing 'Created:' metadata line"
        )
    if not updated_line.startswith("Updated: "):
        raise ValidationError(
            f"Comment '{file_path.name}' missing 'Updated:' metadata line"
        )
    if separator_line.strip() != METADATA_SEPARATOR:
        raise ValidationError(
            f"Comment '{file_path.name}' missing metadata separator line '---'"
        )

    body = "\n".join(lines[4:]).strip()
    stem = file_path.stem
    match = re.match(r"^(\d{8}-\d{6})-(.+)$", stem)
    timestamp_id = match.group(1) if match else ""
    author = match.group(2) if match else ""

    return {
        "comment_id": stem,
        "author": author,
        "timestamp_id": timestamp_id,
        "subject": subject_line[len("Subject: "):].strip(),
        "created": created_line[len("Created: "):].strip(),
        "updated": updated_line[len("Updated: "):].strip(),
        "text": body,
    }


# ── CRUD ─────────────────────────────────────────────────────────────────────


def create_comment(
    ticket_id: str,
    author: str,
    subject: str,
    text: str,
) -> str:
    """Create a comment file and return the comment ID."""
    if not subject.strip():
        raise ValidationError(
            "Comment subject is required. Fix: pass --subject 'Short summary'"
        )

    comments_dir = _comments_dir(ticket_id)
    file_stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_author = sanitize_author(author)
    comment_id = f"{file_stamp}-{safe_author}"
    file_path = comments_dir / f"{comment_id}.md"
    now = now_timestamp()
 
    content = COMMENT_TEMPLATE.format(
        subject=subject.strip(), created=now, updated=now, text=text.lstrip('\ufeff').strip(),
    )
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        raise FileOperationError(f"Failed to create comment for {ticket_id}: {e}")

    return comment_id


def list_comments(ticket_id: str) -> list[dict[str, str]]:
    """List all comments for *ticket_id* with parsed metadata."""
    comments_dir = _comments_dir(ticket_id)
    return [
        _parse_comment_metadata(fp) for fp in sorted(comments_dir.glob("*.md"))
    ]


def get_comment(ticket_id: str, comment_id: str) -> dict[str, str]:
    """Retrieve a single comment with full metadata and text."""
    return _parse_comment_metadata(_comment_file_path(ticket_id, comment_id))


def update_comment(
    ticket_id: str,
    comment_id: str,
    author: str,
    subject: str | None,
    text: str | None,
) -> dict[str, str]:
    """Update an existing comment's subject and/or text."""
    file_path = _comment_file_path(ticket_id, comment_id)
    current = _parse_comment_metadata(file_path)

    new_subject = subject.strip() if subject is not None else current["subject"]
    if not new_subject:
        raise ValidationError("Comment subject cannot be empty")
    new_text = text if text is not None else current["text"]

    content = COMMENT_TEMPLATE.format(
        subject=new_subject,
        created=current["created"],
        updated=now_timestamp(),
        text=(new_text or "").lstrip('\ufeff').strip(),
    )
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        raise FileOperationError(f"Failed to update comment '{comment_id}': {e}")

    return _parse_comment_metadata(file_path)
