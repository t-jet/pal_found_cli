"""Automatic transition rule-evaluation engine.

Evaluates ``automatic_transitions`` rules for ticket types after
``create_ticket`` and ``update_ticket`` operations.  This module must NOT
be imported by ``config``, ``index``, ``validators``, ``links``,
``comments``, or ``formatters`` (acyclic dependency constraint).
"""

from __future__ import annotations

import sys
from typing import Any

from .config import get_runtime_config
from .exceptions import ValidationError
from .index import (
    get_ticket,
    read_canonical_index,
    read_link_index,
)

MAX_RECURSION_DEPTH = 5

_RULE_TYPES = {
    "all_children_reach_status",
    "first_child_reaches_status",
    "linked_ticket_reaches_status",
    "child_blocker_created",
    "all_blockers_cleared",
    "this_ticket_reaches_status",
}


# ── Public entry point ───────────────────────────────────────────────────────


def evaluate_automatic_transitions(
    ticket_id: str,
    event: str,
    _depth: int = 0,
) -> list[str]:
    """Evaluate automatic transition rules for *ticket_id* after *event*.

    Returns a list of human-readable transition descriptions performed.
    Never raises; exceptions are caught and printed to stderr.
    """
    if _depth >= MAX_RECURSION_DEPTH:
        print(
            f"[automations warning] Max recursion depth ({MAX_RECURSION_DEPTH}) "
            f"reached for {ticket_id}; stopping chain.",
            file=sys.stderr,
        )
        return []

    try:
        cfg = get_runtime_config()
        ticket = get_ticket(ticket_id)
        ticket_type = ticket["type"]
        rules: list[dict[str, Any]] = (
            cfg["ticket_specs"].get(ticket_type, {}).get("automatic_transitions", [])
        )
    except Exception as exc:
        print(
            f"[automations warning] Could not load rules for {ticket_id}: {exc}",
            file=sys.stderr,
        )
        return []

    if not rules:
        return []

    transitions: list[str] = []
    links = read_link_index()

    for rule in rules:
        if not isinstance(rule, dict):
            continue
        rule_type = rule.get("rule")
        if rule_type not in _RULE_TYPES:
            continue  # silently skip unknown rules

        try:
            _process_rule(
                ticket_id=ticket_id,
                event=event,
                rule=rule,
                links=links,
                transitions=transitions,
                depth=_depth,
            )
        except Exception as exc:
            print(
                f"[automations warning] Rule '{rule_type}' on {ticket_id} failed: {exc}",
                file=sys.stderr,
            )

    return transitions


# ── Internal dispatcher ──────────────────────────────────────────────────────


def _process_rule(
    ticket_id: str,
    event: str,
    rule: dict[str, Any],
    links: list[dict[str, Any]],
    transitions: list[str],
    depth: int,
) -> None:
    """Evaluate a single rule and fire a transition if the pre-conditions hold."""
    from .validators import validate_status_transition

    rule_type: str = rule["rule"]
    target_status: str = rule.get("target_status", "")

    # Link creation can only satisfy child_blocker_created. Other rules depend
    # on ticket or child status changes and must not run as a side effect.
    if event == "link_created" and rule_type != "child_blocker_created":
        return

    # Re-read ticket on each rule so we have the latest status (may have changed
    # from a previous rule in this same pass).
    ticket = get_ticket(ticket_id)
    current_status = ticket["status"]

    # Source-status guard (applies to most rules; AT-4 uses event guard instead)
    source_status = rule.get("source_status")
    if source_status and current_status != source_status:
        return

    # Evaluate rule-specific condition
    should_fire = False
    actual_target = target_status

    if rule_type == "all_children_reach_status":
        should_fire = _eval_all_children_reach_status(ticket, rule, links)

    elif rule_type == "first_child_reaches_status":
        should_fire = _eval_first_child_reaches_status(ticket, rule, links)

    elif rule_type == "linked_ticket_reaches_status":
        should_fire = _eval_linked_ticket_reaches_status(ticket, rule, links)

    elif rule_type == "child_blocker_created":
        # Ticket creation runs before its links exist, so link creation must
        # provide a second chance to evaluate this rule.
        if event not in {"child_created", "link_created"}:
            return
        should_fire = _eval_child_blocker_created(ticket, rule, links)
        if should_fire:
            # Save prior_status before transitioning
            _save_prior_status(ticket)

    elif rule_type == "all_blockers_cleared":
        should_fire = _eval_all_blockers_cleared(ticket, rule, links)
        if should_fire and target_status == "prior_status":
            actual_target = _read_prior_status(ticket)
            if not actual_target:
                return  # no prior_status — skip silently

    elif rule_type == "this_ticket_reaches_status":
        source_statuses: list[str] = rule.get("source_statuses", [])
        if current_status not in source_statuses:
            return
        fired = _eval_this_ticket_reaches_status(ticket, rule, links)
        if fired:
            transitions.append(
                f"{ticket_id}: linked tickets updated by this_ticket_reaches_status"
            )
        return  # AT-6 handles its own updates; do not fire a transition on this ticket

    if not should_fire:
        return

    # Resolve "prior_status" keyword for target
    if actual_target == "prior_status":
        actual_target = _read_prior_status(ticket)
        if not actual_target:
            return

    # Validate the transition is allowed before firing
    try:
        validate_status_transition(ticket["type"], current_status, actual_target)
    except ValidationError as exc:
        print(
            f"[automations warning] Skipping auto-transition {ticket_id} "
            f"{current_status} -> {actual_target}: {exc}",
            file=sys.stderr,
        )
        return

    # Fire the transition
    from .tickets import update_ticket

    old_status = current_status
    update_ticket(ticket_id, author="system", status=actual_target, _system=True)

    # Clear prior_status after AT-5 restore
    if rule_type == "all_blockers_cleared":
        _clear_prior_status(ticket_id)

    transition_desc = f"{ticket_id}: {old_status} → {actual_target}"
    transitions.append(transition_desc)

    # Recursive chaining
    chained = evaluate_automatic_transitions(ticket_id, "ticket_updated", _depth=depth + 1)
    transitions.extend(chained)


# ── Rule evaluators ──────────────────────────────────────────────────────────


def _collect_children(
    ticket_id: str,
    child_filter: dict[str, Any],
    links: list[dict[str, Any]],
) -> list[dict[str, str]]:
    """Collect child tickets for *ticket_id* according to *child_filter*.

    Children = tickets whose ``parent`` field equals *ticket_id* (optionally
    type-filtered) PLUS tickets linked as children via the link type in
    ``child_filter.link_types``.
    """
    allowed_types: list[str] | None = child_filter.get("types") if child_filter else None
    link_types_filter: list[str] = (child_filter.get("link_types") or []) if child_filter else []

    all_tickets = read_canonical_index()

    children: list[dict[str, str]] = []
    seen: set[str] = set()

    # Parent-field children
    for t in all_tickets:
        if t.get("parent") == ticket_id:
            if allowed_types and t["type"] not in allowed_types:
                continue
            if t["id"] not in seen:
                seen.add(t["id"])
                children.append(t)

    # Link-based children
    if link_types_filter:
        child_ids_from_links: set[str] = set()
        for lnk in links:
            if lnk.get("link_type") in link_types_filter:
                if lnk.get("source_ticket") == ticket_id:
                    child_ids_from_links.add(lnk["target_ticket"])
                elif lnk.get("target_ticket") == ticket_id:
                    child_ids_from_links.add(lnk["source_ticket"])

        for t in all_tickets:
            if t["id"] in child_ids_from_links and t["id"] not in seen:
                if allowed_types and t["type"] not in allowed_types:
                    continue
                seen.add(t["id"])
                children.append(t)

    return children


def _eval_all_children_reach_status(
    ticket: dict[str, str],
    rule: dict[str, Any],
    links: list[dict[str, Any]],
) -> bool:
    """AT-1: Return True when every filtered child is in one of child_statuses."""
    child_filter: dict[str, Any] = rule.get("child_filter") or {}
    child_statuses: list[str] = rule.get("child_statuses", [])
    children = _collect_children(ticket["id"], child_filter, links)
    if not children:
        return False
    return all(c["status"] in child_statuses for c in children)


def _eval_first_child_reaches_status(
    ticket: dict[str, str],
    rule: dict[str, Any],
    links: list[dict[str, Any]],
) -> bool:
    """AT-2: Return True when any filtered child is in one of child_statuses."""
    child_filter: dict[str, Any] = rule.get("child_filter") or {}
    child_statuses: list[str] = rule.get("child_statuses", [])
    children = _collect_children(ticket["id"], child_filter, links)
    if not children:
        return False
    return any(c["status"] in child_statuses for c in children)


def _eval_linked_ticket_reaches_status(
    ticket: dict[str, str],
    rule: dict[str, Any],
    links: list[dict[str, Any]],
) -> bool:
    """AT-3: Return True when any matching linked ticket is in linked_statuses."""
    link_type: str = rule.get("link_type", "")
    link_role: str = rule.get("link_role", "source")  # "source" or "target"
    linked_types: list[str] | None = rule.get("linked_ticket_types")
    linked_statuses: list[str] = rule.get("linked_statuses", [])

    ticket_id = ticket["id"]
    all_tickets = {t["id"]: t for t in read_canonical_index()}

    for lnk in links:
        if lnk.get("link_type") != link_type:
            continue
        if link_role == "source" and lnk.get("source_ticket") != ticket_id:
            continue
        if link_role == "target" and lnk.get("target_ticket") != ticket_id:
            continue

        # The other end
        if link_role == "source":
            other_id = lnk.get("target_ticket", "")
        else:
            other_id = lnk.get("source_ticket", "")

        other = all_tickets.get(other_id)
        if other is None:
            continue
        if linked_types and other["type"] not in linked_types:
            continue
        if other["status"] in linked_statuses:
            return True

    return False


def _eval_child_blocker_created(
    ticket: dict[str, str],
    rule: dict[str, Any],
    links: list[dict[str, Any]],
) -> bool:
    """AT-4: Return True when a matching child blocker link exists targeting this ticket."""
    child_filter: dict[str, Any] = rule.get("child_filter") or {}
    allowed_types: list[str] | None = child_filter.get("types")
    link_type_filter: str = child_filter.get("link_type", "Blocks")

    ticket_id = ticket["id"]
    all_tickets = {t["id"]: t for t in read_canonical_index()}

    for lnk in links:
        if lnk.get("link_type") != link_type_filter:
            continue
        # Child is the source (it Blocks the parent which is target)
        if lnk.get("target_ticket") != ticket_id:
            continue
        source_id = lnk.get("source_ticket", "")
        source = all_tickets.get(source_id)
        if source is None:
            continue
        # Source must be a child of this ticket
        if source.get("parent") != ticket_id:
            continue
        if allowed_types and source["type"] not in allowed_types:
            continue
        return True

    return False


def _eval_all_blockers_cleared(
    ticket: dict[str, str],
    rule: dict[str, Any],
    links: list[dict[str, Any]],
) -> bool:
    """AT-5: Return True when all tickets blocking this ticket are in terminal statuses."""
    blocker_terminal: list[str] = rule.get("blocker_terminal_statuses", [])
    ticket_id = ticket["id"]
    all_tickets = {t["id"]: t for t in read_canonical_index()}

    # This ticket is blocked = it is the target_ticket in a Blocks link
    blockers: list[dict[str, str]] = []
    for lnk in links:
        if lnk.get("link_type") != "Blocks":
            continue
        if lnk.get("target_ticket") != ticket_id:
            continue
        blocker_id = lnk.get("source_ticket", "")
        blocker = all_tickets.get(blocker_id)
        if blocker:
            blockers.append(blocker)

    if not blockers:
        return False
    return all(b["status"] in blocker_terminal for b in blockers)


def _eval_this_ticket_reaches_status(
    ticket: dict[str, str],
    rule: dict[str, Any],
    links: list[dict[str, Any]],
) -> bool:
    """AT-6: Update linked tickets when this ticket reaches a source_status.

    Returns True if at least one linked ticket was updated.
    """
    from .tickets import update_ticket

    link_type: str = rule.get("link_type", "")
    link_role: str = rule.get("link_role", "source")
    linked_types: list[str] | None = rule.get("linked_ticket_types")
    linked_source_status: str = rule.get("linked_ticket_source_status", "")
    linked_target_status: str = rule.get("linked_ticket_target_status", "")

    ticket_id = ticket["id"]
    all_tickets = {t["id"]: t for t in read_canonical_index()}
    updated_any = False

    for lnk in links:
        if lnk.get("link_type") != link_type:
            continue
        if link_role == "source" and lnk.get("source_ticket") != ticket_id:
            continue
        if link_role == "target" and lnk.get("target_ticket") != ticket_id:
            continue

        if link_role == "source":
            other_id = lnk.get("target_ticket", "")
        else:
            other_id = lnk.get("source_ticket", "")

        other = all_tickets.get(other_id)
        if other is None:
            continue
        if linked_types and other["type"] not in linked_types:
            continue
        if linked_source_status and other["status"] != linked_source_status:
            continue

        # Resolve "prior_status" target
        actual_target = linked_target_status
        if actual_target == "prior_status":
            # Read from the linked ticket's frontmatter
            actual_target = _read_prior_status(other)
            if not actual_target:
                continue

        from .validators import validate_status_transition

        try:
            validate_status_transition(other["type"], other["status"], actual_target)
        except ValidationError as exc:
            print(
                f"[automations warning] AT-6 skipping {other_id} "
                f"{other['status']} -> {actual_target}: {exc}",
                file=sys.stderr,
            )
            continue

        try:
            update_ticket(other_id, author="system", status=actual_target, _system=True)
            if linked_target_status == "prior_status":
                _clear_prior_status(other_id)
            updated_any = True
        except Exception as exc:
            print(
                f"[automations warning] AT-6 failed to update {other_id}: {exc}",
                file=sys.stderr,
            )

    return updated_any


# ── prior_status helpers ─────────────────────────────────────────────────────


def _save_prior_status(ticket: dict[str, str]) -> None:
    """Write the ticket's current status as ``prior_status`` in its frontmatter."""
    from .tickets import parse_ticket_file, write_ticket_file

    try:
        metadata, body = parse_ticket_file(ticket)
        metadata["prior_status"] = ticket["status"]
        write_ticket_file(ticket, metadata, body)
    except Exception as exc:
        print(
            f"[automations warning] Could not save prior_status for {ticket['id']}: {exc}",
            file=sys.stderr,
        )


def _read_prior_status(ticket: dict[str, str]) -> str:
    """Read ``prior_status`` from the ticket's frontmatter; return empty string if absent."""
    from .tickets import parse_ticket_file

    try:
        metadata, _ = parse_ticket_file(ticket)
        return str(metadata.get("prior_status") or "").strip()
    except Exception:
        return ""


def _clear_prior_status(ticket_id: str) -> None:
    """Set ``prior_status`` to empty string in the ticket's frontmatter."""
    from .tickets import parse_ticket_file, write_ticket_file
    from .index import get_ticket as _get_ticket

    try:
        ticket = _get_ticket(ticket_id)
        metadata, body = parse_ticket_file(ticket)
        metadata["prior_status"] = ""
        write_ticket_file(ticket, metadata, body)
    except Exception as exc:
        print(
            f"[automations warning] Could not clear prior_status for {ticket_id}: {exc}",
            file=sys.stderr,
        )
