"""Help data builder for the tracking CLI.

This module constructs the complete help documentation data structure
for all commands, subcommands, options, and examples.
"""

from __future__ import annotations

from typing import Any

from .config import get_runtime_config
from .constants import (
    EXIT_CONFIG_ERROR,
    EXIT_FILE_ERROR,
    EXIT_OK,
    EXIT_UNEXPECTED_ERROR,
    EXIT_VALIDATION_ERROR,
)


def build_help_data() -> dict[str, Any]:
    """Build a complete reference of every command, subcommand, and option.

    List-restricted options (ticket type, status, link type, priority) are
    populated from the runtime configuration when available.
    
    Returns:
        Dictionary containing complete help documentation structure including:
        - commands: All command definitions with arguments and options
        - global_options: Global CLI options (like --help-toon)
        - exit_codes: Exit code mappings and descriptions
        - notes: Usage notes and guidelines
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
                    "--parent": _opt("Filter by parent ticket ID"),
                    "--reporter": _opt("Filter by reporter identifier"),
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
                    "--field": _opt("Additional field as key=value (repeatable)", repeatable=True),
                    "--description": _opt("New description text (\\n, \\r\\n, \\t supported)"),
                    "--description-file": _opt(
                        "Path to a file whose contents replace the description",
                    ),
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
            "type-info": {
                "help": "Print the full raw YAML configuration for a ticket type",
                "author": "optional",
                "arguments": {
                    "ticket_type": _arg("Ticket type key", values=ticket_types),
                },
                "options": {"--author": _author_opt},
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
