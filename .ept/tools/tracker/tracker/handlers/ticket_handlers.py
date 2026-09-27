"""Ticket-related command handlers for the tracking CLI.

This module contains handlers for ticket operations: create, get, list, update, and search.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from ..config import get_runtime_config
from ..formatters import format_ticket
from ..index import get_ticket, ticket_exists
from ..links import is_ticket_blocked
from ..tickets import (
    build_status_context,
    create_ticket,
    get_ticket_with_content,
    list_tickets,
    search_tickets,
    update_ticket,
)
from ..utils import decode_escape_sequences, parse_extra_fields
from ..validators import validate_status_value, validate_ticket_type
from ..exceptions import ValidationError


def handle_create(args: argparse.Namespace, create_parser: argparse.ArgumentParser) -> None:
    """Handle the 'create' command to create a new ticket.
    
    Args:
        args: Parsed command-line arguments
        create_parser: The argument parser for the create command (for error messages)
    
    Raises:
        ValidationError: If validation fails for ticket type or required fields
    """
    validate_ticket_type(args.type)
    title = args.title_positional or args.title_opt
    if not title or not title.strip():
        create_parser.error(
            "title is required: provide it as a positional argument "
            'or via --title "Your title here"'
        )
    description = decode_escape_sequences(args.description)
    if args.description_file:
        desc_path = Path(args.description_file)
        if not desc_path.exists():
            create_parser.error(
                f"--description-file not found: {args.description_file}"
            )
        try:
            description = desc_path.read_text(encoding="utf-8")
        except Exception as exc:
            create_parser.error(
                f"Failed to read --description-file "
                f"'{args.description_file}': {exc}"
            )
    extras = parse_extra_fields(args.field)
    ticket_id = create_ticket(
        args.type, title, args.author,
        args.priority, args.assignee, args.parent,
        args.addressed_to, description, extras,
    )
    ticket = get_ticket(ticket_id)
    ctx = build_status_context(ticket_id, args.type, ticket["status"])
    print(yaml.dump(
        ctx, default_flow_style=False, allow_unicode=True,
        sort_keys=False,
    ))


def handle_get(args: argparse.Namespace) -> None:
    """Handle the 'get' command to retrieve ticket details.
    
    Args:
        args: Parsed command-line arguments containing ticket_id
    
    Raises:
        ValidationError: If ticket_id is invalid or not found
    """
    ticket = get_ticket_with_content(args.ticket_id)
    ctx = build_status_context(
        ticket["id"], ticket["type"], ticket["status"],
    )
    print(yaml.dump(
        ctx, default_flow_style=False, allow_unicode=True,
        sort_keys=False,
    ))
    print("Ticket Details:")
    print("=" * 80)
    for key, value in ticket.items():
        if key == "content":
            continue
        print(f"{key:15s}: {value}")
    print("content:")
    print(ticket["content"])


def handle_list(args: argparse.Namespace) -> None:
    """Handle the 'list' command to list tickets with filters.
    
    Args:
        args: Parsed command-line arguments with optional filters
    
    Raises:
        ValidationError: If any filter values are invalid
    """
    cfg = get_runtime_config()
    
    # Validate filters (handle lists for OR logic)
    if args.type:
        for t in args.type:
            validate_ticket_type(t)
    if args.status:
        # Validate each status value against all possible statuses
        for s in args.status:
            # If type filter is provided, validate against those types
            # Otherwise validate against all statuses
            if args.type and len(args.type) == 1:
                validate_status_value(s, args.type[0])
            else:
                validate_status_value(s, None)
    if args.priority and cfg["priority_values"]:
        for p in args.priority:
            if p not in cfg["priority_values"]:
                raise ValidationError(
                    f"Invalid priority filter: {p}. "
                    f"Valid values: {', '.join(cfg['priority_values'])}."
                )
    if args.parent:
        if not ticket_exists(args.parent):
            raise ValidationError(
                f"Parent ticket {args.parent} does not exist"
            )
    
    tickets = list_tickets(
        args.status, args.assignee, args.type, args.priority,
        parent=args.parent,
        reporter=args.reporter,
        non_terminal_only=getattr(args, 'non_terminal_only', False),
    )
    print(f"\nFound {len(tickets)} ticket(s):")
    print("=" * 140)
    print(
        f"{'ID':<15} {'Status':<15} {'Priority':<10} "
        f"{'Assignee':<20} {'Reporter':<15} {'Blocked':<8} {'Title'}"
    )
    print("-" * 140)
    for t in tickets:
        # Add blocked status to ticket dict for formatting
        blocked = is_ticket_blocked(t["id"])
        t["blocked"] = "Yes" if blocked else "No"
        print(format_ticket(t, include_reporter=True, include_blocked=True))


def handle_update(args: argparse.Namespace, update_parser: argparse.ArgumentParser) -> None:
    """Handle the 'update' command to update ticket fields.
    
    Args:
        args: Parsed command-line arguments
        update_parser: The argument parser for error messages
    
    Raises:
        ValidationError: If update validation fails
    """
    new_description: str | None = None
    if args.description:
        new_description = decode_escape_sequences(args.description)
    if args.description_file:
        desc_path = Path(args.description_file)
        if not desc_path.exists():
            update_parser.error(
                f"--description-file not found: {args.description_file}"
            )
        try:
            new_description = desc_path.read_text(encoding="utf-8")
        except Exception as exc:
            update_parser.error(
                f"Failed to read --description-file "
                f"'{args.description_file}': {exc}"
            )
    update_extras: dict[str, str] | None = (
        parse_extra_fields(args.field) if args.field else None
    )
    ticket = update_ticket(
        args.ticket_id, args.author,
        args.status, args.assignee, args.priority,
        extra_fields=update_extras,
        description=new_description,
    )
    if args.status:
        ctx = build_status_context(
            ticket["id"], ticket["type"], ticket["status"],
        )
        print(yaml.dump(
            ctx, default_flow_style=False, allow_unicode=True,
            sort_keys=False,
        ))
    else:
        print(f"Updated ticket: {ticket['id']}")
        print(format_ticket(ticket))


def handle_search(args: argparse.Namespace) -> None:
    """Handle the 'search' command to search tickets by query string.
    
    Args:
        args: Parsed command-line arguments with query and search options
    """
    tickets = search_tickets(
        args.query, args.in_title, args.in_content,
    )
    print(f"\nFound {len(tickets)} ticket(s) matching '{args.query}':")
    print("=" * 100)
    print(
        f"{'ID':<15} {'Status':<15} {'Priority':<10} "
        f"{'Assignee':<20} {'Title'}"
    )
    print("-" * 100)
    for t in tickets:
        print(format_ticket(t))
