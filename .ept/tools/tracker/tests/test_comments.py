"""Tests for tracker.comments — create, list, get, update comments."""

from __future__ import annotations

import threading
from datetime import datetime as _real_datetime
from pathlib import Path

import pytest

from tests.conftest import make_task
from tracker.comments import (
    _comments_dir,
    create_comment,
    get_comment,
    list_comments,
    update_comment,
)
from tracker.constants import COMMENT_TEMPLATE
from tracker.exceptions import ValidationError
from tracker.tickets import create_ticket, update_ticket


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


# ── BUG-005: same-second write preservation ──────────────────────────────────


class _FrozenDateTime:
    """``datetime`` replacement that freezes ``now()`` to one instant.

    ``tracker.comments`` imports the ``datetime`` class directly, so freezing
    the clock guarantees every write in a test lands in the same second and
    exercises the same-second identity path deterministically.
    """

    def __init__(self, instant: _real_datetime) -> None:
        self._instant = instant

    def now(self) -> _real_datetime:  # noqa: D102 - mirrors datetime API
        return self._instant


_FIXED_INSTANT = _real_datetime(2026, 10, 6, 16, 29, 54)


@pytest.fixture()
def frozen_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    """Freeze ``datetime.now()`` used by ``tracker.comments``."""
    monkeypatch.setattr(
        "tracker.comments.datetime", _FrozenDateTime(_FIXED_INSTANT)
    )


class TestSameSecondWrites:
    """BUG-005: same-author writes within one second must not overwrite."""

    def test_same_author_same_second_distinct_ids(
        self, tracker_env: Path, frozen_clock: None
    ) -> None:
        """Two substantive comments get distinct ids; both remain readable."""
        tid = make_task("Same-second comments")
        first = create_comment(tid, "tech-lead", "Approval", "Approved revision 2")
        second = create_comment(tid, "tech-lead", "Second note", "Additional note")

        assert first != second
        assert get_comment(tid, first)["text"] == "Approved revision 2"
        assert get_comment(tid, second)["text"] == "Additional note"

    def test_substantive_comment_survives_field_and_status_update(
        self, tracker_env: Path, frozen_clock: None
    ) -> None:
        """A later ticket update must not replace an earlier approval comment."""
        tid = make_task("Approval then update")
        approval_id = create_comment(
            tid, "tech-lead", "Approval", "Approved BA-DES-015 revision 2"
        )

        # Field update and status update both emit an auto "Ticket updated"
        # comment from the same author in the same frozen second.
        update_ticket(tid, "tech-lead", priority="High")
        update_ticket(tid, "tech-lead", status="Open")

        approval = get_comment(tid, approval_id)
        assert approval["subject"] == "Approval"
        assert approval["text"] == "Approved BA-DES-015 revision 2"

        subjects = [c["subject"] for c in list_comments(tid)]
        assert subjects.count("Approval") == 1
        assert subjects.count("Ticket updated") >= 2

    def test_multiple_same_author_comments_all_preserved(
        self, tracker_env: Path, frozen_clock: None
    ) -> None:
        """Many same-second writes produce one durable comment each."""
        tid = make_task("Many same-second comments")
        bodies = [f"body-{i}" for i in range(5)]
        ids = [create_comment(tid, "qa", f"Note {i}", b) for i, b in enumerate(bodies)]

        assert len(set(ids)) == len(ids)
        for cid, body in zip(ids, bodies):
            assert get_comment(tid, cid)["text"] == body
        listed = {c["comment_id"]: c["subject"] for c in list_comments(tid)}
        for cid, i in zip(ids, range(len(ids))):
            assert listed[cid] == f"Note {i}"

    def test_concurrent_writers_same_second(
        self, tracker_env: Path, frozen_clock: None
    ) -> None:
        """Concurrent same-second writers each get their own file."""
        tid = make_task("Concurrent comments")
        created: list[str] = []
        errors: list[Exception] = []
        barrier = threading.Barrier(8)

        def worker(index: int) -> None:
            try:
                barrier.wait()
                created.append(
                    create_comment(tid, "tech-lead", f"W{index}", f"payload-{index}")
                )
            except Exception as exc:  # pragma: no cover - failure capture
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert len(created) == 8
        assert len(set(created)) == 8
        for i, cid in enumerate(created):
            assert get_comment(tid, cid)["text"].startswith("payload-")

    def test_numeric_author_suffix_keeps_identity(
        self, tracker_env: Path, frozen_clock: None
    ) -> None:
        """An author name ending in digits is not a collision suffix."""
        tid = make_task("Numeric author suffix")
        authors = ("service_001", "service", "service_001", "service")
        ids = [
            create_comment(tid, author, f"Note {index}", f"body-{index}")
            for index, author in enumerate(authors)
        ]

        assert len(set(ids)) == len(ids)
        for index, (cid, author) in enumerate(zip(ids, authors)):
            assert get_comment(tid, cid)["author"] == author
            assert get_comment(tid, cid)["text"] == f"body-{index}"

        listed = {
            comment["comment_id"]: comment["author"]
            for comment in list_comments(tid)
        }
        assert [listed[cid] for cid in ids] == list(authors)

    def test_legacy_comment_ids_remain_readable(
        self, tracker_env: Path, frozen_clock: None
    ) -> None:
        """A previously issued comment ID remains valid after new writes."""
        tid = make_task("Legacy comment IDs")
        comments_dir = _comments_dir(tid)
        first = "20261006-162954-service"
        second = "20261006-162954-service_001"
        for cid, subject, body in (
            (first, "Original", "first body"),
            (second, "Follow-up", "second body"),
        ):
            (comments_dir / f"{cid}.md").write_text(
                COMMENT_TEMPLATE.format(
                    subject=subject,
                    created="2026-10-06T16:29:54",
                    updated="2026-10-06T16:29:54",
                    text=body,
                ),
                encoding="utf-8",
            )

        assert get_comment(tid, first)["author"] == "service"
        assert get_comment(tid, second)["author"] == "service"
        assert get_comment(tid, second)["text"] == "second body"
        update_comment(tid, first, "service", "Edited", None)
        assert get_comment(tid, first)["subject"] == "Edited"
        new = create_comment(tid, "service_001", "New", "third body")
        assert get_comment(tid, new)["author"] == "service_001"
        assert get_comment(tid, second)["text"] == "second body"

    def test_existing_comment_reference_stays_valid(
        self, tracker_env: Path, frozen_clock: None
    ) -> None:
        """Ids created before the fix stay addressable after new writes."""
        tid = make_task("Reference stability")
        first = create_comment(tid, "dev", "Original", "original body")
        create_comment(tid, "dev", "Later", "later body")

        assert get_comment(tid, first)["subject"] == "Original"
        update_comment(tid, first, "dev", "Edited", None)
        assert get_comment(tid, first)["subject"] == "Edited"

    def test_created_ticket_auto_comment_then_manual_same_second(
        self, tracker_env: Path, frozen_clock: None
    ) -> None:
        """The create-time auto comment is not clobbered by a same-second note."""
        tid = create_ticket("task", "Auto then manual", author="architect", assignee="dev")
        note = create_comment(tid, "architect", "Manual note", "kept")

        comments = list_comments(tid)
        subjects = [c["subject"] for c in comments]
        assert "Ticket created" in subjects
        assert get_comment(tid, note)["text"] == "kept"
        assert len(comments) >= 2
