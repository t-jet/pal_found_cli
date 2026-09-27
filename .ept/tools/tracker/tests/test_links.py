"""Tests for tracker.links — create, list, remove links."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.conftest import make_task
from tracker.exceptions import ValidationError
from tracker.links import create_link, get_link_roles, list_links, remove_link


# ── get_link_roles ───────────────────────────────────────────────────────────


class TestGetLinkRoles:
    def test_known_type(self, tracker_env: Path) -> None:
        src, tgt = get_link_roles("Blocks")
        assert src == "Blocks"
        assert tgt == "Is Blocked By"

    def test_symmetric(self, tracker_env: Path) -> None:
        src, tgt = get_link_roles("RelatesTo")
        assert src == "Relates To"
        assert tgt == "Relates To"


# ── create_link ──────────────────────────────────────────────────────────────


class TestCreateLink:
    def test_returns_link_id(self, tracker_env: Path) -> None:
        t1 = make_task("A")
        t2 = make_task("B")
        lid = create_link(t1, t2, "Blocks", "architect")
        assert lid.startswith("LINK-")

    def test_written_to_index(self, tracker_env: Path) -> None:
        t1 = make_task("A")
        t2 = make_task("B")
        lid = create_link(t1, t2, "Blocks", "architect")
        links = list_links(t1)
        ids = [lk["link_id"] for lk in links]
        assert lid in ids

    def test_duplicate_raises(self, tracker_env: Path) -> None:
        t1 = make_task("A")
        t2 = make_task("B")
        create_link(t1, t2, "Blocks", "architect")
        with pytest.raises(ValidationError, match="already exists"):
            create_link(t1, t2, "Blocks", "architect")

    def test_source_not_found_raises(self, tracker_env: Path) -> None:
        t2 = make_task("B")
        with pytest.raises(ValidationError, match="does not exist"):
            create_link("FAKE-999", t2, "Blocks", "architect")

    def test_target_not_found_raises(self, tracker_env: Path) -> None:
        t1 = make_task("A")
        with pytest.raises(ValidationError, match="does not exist"):
            create_link(t1, "FAKE-999", "Blocks", "architect")

    def test_invalid_type_raises(self, tracker_env: Path) -> None:
        t1 = make_task("A")
        t2 = make_task("B")
        with pytest.raises(ValidationError, match="Invalid link type"):
            create_link(t1, t2, "Unknown", "architect")


# ── list_links ───────────────────────────────────────────────────────────────


class TestListLinks:
    def test_direction_out(self, tracker_env: Path) -> None:
        t1 = make_task("A")
        t2 = make_task("B")
        create_link(t1, t2, "Blocks", "architect")
        out_links = list_links(t1, "out")
        assert len(out_links) == 1
        in_links = list_links(t1, "in")
        assert len(in_links) == 0

    def test_direction_in(self, tracker_env: Path) -> None:
        t1 = make_task("A")
        t2 = make_task("B")
        create_link(t1, t2, "Blocks", "architect")
        in_links = list_links(t2, "in")
        assert len(in_links) == 1

    def test_direction_all(self, tracker_env: Path) -> None:
        t1 = make_task("A")
        t2 = make_task("B")
        create_link(t1, t2, "Blocks", "architect")
        all_links = list_links(t1, "all")
        assert len(all_links) == 1

    def test_nonexistent_ticket_raises(self, tracker_env: Path) -> None:
        with pytest.raises(ValidationError, match="does not exist"):
            list_links("FAKE-999")

    def test_invalid_direction_raises(self, tracker_env: Path) -> None:
        t1 = make_task("A")
        with pytest.raises(ValidationError, match="Invalid link direction"):
            list_links(t1, "sideways")


# ── remove_link ──────────────────────────────────────────────────────────────


class TestRemoveLink:
    def test_removes_entry(self, tracker_env: Path) -> None:
        t1 = make_task("A")
        t2 = make_task("B")
        lid = create_link(t1, t2, "Blocks", "architect")
        assert remove_link(lid) is True
        links = list_links(t1)
        assert len(links) == 0

    def test_nonexistent_raises(self, tracker_env: Path) -> None:
        with pytest.raises(ValidationError, match="not found"):
            remove_link("LINK-99999")
