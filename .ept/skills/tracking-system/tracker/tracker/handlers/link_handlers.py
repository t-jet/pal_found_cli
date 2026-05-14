"""Link-related command handlers for the tracking CLI.

This module contains handlers for link operations: create, list, and remove.
"""

from __future__ import annotations

import argparse
from typing import Any

from ..constants import EXIT_VALIDATION_ERROR
from ..formatters import format_link
from ..links import create_link, list_links, remove_link
from ..validators import validate_link_type


def handle_link(args: argparse.Namespace, link_parser: argparse.ArgumentParser) -> int:
    """Handle the 'link' command and its subcommands.
    
    Args:
        args: Parsed command-line arguments
        link_parser: The argument parser for the link command (for help)
    
    Returns:
        Exit code (0 for success, EXIT_VALIDATION_ERROR if subcommand missing)
    
    Raises:
        ValidationError: If validation fails for link operations
    """
    if not args.link_command:
        link_parser.print_help()
        return EXIT_VALIDATION_ERROR
        
    if args.link_command == "create":
        validate_link_type(args.link_type)
        lid = create_link(
            args.source_id, args.target_id, args.link_type,
            args.author, args.comment,
        )
        print(f"Created link: {lid}")
    elif args.link_command == "list":
        links = list_links(args.ticket_id, args.direction)
        print(f"\nFound {len(links)} link(s) for {args.ticket_id}:")
        print("=" * 100)
        print(
            f"{'Link ID':<15} {'Source':<15}    "
            f"{'Target':<15} {'Type':<15} {'Role'}"
        )
        print("-" * 100)
        for lk in links:
            print(format_link(lk))
    elif args.link_command == "remove":
        remove_link(args.link_id)
        print(f"Removed link: {args.link_id}")
    
    return 0
