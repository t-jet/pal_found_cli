"""Ticket CRUD operations, frontmatter parsing, and status-context building."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from .comments import create_comment
from .config import get_paths, get_runtime_config
from .constants import TICKET_CONTENT_FILE, TICKET_TEMPLATE
from .exceptions import FileOperationError, ValidationError
from .index import (
    get_next_ticket_id,
    get_ticket,
    increment_counter,
    read_index,
    ticket_exists,
    write_index,
)
from .utils import build_frontmatter_text, now_date
from .validators import validate_ticket_type


# ── Path helpers ─────────────────────────────────────────────────────────────


def ticket_path_by_id(ticket_id: str) -> Path:
    """Resolve the directory path for *ticket_id*."""
    ticket = get_ticket(ticket_id)
    raw = Path(ticket["path"])
    return raw if raw.is_absolute() else get_paths().tracker_root / raw


def ticket_file_path(ticket: dict[str, Any]) -> Path:
    """Resolve the ticket content file (``ticket.md``) path."""
    cfg = get_runtime_config()
    content_file = cfg["ticket_specs"][ticket["type"]]["content_file"]
    raw = Path(ticket["path"])
    base = raw if raw.is_absolute() else get_paths().tracker_root / raw
    return base / content_file


# ── File parsing / writing ───────────────────────────────────────────────────


def parse_ticket_file(
    ticket: dict[str, Any],
) -> tuple[dict[str, Any], str]:
    """Parse a ticket file into ``(metadata_dict, body_text)``."""
    tf = ticket_file_path(ticket)
    try:
        with open(tf, "r", encoding="utf-8-sig", newline="") as f:
            raw = f.read().replace("\r\n", "\n").replace("\r", "\n")
    except Exception as e:
        raise FileOperationError(f"Failed to read ticket file {tf}: {e}")

    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", raw, re.DOTALL)
    if not match:
        raise ValidationError(
            f"Ticket format invalid for {ticket['id']}. "
            "Fix: recreate ticket file with CLI create command format"
        )

    try:
        metadata = yaml.safe_load(match.group(1)) or {}
    except Exception as e:
        raise ValidationError(
            f"Ticket frontmatter parse error for {ticket['id']}: {e}"
        )
    return metadata, match.group(2).strip()


def write_ticket_file(
    ticket: dict[str, Any],
    metadata: dict[str, Any],
    body: str,
) -> None:
    """Write ticket metadata and body back to disk."""
    tf = ticket_file_path(ticket)
    cfg = get_runtime_config()
    spec = cfg["ticket_specs"][ticket["type"]]
    ordered = [f for f in spec["required_fields"] if f != "parent"] + [
        k
        for k in spec["optional_fields"]
        if k in metadata and str(metadata.get(k, "")).strip()
    ]
    frontmatter_text = build_frontmatter_text(metadata, ordered)
    content = f"---\n{frontmatter_text}\n---\n\n{body.strip()}\n"
    try:
        with open(tf, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        raise FileOperationError(f"Failed to write ticket file {tf}: {e}")


# ── CRUD operations ──────────────────────────────────────────────────────────


def create_ticket(
    ticket_type: str,
    title: str,
    author: str,
    priority: str = "Medium",
    assignee: str = "",
    parent: str = "",
    addressed_to: str = "",
    description: str = "",
    extra_fields: dict[str, str] | None = None,
) -> str:
    """Create a new ticket and return its ID."""
    cfg = get_runtime_config()
    paths = get_paths()
    validate_ticket_type(ticket_type)

    if cfg["priority_values"] and priority not in cfg["priority_values"]:
        raise ValidationError(
            f"Invalid priority: {priority}. "
            f"Valid values: {', '.join(cfg['priority_values'])}. "
            "Fix: pass one of configured priority values"
        )

    spec = cfg["ticket_specs"][ticket_type]
    required_fields: list[str] = spec["required_fields"]
    optional_fields: list[str] = spec["optional_fields"]
    allowed_fields = set(required_fields) | set(optional_fields)

    extras = extra_fields or {}
    unknown = [k for k in extras if k not in cfg["valid_field_names"]]
    if unknown:
        raise ValidationError(
            f"Unknown field(s): {', '.join(sorted(unknown))}. "
            f"Valid fields: {', '.join(sorted(cfg['valid_field_names']))}. "
            "Fix: use configured field names"
        )
    disallowed = [k for k in extras if k not in allowed_fields]
    if disallowed:
        raise ValidationError(
            f"Field(s) not allowed for type '{ticket_type}': "
            f"{', '.join(sorted(disallowed))}. "
            f"Allowed fields for this type: {', '.join(sorted(allowed_fields))}."
        )

    ticket_id, _ = get_next_ticket_id(ticket_type)

    if parent:
        if not ticket_exists(parent):
            raise ValidationError(f"Parent ticket {parent} does not exist")
        ticket_path = paths.tracker_root / parent / ticket_id
    else:
        ticket_path = paths.tracker_root / ticket_id

    ticket_path.mkdir(parents=True, exist_ok=True)
    ticket_file = ticket_path / spec["content_file"]
    date_now = now_date()
    status = spec["initial_status"]

    frontmatter_values: dict[str, Any] = {
        "id": ticket_id,
        "type": ticket_type,
        "title": title,
        "status": status,
        "priority": priority,
        "assignee": assignee,
        "reporter": author,
        "addressed_to": addressed_to,
        "created": date_now,
        "updated": date_now,
    }
    # NOTE: 'parent' is intentionally NOT written to frontmatter.
    # Folder structure is the authoritative source of parentage.
    frontmatter_values.update(extras)

    missing_required = [
        f
        for f in required_fields
        if f != "parent" and not str(frontmatter_values.get(f, "")).strip()
    ]
    if missing_required:
        raise ValidationError(
            f"Missing required field(s) for type '{ticket_type}': "
            f"{', '.join(missing_required)}. "
            "Fix: pass values via command options or --field key=value"
        )

    # Exclude 'parent' from frontmatter output
    ordered_fields = [f for f in required_fields if f != "parent"] + [
        f
        for f in optional_fields
        if f in frontmatter_values
        and str(frontmatter_values.get(f, "")).strip()
    ]
    frontmatter_text = build_frontmatter_text(frontmatter_values, ordered_fields)
    ticket_content = TICKET_TEMPLATE.format(
        frontmatter=frontmatter_text,
        ticket_id=ticket_id,
        title=title,
        description=description or "TODO: Add description",
    )

    try:
        with open(ticket_file, "w", encoding="utf-8") as f:
            f.write(ticket_content)
    except Exception as e:
        raise FileOperationError(
            f"Failed to write ticket file {ticket_file}: {e}"
        )

    (ticket_path / "comments").mkdir(exist_ok=True)

    # Store path relative to tracker root for portability
    tickets = read_index()
    try:
        rel_path = ticket_path.relative_to(paths.tracker_root)
    except ValueError:
        rel_path = ticket_path

    tickets.append({
        "id": ticket_id,
        "type": ticket_type,
        "title": title,
        "status": status,
        "priority": priority,
        "assignee": assignee,
        "reporter": author,
        "parent": parent,
        "addressed_to": addressed_to,
        "path": str(rel_path).replace("\\", "/"),
        "created": date_now,
        "updated": date_now,
    })
    write_index(tickets)
    increment_counter(ticket_type)

    create_comment(
        ticket_id, author, "Ticket created",
        f"Created ticket of type '{ticket_type}'",
    )
    return ticket_id


def get_ticket_with_content(ticket_id: str) -> dict[str, Any]:
    """Return ticket metadata merged with the parsed body content."""
    ticket = get_ticket(ticket_id)
    metadata, body = parse_ticket_file(ticket)
    result = {**ticket, **metadata}
    result["content"] = body
    return result


def list_tickets(
    status: str | None = None,
    assignee: str | None = None,
    ticket_type: str | None = None,
    priority: str | None = None,
) -> list[dict[str, str]]:
    """List tickets with optional single-pass filtering."""
    tickets = read_index()
    results: list[dict[str, str]] = []
    for ticket in tickets:
        if status and ticket["status"] != status:
            continue
        if assignee and ticket["assignee"] != assignee:
            continue
        if ticket_type and ticket["type"] != ticket_type:
            continue
        if priority and ticket["priority"] != priority:
            continue
        results.append(ticket)
    return results


def update_ticket(
    ticket_id: str,
    author: str,
    status: str | None = None,
    assignee: str | None = None,
    priority: str | None = None,
) -> dict[str, str]:
    """Update ticket metadata and synchronise index + file."""
    from .validators import validate_status_transition, validate_status_value

    cfg = get_runtime_config()
    tickets = read_index()
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if not ticket:
        raise ValidationError(f"Ticket {ticket_id} not found")

    updated = False
    if status and status != ticket["status"]:
        validate_status_value(status, ticket["type"])
        validate_status_transition(ticket["type"], ticket["status"], status)
        ticket["status"] = status
        updated = True
    if assignee is not None and assignee != ticket["assignee"]:
        ticket["assignee"] = assignee
        updated = True
    if priority and priority != ticket["priority"]:
        if cfg["priority_values"] and priority not in cfg["priority_values"]:
            raise ValidationError(
                f"Invalid priority: {priority}. "
                f"Valid values: {', '.join(cfg['priority_values'])}."
            )
        ticket["priority"] = priority
        updated = True

    if updated:
        ticket["updated"] = now_date()
        write_index(tickets)

        metadata, body = parse_ticket_file(ticket)
        if status:
            metadata["status"] = ticket["status"]
        if assignee is not None:
            metadata["assignee"] = ticket["assignee"]
        if priority:
            metadata["priority"] = ticket["priority"]
        metadata["updated"] = ticket["updated"]
        write_ticket_file(ticket, metadata, body)

        create_comment(
            ticket_id, author, "Ticket updated",
            f"Updated fields: status={status}, assignee={assignee}, "
            f"priority={priority}",
        )
    return ticket


def search_tickets(
    query: str,
    in_title: bool = True,
    in_content: bool = False,
) -> list[dict[str, str]]:
    """Search tickets by title and/or content."""
    paths = get_paths()
    tickets = read_index()
    results: list[dict[str, str]] = []
    query_lower = query.lower()

    for ticket in tickets:
        if in_title and query_lower in ticket["title"].lower():
            results.append(ticket)
            continue
        if in_content:
            raw = Path(ticket["path"])
            ticket_path = raw if raw.is_absolute() else paths.tracker_root / raw
            tf = ticket_path / TICKET_CONTENT_FILE
            if tf.exists():
                try:
                    with open(tf, "r", encoding="utf-8-sig") as f:
                        if query_lower in f.read().lower():
                            results.append(ticket)
                except Exception:
                    pass
    return results


# ── Status context ───────────────────────────────────────────────────────────


def build_status_context(
    ticket_id: str,
    ticket_type: str,
    current_status: str,
) -> dict[str, Any]:
    """Build the status-context dict for YAML output after create/update."""
    cfg = get_runtime_config()
    spec = cfg["ticket_specs"].get(ticket_type, {})
    allowed_transitions = spec.get("allowed_transitions", {}).get(
        current_status, [],
    )
    status_detail: dict[str, Any] = spec.get("status_details", {}).get(
        current_status, {},
    )
    ticket_instructions: dict[str, Any] = spec.get("ticket_instructions", {})
    status_data = ticket_instructions.get(current_status, {})

    if isinstance(status_data, dict):
        instructions: list[Any] = status_data.get("instructions", []) or []
        definitions_of_done: list[Any] = (
            status_data.get("transition_dods", []) or []
        )
    else:
        instructions = []
        definitions_of_done = []

    return {
        "ticket_id": ticket_id,
        "current_status": current_status,
        "status_description": status_detail.get("description", ""),
        "status_goal": status_detail.get("stage_goal", ""),
        "status_responsible_roles": status_detail.get(
            "responsible_roles", [],
        ),
        "allowed_transitions": allowed_transitions,
        "instructions": instructions,
        "definitions_of_done": definitions_of_done,
    }
