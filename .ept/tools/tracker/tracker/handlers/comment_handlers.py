"""Comment-related command handlers for the tracking CLI.

This module contains handlers for comment operations: create, list, get, and update.
"""

from __future__ import annotations

import argparse
from typing import Any

from ..comments import create_comment, get_comment, list_comments, update_comment
from ..constants import EXIT_VALIDATION_ERROR
from ..exceptions import ValidationError
from ..utils import decode_escape_sequences


def handle_comment(args: argparse.Namespace, comment_parser: argparse.ArgumentParser) -> int:
    """Handle the 'comment' command and its subcommands.
    
    Args:
        args: Parsed command-line arguments
        comment_parser: The argument parser for the comment command (for help)
    
    Returns:
        Exit code (0 for success, EXIT_VALIDATION_ERROR if subcommand missing)
    
    Raises:
        ValidationError: If validation fails for comment operations
    """
    if not args.comment_command:
        comment_parser.print_help()
        return EXIT_VALIDATION_ERROR
        
    if args.comment_command == "create":
        cid = create_comment(
            args.ticket_id, args.author, args.subject,
            decode_escape_sequences(args.text),
        )
        print(f"Created comment: {cid}")
    elif args.comment_command == "list":
        comments = list_comments(args.ticket_id)
        print(f"\nFound {len(comments)} comment(s) for {args.ticket_id}:")
        print("=" * 120)
        print(
            f"{'Comment ID':<30} {'Author':<20} "
            f"{'Created':<20} {'Updated':<20} {'Subject'}"
        )
        print("-" * 120)
        for c in comments:
            print(
                f"{c['comment_id']:<30} {c['author']:<20} "
                f"{c['created']:<20} {c['updated']:<20} {c['subject']}"
            )
    elif args.comment_command == "get":
        comment = get_comment(args.ticket_id, args.comment_id)
        print("\nComment Details:")
        print("=" * 80)
        print(f"comment_id      : {comment['comment_id']}")
        print(f"author          : {comment['author']}")
        print(f"subject         : {comment['subject']}")
        print(f"created         : {comment['created']}")
        print(f"updated         : {comment['updated']}")
        print("text:")
        print(comment["text"])
    elif args.comment_command == "update":
        if args.subject is None and args.text is None:
            raise ValidationError(
                "Nothing to update. Fix: pass --subject and/or --text"
            )
        decoded_text = (
            decode_escape_sequences(args.text)
            if args.text is not None
            else None
        )
        updated = update_comment(
            args.ticket_id, args.comment_id, args.author,
            args.subject, decoded_text,
        )
        print(f"Updated comment: {updated['comment_id']}")
    
    return 0
