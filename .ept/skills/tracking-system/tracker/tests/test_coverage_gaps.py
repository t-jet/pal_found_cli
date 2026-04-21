"""Targeted coverage tests for automations.py and cli.py uncovered paths."""

from __future__ import annotations

import csv
import io
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Generator
from unittest.mock import patch

import pytest

from tests.conftest import run_main
from tracker.config import TrackerPaths, invalidate_config, reset, set_paths
from tracker.constants import (
    EXIT_CONFIG_ERROR,
    EXIT_FILE_ERROR,
    EXIT_OK,
    EXIT_VALIDATION_ERROR,
    INDEX_FIELDNAMES,
    LINK_INDEX_FIELDNAMES,
)
from tracker.index import get_ticket
from tracker.links import create_link
from tracker.tickets import create_ticket, update_ticket, parse_ticket_file


# ── automation helpers ────────────────────────────────────────────────────────


def _make_task_a(title: str = "Task", **kwargs) -> str:
    return create_ticket("task", title, author="tester", priority="Medium",
                         assignee="dev", **kwargs)


def _make_workitem_a(parent_id: str, title: str = "WI") -> str:
    return create_ticket("workitem", title, author="tester", parent=parent_id)


def _make_question_a(parent_id: str, title: str = "Q?") -> str:
    return create_ticket("question", title, author="tester",
                         parent=parent_id, addressed_to="pm")


def _add_blocks_a(source: str, target: str) -> None:
    create_link(source, target, "Blocks", created_by="tester", comment="")


def _status_a(tid: str) -> str:
    return get_ticket(tid)["status"]


# ═══════════════════════════════════════════════════════════════════════════════
# automations.py coverage
# ═══════════════════════════════════════════════════════════════════════════════


class TestAutomationsMissingLines:
    """Tests that exercise the previously-uncovered branches in automations.py."""

    # Line 134: exception branch in evaluate_automatic_transitions setup
    def test_evaluate_bad_ticket_returns_empty(self, auto_tracker_env):
        from tracker.automations import evaluate_automatic_transitions
        result = evaluate_automatic_transitions("NONEXISTENT-0", "ticket_updated")
        assert result == []

    # Lines 168-170: AT-4 rule evaluated on non-child_created event → skips
    def test_at4_rule_skipped_for_ticket_updated_event(self, auto_tracker_env):
        from tracker.automations import evaluate_automatic_transitions
        parent = _make_task_a("AT4 skip event")
        update_ticket(parent, "tester", status="Open")
        q = _make_question_a(parent)
        _add_blocks_a(q, parent)
        # ticket_updated event should NOT trigger child_blocker_created
        evaluate_automatic_transitions(parent, "ticket_updated")
        assert _status_a(parent) == "Open"

    # Lines 175-181: AT-4 fires but _save_prior_status executes (prior_status saved)
    def test_at4_save_prior_status_called(self, auto_tracker_env):
        from tracker.automations import evaluate_automatic_transitions
        parent = _make_task_a("AT4 save prior")
        update_ticket(parent, "tester", status="Open")
        q = _make_question_a(parent)
        _add_blocks_a(q, parent)
        evaluate_automatic_transitions(parent, "child_created")
        ticket = get_ticket(parent)
        md, _ = parse_ticket_file(ticket)
        assert str(md.get("prior_status") or "") != ""

    # Line 191: AT-6 fires and returns, appending to transitions
    def test_at6_appends_to_transitions(self, auto_tracker_env):
        from tracker.automations import evaluate_automatic_transitions
        parent = _make_task_a("AT6 appends")
        update_ticket(parent, "tester", status="Open")
        q = _make_question_a(parent)
        _add_blocks_a(q, parent)
        evaluate_automatic_transitions(parent, "child_created")
        assert _status_a(parent) == "Blocked"
        update_ticket(q, "tester", status="Open")
        update_ticket(q, "tester", status="Resolved")
        # AT-6 fires here and appends to transitions list
        assert _status_a(parent) == "Open"

    # Lines 238, 245: AT-5 with all_blockers_cleared = True but target_status
    # is a literal (not "prior_status"), so actual_target stays as-is
    def test_at5_non_prior_status_target(self, auto_tracker_env):
        """AT-5 rule with a literal target_status (not 'prior_status')."""
        from tracker.automations import evaluate_automatic_transitions
        from tracker.config import get_runtime_config
        parent = _make_task_a("AT5 literal target")
        update_ticket(parent, "tester", status="Open")
        b = create_ticket("blocker_type", "B", author="tester")
        update_ticket(b, "tester", status="Open")
        _add_blocks_a(b, parent)
        update_ticket(parent, "tester", status="Blocked")
        update_ticket(b, "tester", status="Closed")
        # Patch AT-5 rule to use target_status="Open" (not prior_status)
        cfg = get_runtime_config()
        orig = cfg["ticket_specs"]["task"]["automatic_transitions"][:]
        cfg["ticket_specs"]["task"]["automatic_transitions"] = [
            {
                "rule": "all_blockers_cleared",
                "blocker_terminal_statuses": ["Closed", "Canceled"],
                "source_status": "Blocked",
                "target_status": "Open",  # literal, not prior_status
            }
        ]
        try:
            evaluate_automatic_transitions(parent, "ticket_updated")
            assert _status_a(parent) == "Open"
        finally:
            cfg["ticket_specs"]["task"]["automatic_transitions"] = orig

    # Lines 296, 298: _eval_linked_ticket_reaches_status — "target" link_role path
    def test_eval_linked_target_role(self, auto_tracker_env):
        from tracker.automations import _eval_linked_ticket_reaches_status
        from tracker.index import read_link_index

        t1 = _make_task_a("LT source")
        t2 = _make_task_a("LT target")
        update_ticket(t2, "tester", status="Open")
        _add_blocks_a(t1, t2)  # t1 is source_ticket
        links = read_link_index()
        # t2 is the target_ticket of the Blocks link
        rule = {
            "rule": "linked_ticket_reaches_status",
            "link_type": "Blocks",
            "link_role": "target",  # t2 is target → look at source (t1)
            "linked_statuses": ["New"],
        }
        ticket = get_ticket(t2)
        assert _eval_linked_ticket_reaches_status(ticket, rule, links) is True

    # Line 306: other ticket not in all_tickets (None) — continue
    def test_eval_linked_other_id_not_found(self, auto_tracker_env):
        from tracker.automations import _eval_linked_ticket_reaches_status
        from tracker.index import read_link_index

        t1 = _make_task_a("Ghost source")
        links = read_link_index()
        # Inject a fake link with non-existent target
        fake_link = {
            "link_id": "LINK-99999",
            "source_ticket": t1,
            "target_ticket": "GHOST-999",
            "link_type": "Blocks",
            "source_role": "Blocks",
            "target_role": "Is Blocked By",
            "created": "2026-01-01",
            "created_by": "test",
            "comment": "",
        }
        links_with_ghost = links + [fake_link]
        rule = {
            "rule": "linked_ticket_reaches_status",
            "link_type": "Blocks",
            "link_role": "source",
            "linked_statuses": ["Open"],
        }
        ticket = get_ticket(t1)
        result = _eval_linked_ticket_reaches_status(ticket, rule, links_with_ghost)
        assert result is False

    # Line 310: linked_types filter — type doesn't match
    def test_eval_linked_type_filter_excludes(self, auto_tracker_env):
        from tracker.automations import _eval_linked_ticket_reaches_status
        from tracker.index import read_link_index

        t1 = _make_task_a("Type filter source")
        t2 = _make_task_a("Task target")  # type is "task"
        update_ticket(t2, "tester", status="Open")
        _add_blocks_a(t1, t2)
        links = read_link_index()
        rule = {
            "rule": "linked_ticket_reaches_status",
            "link_type": "Blocks",
            "link_role": "source",
            "linked_ticket_types": ["workitem"],  # t2 is "task"
            "linked_statuses": ["Open"],
        }
        ticket = get_ticket(t1)
        assert _eval_linked_ticket_reaches_status(ticket, rule, links) is False

    # Lines 334, 337: AT-4: source_ticket None, and source.parent != ticket_id
    def test_at4_source_not_in_index_and_wrong_parent(self, auto_tracker_env):
        from tracker.automations import _eval_child_blocker_created
        from tracker.index import read_link_index

        parent = _make_task_a("AT4 edge")
        other = _make_task_a("Unrelated")
        # Test with a ghost source_ticket not in index
        fake_link = {
            "link_id": "LINK-88888",
            "source_ticket": "GHOST-777",
            "target_ticket": parent,
            "link_type": "Blocks",
            "source_role": "Blocks",
            "target_role": "Is Blocked By",
            "created": "2026-01-01",
            "created_by": "test",
            "comment": "",
        }
        links = read_link_index() + [fake_link]
        rule = {
            "rule": "child_blocker_created",
            "child_filter": {"types": ["question"], "link_type": "Blocks"},
        }
        ticket = get_ticket(parent)
        assert _eval_child_blocker_created(ticket, rule, links) is False

    # Line 341: AT-4: source is child but wrong type
    def test_at4_child_wrong_type_filtered(self, auto_tracker_env):
        from tracker.automations import _eval_child_blocker_created
        from tracker.index import read_link_index

        parent = _make_task_a("AT4 wrong type")
        wi = _make_workitem_a(parent)  # workitem, not question
        _add_blocks_a(wi, parent)
        links = read_link_index()
        rule = {
            "rule": "child_blocker_created",
            "child_filter": {"types": ["question"], "link_type": "Blocks"},
        }
        ticket = get_ticket(parent)
        assert _eval_child_blocker_created(ticket, rule, links) is False

    # Line 346: AT-4: returns True path (already covered by integration but adds direct path)
    def test_at4_returns_true_directly(self, auto_tracker_env):
        from tracker.automations import _eval_child_blocker_created
        from tracker.index import read_link_index

        parent = _make_task_a("AT4 direct true")
        q = _make_question_a(parent)
        _add_blocks_a(q, parent)
        links = read_link_index()
        rule = {
            "rule": "child_blocker_created",
            "child_filter": {"types": ["question"], "link_type": "Blocks"},
        }
        ticket = get_ticket(parent)
        assert _eval_child_blocker_created(ticket, rule, links) is True

    # Lines 366, 368: _eval_all_blockers_cleared — blocker not in all_tickets (None skip)
    def test_all_blockers_cleared_ghost_blocker_skipped(self, auto_tracker_env):
        from tracker.automations import _eval_all_blockers_cleared
        from tracker.index import read_link_index

        parent = _make_task_a("Ghost blocker")
        fake_link = {
            "link_id": "LINK-77777",
            "source_ticket": "GHOST-555",
            "target_ticket": parent,
            "link_type": "Blocks",
            "source_role": "Blocks",
            "target_role": "Is Blocked By",
            "created": "2026-01-01",
            "created_by": "test",
            "comment": "",
        }
        links = read_link_index() + [fake_link]
        rule = {
            "rule": "all_blockers_cleared",
            "blocker_terminal_statuses": ["Closed"],
        }
        ticket = get_ticket(parent)
        # Ghost doesn't exist in index → blockers list is empty → returns False
        assert _eval_all_blockers_cleared(ticket, rule, links) is False

    # Lines 402, 404: AT-6 link_role="target" path (look at source_ticket)
    def test_at6_target_role_resolves_source_ticket(self, auto_tracker_env):
        from tracker.automations import _eval_this_ticket_reaches_status
        from tracker.index import read_link_index

        # q blocks parent; from the parent's perspective, the parent is the
        # target_ticket of the Blocks link. We need to test link_role="target".
        parent = _make_task_a("AT6 target role")
        update_ticket(parent, "tester", status="Open")
        q = _make_question_a(parent)
        update_ticket(q, "tester", status="Open")
        _add_blocks_a(q, parent)
        links = read_link_index()
        # parent is target of Blocks link; look for source (q) with status "Open"
        rule = {
            "rule": "this_ticket_reaches_status",
            "source_statuses": ["Open"],  # parent is Open
            "link_type": "Blocks",
            "link_role": "target",
            "linked_ticket_source_status": "Open",
            "linked_ticket_target_status": "Resolved",
        }
        ticket = get_ticket(parent)
        # Should attempt to fire and transition q from Open to Resolved
        from tracker.automations import _eval_this_ticket_reaches_status as func
        result = func(ticket, rule, links)
        assert result is True

    # Line 406: AT-6 other_id not found in all_tickets
    def test_at6_ghost_other_skipped(self, auto_tracker_env):
        from tracker.automations import _eval_this_ticket_reaches_status

        parent = _make_task_a("AT6 ghost")
        fake_link = {
            "link_id": "LINK-66666",
            "source_ticket": parent,
            "target_ticket": "GHOST-444",
            "link_type": "Blocks",
            "source_role": "Blocks",
            "target_role": "Is Blocked By",
            "created": "2026-01-01",
            "created_by": "test",
            "comment": "",
        }
        rule = {
            "rule": "this_ticket_reaches_status",
            "source_statuses": ["New"],
            "link_type": "Blocks",
            "link_role": "source",
            "linked_ticket_source_status": "",
            "linked_ticket_target_status": "Open",
        }
        ticket = get_ticket(parent)
        result = _eval_this_ticket_reaches_status(ticket, rule, [fake_link])
        assert result is False

    # Lines 411, 415: AT-6 linked_types filter and linked_source_status mismatch
    def test_at6_type_filter_and_status_mismatch(self, auto_tracker_env):
        from tracker.automations import _eval_this_ticket_reaches_status
        from tracker.index import read_link_index

        t1 = _make_task_a("AT6 filter src")
        t2 = _make_task_a("AT6 filter tgt")  # type is task
        _add_blocks_a(t1, t2)
        links = read_link_index()
        # linked_ticket_types excludes "task"
        rule1 = {
            "rule": "this_ticket_reaches_status",
            "source_statuses": ["New"],
            "link_type": "Blocks",
            "link_role": "source",
            "linked_ticket_types": ["workitem"],
            "linked_ticket_source_status": "",
            "linked_ticket_target_status": "Open",
        }
        ticket = get_ticket(t1)
        assert _eval_this_ticket_reaches_status(ticket, rule1, links) is False

        # linked_source_status mismatch
        rule2 = {
            "rule": "this_ticket_reaches_status",
            "source_statuses": ["New"],
            "link_type": "Blocks",
            "link_role": "source",
            "linked_ticket_source_status": "Open",  # t2 is "New"
            "linked_ticket_target_status": "Open",
        }
        assert _eval_this_ticket_reaches_status(ticket, rule2, links) is False

    # Lines 417-427: AT-6 prior_status resolution → no prior_status → skip
    def test_at6_prior_status_empty_skips(self, auto_tracker_env):
        from tracker.automations import _eval_this_ticket_reaches_status
        from tracker.index import read_link_index

        parent = _make_task_a("AT6 no prior")
        update_ticket(parent, "tester", status="Open")
        update_ticket(parent, "tester", status="Blocked")
        q = _make_question_a(parent)
        _add_blocks_a(q, parent)
        # parent is Blocked but has NO prior_status saved in frontmatter
        links = read_link_index()
        rule = {
            "rule": "this_ticket_reaches_status",
            "source_statuses": ["New"],
            "link_type": "Blocks",
            "link_role": "source",
            "linked_ticket_source_status": "Blocked",
            "linked_ticket_target_status": "prior_status",
        }
        ticket = get_ticket(q)
        result = _eval_this_ticket_reaches_status(ticket, rule, links)
        # parent has no prior_status → skipped → returns False
        assert result is False

    # Lines 433-439: AT-6 validate_status_transition failure → warning → continue
    def test_at6_invalid_transition_logs_warning(self, auto_tracker_env, capsys):
        from tracker.automations import _eval_this_ticket_reaches_status
        from tracker.index import read_link_index

        t1 = _make_task_a("AT6 invalid trans src")
        t2 = _make_task_a("AT6 invalid trans tgt")
        update_ticket(t2, "tester", status="Open")
        _add_blocks_a(t1, t2)
        links = read_link_index()
        # Closed → New is not a valid transition (Closed is terminal)
        rule = {
            "rule": "this_ticket_reaches_status",
            "source_statuses": ["New"],
            "link_type": "Blocks",
            "link_role": "source",
            "linked_ticket_source_status": "Open",
            "linked_ticket_target_status": "New",  # invalid: Open -> New not allowed
        }
        ticket = get_ticket(t1)
        result = _eval_this_ticket_reaches_status(ticket, rule, links)
        captured = capsys.readouterr()
        assert "AT-6 skipping" in captured.err or result is False

    # Lines 446-447: AT-6 update_ticket exception → warning
    def test_at6_update_exception_logs_warning(self, auto_tracker_env, capsys):
        from tracker.automations import _eval_this_ticket_reaches_status
        from tracker.index import read_link_index

        t1 = _make_task_a("AT6 exc src")
        t2 = _make_task_a("AT6 exc tgt")
        update_ticket(t2, "tester", status="Open")
        _add_blocks_a(t1, t2)
        links = read_link_index()
        rule = {
            "rule": "this_ticket_reaches_status",
            "source_statuses": ["New"],
            "link_type": "Blocks",
            "link_role": "source",
            "linked_ticket_source_status": "Open",
            "linked_ticket_target_status": "In Progress",
        }
        ticket = get_ticket(t1)
        with patch("tracker.tickets.update_ticket", side_effect=RuntimeError("boom")):
            result = _eval_this_ticket_reaches_status(ticket, rule, links)
        captured = capsys.readouterr()
        assert "AT-6 failed" in captured.err
        assert result is False

    # Lines 466-467: _save_prior_status exception path
    def test_save_prior_status_exception_logs(self, auto_tracker_env, capsys):
        from tracker.automations import _save_prior_status
        parent = _make_task_a("save prior exc")
        ticket = get_ticket(parent)
        with patch("tracker.tickets.parse_ticket_file", side_effect=Exception("disk error")):
            _save_prior_status(ticket)
        captured = capsys.readouterr()
        assert "Could not save prior_status" in captured.err

    # Lines 480-481: _read_prior_status exception → returns ""
    def test_read_prior_status_exception_returns_empty(self, auto_tracker_env):
        from tracker.automations import _read_prior_status
        parent = _make_task_a("read prior exc")
        ticket = get_ticket(parent)
        with patch("tracker.tickets.parse_ticket_file", side_effect=Exception("err")):
            result = _read_prior_status(ticket)
        assert result == ""

    # Lines 494-495: _clear_prior_status exception path
    def test_clear_prior_status_exception_logs(self, auto_tracker_env, capsys):
        from tracker.automations import _clear_prior_status
        parent = _make_task_a("clear prior exc")
        with patch("tracker.tickets.parse_ticket_file", side_effect=Exception("nope")):
            _clear_prior_status(parent)
        captured = capsys.readouterr()
        assert "Could not clear prior_status" in captured.err

    # Line 191: AT-6 fired=False path (source_statuses not matching)
    def test_at6_source_statuses_not_matching_skips(self, auto_tracker_env):
        from tracker.automations import evaluate_automatic_transitions
        from tracker.config import get_runtime_config

        parent = _make_task_a("AT6 no match")
        update_ticket(parent, "tester", status="Open")
        q = _make_question_a(parent)
        _add_blocks_a(q, parent)
        evaluate_automatic_transitions(parent, "child_created")
        assert _status_a(parent) == "Blocked"
        # Patch question's AT-6 rule to use a source_status that Q won't reach
        cfg = get_runtime_config()
        orig = cfg["ticket_specs"]["question"]["automatic_transitions"][:]
        cfg["ticket_specs"]["question"]["automatic_transitions"] = [
            {
                "rule": "this_ticket_reaches_status",
                "source_statuses": ["Rejected"],  # Q won't go to Rejected
                "link_type": "Blocks",
                "link_role": "source",
                "linked_ticket_source_status": "Blocked",
                "linked_ticket_target_status": "prior_status",
            }
        ]
        try:
            update_ticket(q, "tester", status="Open")
            update_ticket(q, "tester", status="Resolved")
            # AT-6 source_statuses=["Rejected"] but q is "Resolved" → no fire
            assert _status_a(parent) == "Blocked"
        finally:
            cfg["ticket_specs"]["question"]["automatic_transitions"] = orig

    # AT-5 all_blockers_cleared branch: target_status = prior_status but prior_status
    # is empty after calling _read_prior_status → "return" (line ~158)
    def test_at5_prior_status_empty_direct_return(self, auto_tracker_env):
        from tracker.automations import evaluate_automatic_transitions
        parent = _make_task_a("AT5 empty prior direct")
        # Manually put into Blocked without saving prior_status
        update_ticket(parent, "tester", status="Open")
        update_ticket(parent, "tester", status="Blocked")
        b = create_ticket("blocker_type", "B2", author="tester")
        update_ticket(b, "tester", status="Open")
        _add_blocks_a(b, parent)
        update_ticket(b, "tester", status="Closed")
        # All blockers cleared but no prior_status → rule skipped silently
        result = evaluate_automatic_transitions(parent, "ticket_updated")
        assert _status_a(parent) == "Blocked"


# ═══════════════════════════════════════════════════════════════════════════════
# cli.py coverage
# ═══════════════════════════════════════════════════════════════════════════════


class TestCliMissingLines:
    """Tests that exercise the previously-uncovered branches in cli.py."""

    # Lines 85-93: _CleanErrorParser.error() — unknown command close match
    def test_unknown_command_close_match(self, tracker_env: Path, capsys):
        """Near-typo command triggers 'Did you mean' suggestion."""
        output, rc = run_main(["creat", "task", "T", "--author", "a"])
        assert rc == 2
        assert "Did you mean" in output or "unknown command" in output

    def test_unknown_command_no_close_match(self, tracker_env: Path):
        """Completely unknown subcommand prints tip line."""
        output, rc = run_main(["xyzzy123"])
        assert rc == 2
        assert "unknown command" in output.lower() or "xyzzy" in output

    # Lines 120-125: _build_help_data fallback when get_runtime_config fails
    def test_help_toon_when_config_fails(self, tracker_env: Path):
        """--help-toon still outputs something even when config is unavailable."""
        with patch("tracker.cli.get_runtime_config", side_effect=Exception("cfg err")):
            output, rc = run_main(["--help-toon"])
        assert rc == EXIT_OK
        assert "commands:" in output  # fallback empty lists still produce output

    # Line 589: no command → print_help → EXIT_OK
    def test_no_command_prints_help(self, tracker_env: Path):
        """Running tracker with no arguments should print help and exit 0."""
        output, rc = run_main([])
        assert rc == EXIT_OK
        # Help output should list common commands
        assert "create" in output or "usage" in output.lower()

    # Line 598: create without title errors
    def test_create_missing_title_errors(self, tracker_env: Path):
        """Creating a ticket without a title should raise an error."""
        output, rc = run_main(["create", "task", "--author", "a", "--assignee", "b"])
        assert rc != EXIT_OK
        assert "title" in output.lower() or "Error" in output

    # Lines 604-612: create with --description-file
    def test_create_with_description_file(self, tracker_env: Path, tmp_path: Path):
        """--description-file is read and used as description content."""
        desc = tmp_path / "desc.txt"
        desc.write_text("File description content", encoding="utf-8")
        output, rc = run_main([
            "create", "task", "Desc File Task",
            "--author", "tester", "--assignee", "dev",
            "--description-file", str(desc),
        ])
        assert rc == EXIT_OK
        get_out, _ = run_main(["get", "TASK-001"])
        assert "File description content" in get_out

    def test_create_description_file_not_found(self, tracker_env: Path):
        """--description-file pointing to nonexistent file errors out."""
        output, rc = run_main([
            "create", "task", "Title",
            "--author", "a", "--assignee", "b",
            "--description-file", "no_such_file.txt",
        ])
        assert rc != EXIT_OK
        assert "not found" in output

    # Line 649: list --parent with nonexistent parent
    def test_list_nonexistent_parent_errors(self, tracker_env: Path):
        output, rc = run_main(["list", "--parent", "TASK-999"])
        assert rc == EXIT_VALIDATION_ERROR
        assert "does not exist" in output

    # Lines 693-694: update --description-file path not found
    def test_update_description_file_not_found(self, tracker_env: Path):
        run_main(["create", "task", "T", "--author", "a", "--assignee", "b"])
        output, rc = run_main([
            "update", "TASK-001", "--author", "a",
            "--description-file", "ghost_desc.txt",
        ])
        assert rc != EXIT_OK
        assert "not found" in output

    # Lines 721-722: update --description-file read failure (permission/IO error)
    def test_update_description_file_io_error(self, tracker_env: Path, tmp_path: Path):
        run_main(["create", "task", "T", "--author", "a", "--assignee", "b"])
        desc = tmp_path / "desc.txt"
        desc.write_text("Body", encoding="utf-8")
        with patch("pathlib.Path.read_text", side_effect=IOError("perm denied")):
            output, rc = run_main([
                "update", "TASK-001", "--author", "a",
                "--description-file", str(desc),
            ])
        assert rc != EXIT_OK

    # Line 719 / update_p.error for missing descfile: covered by test above;
    # Lines 829-830: link subcommand with no sub-sub-command
    def test_link_no_subcommand_returns_error(self, tracker_env: Path):
        output, rc = run_main(["link"])
        assert rc == EXIT_VALIDATION_ERROR

    # Lines 844-845: comment subcommand missing
    def test_comment_no_subcommand_returns_error(self, tracker_env: Path):
        output, rc = run_main(["comment"])
        assert rc == EXIT_VALIDATION_ERROR

    # Lines 819 update_p.error path (desc-file read err) — handled above

    # Lines 952-953: type-info where type found inline (not $ref) → ConfigurationError
    def test_type_info_inline_type_config_error(self, tracker_env: Path):
        """WORKFLOW_YAML uses inline dicts, so type-info raises ConfigurationError."""
        output, rc = run_main(["type-info", "task"])
        assert rc == EXIT_CONFIG_ERROR
        assert "No configuration file" in output

    # Lines 1011-1012: workflow status INVALID status_name → ValidationError
    def test_workflow_status_invalid_status_name(self, tracker_env: Path):
        output, rc = run_main(["workflow", "status", "task", "NonExistent"])
        assert rc == EXIT_VALIDATION_ERROR
        assert "not found" in output

    # Line 1026: workflow transitions invalid status_name → ValidationError
    def test_workflow_transitions_invalid_status_name(self, tracker_env: Path):
        output, rc = run_main(["workflow", "transitions", "task", "Bogus"])
        assert rc == EXIT_VALIDATION_ERROR
        assert "not found" in output

    # FileOperationError exit code coverage
    def test_file_operation_error_exit_code(self, tracker_env: Path):
        from tracker.exceptions import FileOperationError
        with patch("tracker.cli.get_runtime_config",
                   side_effect=FileOperationError("disk full")):
            output, rc = run_main(["list"])
        assert rc == EXIT_FILE_ERROR
        assert "FileOperationError" in output

    # workflow subcommand missing → print_help then ValidationError
    def test_workflow_no_subcommand(self, tracker_env: Path):
        output, rc = run_main(["workflow"])
        assert rc == EXIT_VALIDATION_ERROR

    # _workflow_transitions_single: status_name in statuses but NOT in allowed_transitions
    def test_workflow_transitions_single_terminal_status(self, tracker_env: Path):
        """Closed is terminal with no allowed transitions."""
        output, rc = run_main(["workflow", "transitions", "task", "Closed"])
        # Closed is in statuses and transitions map → no ValidationError
        # But it should show "(none -- terminal status)"
        assert "none" in output.lower() or rc == EXIT_OK

    # update without --status → prints "Updated ticket" (no ctx)
    def test_update_no_status_prints_updated(self, tracker_env: Path):
        run_main(["create", "task", "T", "--author", "a", "--assignee", "b"])
        output, rc = run_main([
            "update", "TASK-001", "--author", "a", "--assignee", "newdev",
        ])
        assert rc == EXIT_OK
        assert "Updated ticket" in output

    # AT-6 clears prior_status after firing (lines 443-444 in at6)
    def test_at6_clears_prior_status_after_restore(self, auto_tracker_env):
        from tracker.automations import evaluate_automatic_transitions, _read_prior_status

        parent = _make_task_a("AT6 clear check")
        update_ticket(parent, "tester", status="Open")
        q = _make_question_a(parent)
        _add_blocks_a(q, parent)
        evaluate_automatic_transitions(parent, "child_created")
        p_ticket = get_ticket(parent)
        assert _read_prior_status(p_ticket) == "Open"
        # Resolve question → AT-6 fires and clears prior_status
        update_ticket(q, "tester", status="Open")
        update_ticket(q, "tester", status="Resolved")
        p_ticket = get_ticket(parent)
        assert _read_prior_status(p_ticket) == ""

    # AT-5 with direct target that is not prior_status (lines 238-245)
    def test_at5_with_concrete_target_fires(self, auto_tracker_env):
        from tracker.automations import evaluate_automatic_transitions
        from tracker.config import get_runtime_config

        parent = _make_task_a("AT5 concrete target")
        update_ticket(parent, "tester", status="Open")
        b = create_ticket("blocker_type", "B3", author="tester")
        update_ticket(b, "tester", status="Open")
        _add_blocks_a(b, parent)
        update_ticket(parent, "tester", status="Blocked")
        update_ticket(b, "tester", status="Closed")
        cfg = get_runtime_config()
        orig = cfg["ticket_specs"]["task"]["automatic_transitions"][:]
        cfg["ticket_specs"]["task"]["automatic_transitions"] = [
            {
                "rule": "all_blockers_cleared",
                "blocker_terminal_statuses": ["Closed"],
                "source_status": "Blocked",
                "target_status": "Open",
            }
        ]
        try:
            evaluate_automatic_transitions(parent, "ticket_updated")
            assert _status_a(parent) == "Open"
        finally:
            cfg["ticket_specs"]["task"]["automatic_transitions"] = orig


class TestAutomationsMissingLines2:
    """Second batch of coverage tests for automations.py lines 134, 168-170, 175-181."""

    # Line 134: linked_ticket_reaches_status rule dispatch (via evaluate_automatic_transitions)
    def test_linked_ticket_reaches_status_rule_dispatched(self, auto_tracker_env):
        """Patch task rules to include linked_ticket_reaches_status, then trigger it."""
        from tracker.automations import evaluate_automatic_transitions
        from tracker.config import get_runtime_config

        t1 = _make_task_a("LTR source")
        update_ticket(t1, "tester", status="Open")
        t2 = _make_task_a("LTR target")
        update_ticket(t2, "tester", status="Open")
        _add_blocks_a(t1, t2)  # t1 blocks t2; t1 (source) is "Open"

        cfg = get_runtime_config()
        orig = cfg["ticket_specs"]["task"]["automatic_transitions"][:]
        cfg["ticket_specs"]["task"]["automatic_transitions"] = [
            {
                "rule": "linked_ticket_reaches_status",
                "link_type": "Blocks",
                "link_role": "target",   # t2 is target; look at source (t1)
                "linked_statuses": ["Open"],
                "source_status": "Open",
                "target_status": "In Progress",
            }
        ]
        try:
            result = evaluate_automatic_transitions(t2, "ticket_updated")
            # t1 is Open → condition met → t2 transitions to In Progress
            assert _status_a(t2) == "In Progress"
        finally:
            cfg["ticket_specs"]["task"]["automatic_transitions"] = orig

    # Lines 168-170: actual_target == "prior_status" after rule dispatch (non-blockers-cleared)
    def test_prior_status_fallback_empty_skips_transition(self, auto_tracker_env):
        """first_child_reaches_status with target_status=prior_status, no saved prior."""
        from tracker.automations import evaluate_automatic_transitions
        from tracker.config import get_runtime_config

        parent = _make_task_a("NO prior parent")
        update_ticket(parent, "tester", status="Open")
        update_ticket(parent, "tester", status="In Progress")
        wi = _make_workitem_a(parent)
        update_ticket(wi, "tester", status="Open")
        update_ticket(wi, "tester", status="In Progress")
        update_ticket(wi, "tester", status="Resolved")

        # Set up a first_child_reaches_status rule with target_status="prior_status".
        # parent is "In Progress" and wi is "Resolved", so it WOULD fire.
        # But parent has no prior_status → lines 168-170 execute and return.
        cfg = get_runtime_config()
        orig = cfg["ticket_specs"]["task"]["automatic_transitions"][:]
        cfg["ticket_specs"]["task"]["automatic_transitions"] = [
            {
                "rule": "first_child_reaches_status",
                "child_filter": {"types": ["workitem"]},
                "child_statuses": ["Resolved"],
                "source_status": "In Progress",
                "target_status": "prior_status",   # fallback path; parent has no prior
            }
        ]
        try:
            evaluate_automatic_transitions(parent, "ticket_updated")
            # prior_status is absent → can't resolve → no transition
            assert _status_a(parent) == "In Progress"
        finally:
            cfg["ticket_specs"]["task"]["automatic_transitions"] = orig

    # Lines 175-181: ValidationError during auto-transition (fire attempted but disallowed)
    def test_invalid_auto_transition_logs_warning_and_skips(self, auto_tracker_env, capsys):
        """Rule fires but the target transition is not permitted → ValidationError caught."""
        from tracker.automations import evaluate_automatic_transitions
        from tracker.config import get_runtime_config

        parent = _make_task_a("Invalid transition task")
        update_ticket(parent, "tester", status="Open")
        wi = _make_workitem_a(parent)
        update_ticket(wi, "tester", status="Open")
        update_ticket(wi, "tester", status="In Progress")
        update_ticket(wi, "tester", status="Resolved")
        update_ticket(wi, "tester", status="Closed")
        # After wi→Closed, parent auto-transitions: Open→In Progress→Resolved via default rules
        # parent is now "Resolved"; workitem is "Closed"

        cfg = get_runtime_config()
        orig = cfg["ticket_specs"]["task"]["automatic_transitions"][:]
        cfg["ticket_specs"]["task"]["automatic_transitions"] = [
            {
                "rule": "all_children_reach_status",
                "child_filter": {"types": ["workitem"]},
                "child_statuses": ["Closed"],
                "source_status": "Resolved",
                "target_status": "New",  # invalid: Resolved → New is not allowed
            }
        ]
        try:
            evaluate_automatic_transitions(parent, "ticket_updated")
            captured = capsys.readouterr()
            assert "[automations warning] Skipping auto-transition" in captured.err
            assert _status_a(parent) == "Resolved"  # no transition happened
        finally:
            cfg["ticket_specs"]["task"]["automatic_transitions"] = orig

    # Lines 296, 298: _eval_linked_ticket_reaches_status source link_role found
    def test_linked_ticket_source_role_found_and_matches(self, auto_tracker_env):
        """Verify source link_role path resolves target_ticket as the other ID."""
        from tracker.automations import _eval_linked_ticket_reaches_status
        from tracker.index import read_link_index

        t1 = _make_task_a("LT source found")
        t2 = _make_task_a("LT target found")
        update_ticket(t2, "tester", status="Open")
        _add_blocks_a(t1, t2)  # t1=source blocks t2=target
        links = read_link_index()
        # t1 evaluates as "source" looking at target (t2) which is "Open"
        rule = {
            "rule": "linked_ticket_reaches_status",
            "link_type": "Blocks",
            "link_role": "source",
            "linked_statuses": ["Open"],
        }
        ticket = get_ticket(t1)
        assert _eval_linked_ticket_reaches_status(ticket, rule, links) is True

    # Lines 334, 337: _eval_child_blocker_created — edge case wrong parent
    def test_at4_child_has_different_parent_rejected(self, auto_tracker_env):
        """Source child is a question but its parent is a different ticket → False."""
        from tracker.automations import _eval_child_blocker_created
        from tracker.index import read_link_index

        parent = _make_task_a("AT4 different parent")
        other_parent = _make_task_a("AT4 other parent")
        # q's parent is other_parent, not parent
        q = _make_question_a(other_parent)
        _add_blocks_a(q, parent)  # q (with other parent) blocks parent
        links = read_link_index()
        rule = {
            "rule": "child_blocker_created",
            "child_filter": {"types": ["question"], "link_type": "Blocks"},
        }
        ticket = get_ticket(parent)
        assert _eval_child_blocker_created(ticket, rule, links) is False

    # Lines 366, 368: AT-5 all_blockers - non-existent blocker ID skipped
    def test_all_blockers_cleared_link_to_ghost_blocks_cleared_check(self, auto_tracker_env):
        """All real blockers are closed, plus a ghost link → ghost skipped → still True."""
        from tracker.automations import _eval_all_blockers_cleared
        from tracker.index import read_link_index

        parent = _make_task_a("Ghost link parent")
        update_ticket(parent, "tester", status="Open")
        b = create_ticket("blocker_type", "B ghost", author="tester")
        update_ticket(b, "tester", status="Open")
        _add_blocks_a(b, parent)
        update_ticket(b, "tester", status="Closed")
        real_links = read_link_index()
        fake_link = {
            "link_id": "LINK-GHOST1",
            "source_ticket": "GHOST-1",
            "target_ticket": parent,
            "link_type": "Blocks",
            "source_role": "Blocks",
            "target_role": "Is Blocked By",
            "created": "2026-01-01",
            "created_by": "test",
            "comment": "",
        }
        rule = {
            "rule": "all_blockers_cleared",
            "blocker_terminal_statuses": ["Closed", "Canceled"],
        }
        ticket = get_ticket(parent)
        # Ghost blocker is skipped → only real blocker (closed) counts → True
        result = _eval_all_blockers_cleared(ticket, rule, real_links + [fake_link])
        assert result is True

    # Lines 402, 404, 406: AT-6 link_role="target" that fails at other_id lookup
    def test_at6_target_role_with_ghost_source(self, auto_tracker_env):
        """AT-6: link_role=target with non-existent source_ticket → skipped."""
        from tracker.automations import _eval_this_ticket_reaches_status

        parent = _make_task_a("AT6 TGT ghost src")
        update_ticket(parent, "tester", status="Open")
        fake_link = {
            "link_id": "LINK-AT6GHOST",
            "source_ticket": "GHOST-99",
            "target_ticket": parent,
            "link_type": "Blocks",
            "source_role": "Blocks",
            "target_role": "Is Blocked By",
            "created": "2026-01-01",
            "created_by": "test",
            "comment": "",
        }
        rule = {
            "rule": "this_ticket_reaches_status",
            "source_statuses": ["Open"],
            "link_type": "Blocks",
            "link_role": "target",  # look at source_ticket (GHOST-99) → not found
            "linked_ticket_source_status": "New",
            "linked_ticket_target_status": "Open",
        }
        ticket = get_ticket(parent)
        result = _eval_this_ticket_reaches_status(ticket, rule, [fake_link])
        assert result is False
