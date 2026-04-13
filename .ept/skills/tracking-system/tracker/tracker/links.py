"""Inter-ticket link CRUD operations."""

from __future__ import annotations

from datetime import datetime

from .config import get_runtime_config
from .exceptions import ValidationError
from .index import (
    get_next_link_id,
    increment_link_counter,
    read_link_index,
    ticket_exists,
    write_link_index,
)
from .validators import validate_link_direction, validate_link_type


def get_link_roles(link_type: str) -> tuple[str, str]:
    """Return ``(source_role, target_role)`` for *link_type*."""
    return get_runtime_config()["link_roles"].get(
        link_type, (link_type, link_type),
    )


def create_link(
    source_id: str,
    target_id: str,
    link_type: str,
    created_by: str,
    comment: str = "",
) -> str:
    """Create a link between two tickets and return the link ID."""
    if not ticket_exists(source_id):
        raise ValidationError(f"Source ticket {source_id} does not exist")
    if not ticket_exists(target_id):
        raise ValidationError(f"Target ticket {target_id} does not exist")
    validate_link_type(link_type)

    links = read_link_index()
    duplicate = next(
        (
            lk
            for lk in links
            if lk["source_ticket"] == source_id
            and lk["target_ticket"] == target_id
            and lk["link_type"] == link_type
        ),
        None,
    )
    if duplicate:
        raise ValidationError(f"Link already exists: {duplicate['link_id']}")

    link_id = get_next_link_id()
    source_role, target_role = get_link_roles(link_type)

    links.append({
        "link_id": link_id,
        "source_ticket": source_id,
        "target_ticket": target_id,
        "link_type": link_type,
        "source_role": source_role,
        "target_role": target_role,
        "created": datetime.now().isoformat(),
        "created_by": created_by,
        "comment": comment,
    })
    write_link_index(links)
    increment_link_counter()
    return link_id


def list_links(
    ticket_id: str,
    direction: str = "all",
) -> list[dict[str, str]]:
    """List links for *ticket_id*, filtered by *direction*."""
    if not ticket_exists(ticket_id):
        raise ValidationError(f"Ticket {ticket_id} does not exist")
    validate_link_direction(direction)

    links = read_link_index()
    if direction == "out":
        return [lk for lk in links if lk["source_ticket"] == ticket_id]
    if direction == "in":
        return [lk for lk in links if lk["target_ticket"] == ticket_id]
    return [
        lk
        for lk in links
        if lk["source_ticket"] == ticket_id
        or lk["target_ticket"] == ticket_id
    ]


def remove_link(link_id: str) -> bool:
    """Remove a link by ID.  Returns ``True`` on success."""
    links = read_link_index()
    if not any(lk["link_id"] == link_id for lk in links):
        raise ValidationError(f"Link {link_id} not found")
    write_link_index([lk for lk in links if lk["link_id"] != link_id])
    return True
