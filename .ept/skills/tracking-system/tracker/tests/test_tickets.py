"""Tests for tracker.tickets — create, update, get, list, search, status context."""

from __future__ import annotations

import re
from pathlib import Path
from unittest.mock import patch

import pytest

from tests.conftest import make_task, make_workitem
from tracker.config import get_paths, get_runtime_config, invalidate_config
from tracker.constants import TICKET_CONTENT_FILE
from tracker.exceptions import ValidationError
from tracker.index import get_ticket, read_index
from tracker.tickets import (
    build_status_context,
    create_ticket,
    get_ticket_with_content,
    list_tickets,
    parse_ticket_file,
    search_tickets,
    ticket_file_path,
    update_ticket,
)


# ── create_ticket ────────────────────────────────────────────────────────────


class TestCreateTicket:
    def test_returns_id(self, tracker_env: Path) -> None:
        tid = make_task("First task")
        assert tid == "TASK-001"

    def test_increments_counter(self, tracker_env: Path) -> None:
        make_task("A")
        tid2 = make_task("B")
        assert tid2 == "TASK-002"

    def test_ticket_file_exists(self, tracker_env: Path) -> None:
        tid = make_task("File check")
        ticket = get_ticket(tid)
        fp = ticket_file_path(ticket)
        assert fp.exists()

    def test_ticket_no_parent_in_frontmatter(self, tracker_env: Path) -> None:
        tid = make_task("No parent field")
        ticket = get_ticket(tid)
        metadata, _ = parse_ticket_file(ticket)
        assert "parent" not in metadata

    def test_workitem_nested_in_parent_folder(self, tracker_env: Path) -> None:
        parent_id = make_task("Parent")
        child_id = make_workitem(parent_id, "Child")
        child_ticket = get_ticket(child_id)
        # Path should contain the parent ID
        assert parent_id in child_ticket["path"]

    def test_indexed(self, tracker_env: Path) -> None:
        tid = make_task("Indexed")
        tickets = read_index()
        ids = [t["id"] for t in tickets]
        assert tid in ids

    def test_invalid_type_raises(self, tracker_env: Path) -> None:
        with pytest.raises(ValidationError, match="Invalid ticket type"):
            create_ticket("nonexistent", "T", author="a", assignee="b")

    def test_invalid_priority_raises(self, tracker_env: Path) -> None:
        with pytest.raises(ValidationError, match="Invalid priority"):
            create_ticket(
                "task", "T", author="a", priority="NotReal", assignee="b",
            )

    def test_parent_not_found_raises(self, tracker_env: Path) -> None:
        with pytest.raises(ValidationError, match="does not exist"):
            create_ticket(
                "workitem", "T", author="a", parent="FAKE-999",
            )

    def test_unknown_extra_field_raises(self, tracker_env: Path) -> None:
        with pytest.raises(ValidationError, match="Unknown field"):
            create_ticket(
                "task", "T", author="a", assignee="b",
                extra_fields={"fake_field": "val"},
            )

    def test_frontmatter_no_yaml_doc_end_marker(self, tracker_env: Path) -> None:
        """BUG-002: ticket file must not have ``...`` YAML doc-end marker."""
        tid = make_task("No doc end")
        ticket = get_ticket(tid)
        fp = ticket_file_path(ticket)
        content = fp.read_text(encoding="utf-8")
        assert "\n...\n" not in content

    def test_create_with_description(self, tracker_env: Path) -> None:
        tid = create_ticket(
            "task", "Described", author="a", assignee="b",
            description="Some body text",
        )
        ticket = get_ticket(tid)
        _, body = parse_ticket_file(ticket)
        assert "Some body text" in body


# ── update_ticket ────────────────────────────────────────────────────────────


class TestUpdateTicket:
    def test_update_status(self, tracker_env: Path) -> None:
        tid = make_task("Update me")
        result = update_ticket(tid, "architect", status="Open")
        assert result["status"] == "Open"

    def test_update_priority(self, tracker_env: Path) -> None:
        tid = make_task("Priority change")
        result = update_ticket(tid, "architect", priority="High")
        assert result["priority"] == "High"

    def test_update_assignee(self, tracker_env: Path) -> None:
        tid = make_task("Assign")
        result = update_ticket(tid, "architect", assignee="new-dev")
        assert result["assignee"] == "new-dev"

    def test_update_writes_file_without_yaml_end_marker(
        self, tracker_env: Path,
    ) -> None:
        tid = make_task("Update file")
        update_ticket(tid, "architect", status="Open")
        ticket = get_ticket(tid)
        fp = ticket_file_path(ticket)
        content = fp.read_text(encoding="utf-8")
        assert "\n...\n" not in content

    def test_update_writes_file_without_parent_field(
        self, tracker_env: Path,
    ) -> None:
        tid = make_task("No parent field")
        update_ticket(tid, "architect", status="Open")
        ticket = get_ticket(tid)
        fp = ticket_file_path(ticket)
        content = fp.read_text(encoding="utf-8")
        # Extract frontmatter
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        assert match
        assert "parent:" not in match.group(1)

    def test_update_nonexistent_raises(self, tracker_env: Path) -> None:
        with pytest.raises(ValidationError, match="not found"):
            update_ticket("FAKE-999", "architect", status="Open")

    def test_update_invalid_priority_raises(self, tracker_env: Path) -> None:
        tid = make_task("Bad prio")
        with pytest.raises(ValidationError, match="Invalid priority"):
            update_ticket(tid, "architect", priority="NotReal")

    def test_noop_no_write(self, tracker_env: Path) -> None:
        """When no fields actually change, no write should occur."""
        tid = make_task("Noop")
        ticket_before = get_ticket(tid)
        result = update_ticket(
            tid, "architect",
            status=ticket_before["status"],
        )
        assert result["updated"] == ticket_before["updated"]

    def test_status_transition_blocked(self, rich_tracker_env: Path) -> None:
        tid = create_ticket(
            "task", "Transition test", author="a",
            priority="Medium", assignee="b",
        )
        with pytest.raises(ValidationError, match="Invalid status transition"):
            update_ticket(tid, "a", status="Closed")


# ── get_ticket_with_content ──────────────────────────────────────────────────


class TestGetTicketWithContent:
    def test_returns_metadata(self, tracker_env: Path) -> None:
        tid = make_task("Get me")
        result = get_ticket_with_content(tid)
        assert result["id"] == tid
        assert result["type"] == "task"

    def test_includes_body(self, tracker_env: Path) -> None:
        tid = make_task("Body check")
        result = get_ticket_with_content(tid)
        assert "content" in result

    def test_not_found_raises(self, tracker_env: Path) -> None:
        with pytest.raises(ValidationError, match="not found"):
            get_ticket_with_content("FAKE-999")


# ── list_tickets ─────────────────────────────────────────────────────────────


class TestListTickets:
    def test_list_all(self, tracker_env: Path) -> None:
        make_task("A")
        make_task("B")
        results = list_tickets()
        assert len(results) == 2

    def test_filter_by_status(self, tracker_env: Path) -> None:
        make_task("New one")
        results = list_tickets(status="New")
        assert all(t["status"] == "New" for t in results)

    def test_filter_by_assignee(self, tracker_env: Path) -> None:
        make_task("Assigned", assignee="alice")
        make_task("Other", assignee="bob")
        results = list_tickets(assignee="alice")
        assert len(results) == 1
        assert results[0]["assignee"] == "alice"

    def test_filter_by_type(self, tracker_env: Path) -> None:
        make_task("A task")
        parent_id = make_task("Parent")
        make_workitem(parent_id, "A workitem")
        results = list_tickets(ticket_type="workitem")
        assert len(results) == 1
        assert results[0]["type"] == "workitem"

    def test_filter_by_priority(self, tracker_env: Path) -> None:
        make_task("High prio", priority="High")
        make_task("Low prio", priority="Low")
        results = list_tickets(priority="High")
        assert len(results) == 1


# ── search_tickets ───────────────────────────────────────────────────────────


class TestSearchTickets:
    def test_search_in_title(self, tracker_env: Path) -> None:
        make_task("Find me please")
        make_task("Nothing here")
        results = search_tickets("Find me", in_title=True, in_content=False)
        assert len(results) == 1
        assert results[0]["title"] == "Find me please"

    def test_search_in_content(self, tracker_env: Path) -> None:
        tid = create_ticket(
            "task", "Content search", author="a", assignee="b",
            description="unique_magic_string",
        )
        results = search_tickets(
            "unique_magic_string", in_title=False, in_content=True,
        )
        assert len(results) == 1

    def test_search_no_results(self, tracker_env: Path) -> None:
        make_task("Irrelevant")
        results = search_tickets("zzz_no_match", in_title=True, in_content=True)
        assert len(results) == 0


# ── build_status_context ─────────────────────────────────────────────────────


class TestBuildStatusContext:
    def test_basic_context(self, tracker_env: Path) -> None:
        ctx = build_status_context("TASK-001", "task", "New")
        assert ctx["ticket_id"] == "TASK-001"
        assert ctx["current_status"] == "New"

    def test_rich_context(self, rich_tracker_env: Path) -> None:
        ctx = build_status_context("TASK-001", "task", "New")
        assert ctx["allowed_transitions"] == ["Open"]
        assert ctx["status_description"] == "Ticket just created."
        assert ctx["status_goal"] == "Prepare ticket."
        assert "Architect" in ctx["status_responsible_roles"]


# ── GAP-01: update_ticket extra_fields ───────────────────────────────────────


class TestUpdateTicketExtraFields:
    def test_update_known_optional_field(self, tracker_env: Path) -> None:
        tid = make_task("Field update")
        result = update_ticket(tid, "architect", extra_fields={"addressed_to": "pm"})
        ticket = get_ticket(tid)
        metadata, _ = parse_ticket_file(ticket)
        assert metadata.get("addressed_to") == "pm"

    def test_updated_field_visible_via_get(self, tracker_env: Path) -> None:
        tid = make_task("Get after update")
        update_ticket(tid, "architect", extra_fields={"addressed_to": "qa"})
        data = get_ticket_with_content(tid)
        assert data.get("addressed_to") == "qa"

    def test_update_unknown_field_raises(self, tracker_env: Path) -> None:
        tid = make_task("Unknown field")
        with pytest.raises(ValidationError, match="Unknown field"):
            update_ticket(tid, "architect", extra_fields={"nonexistent_field": "x"})

    def test_update_disallowed_field_raises(self, tracker_env: Path) -> None:
        """Field in valid_field_names but not in type optional_fields raises."""
        parent_id = make_task("Parent")
        child_id = make_workitem(parent_id, "Child")
        # 'addressed_to' is not in workitem optional_fields
        with pytest.raises(ValidationError, match="not allowed for type"):
            update_ticket(child_id, "architect", extra_fields={"addressed_to": "x"})


# ── GAP-02: list_tickets parent filter ───────────────────────────────────────


class TestListTicketsParentFilter:
    def test_filter_by_parent_returns_children(self, tracker_env: Path) -> None:
        parent_id = make_task("Parent ticket")
        child1 = make_workitem(parent_id, "Child 1")
        child2 = make_workitem(parent_id, "Child 2")
        make_task("Unrelated")
        results = list_tickets(parent=parent_id)
        ids = [t["id"] for t in results]
        assert child1 in ids
        assert child2 in ids
        assert len(results) == 2

    def test_filter_by_parent_combined_with_status(self, tracker_env: Path) -> None:
        parent_id = make_task("Parent")
        child1 = make_workitem(parent_id, "Open child")
        make_workitem(parent_id, "New child")
        # Move child1 to Open
        update_ticket(child1, "architect", status="Open")
        results = list_tickets(status="Open", parent=parent_id)
        assert len(results) == 1
        assert results[0]["id"] == child1

    def test_filter_by_parent_combined_with_type(self, tracker_env: Path) -> None:
        parent_id = make_task("Parent")
        make_workitem(parent_id, "Child workitem")
        results = list_tickets(ticket_type="workitem", parent=parent_id)
        assert len(results) == 1

    def test_nonexistent_parent_returns_empty(self, tracker_env: Path) -> None:
        make_task("Task A")
        # No ticket has FAKE-999 as parent; just returns empty list
        results = list_tickets(parent="FAKE-999")
        assert results == []


# ── GAP-03: update_ticket description ────────────────────────────────────────


class TestUpdateTicketDescription:
    def test_update_description_replaces_body(self, tracker_env: Path) -> None:
        tid = make_task("Desc update")
        update_ticket(tid, "architect", description="New body text")
        ticket = get_ticket(tid)
        _, body = parse_ticket_file(ticket)
        assert "New body text" in body

    def test_update_description_readable_via_get(self, tracker_env: Path) -> None:
        tid = make_task("Desc via get")
        update_ticket(tid, "architect", description="Updated content here")
        data = get_ticket_with_content(tid)
        assert "Updated content here" in data["content"]

    def test_no_description_leaves_body_unchanged(self, tracker_env: Path) -> None:
        tid = create_ticket(
            "task", "Body unchanged", author="a", assignee="b",
            description="Original body",
        )
        update_ticket(tid, "architect", assignee="new-dev")
        ticket = get_ticket(tid)
        _, body = parse_ticket_file(ticket)
        assert "Original body" in body

    def test_update_description_escape_sequences(self, tracker_env: Path) -> None:
        tid = make_task("Escape test")
        update_ticket(tid, "architect", description="Line1\\nLine2")
        ticket = get_ticket(tid)
        _, body = parse_ticket_file(ticket)
        assert "Line1\nLine2" in body


# ── GAP-04: list_tickets reporter filter ─────────────────────────────────────


class TestListTicketsReporterFilter:
    def test_filter_by_reporter(self, tracker_env: Path) -> None:
        create_ticket("task", "By Alice", author="alice", assignee="dev")
        create_ticket("task", "By Bob", author="bob", assignee="dev")
        results = list_tickets(reporter="alice")
        assert len(results) == 1
        assert results[0]["reporter"] == "alice"

    def test_filter_by_reporter_no_match(self, tracker_env: Path) -> None:
        make_task("Task")
        results = list_tickets(reporter="nobody")
        assert results == []
