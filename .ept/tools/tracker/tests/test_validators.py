"""Tests for tracker.validators — type, status, link, and direction validation."""

from __future__ import annotations

from pathlib import Path

import pytest

from tracker.exceptions import ValidationError
from tracker.validators import (
    validate_link_direction,
    validate_link_type,
    validate_status_transition,
    validate_status_value,
    validate_ticket_type,
)


# ── validate_ticket_type ─────────────────────────────────────────────────────


class TestValidateTicketType:
    def test_valid_types(self, tracker_env: Path) -> None:
        for t in ("task", "workitem", "question"):
            validate_ticket_type(t)

    def test_invalid_type_raises(self, tracker_env: Path) -> None:
        with pytest.raises(ValidationError, match="Invalid ticket type"):
            validate_ticket_type("nonexistent")


# ── validate_link_type ───────────────────────────────────────────────────────


class TestValidateLinkType:
    def test_valid_link_types(self, tracker_env: Path) -> None:
        for lt in ("Blocks", "RelatesTo", "ParentChild"):
            validate_link_type(lt)

    def test_invalid_link_type_raises(self, tracker_env: Path) -> None:
        with pytest.raises(ValidationError, match="Invalid link type"):
            validate_link_type("Unknown")


# ── validate_status_value ────────────────────────────────────────────────────


class TestValidateStatusValue:
    def test_valid_global(self, tracker_env: Path) -> None:
        validate_status_value("New")
        validate_status_value("Closed")

    def test_valid_for_type(self, tracker_env: Path) -> None:
        validate_status_value("New", "task")

    def test_invalid_global(self, tracker_env: Path) -> None:
        with pytest.raises(ValidationError, match="Invalid status"):
            validate_status_value("NoSuchStatus")

    def test_invalid_for_type(self, tracker_env: Path) -> None:
        with pytest.raises(ValidationError, match="Invalid status"):
            validate_status_value("NoSuchStatus", "task")


# ── validate_status_transition ───────────────────────────────────────────────


class TestValidateStatusTransition:
    """Uses the rich_tracker_env which defines allowed_transitions."""

    def test_allowed_transition(self, rich_tracker_env: Path) -> None:
        validate_status_transition("task", "New", "Open")
        validate_status_transition("task", "Open", "Closed")

    def test_disallowed_transition(self, rich_tracker_env: Path) -> None:
        with pytest.raises(ValidationError, match="Invalid status transition"):
            validate_status_transition("task", "New", "Closed")

    def test_terminal_status_message(self, rich_tracker_env: Path) -> None:
        with pytest.raises(ValidationError, match="terminal status"):
            validate_status_transition("task", "Closed", "New")

    def test_ascii_arrow_in_message(self, rich_tracker_env: Path) -> None:
        """BUG-003 regression: must use ASCII ``->`` not Unicode arrow."""
        with pytest.raises(ValidationError) as exc_info:
            validate_status_transition("task", "New", "Closed")
        assert "->" in str(exc_info.value)
        assert "\u2192" not in str(exc_info.value)

    def test_no_transitions_configured_allows_any(self, tracker_env: Path) -> None:
        """When allowed_transitions is empty, any transition is allowed."""
        validate_status_transition("task", "New", "Closed")


# ── validate_link_direction ──────────────────────────────────────────────────


class TestValidateLinkDirection:
    @pytest.mark.parametrize("d", ["in", "out", "all"])
    def test_valid(self, d: str) -> None:
        validate_link_direction(d)

    def test_invalid(self) -> None:
        with pytest.raises(ValidationError, match="Invalid link direction"):
            validate_link_direction("sideways")
