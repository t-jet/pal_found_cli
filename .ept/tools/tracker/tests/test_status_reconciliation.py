"""Regression tests for canonical ticket status and index reconciliation."""

from __future__ import annotations

import csv
from pathlib import Path

from tests.conftest import make_task, run_main
from tracker.build_queue import build_queue
from tracker.comments import list_comments
from tracker.config import get_paths
from tracker.index import read_index, read_link_index, reconcile_index_statuses
from tracker.links import create_link
from tracker.tickets import (
    get_ticket_with_content,
    list_tickets,
    ticket_file_path,
    update_ticket,
)


def _set_index_status(ticket_id: str, status: str) -> None:
    """Write a stale status into an isolated fixture's CSV index."""
    index_path = get_paths().index_file
    with index_path.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
        fieldnames = list(rows[0])
    for row in rows:
        if row["id"] == ticket_id:
            row["status"] = status
    with index_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_get_and_list_use_frontmatter_status(tracker_env: Path) -> None:
    """Canonical reads ignore a stale, invalid index status."""
    ticket_id = make_task("Canonical status")
    _set_index_status(ticket_id, "In Development")

    assert get_ticket_with_content(ticket_id)["status"] == "New"
    assert [ticket["id"] for ticket in list_tickets(status="New")] == [ticket_id]
    assert list_tickets(status="In Development") == []


def test_build_queue_outputs_canonical_status(
    tracker_env: Path,
    capsys,
) -> None:
    """Queue filtering and output use the ticket-file status."""
    ticket_id = make_task("Queued ticket")
    _set_index_status(ticket_id, "In Development")

    queue = build_queue(stage="all")
    output = capsys.readouterr().out

    assert queue[0]["status"] == "New"
    assert ticket_id in output
    assert "In Development" not in output


def test_update_validates_transition_from_canonical_status(
    rich_tracker_env: Path,
) -> None:
    """A stale index value cannot block a valid transition."""
    ticket_id = make_task("Transition ticket")
    _set_index_status(ticket_id, "In Development")

    updated = update_ticket(ticket_id, "developer", status="Open")

    assert updated["status"] == "Open"
    assert read_index()[0]["status"] == "Open"
    assert get_ticket_with_content(ticket_id)["status"] == "Open"


def test_reconciliation_check_is_read_only_and_apply_preserves_related_data(
    tracker_env: Path,
) -> None:
    """Repair changes only stale index status values."""
    ticket_id = make_task("Drifted ticket")
    related_id = make_task("Related ticket")
    create_link(ticket_id, related_id, "RelatesTo", "developer", "context")
    _set_index_status(ticket_id, "In Development")

    ticket_path = ticket_file_path(get_ticket_with_content(ticket_id))
    ticket_before = ticket_path.read_bytes()
    comments_before = list_comments(ticket_id)
    links_before = read_link_index()

    expected = [
        {
            "ticket_id": ticket_id,
            "index_status": "In Development",
            "canonical_status": "New",
        }
    ]
    assert reconcile_index_statuses() == expected
    assert read_index()[0]["status"] == "In Development"

    assert reconcile_index_statuses(apply=True) == expected
    assert read_index()[0]["status"] == "New"
    assert ticket_path.read_bytes() == ticket_before
    assert list_comments(ticket_id) == comments_before
    assert read_link_index() == links_before


def test_reconcile_index_cli_requires_explicit_apply(tracker_env: Path) -> None:
    """CLI defaults to check mode and repairs only with ``--apply``."""
    ticket_id = make_task("CLI reconciliation")
    _set_index_status(ticket_id, "In Development")

    check_output, check_rc = run_main(
        [
            "reconcile-index",
            "--author",
            "developer",
        ]
    )
    assert check_rc == 0
    assert "mode: check" in check_output
    assert "changed: 0" in check_output
    assert read_index()[0]["status"] == "In Development"

    apply_output, apply_rc = run_main(
        [
            "reconcile-index",
            "--author",
            "developer",
            "--apply",
        ]
    )
    assert apply_rc == 0
    assert "mode: apply" in apply_output
    assert "changed: 1" in apply_output
    assert read_index()[0]["status"] == "New"
