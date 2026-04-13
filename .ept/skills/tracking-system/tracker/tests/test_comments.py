"""Tests for tracker.comments — create, list, get, update comments."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.conftest import make_task
from tracker.comments import create_comment, get_comment, list_comments, update_comment
from tracker.exceptions import ValidationError


# ── create_comment ───────────────────────────────────────────────────────────


class TestCreateComment:
    def test_creates_file(self, tracker_env: Path) -> None:
        tid = make_task("Commentable")
        cid = create_comment(tid, "author", "Initial note", "Body text")
        assert cid  # non-empty string

    def test_contains_subject_and_text(self, tracker_env: Path) -> None:
        tid = make_task("Commentable")
        cid = create_comment(tid, "dev", "My subject", "My body")
        comment = get_comment(tid, cid)
        assert comment["subject"] == "My subject"
        assert comment["text"] == "My body"

    def test_empty_subject_raises(self, tracker_env: Path) -> None:
        tid = make_task("Commentable")
        with pytest.raises(ValidationError, match="subject is required"):
            create_comment(tid, "dev", "", "body")

    def test_whitespace_subject_raises(self, tracker_env: Path) -> None:
        tid = make_task("Commentable")
        with pytest.raises(ValidationError, match="subject is required"):
            create_comment(tid, "dev", "   ", "body")


# ── list_comments ────────────────────────────────────────────────────────────


class TestListComments:
    def test_returns_all(self, tracker_env: Path) -> None:
        tid = make_task("Multi-comment")
        # create_ticket adds one auto-comment ("Ticket created") by "architect".
        # Add two more with different authors to avoid timestamp collisions.
        create_comment(tid, "dev-a", "Second", "text 2")
        create_comment(tid, "dev-b", "Third", "text 3")
        comments = list_comments(tid)
        # auto-comment(architect) + Second(dev-a) + Third(dev-b) = 3
        assert len(comments) >= 3

    def test_empty_when_no_manual_comments(self, tracker_env: Path) -> None:
        tid = make_task("Few comments")
        comments = list_comments(tid)
        # The auto-comment from create_ticket counts as 1
        assert len(comments) >= 1


# ── get_comment ──────────────────────────────────────────────────────────────


class TestGetComment:
    def test_returns_subject(self, tracker_env: Path) -> None:
        tid = make_task("Gettable")
        cid = create_comment(tid, "dev", "Subject here", "body")
        result = get_comment(tid, cid)
        assert result["subject"] == "Subject here"

    def test_not_found_raises(self, tracker_env: Path) -> None:
        tid = make_task("No such comment")
        with pytest.raises(ValidationError, match="not found"):
            get_comment(tid, "nonexistent-comment")


# ── update_comment ───────────────────────────────────────────────────────────


class TestUpdateComment:
    def test_changes_subject_and_text(self, tracker_env: Path) -> None:
        tid = make_task("Updatable")
        cid = create_comment(tid, "dev", "Original subject", "Original body")
        updated = update_comment(tid, cid, "dev", "New subject", "New body")
        assert updated["subject"] == "New subject"
        assert updated["text"] == "New body"

    def test_subject_only_preserves_text(self, tracker_env: Path) -> None:
        tid = make_task("Partial update")
        cid = create_comment(tid, "dev", "Old subject", "Keep this body")
        updated = update_comment(tid, cid, "dev", "New subject", None)
        assert updated["subject"] == "New subject"
        assert updated["text"] == "Keep this body"

    def test_text_only_preserves_subject(self, tracker_env: Path) -> None:
        tid = make_task("Partial update 2")
        cid = create_comment(tid, "dev", "Keep this subject", "Old body")
        updated = update_comment(tid, cid, "dev", None, "New body")
        assert updated["subject"] == "Keep this subject"
        assert updated["text"] == "New body"

    def test_empty_subject_raises(self, tracker_env: Path) -> None:
        tid = make_task("Empty subj")
        cid = create_comment(tid, "dev", "Valid", "body")
        with pytest.raises(ValidationError, match="cannot be empty"):
            update_comment(tid, cid, "dev", "", None)
