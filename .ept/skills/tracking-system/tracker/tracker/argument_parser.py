"""Argument parser construction for the tracking CLI.

This module builds the argparse ArgumentParser with all commands, subcommands,
and their respective arguments and options.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys


class CleanErrorParser(argparse.ArgumentParser):
    """ArgumentParser that emits a concise error line (no usage block).

    Standard argparse prints the full usage string before the error message,
    which looks like a stack-trace dump in PowerShell / CI logs. This
    subclass suppresses the usage header so every argument error surfaces as
    a single, actionable line.
    """

    def error(self, message: str) -> None:  # type: ignore[override]
        """Handle argument parsing errors with clean, concise messages.
        
        Args:
            message: Error message from argparse
        """
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


def build_argument_parser() -> tuple[argparse.ArgumentParser, dict[str, argparse.ArgumentParser]]:
    """Build the complete argument parser for the tracking CLI.
    
    Returns:
        Tuple containing:
        - Main ArgumentParser instance
        - Dictionary of subparser references for command handlers (keys: command names)
    """
    parser = CleanErrorParser(
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

  # Show full configuration for a ticket type
  %(prog)s type-info feature
  %(prog)s type-info task
        """,
    )

    parser.add_argument(
        "--help-toon", action="store_true", default=False,
        help="Print the full command reference in TOON format and exit",
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Command to execute",
        parser_class=CleanErrorParser,
    )

    def _add_author(cmd_parser: argparse.ArgumentParser, *, required: bool = True) -> None:
        """Add --author argument to a command parser.
        
        Args:
            cmd_parser: The parser to add the --author argument to
            required: Whether --author is required for this command
        """
        cmd_parser.add_argument(
            "--author", required=required, default=None,
            help="Author identifier (e.g. architect, ux-designer)",
        )

    # Store references to subparsers for handler access
    subparser_refs: dict[str, argparse.ArgumentParser] = {}

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
    subparser_refs["create"] = create_p

    # ── get (read-only) ──────────────────────────────────────────────────
    get_p = subparsers.add_parser("get", help="Get ticket details")
    _add_author(get_p, required=False)
    get_p.add_argument("ticket_id")
    subparser_refs["get"] = get_p

    # ── list (read-only) ─────────────────────────────────────────────────
    list_p = subparsers.add_parser("list", help="List tickets")
    _add_author(list_p, required=False)
    list_p.add_argument("--status", action="append", default=None,
                        help="Filter by status; can repeat for multiple values (OR)")
    list_p.add_argument("--assignee")
    list_p.add_argument("--type", action="append", default=None,
                        help="Filter by type; can repeat for multiple values (OR)")
    list_p.add_argument("--priority", action="append", default=None,
                        help="Filter by priority; can repeat for multiple values (OR)")
    list_p.add_argument("--parent")
    list_p.add_argument("--reporter")
    list_p.add_argument("--non-terminal-only", action="store_true",
                        help="Only show tickets not in terminal statuses")
    subparser_refs["list"] = list_p

    # ── update ───────────────────────────────────────────────────────────
    update_p = subparsers.add_parser("update", help="Update ticket")
    _add_author(update_p, required=True)
    update_p.add_argument("ticket_id")
    update_p.add_argument("--status")
    update_p.add_argument("--assignee")
    update_p.add_argument("--priority")
    update_p.add_argument("--field", action="append", default=[])
    update_p.add_argument("--description", default="")
    update_p.add_argument("--description-file", default="", metavar="FILE")
    subparser_refs["update"] = update_p

    # ── link ─────────────────────────────────────────────────────────────
    link_p = subparsers.add_parser("link", help="Manage links")
    link_subs = link_p.add_subparsers(
        dest="link_command", help="Link operation",
        parser_class=CleanErrorParser,
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
    subparser_refs["link"] = link_p

    # ── comment ──────────────────────────────────────────────────────────
    comment_p = subparsers.add_parser("comment", help="Manage comments")
    comment_subs = comment_p.add_subparsers(
        dest="comment_command", help="Comment operation",
        parser_class=CleanErrorParser,
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
    subparser_refs["comment"] = comment_p

    # ── search (read-only) ───────────────────────────────────────────────
    search_p = subparsers.add_parser("search", help="Search tickets")
    _add_author(search_p, required=False)
    search_p.add_argument("query")
    search_p.add_argument("--in-title", action="store_true", default=True)
    search_p.add_argument("--in-content", action="store_true")
    subparser_refs["search"] = search_p

    # ── type-info (read-only) ────────────────────────────────────────────
    type_info_p = subparsers.add_parser(
        "type-info", help="Print full YAML configuration for a ticket type",
    )
    _add_author(type_info_p, required=False)
    type_info_p.add_argument("ticket_type", help="Ticket type key (e.g. feature, task)")
    subparser_refs["type-info"] = type_info_p

    # ── reconcile-index ─────────────────────────────────────────────────
    reconcile_p = subparsers.add_parser(
        "reconcile-index",
        help="Check or repair index status values from ticket files",
    )
    _add_author(reconcile_p, required=True)
    reconcile_p.add_argument(
        "--apply",
        action="store_true",
        help="Write canonical ticket-file statuses to the index",
    )
    subparser_refs["reconcile-index"] = reconcile_p

    # ── workflow (read-only) ─────────────────────────────────────────────
    wf_p = subparsers.add_parser("workflow", help="Inspect workflow definitions")
    wf_subs = wf_p.add_subparsers(
        dest="workflow_command", help="Workflow operation",
        parser_class=CleanErrorParser,
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
    subparser_refs["workflow"] = wf_p

    # ── build-queue (read-only) ─────────────────────────────────────────
    bq_p = subparsers.add_parser(
        "build-queue", help="Display build queue with blocking relationships",
    )
    bq_subs = bq_p.add_subparsers(
        dest="build_queue_command", help="Build queue subcommand",
        parser_class=CleanErrorParser,
    )

    bq_stage1_p = bq_subs.add_parser("stage1", help="Filter to non-terminal tickets")
    _add_author(bq_stage1_p, required=False)

    bq_stage2_p = bq_subs.add_parser("stage2", help="Recursive priority reconciliation")
    _add_author(bq_stage2_p, required=False)

    bq_stage3_p = bq_subs.add_parser("stage3", help="Sort and organize queue")
    _add_author(bq_stage3_p, required=False)

    bq_stage4_p = bq_subs.add_parser("stage4", help="Format output")
    _add_author(bq_stage4_p, required=False)

    bq_all_p = bq_subs.add_parser("all", help="Run all stages")
    _add_author(bq_all_p, required=False)
    subparser_refs["build-queue"] = bq_p

    return parser, subparser_refs
