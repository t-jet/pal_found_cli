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

import argparse
import difflib
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from .comments import create_comment, get_comment, list_comments, update_comment
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
from .formatters import format_link, format_ticket, to_toon
from .index import get_ticket
from .links import create_link, list_links, remove_link
from .tickets import (
    build_status_context,
    create_ticket,
    get_ticket_with_content,
    list_tickets,
    search_tickets,
    update_ticket,
)
from .utils import decode_escape_sequences, parse_extra_fields
from .validators import (
    validate_link_type,
    validate_status_value,
    validate_ticket_type,
)


# ── Custom argument parser ───────────────────────────────────────────────────


class _CleanErrorParser(argparse.ArgumentParser):
    """``ArgumentParser`` that emits a concise error line (no usage block).

    Standard argparse prints the full usage string before the error message,
    which looks like a stack-trace dump in PowerShell / CI logs.  This
    subclass suppresses the usage header so every argument error surfaces as
    a single, actionable line.
    """

    def error(self, message: str) -> None:  # type: ignore[override]
        m = re.search(
            r"invalid choice: '([^']+)' \(choose from ([^)]+)\)", message,
        )
        if m:
            bad = m.group(1)
            choices = [c.strip().strip("'") for c in m.group(2).split(",")]
            close = difflib.get_close_matches(bad, choices, n=1, cutoff=0.6)
            if close:
                print(f"Error: unknown command '{bad}'. Did you mean '{close[0]}'?")
            else:
                print(f"Error: unknown command '{bad}'.")
                print(f"Tip: run '{self.prog} --help' for available commands.")
            sys.exit(2)
        print(f"Error: {message}")
        print(f"Tip: run '{self.prog} --help' for usage and examples.")
        sys.exit(2)


# ── Help-data builder ────────────────────────────────────────────────────────


def _build_help_data() -> dict[str, Any]:
    """Build a complete reference of every command, subcommand, and option.

    List-restricted options (ticket type, status, link type, priority) are
    populated from the runtime configuration when available.
    """
    try:
        cfg = get_runtime_config()
        ticket_types: list[str] = cfg["ticket_types"]
        link_types: list[str] = cfg["link_types"]
        priority_values: list[str] = cfg["priority_values"]
        all_statuses: list[str] = sorted(
            {s for spec in cfg["ticket_specs"].values() for s in spec["statuses"]}
        )
        per_type_statuses: dict[str, list[str]] = {
            t: list(spec["statuses"])
            for t, spec in cfg["ticket_specs"].items()
        }
    except Exception:
        ticket_types = []
        link_types = []
        priority_values = []
        all_statuses = []
        per_type_statuses = {}

    def _arg(
        help_text: str,
        values: list[str] | None = None,
        optional: bool = False,
    ) -> dict[str, Any]:
        entry: dict[str, Any] = {"help": help_text}
        if optional:
            entry["optional"] = True
        if values:
            entry["values"] = values
        return entry

    def _opt(
        help_text: str,
        required: bool = False,
        default: Any = None,
        values: list[str] | None = None,
        flag: bool = False,
        repeatable: bool = False,
    ) -> dict[str, Any]:
        entry: dict[str, Any] = {"help": help_text}
        if required:
            entry["required"] = True
        if default is not None:
            entry["default"] = default
        if values:
            entry["values"] = values
        if flag:
            entry["flag"] = True
        if repeatable:
            entry["repeatable"] = True
        return entry

    _author_req = _opt(
        "Author identifier (e.g. architect, ux-designer)", required=True,
    )
    _author_opt = _opt(
        "Author identifier (e.g. architect, ux-designer)", required=False,
    )

    return {
        "commands": {
            "create": {
                "help": "Create a new ticket",
                "author": "required",
                "arguments": {
                    "type": _arg("Ticket type key", values=ticket_types),
                    "title": _arg(
                        "Ticket title -- positional form; alternatively use --title",
                        optional=True,
                    ),
                },
                "options": {
                    "--title": _opt("Ticket title as a keyword argument"),
                    "--priority": _opt("Priority level", default="Medium", values=priority_values),
                    "--assignee": _opt("Assignee identifier"),
                    "--parent": _opt("Parent ticket ID (alias: --child-of)"),
                    "--child-of": _opt("Parent ticket ID (alias: --parent)"),
                    "--addressed-to": _opt("Addressed-to identifier"),
                    "--description": _opt("Description text (\\n, \\r\\n, \\t supported)"),
                    "--description-file": _opt(
                        "Path to a file whose contents are used as the description",
                    ),
                    "--field": _opt("Additional field as key=value (repeatable)", repeatable=True),
                    "--author": _author_req,
                },
            },
            "get": {
                "help": "Get full ticket details including content body",
                "author": "optional",
                "arguments": {"ticket_id": _arg("Ticket ID (e.g. TASK-001)")},
                "options": {"--author": _author_opt},
            },
            "list": {
                "help": "List tickets with optional filters",
                "author": "optional",
                "options": {
                    "--status": _opt("Filter by status", values=all_statuses),
                    "--assignee": _opt("Filter by assignee"),
                    "--type": _opt("Filter by ticket type", values=ticket_types),
                    "--priority": _opt("Filter by priority", values=priority_values),
                    "--author": _author_opt,
                },
            },
            "update": {
                "help": "Update ticket fields; status changes validated against transitions",
                "author": "required",
                "arguments": {"ticket_id": _arg("Ticket ID to update")},
                "options": {
                    "--status": _opt("New status value", values=all_statuses),
                    "--assignee": _opt("New assignee"),
                    "--priority": _opt("New priority", values=priority_values),
                    "--author": _author_req,
                },
            },
            "search": {
                "help": "Search tickets by query string",
                "author": "optional",
                "arguments": {"query": _arg("Search query text")},
                "options": {
                    "--in-title": _opt("Search in titles (default)", flag=True, default=True),
                    "--in-content": _opt("Search in content body", flag=True),
                    "--author": _author_opt,
                },
            },
            "link": {
                "help": "Manage inter-ticket links",
                "subcommands": {
                    "create": {
                        "help": "Create a link between two tickets",
                        "author": "required",
                        "arguments": {
                            "source_id": _arg("Source ticket ID"),
                            "target_id": _arg("Target ticket ID"),
                            "link_type": _arg("Link type", values=link_types),
                        },
                        "options": {
                            "--comment": _opt("Optional comment"),
                            "--author": _author_req,
                        },
                    },
                    "list": {
                        "help": "List links for a ticket",
                        "author": "optional",
                        "arguments": {"ticket_id": _arg("Ticket ID")},
                        "options": {
                            "--direction": _opt(
                                "Filter by direction", values=["in", "out", "all"], default="all",
                            ),
                            "--author": _author_opt,
                        },
                    },
                    "remove": {
                        "help": "Remove a link by its link ID",
                        "author": "required",
                        "arguments": {"link_id": _arg("Link ID (e.g. LINK-00001)")},
                        "options": {"--author": _author_req},
                    },
                },
            },
            "comment": {
                "help": "Manage ticket comments",
                "subcommands": {
                    "create": {
                        "help": "Create a comment on a ticket",
                        "author": "required",
                        "arguments": {"ticket_id": _arg("Ticket ID")},
                        "options": {
                            "--subject": _opt("Short comment subject line", required=True),
                            "--text": _opt("Comment body text (\\n supported)"),
                            "--author": _author_req,
                        },
                    },
                    "list": {
                        "help": "List all comments for a ticket",
                        "author": "optional",
                        "arguments": {"ticket_id": _arg("Ticket ID")},
                        "options": {"--author": _author_opt},
                    },
                    "get": {
                        "help": "Get a single comment with full metadata and body",
                        "author": "optional",
                        "arguments": {
                            "ticket_id": _arg("Ticket ID"),
                            "comment_id": _arg("Comment ID (timestamp-author)"),
                        },
                        "options": {"--author": _author_opt},
                    },
                    "update": {
                        "help": "Update subject and/or text of an existing comment",
                        "author": "required",
                        "arguments": {
                            "ticket_id": _arg("Ticket ID"),
                            "comment_id": _arg("Comment ID (timestamp-author)"),
                        },
                        "options": {
                            "--subject": _opt("Updated subject line"),
                            "--text": _opt("Updated body text (\\n supported)"),
                            "--author": _author_req,
                        },
                    },
                },
            },
            "workflow": {
                "help": "Inspect workflow definitions (all subcommands are read-only)",
                "author": "optional",
                "subcommands": {
                    "types": {
                        "help": "List all registered ticket types",
                        "author": "optional",
                        "options": {"--author": _author_opt},
                    },
                    "status": {
                        "help": "Show status details for a ticket type",
                        "author": "optional",
                        "arguments": {
                            "ticket_type": _arg(
                                "Ticket type key; omit to show all types",
                                values=ticket_types, optional=True,
                            ),
                            "status_name": _arg(
                                "Specific status name; omit to list all",
                                values=all_statuses, optional=True,
                            ),
                        },
                        "per_type_statuses": per_type_statuses or None,
                        "options": {"--author": _author_opt},
                    },
                    "transitions": {
                        "help": "Show allowed status transitions",
                        "author": "optional",
                        "arguments": {
                            "ticket_type": _arg("Ticket type key", values=ticket_types),
                            "status_name": _arg(
                                "Status name; omit for full table",
                                values=all_statuses, optional=True,
                            ),
                        },
                        "options": {"--author": _author_opt},
                    },
                },
            },
        },
        "global_options": {
            "--help-toon": {"help": "Print full command reference in TOON format and exit", "flag": True},
            "--help": {"help": "Print the standard help message and exit", "flag": True},
        },
        "exit_codes": {
            EXIT_OK: "success",
            EXIT_VALIDATION_ERROR: "validation error",
            EXIT_CONFIG_ERROR: "configuration error",
            EXIT_FILE_ERROR: "file operation error",
            EXIT_UNEXPECTED_ERROR: "unexpected error",
        },
        "notes": [
            "--author is required for write commands: "
            "create, update, link create, link remove, comment create, comment update",
            "--author is optional for read-only commands: "
            "get, list, search, link list, comment list, comment get, "
            "workflow status, workflow transitions, workflow types",
            r"Escape sequences (\n, \r\n, \t) are decoded in --text and --description values",
            "status changes in update are validated against allowed_transitions.",
            "Ticket IDs follow the pattern <PREFIX>-<NNN> (e.g. TASK-001, LINK-00001)",
        ],
    }


# ── CLI entry point ──────────────────────────────────────────────────────────


def main() -> int:
    """Main CLI entry point.  Returns an integer exit code."""
    parser = _CleanErrorParser(
        description="Tracking System CLI Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a task (positional title)
  %(prog)s create task "Implement feature X" --priority High --assignee developer

  # Create a task (--title keyword, avoids shell quoting issues)
  %(prog)s create task --title "Implement feature X" --priority High --assignee developer

  # Create a task with long description stored in a file
  %(prog)s create task --title "Implement feature X" --description-file desc.txt --author me

  # Get ticket details
  %(prog)s get TASK-001

  # List open tasks assigned to me
  %(prog)s list --status Open --assignee solution-architect

  # Update ticket status
  %(prog)s update TASK-001 --status "In Progress"

  # Create a blocking link
  %(prog)s link create TASK-001 TASK-002 Blocks --comment "Task 1 blocks Task 2"

  # List all links for a ticket
  %(prog)s link list TASK-001

  # Remove a link
  %(prog)s link remove LINK-00001

  # Search tickets
  %(prog)s search "feature X" --in-title --in-content
        """,
    )

    parser.add_argument(
        "--help-toon", action="store_true", default=False,
        help="Print the full command reference in TOON format and exit",
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Command to execute",
        parser_class=_CleanErrorParser,
    )

    def _add_author(cmd_parser: argparse.ArgumentParser, *, required: bool = True) -> None:
        cmd_parser.add_argument(
            "--author", required=required, default=None,
            help="Author identifier (e.g. architect, ux-designer)",
        )

    # ── create ───────────────────────────────────────────────────────────
    create_p = subparsers.add_parser("create", help="Create a new ticket")
    _add_author(create_p, required=True)
    create_p.add_argument("type", help="Ticket type key")
    create_p.add_argument(
        "title_positional", nargs="?", default=None, metavar="title",
        help="Ticket title (positional; alternative: --title)",
    )
    create_p.add_argument("--title", dest="title_opt", default=None, metavar="TITLE")
    create_p.add_argument("--priority", default="Medium")
    create_p.add_argument("--assignee", default="")
    create_p.add_argument("--parent", "--child-of", dest="parent", default="")
    create_p.add_argument("--addressed-to", default="")
    create_p.add_argument("--description", default="")
    create_p.add_argument("--description-file", default="", metavar="FILE")
    create_p.add_argument("--field", action="append", default=[])

    # ── get (read-only) ──────────────────────────────────────────────────
    get_p = subparsers.add_parser("get", help="Get ticket details")
    _add_author(get_p, required=False)
    get_p.add_argument("ticket_id")

    # ── list (read-only) ─────────────────────────────────────────────────
    list_p = subparsers.add_parser("list", help="List tickets")
    _add_author(list_p, required=False)
    list_p.add_argument("--status")
    list_p.add_argument("--assignee")
    list_p.add_argument("--type")
    list_p.add_argument("--priority")

    # ── update ───────────────────────────────────────────────────────────
    update_p = subparsers.add_parser("update", help="Update ticket")
    _add_author(update_p, required=True)
    update_p.add_argument("ticket_id")
    update_p.add_argument("--status")
    update_p.add_argument("--assignee")
    update_p.add_argument("--priority")

    # ── link ─────────────────────────────────────────────────────────────
    link_p = subparsers.add_parser("link", help="Manage links")
    link_subs = link_p.add_subparsers(
        dest="link_command", help="Link operation",
        parser_class=_CleanErrorParser,
    )

    lnk_create_p = link_subs.add_parser("create", help="Create a link")
    _add_author(lnk_create_p, required=True)
    lnk_create_p.add_argument("source_id")
    lnk_create_p.add_argument("target_id")
    lnk_create_p.add_argument("link_type")
    lnk_create_p.add_argument("--comment", default="")

    lnk_list_p = link_subs.add_parser("list", help="List links")
    _add_author(lnk_list_p, required=False)
    lnk_list_p.add_argument("ticket_id")
    lnk_list_p.add_argument("--direction", default="all")

    lnk_remove_p = link_subs.add_parser("remove", help="Remove a link")
    _add_author(lnk_remove_p, required=True)
    lnk_remove_p.add_argument("link_id")

    # ── comment ──────────────────────────────────────────────────────────
    comment_p = subparsers.add_parser("comment", help="Manage comments")
    comment_subs = comment_p.add_subparsers(
        dest="comment_command", help="Comment operation",
        parser_class=_CleanErrorParser,
    )

    cmt_create_p = comment_subs.add_parser("create", help="Create comment")
    _add_author(cmt_create_p, required=True)
    cmt_create_p.add_argument("ticket_id")
    cmt_create_p.add_argument("--subject", required=True)
    cmt_create_p.add_argument("--text", default="")

    cmt_list_p = comment_subs.add_parser("list", help="List comments")
    _add_author(cmt_list_p, required=False)
    cmt_list_p.add_argument("ticket_id")

    cmt_get_p = comment_subs.add_parser("get", help="Get comment")
    _add_author(cmt_get_p, required=False)
    cmt_get_p.add_argument("ticket_id")
    cmt_get_p.add_argument("comment_id")

    cmt_update_p = comment_subs.add_parser("update", help="Update comment")
    _add_author(cmt_update_p, required=True)
    cmt_update_p.add_argument("ticket_id")
    cmt_update_p.add_argument("comment_id")
    cmt_update_p.add_argument("--subject")
    cmt_update_p.add_argument("--text")

    # ── search (read-only) ───────────────────────────────────────────────
    search_p = subparsers.add_parser("search", help="Search tickets")
    _add_author(search_p, required=False)
    search_p.add_argument("query")
    search_p.add_argument("--in-title", action="store_true", default=True)
    search_p.add_argument("--in-content", action="store_true")

    # ── workflow (read-only) ─────────────────────────────────────────────
    wf_p = subparsers.add_parser("workflow", help="Inspect workflow definitions")
    wf_subs = wf_p.add_subparsers(
        dest="workflow_command", help="Workflow operation",
        parser_class=_CleanErrorParser,
    )

    wf_types_p = wf_subs.add_parser("types", help="List all ticket types")
    _add_author(wf_types_p, required=False)

    wf_status_p = wf_subs.add_parser("status", help="Show status details")
    _add_author(wf_status_p, required=False)
    wf_status_p.add_argument("ticket_type", nargs="?", default="")
    wf_status_p.add_argument("status_name", nargs="?", default="")

    wf_trans_p = wf_subs.add_parser("transitions", help="Show allowed transitions")
    _add_author(wf_trans_p, required=False)
    wf_trans_p.add_argument("ticket_type")
    wf_trans_p.add_argument("status_name", nargs="?", default="")

    # ── Parse & dispatch ─────────────────────────────────────────────────
    args = parser.parse_args()

    if args.help_toon:
        print(to_toon(_build_help_data()), end="")
        return EXIT_OK

    if not args.command:
        parser.print_help()
        return EXIT_OK

    try:
        cfg = get_runtime_config()

        if args.command == "create":
            validate_ticket_type(args.type)
            title = args.title_positional or args.title_opt
            if not title or not title.strip():
                create_p.error(
                    "title is required: provide it as a positional argument "
                    'or via --title "Your title here"'
                )
            description = decode_escape_sequences(args.description)
            if args.description_file:
                desc_path = Path(args.description_file)
                if not desc_path.exists():
                    create_p.error(
                        f"--description-file not found: {args.description_file}"
                    )
                try:
                    description = desc_path.read_text(encoding="utf-8")
                except Exception as exc:
                    create_p.error(
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

        elif args.command == "get":
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

        elif args.command == "list":
            if args.type:
                validate_ticket_type(args.type)
            if args.status:
                validate_status_value(args.status, args.type)
            if (
                args.priority
                and cfg["priority_values"]
                and args.priority not in cfg["priority_values"]
            ):
                raise ValidationError(
                    f"Invalid priority filter: {args.priority}. "
                    f"Valid values: {', '.join(cfg['priority_values'])}."
                )
            tickets = list_tickets(
                args.status, args.assignee, args.type, args.priority,
            )
            print(f"\nFound {len(tickets)} ticket(s):")
            print("=" * 100)
            print(
                f"{'ID':<15} {'Status':<15} {'Priority':<10} "
                f"{'Assignee':<20} {'Title'}"
            )
            print("-" * 100)
            for t in tickets:
                print(format_ticket(t))

        elif args.command == "update":
            ticket = update_ticket(
                args.ticket_id, args.author,
                args.status, args.assignee, args.priority,
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

        elif args.command == "link":
            if not args.link_command:
                link_p.print_help()
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

        elif args.command == "comment":
            if not args.comment_command:
                comment_p.print_help()
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

        elif args.command == "search":
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

        elif args.command == "workflow":
            _handle_workflow(args, cfg, wf_p)

        return EXIT_OK

    except FileOperationError as e:
        print(f"FileOperationError [{EXIT_FILE_ERROR}]: {e}")
        return EXIT_FILE_ERROR
    except ConfigurationError as e:
        print(f"ConfigurationError [{EXIT_CONFIG_ERROR}]: {e}")
        return EXIT_CONFIG_ERROR
    except TrackerError as e:
        print(f"ValidationError [{EXIT_VALIDATION_ERROR}]: {e}")
        return EXIT_VALIDATION_ERROR
    except Exception as e:
        print(f"UnexpectedError [{EXIT_UNEXPECTED_ERROR}]: {e}")
        return EXIT_UNEXPECTED_ERROR


# ── Workflow sub-handler ─────────────────────────────────────────────────────


def _handle_workflow(
    args: argparse.Namespace,
    cfg: dict[str, Any],
    wf_parser: argparse.ArgumentParser,
) -> None:
    """Dispatch ``workflow`` subcommands."""
    if not args.workflow_command:
        wf_parser.print_help()
        raise ValidationError("workflow subcommand required")

    if args.workflow_command == "types":
        types = cfg["ticket_types"]
        registry = cfg["type_registry"]
        specs = cfg["ticket_specs"]
        print(f"\nTicket Types ({len(types)}):")
        print("=" * 100)
        print(
            f"{'Type':<30} {'Prefix':<10} {'Statuses':>8}  "
            f"{'Initial':<20} {'Terminals'}"
        )
        print("-" * 100)
        for t in types:
            spec = specs[t]
            prefix = registry[t].get("id_prefix", "")
            n_statuses = len(spec["statuses"])
            initial = spec["initial_status"]
            terminals = " ".join(spec["terminal_statuses"]) or "--"
            print(
                f"{t:<30} {prefix:<10} {n_statuses:>8}  "
                f"{initial:<20} {terminals}"
            )

    elif args.workflow_command == "status":
        if not args.ticket_type:
            _workflow_status_all(cfg)
        else:
            validate_ticket_type(args.ticket_type)
            spec = cfg["ticket_specs"][args.ticket_type]
            if args.status_name:
                _workflow_status_single(args.ticket_type, args.status_name, spec)
            else:
                _workflow_status_type(args.ticket_type, spec)

    elif args.workflow_command == "transitions":
        validate_ticket_type(args.ticket_type)
        spec = cfg["ticket_specs"][args.ticket_type]
        if args.status_name:
            _workflow_transitions_single(
                args.ticket_type, args.status_name, spec,
            )
        else:
            _workflow_transitions_all(args.ticket_type, spec)


def _workflow_status_all(cfg: dict[str, Any]) -> None:
    types = cfg["ticket_types"]
    specs = cfg["ticket_specs"]
    print("\nStatus summary for all ticket types:")
    print("=" * 100)
    print(f"{'Type':<30} {'N':>3}  Statuses")
    print("-" * 100)
    for t in types:
        spec = specs[t]
        statuses = spec["statuses"]
        terminal_set = set(spec["terminal_statuses"])
        tagged = [f"{s}*" if s in terminal_set else s for s in statuses]
        print(f"{t:<30} {len(statuses):>3}  {', '.join(tagged)}")
    print("\n* = terminal status")


def _workflow_status_type(ticket_type: str, spec: dict[str, Any]) -> None:
    status_details: dict[str, Any] = spec.get("status_details", {})
    terminal: list[str] = spec.get("terminal_statuses", [])
    print(f"\nStatuses for ticket type '{ticket_type}':")
    print("=" * 100)
    print(f"{'Status':<30} {'T':<3} {'Stage Goal'}")
    print("-" * 100)
    for sname in spec["statuses"]:
        detail = status_details.get(sname, {})
        t_mark = "*" if sname in terminal else " "
        print(f"{sname:<30} {t_mark:<3} {detail.get('stage_goal', '')}")
    print("\n* = terminal status")


def _workflow_status_single(
    ticket_type: str,
    status_name: str,
    spec: dict[str, Any],
) -> None:
    status_details = spec.get("status_details", {})
    terminal = spec.get("terminal_statuses", [])
    if status_name not in status_details:
        valid = ", ".join(sorted(status_details.keys()))
        raise ValidationError(
            f"Status '{status_name}' not found for type '{ticket_type}'. "
            f"Valid statuses: {valid}"
        )
    detail = status_details[status_name]
    is_terminal = status_name in terminal
    label = "TERMINAL" if is_terminal else "active"
    print(f"\nStatus: {status_name}  [{label}]")
    print("=" * 70)
    roles = detail["responsible_roles"]
    roles_str = ", ".join(roles) if roles else "--"
    print(f"Description       : {detail['description']}")
    print(f"Stage Goal        : {detail['stage_goal']}")
    print(f"Responsible Roles : {roles_str}")
    transitions = spec.get("allowed_transitions", {}).get(status_name, [])
    print(
        f"Allowed Transitions: "
        f"{', '.join(transitions) if transitions else 'none (terminal)'}"
    )


def _workflow_transitions_all(
    ticket_type: str,
    spec: dict[str, Any],
) -> None:
    terminal_list = spec.get("terminal_statuses", [])
    all_transitions = spec.get("allowed_transitions", {})
    print(f"\nTransition map for '{ticket_type}':")
    print("=" * 100)
    print(f"{'From':<30}    {'To'}")
    print("-" * 100)
    for sname in spec["statuses"]:
        targets = all_transitions.get(sname, [])
        is_term = sname in terminal_list
        if targets:
            tagged = [
                f"{t} [T]" if t in terminal_list else t for t in targets
            ]
            print(f"{sname:<30} ->  {', '.join(tagged)}")
        else:
            marker = (
                "(terminal)" if is_term else "(no transitions configured)"
            )
            print(f"{sname:<30}     {marker}")
    print("\n[T] = terminal status")


def _workflow_transitions_single(
    ticket_type: str,
    status_name: str,
    spec: dict[str, Any],
) -> None:
    all_transitions = spec.get("allowed_transitions", {})
    terminal_list = spec.get("terminal_statuses", [])
    if (
        status_name not in all_transitions
        and status_name not in spec["statuses"]
    ):
        valid = ", ".join(spec["statuses"])
        raise ValidationError(
            f"Status '{status_name}' not found for type '{ticket_type}'. "
            f"Valid statuses: {valid}"
        )
    transitions = all_transitions.get(status_name, [])
    print(
        f"\nAllowed transitions from '{status_name}' ({ticket_type}):"
    )
    print("=" * 60)
    if transitions:
        for t in transitions:
            t_mark = " [TERMINAL]" if t in terminal_list else ""
            print(f"  -> {t}{t_mark}")
    else:
        print("  (none -- terminal status)")
