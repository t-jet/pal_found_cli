#!/usr/bin/env python3
"""
Tracking System CLI Utility

A command-line interface for managing the file-based tracking system.
Provides safe, validated operations for ticket and link management.

Usage:
    tracker_cli.py create <type> [title] --author AUTHOR [options]
    tracker_cli.py create <type> --title TITLE --author AUTHOR [options]
    tracker_cli.py get <ticket-id> [--author AUTHOR]
    tracker_cli.py list [--author AUTHOR] [--status STATUS] [--assignee ASSIGNEE] [--type TYPE] [--priority PRIORITY]
    tracker_cli.py update <ticket-id> --author AUTHOR [--status STATUS] [--assignee ASSIGNEE] [--priority PRIORITY]
    tracker_cli.py link create <source-id> <target-id> <link-type> --author AUTHOR [--comment COMMENT]
    tracker_cli.py link list <ticket-id> [--author AUTHOR] [--direction in|out|all]
    tracker_cli.py link remove <link-id> --author AUTHOR
    tracker_cli.py search <query> [--author AUTHOR] [--in-title] [--in-content]

Note: --author is required for write commands (create, update, link create, link remove,
      comment create, comment update) and optional for read-only commands.
"""

from __future__ import annotations

from .argument_parser import build_argument_parser
from .config import get_runtime_config
from .constants import (
    EXIT_CONFIG_ERROR,
    EXIT_FILE_ERROR,
    EXIT_OK,
    EXIT_UNEXPECTED_ERROR,
    EXIT_VALIDATION_ERROR,
)
from .exceptions import (
    ConfigurationError,
    FileOperationError,
    TrackerError,
    ValidationError,
)
from .formatters import to_toon
from .handlers import (
    handle_build_queue,
    handle_comment,
    handle_create,
    handle_get,
    handle_link,
    handle_list,
    handle_search,
    handle_type_info,
    handle_update,
    handle_workflow,
)
from .help_builder import build_help_data


# ── CLI entry point ──────────────────────────────────────────────────────────


def main() -> int:
    """Main CLI entry point. Returns an integer exit code."""
    parser, subparser_refs = build_argument_parser()
    args = parser.parse_args()

    if args.help_toon:
        print(to_toon(build_help_data()), end="")
        return EXIT_OK

    if not args.command:
        parser.print_help()
        return EXIT_OK

    try:
        cfg = get_runtime_config()

        # Extract subparser references for handlers that need them
        create_p = subparser_refs.get("create")
        update_p = subparser_refs.get("update")
        link_p = subparser_refs.get("link")
        comment_p = subparser_refs.get("comment")
        wf_p = subparser_refs.get("workflow")
        bq_p = subparser_refs.get("build-queue")

        # Dispatch to appropriate handler
        if args.command == "create":
            assert create_p is not None
            handle_create(args, create_p)
            return EXIT_OK
        elif args.command == "get":
            handle_get(args)
            return EXIT_OK
        elif args.command == "list":
            handle_list(args)
            return EXIT_OK
        elif args.command == "update":
            assert update_p is not None
            handle_update(args, update_p)
            return EXIT_OK
        elif args.command == "search":
            handle_search(args)
            return EXIT_OK
        elif args.command == "link":
            assert link_p is not None
            return handle_link(args, link_p)
        elif args.command == "comment":
            assert comment_p is not None
            return handle_comment(args, comment_p)
        elif args.command == "type-info":
            handle_type_info(args)
            return EXIT_OK
        elif args.command == "workflow":
            assert wf_p is not None
            handle_workflow(args, cfg, wf_p)
            return EXIT_OK
        elif args.command == "build-queue":
            assert bq_p is not None
            handle_build_queue(args, bq_p)
            return EXIT_OK
        else:
            parser.print_help()
            return EXIT_OK

    except ValidationError as e:
        print(f"ValidationError [{EXIT_VALIDATION_ERROR}]: {e}")
        return EXIT_VALIDATION_ERROR
    except ConfigurationError as e:
        print(f"ConfigurationError [{EXIT_CONFIG_ERROR}]: {e}")
        return EXIT_CONFIG_ERROR
    except FileOperationError as e:
        print(f"FileOperationError [{EXIT_FILE_ERROR}]: {e}")
        return EXIT_FILE_ERROR
    except TrackerError as e:
        print(f"TrackerError [{EXIT_UNEXPECTED_ERROR}]: {e}")
        return EXIT_UNEXPECTED_ERROR
    except Exception as e:
        print(f"UnexpectedError [{EXIT_UNEXPECTED_ERROR}]: {e}")
        return EXIT_UNEXPECTED_ERROR
