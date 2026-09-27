"""Workflow and type-info command handlers for the tracking CLI.

This module contains handlers for workflow inspection commands and type-info display.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from ..config import get_paths, get_runtime_config
from ..exceptions import ConfigurationError, ValidationError
from ..validators import validate_ticket_type


def handle_type_info(args: argparse.Namespace) -> None:
    """Handle the 'type-info' command to display ticket type configuration.
    
    Args:
        args: Parsed command-line arguments containing ticket_type
    
    Raises:
        ValidationError: If ticket type is invalid
        ConfigurationError: If configuration file not found
    """
    validate_ticket_type(args.ticket_type)
    paths = get_paths()
    # Find the $ref path for this ticket type in the raw workflow file
    with open(paths.workflow_file, "r", encoding="utf-8") as _wf:
        raw_workflow = yaml.safe_load(_wf) or {}
    ref_file: Path | None = None
    for _entry in raw_workflow.get("ticket_types", []):
        if not isinstance(_entry, dict):
            continue
        _ref = _entry.get("$ref")
        if _ref:
            _candidate = paths.config_dir / _ref
            try:
                with open(_candidate, "r", encoding="utf-8") as _tf:
                    _loaded = yaml.safe_load(_tf)
                if isinstance(_loaded, dict) and _loaded.get("type") == args.ticket_type:
                    ref_file = _candidate
                    break
            except Exception:
                continue
    if ref_file is None:
        raise ConfigurationError(
            f"No configuration file found for ticket type '{args.ticket_type}'. "
            "Fix: ensure the type has a $ref entry in ticket_types in .workflow.yaml"
        )
    print(ref_file.read_text(encoding="utf-8"), end="")


def handle_workflow(
    args: argparse.Namespace,
    cfg: dict[str, Any],
    wf_parser: argparse.ArgumentParser,
) -> None:
    """Handle the 'workflow' command and its subcommands.
    
    Args:
        args: Parsed command-line arguments
        cfg: Runtime configuration dictionary
        wf_parser: The argument parser for the workflow command (for help)
    
    Raises:
        ValidationError: If workflow subcommand or arguments are invalid
    """
    if not args.workflow_command:
        wf_parser.print_help()
        raise ValidationError("workflow subcommand required")

    if args.workflow_command == "types":
        _workflow_types(cfg)
    elif args.workflow_command == "status":
        _workflow_status(args, cfg)
    elif args.workflow_command == "transitions":
        _workflow_transitions(args, cfg)


def _workflow_types(cfg: dict[str, Any]) -> None:
    """Display all registered ticket types.
    
    Args:
        cfg: Runtime configuration dictionary
    """
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


def _workflow_status(args: argparse.Namespace, cfg: dict[str, Any]) -> None:
    """Display status information for ticket types.
    
    Args:
        args: Parsed command-line arguments
        cfg: Runtime configuration dictionary
    
    Raises:
        ValidationError: If ticket type or status name is invalid
    """
    if not args.ticket_type:
        _workflow_status_all(cfg)
    else:
        validate_ticket_type(args.ticket_type)
        spec = cfg["ticket_specs"][args.ticket_type]
        if args.status_name:
            _workflow_status_single(args.ticket_type, args.status_name, spec)
        else:
            _workflow_status_type(args.ticket_type, spec)


def _workflow_status_all(cfg: dict[str, Any]) -> None:
    """Display status summary for all ticket types.
    
    Args:
        cfg: Runtime configuration dictionary
    """
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
    """Display detailed status information for a specific ticket type.
    
    Args:
        ticket_type: The ticket type key
        spec: Ticket type specification from runtime config
    """
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
    """Display detailed information for a specific status.
    
    Args:
        ticket_type: The ticket type key
        status_name: The status name to display
        spec: Ticket type specification from runtime config
    
    Raises:
        ValidationError: If status_name is not found
    """
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


def _workflow_transitions(args: argparse.Namespace, cfg: dict[str, Any]) -> None:
    """Display transition information for a ticket type.
    
    Args:
        args: Parsed command-line arguments
        cfg: Runtime configuration dictionary
    
    Raises:
        ValidationError: If ticket type or status name is invalid
    """
    validate_ticket_type(args.ticket_type)
    spec = cfg["ticket_specs"][args.ticket_type]
    if args.status_name:
        _workflow_transitions_single(
            args.ticket_type, args.status_name, spec,
        )
    else:
        _workflow_transitions_all(args.ticket_type, spec)


def _workflow_transitions_all(
    ticket_type: str,
    spec: dict[str, Any],
) -> None:
    """Display complete transition map for a ticket type.
    
    Args:
        ticket_type: The ticket type key
        spec: Ticket type specification from runtime config
    """
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
    """Display transitions for a specific status.
    
    Args:
        ticket_type: The ticket type key
        status_name: The status name to show transitions for
        spec: Ticket type specification from runtime config
    
    Raises:
        ValidationError: If status_name is not found
    """
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
