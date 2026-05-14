"""Build-queue command for prioritizing non-terminal tickets."""

from __future__ import annotations

from typing import Any

from .config import get_runtime_config
from .index import read_index, read_link_index, write_index
from .tickets import update_ticket


# ── Priority ordering ─────────────────────────────────────────────────────────


def get_priority_index(priority: str) -> int:
    """Return the numerical priority index (lower number = higher priority).
    
    Priority values from config are ordered from lowest to highest.
    We reverse this for sorting (0 = highest priority).
    """
    cfg = get_runtime_config()
    priority_values = cfg.get("priority_values", ["Low", "Medium", "High", "Critical"])
    # Reverse to get index where 0 = highest priority (Critical)
    reversed_priorities = list(reversed(priority_values))
    if priority in reversed_priorities:
        return reversed_priorities.index(priority)
    return 999  # Unknown priority = lowest priority


# ── Stage 1: Get non-terminal tickets ────────────────────────────────────────


def stage1_get_non_terminal_tickets() -> list[dict[str, str]]:
    """Stage 1: Get a list of non-terminal tickets to work on.
    
    Returns:
        List of tickets not in terminal statuses
    """
    cfg = get_runtime_config()
    all_tickets = read_index()
    non_terminal_tickets: list[dict[str, str]] = []
    
    for ticket in all_tickets:
        ticket_type = ticket["type"]
        terminal_statuses = cfg["ticket_specs"][ticket_type]["terminal_statuses"]
        if ticket["status"] not in terminal_statuses:
            non_terminal_tickets.append(ticket)
    
    return non_terminal_tickets


# ── Stage 2: Priority cleanup ────────────────────────────────────────────────


def stage2_priority_cleanup(tickets: list[dict[str, str]], author: str = "build-queue") -> list[dict[str, str]]:
    """Stage 2: Priority cleanup to ensure consistency.
    
    For each ticket:
    - Check all child tickets have priority >= parent priority
    - Check all blocking tickets have priority >= blocked ticket priority
    
    Args:
        tickets: List of non-terminal tickets
        author: Author identifier for ticket updates
    
    Returns:
        Updated list of tickets
    """
    cfg = get_runtime_config()
    all_links = read_link_index()
    link_blocking = cfg.get("link_blocking", {})
    
    # Build ticket lookup
    ticket_map = {t["id"]: t for t in tickets}
    
    # Build parent-child and blocking relationships
    parent_children: dict[str, list[str]] = {}  # parent_id -> [child_id, ...]
    blocking_map: dict[str, list[str]] = {}  # blocked_ticket -> [blocking_ticket, ...]
    
    for link in all_links:
        source_id = link["source_ticket"]
        target_id = link["target_ticket"]
        link_type = link["link_type"]
        
        # Skip if either ticket not in our non-terminal list
        if source_id not in ticket_map or target_id not in ticket_map:
            continue
        
        # Check if it's a parent-child relationship (Contains link type)
        if link_type == "Contains":
            if source_id not in parent_children:
                parent_children[source_id] = []
            parent_children[source_id].append(target_id)
        
        # Check if it's a blocking relationship
        if link_blocking.get(link_type, False):
            if target_id not in blocking_map:
                blocking_map[target_id] = []
            blocking_map[target_id].append(source_id)
    
    # Recursively update priorities
    max_iterations = 100
    iteration = 0
    changes_made = True
    
    while changes_made and iteration < max_iterations:
        changes_made = False
        iteration += 1
        
        # Check parent-child relationships
        for parent_id, child_ids in parent_children.items():
            if parent_id not in ticket_map:
                continue
            parent_priority_idx = get_priority_index(ticket_map[parent_id]["priority"])
            
            for child_id in child_ids:
                if child_id not in ticket_map:
                    continue
                child_priority_idx = get_priority_index(ticket_map[child_id]["priority"])
                
                # Child must have priority >= parent (lower index = higher priority)
                if child_priority_idx > parent_priority_idx:
                    # Update child to match parent
                    old_priority = ticket_map[child_id]["priority"]
                    new_priority = ticket_map[parent_id]["priority"]
                    ticket_map[child_id]["priority"] = new_priority
                    
                    # Persist the change
                    update_ticket(
                        child_id,
                        author,
                        priority=new_priority,
                        _system=True,
                    )
                    changes_made = True
                    print(f"  Updated {child_id} priority: {old_priority} → {new_priority} (child of {parent_id})")
        
        # Check blocking relationships
        for blocked_id, blocker_ids in blocking_map.items():
            if blocked_id not in ticket_map:
                continue
            blocked_priority_idx = get_priority_index(ticket_map[blocked_id]["priority"])
            
            for blocker_id in blocker_ids:
                if blocker_id not in ticket_map:
                    continue
                blocker_priority_idx = get_priority_index(ticket_map[blocker_id]["priority"])
                
                # Blocker must have priority >= blocked (lower index = higher priority)
                if blocker_priority_idx > blocked_priority_idx:
                    # Update blocker to match blocked
                    old_priority = ticket_map[blocker_id]["priority"]
                    new_priority = ticket_map[blocked_id]["priority"]
                    ticket_map[blocker_id]["priority"] = new_priority
                    
                    # Persist the change
                    update_ticket(
                        blocker_id,
                        author,
                        priority=new_priority,
                        _system=True,
                    )
                    changes_made = True
                    print(f"  Updated {blocker_id} priority: {old_priority} → {new_priority} (blocks {blocked_id})")
    
    return list(ticket_map.values())


# ── Stage 3: Build the queue ─────────────────────────────────────────────────


def stage3_build_queue(tickets: list[dict[str, str]]) -> list[dict[str, str]]:
    """Stage 3: Sort tickets based on priority and blocking relationships.
    
    Sorting criteria:
    - Tickets that block others with highest priority
    - Tickets with highest priority
    - Tickets that block others with next priority
    - Tickets with next priority
    - ... and so on
    
    Args:
        tickets: List of non-terminal tickets with cleaned priorities
    
    Returns:
        Sorted list of tickets
    """
    cfg = get_runtime_config()
    all_links = read_link_index()
    link_blocking = cfg.get("link_blocking", {})
    
    # Build set of ticket IDs for quick lookup
    ticket_ids = {t["id"] for t in tickets}
    
    # Build blocking relationships: ticket -> set of tickets it blocks (in our list)
    blocks_map: dict[str, set[str]] = {}
    for link in all_links:
        if link_blocking.get(link["link_type"], False):
            source_id = link["source_ticket"]
            target_id = link["target_ticket"]
            # Only consider if both are in our non-terminal list
            if source_id in ticket_ids and target_id in ticket_ids:
                if source_id not in blocks_map:
                    blocks_map[source_id] = set()
                blocks_map[source_id].add(target_id)
    
    # Get priority values (reversed so highest priority first)
    cfg_priority_values = cfg.get("priority_values", ["Low", "Medium", "High", "Critical"])
    priority_values = list(reversed(cfg_priority_values))
    
    # Build sorted queue: for each priority level, add blocking then non-blocking
    sorted_queue: list[dict[str, str]] = []
    remaining_tickets = tickets.copy()
    
    for priority in priority_values:
        # Get tickets with this priority
        priority_tickets = [t for t in remaining_tickets if t["priority"] == priority]
        
        # Split into blocking and non-blocking
        blocking_tickets = [t for t in priority_tickets if t["id"] in blocks_map]
        non_blocking_tickets = [t for t in priority_tickets if t["id"] not in blocks_map]
        
        # Add blocking tickets first, then non-blocking
        sorted_queue.extend(blocking_tickets)
        sorted_queue.extend(non_blocking_tickets)
        
        # Remove from remaining
        for t in priority_tickets:
            remaining_tickets.remove(t)
    
    # Add any remaining tickets (shouldn't happen if all have valid priorities)
    sorted_queue.extend(remaining_tickets)
    
    return sorted_queue


# ── Stage 4: Output the queue ────────────────────────────────────────────────


def stage4_output_queue(sorted_queue: list[dict[str, str]]) -> None:
    """Stage 4: Output the sorted queue with position and blocking info.
    
    Args:
        sorted_queue: Sorted list of tickets
    """
    cfg = get_runtime_config()
    all_links = read_link_index()
    link_blocking = cfg.get("link_blocking", {})
    
    # Build blocking relationships for display
    blocks_map: dict[str, list[str]] = {}
    for link in all_links:
        if link_blocking.get(link["link_type"], False):
            source_id = link["source_ticket"]
            target_id = link["target_ticket"]
            if source_id not in blocks_map:
                blocks_map[source_id] = []
            blocks_map[source_id].append(target_id)
    
    print(f"\nBuild Queue ({len(sorted_queue)} tickets):")
    print("=" * 180)
    print(
        f"{'Pos':<5} {'ID':<15} {'Status':<15} {'Priority':<10} "
        f"{'Assignee':<20} {'Blocks':<40} {'Title'}"
    )
    print("-" * 180)
    
    for position, ticket in enumerate(sorted_queue, start=1):
        ticket_id = ticket["id"]
        blocks_tickets = blocks_map.get(ticket_id, [])
        blocks_str = ", ".join(blocks_tickets) if blocks_tickets else ""
        
        print(
            f"{position:<5} {ticket_id:<15} {ticket['status']:<15} "
            f"{ticket['priority']:<10} {ticket['assignee']:<20} "
            f"{blocks_str:<40} {ticket['title']}"
        )


# ── Main build-queue function ────────────────────────────────────────────────


def build_queue(author: str = "build-queue", stage: str = "all") -> list[dict[str, str]]:
    """Build a prioritized queue of non-terminal tickets.
    
    Args:
        author: Author identifier for ticket updates
        stage: Which stage(s) to run: "stage1", "stage2", "stage3", "stage4", or "all"
    
    Returns:
        Sorted list of tickets
    """
    print("\n=== Build Queue ===\n")
    
    # Stage 1
    if stage in ("stage1", "all"):
        print("Stage 1: Filtering non-terminal tickets...")
        tickets = stage1_get_non_terminal_tickets()
        print(f"  Found {len(tickets)} non-terminal tickets")
        if stage == "stage1":
            return tickets
    else:
        tickets = stage1_get_non_terminal_tickets()
    
    # Stage 2
    if stage in ("stage2", "all"):
        print("\nStage 2: Priority cleanup...")
        tickets = stage2_priority_cleanup(tickets, author)
        print(f"  Completed priority cleanup")
        if stage == "stage2":
            return tickets
    else:
        tickets = stage2_priority_cleanup(tickets, author)
    
    # Stage 3
    if stage in ("stage3", "all"):
        print("\nStage 3: Building sorted queue...")
        tickets = stage3_build_queue(tickets)
        print(f"  Queue built with {len(tickets)} tickets")
        if stage == "stage3":
            return tickets
    else:
        tickets = stage3_build_queue(tickets)
    
    # Stage 4
    if stage in ("stage4", "all"):
        print("\nStage 4: Output...")
        stage4_output_queue(tickets)
    
    return tickets