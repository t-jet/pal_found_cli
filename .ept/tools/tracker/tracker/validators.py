"""Validation functions for tickets, links, statuses, and directions."""

from __future__ import annotations

from .config import get_runtime_config
from .exceptions import ValidationError


def validate_ticket_type(ticket_type: str) -> None:
    """Raise :class:`ValidationError` if *ticket_type* is not registered."""
    valid_types = get_runtime_config()["ticket_types"]
    if ticket_type not in valid_types:
        raise ValidationError(
            f"Invalid ticket type: {ticket_type}. "
            f"Valid types: {', '.join(valid_types)}. "
            "Fix: pass one of the supported ticket type keys"
        )


def validate_link_type(link_type: str) -> None:
    """Raise :class:`ValidationError` if *link_type* is not configured."""
    valid = get_runtime_config()["link_types"]
    if link_type not in valid:
        raise ValidationError(
            f"Invalid link type: {link_type}. "
            f"Valid types: {', '.join(valid)}. "
            "Fix: choose one of the configured link types"
        )


def validate_status_value(
    status: str,
    ticket_type: str | None = None,
) -> None:
    """Validate a status value, optionally scoped to a ticket type."""
    cfg = get_runtime_config()
    if ticket_type:
        statuses = cfg["ticket_specs"][ticket_type]["statuses"]
        if status not in statuses:
            raise ValidationError(
                f"Invalid status: {status} for type '{ticket_type}'. "
                f"Valid statuses: {', '.join(statuses)}. Fix: use one of listed values"
            )
        return

    all_statuses = sorted(
        {s for spec in cfg["ticket_specs"].values() for s in spec["statuses"]}
    )
    if status not in all_statuses:
        raise ValidationError(
            f"Invalid status: {status}. "
            f"Valid statuses: {', '.join(all_statuses)}. Fix: use one of listed values"
        )


def validate_status_transition(
    ticket_type: str,
    from_status: str,
    to_status: str,
) -> None:
    """Validate that *from_status* → *to_status* is a permitted transition.

    If no transition rules are configured the check is skipped (any
    transition is allowed).
    """
    cfg = get_runtime_config()
    spec = cfg["ticket_specs"].get(ticket_type, {})
    transitions: dict[str, list[str]] = spec.get("allowed_transitions", {})
    if not transitions:
        return

    allowed: list[str] = transitions.get(from_status, [])
    if to_status not in allowed:
        terminal = spec.get("terminal_statuses", [])
        if from_status in terminal:
            hint = (
                f"'{from_status}' is a terminal status and cannot be "
                "transitioned."
            )
        else:
            targets = ", ".join(allowed) if allowed else "none"
            hint = f"Allowed transitions from '{from_status}': {targets}."
        raise ValidationError(
            f"Invalid status transition for '{ticket_type}': "
            f"'{from_status}' -> '{to_status}'. "
            f"{hint} Fix: choose one of the allowed target statuses"
        )


def validate_link_direction(direction: str) -> None:
    """Raise :class:`ValidationError` if *direction* is not valid."""
    valid = ["in", "out", "all"]
    if direction not in valid:
        raise ValidationError(
            f"Invalid link direction: {direction}. "
            f"Valid values: {', '.join(valid)}. Fix: pass --direction in|out|all"
        )
