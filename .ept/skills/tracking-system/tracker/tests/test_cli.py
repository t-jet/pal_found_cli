"""CLI integration tests — exercises ``tracker.cli.main()`` with patched sys.argv."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from tests.conftest import make_task, make_workitem, run_main
from tracker.config import get_paths, invalidate_config
from tracker.constants import EXIT_CONFIG_ERROR, EXIT_OK, EXIT_VALIDATION_ERROR


# ── Create ───────────────────────────────────────────────────────────────────


class TestMainCreate:
    def test_create_task(self, tracker_env: Path) -> None:
        output, rc = run_main([
            "create", "task", "My new task",
            "--author", "architect",
            "--assignee", "dev",
            "--priority", "High",
        ])
        assert rc == EXIT_OK
        assert "TASK-001" in output

    def test_create_task_keyword_title(self, tracker_env: Path) -> None:
        output, rc = run_main([
            "create", "task",
            "--title", "Keyword title",
            "--author", "architect",
            "--assignee", "dev",
        ])
        assert rc == EXIT_OK
        assert "TASK-001" in output

    def test_create_invalid_type(self, tracker_env: Path) -> None:
        output, rc = run_main([
            "create", "bogus", "Title",
            "--author", "architect",
            "--assignee", "dev",
        ])
        assert rc == EXIT_VALIDATION_ERROR
        assert "Invalid ticket type" in output

    def test_create_child_ticket(self, tracker_env: Path) -> None:
        run_main([
            "create", "task", "Parent",
            "--author", "architect", "--assignee", "dev",
        ])
        output, rc = run_main([
            "create", "workitem", "Child",
            "--author", "architect", "--parent", "TASK-001",
        ])
        assert rc == EXIT_OK
        assert "WORK-001" in output


# ── Get ──────────────────────────────────────────────────────────────────────


class TestMainGet:
    def test_get_returns_content(self, tracker_env: Path) -> None:
        run_main([
            "create", "task", "Content ticket",
            "--author", "arch", "--assignee", "dev",
        ])
        output, rc = run_main(["get", "TASK-001"])
        assert rc == EXIT_OK
        assert "TASK-001" in output
        assert "Content ticket" in output

    def test_get_missing_ticket(self, tracker_env: Path) -> None:
        output, rc = run_main(["get", "FAKE-999"])
        assert rc == EXIT_VALIDATION_ERROR
        assert "not found" in output


# ── List ─────────────────────────────────────────────────────────────────────


class TestMainList:
    def test_list_all(self, tracker_env: Path) -> None:
        run_main(["create", "task", "A", "--author", "a", "--assignee", "b"])
        run_main(["create", "task", "B", "--author", "a", "--assignee", "b"])
        output, rc = run_main(["list"])
        assert rc == EXIT_OK
        assert "2 ticket(s)" in output

    def test_list_filter_status(self, tracker_env: Path) -> None:
        run_main(["create", "task", "A", "--author", "a", "--assignee", "b"])
        output, rc = run_main(["list", "--status", "New"])
        assert rc == EXIT_OK
        assert "1 ticket(s)" in output

    def test_invalid_status_filter(self, tracker_env: Path) -> None:
        output, rc = run_main(["list", "--status", "Bogus"])
        assert rc == EXIT_VALIDATION_ERROR
        assert "Invalid status" in output

    def test_invalid_priority_filter(self, tracker_env: Path) -> None:
        output, rc = run_main(["list", "--priority", "Bogus"])
        assert rc == EXIT_VALIDATION_ERROR
        assert "Invalid priority" in output


# ── Update ───────────────────────────────────────────────────────────────────


class TestMainUpdate:
    def test_update_status(self, tracker_env: Path) -> None:
        run_main(["create", "task", "U", "--author", "a", "--assignee", "b"])
        output, rc = run_main([
            "update", "TASK-001", "--author", "a", "--status", "Open",
        ])
        assert rc == EXIT_OK

    def test_update_nonexistent(self, tracker_env: Path) -> None:
        output, rc = run_main([
            "update", "FAKE-999", "--author", "a", "--status", "Open",
        ])
        assert rc == EXIT_VALIDATION_ERROR
        assert "not found" in output


# ── Link ─────────────────────────────────────────────────────────────────────


class TestMainLink:
    def _setup_two_tickets(self) -> None:
        run_main(["create", "task", "A", "--author", "a", "--assignee", "b"])
        run_main(["create", "task", "B", "--author", "a", "--assignee", "b"])

    def test_link_create(self, tracker_env: Path) -> None:
        self._setup_two_tickets()
        output, rc = run_main([
            "link", "create", "TASK-001", "TASK-002", "Blocks",
            "--author", "a",
        ])
        assert rc == EXIT_OK
        assert "LINK-" in output

    def test_link_list(self, tracker_env: Path) -> None:
        self._setup_two_tickets()
        run_main([
            "link", "create", "TASK-001", "TASK-002", "Blocks", "--author", "a",
        ])
        output, rc = run_main(["link", "list", "TASK-001"])
        assert rc == EXIT_OK
        assert "1 link(s)" in output

    def test_link_remove(self, tracker_env: Path) -> None:
        self._setup_two_tickets()
        run_main([
            "link", "create", "TASK-001", "TASK-002", "Blocks", "--author", "a",
        ])
        output, rc = run_main(["link", "remove", "LINK-00001", "--author", "a"])
        assert rc == EXIT_OK
        assert "Removed" in output

    def test_link_invalid_type(self, tracker_env: Path) -> None:
        self._setup_two_tickets()
        output, rc = run_main([
            "link", "create", "TASK-001", "TASK-002", "Bogus",
            "--author", "a",
        ])
        assert rc == EXIT_VALIDATION_ERROR
        assert "Invalid link type" in output

    def test_link_direction_validation(self, tracker_env: Path) -> None:
        self._setup_two_tickets()
        run_main([
            "link", "create", "TASK-001", "TASK-002", "Blocks", "--author", "a",
        ])
        output, rc = run_main([
            "link", "list", "TASK-001", "--direction", "out",
        ])
        assert rc == EXIT_OK
        assert "1 link(s)" in output

        output, rc = run_main([
            "link", "list", "TASK-001", "--direction", "in",
        ])
        assert rc == EXIT_OK
        assert "0 link(s)" in output


# ── Comment ──────────────────────────────────────────────────────────────────


class TestMainComment:
    def test_comment_create(self, tracker_env: Path) -> None:
        run_main(["create", "task", "C", "--author", "a", "--assignee", "b"])
        output, rc = run_main([
            "comment", "create", "TASK-001",
            "--author", "a", "--subject", "Note", "--text", "Body",
        ])
        assert rc == EXIT_OK
        assert "Created comment" in output

    def test_comment_list(self, tracker_env: Path) -> None:
        run_main(["create", "task", "C", "--author", "a", "--assignee", "b"])
        run_main([
            "comment", "create", "TASK-001",
            "--author", "dev", "--subject", "Note", "--text", "Body",
        ])
        output, rc = run_main(["comment", "list", "TASK-001"])
        assert rc == EXIT_OK
        assert "comment(s)" in output

    def test_comment_get(self, tracker_env: Path) -> None:
        run_main(["create", "task", "C", "--author", "a", "--assignee", "b"])
        out1, _ = run_main([
            "comment", "create", "TASK-001",
            "--author", "a", "--subject", "Hello", "--text", "World",
        ])
        # Parse comment ID from "Created comment: <id>"
        cid = out1.strip().split(":")[-1].strip()
        output, rc = run_main(["comment", "get", "TASK-001", cid])
        assert rc == EXIT_OK
        assert "Hello" in output

    def test_comment_update(self, tracker_env: Path) -> None:
        run_main(["create", "task", "C", "--author", "a", "--assignee", "b"])
        out1, _ = run_main([
            "comment", "create", "TASK-001",
            "--author", "a", "--subject", "Old", "--text", "Old body",
        ])
        cid = out1.strip().split(":")[-1].strip()
        output, rc = run_main([
            "comment", "update", "TASK-001", cid,
            "--author", "a", "--subject", "New",
        ])
        assert rc == EXIT_OK
        assert "Updated comment" in output

    def test_comment_update_no_fields_error(self, tracker_env: Path) -> None:
        run_main(["create", "task", "C", "--author", "a", "--assignee", "b"])
        out1, _ = run_main([
            "comment", "create", "TASK-001",
            "--author", "a", "--subject", "S", "--text", "T",
        ])
        cid = out1.strip().split(":")[-1].strip()
        output, rc = run_main([
            "comment", "update", "TASK-001", cid, "--author", "a",
        ])
        assert rc == EXIT_VALIDATION_ERROR
        assert "Nothing to update" in output

    def test_comment_missing_subcommand(self, tracker_env: Path) -> None:
        run_main(["create", "task", "C", "--author", "a", "--assignee", "b"])
        output, rc = run_main(["comment"])
        assert rc == EXIT_VALIDATION_ERROR


# ── Search ───────────────────────────────────────────────────────────────────


class TestMainSearch:
    def test_search_title(self, tracker_env: Path) -> None:
        run_main([
            "create", "task", "Unique needle",
            "--author", "a", "--assignee", "b",
        ])
        output, rc = run_main(["search", "needle"])
        assert rc == EXIT_OK
        assert "1 ticket(s)" in output

    def test_search_content(self, tracker_env: Path) -> None:
        run_main([
            "create", "task", "Content search",
            "--author", "a", "--assignee", "b",
            "--description", "magic_keyword_42",
        ])
        output, rc = run_main([
            "search", "magic_keyword_42", "--in-content",
        ])
        assert rc == EXIT_OK
        assert "1 ticket(s)" in output


# ── Workflow ─────────────────────────────────────────────────────────────────


class TestMainWorkflow:
    def test_workflow_types(self, tracker_env: Path) -> None:
        output, rc = run_main(["workflow", "types"])
        assert rc == EXIT_OK
        assert "task" in output

    def test_workflow_status_all(self, tracker_env: Path) -> None:
        output, rc = run_main(["workflow", "status"])
        assert rc == EXIT_OK
        assert "task" in output

    def test_workflow_status_single_type(self, rich_tracker_env: Path) -> None:
        output, rc = run_main(["workflow", "status", "task"])
        assert rc == EXIT_OK
        assert "New" in output
        assert "Closed" in output

    def test_workflow_status_single_name(self, rich_tracker_env: Path) -> None:
        output, rc = run_main(["workflow", "status", "task", "New"])
        assert rc == EXIT_OK
        assert "Ticket just created" in output

    def test_workflow_transitions_all(self, rich_tracker_env: Path) -> None:
        output, rc = run_main(["workflow", "transitions", "task"])
        assert rc == EXIT_OK
        assert "New" in output

    def test_workflow_transitions_single(self, rich_tracker_env: Path) -> None:
        output, rc = run_main(["workflow", "transitions", "task", "New"])
        assert rc == EXIT_OK
        assert "Open" in output


# ── Help-toon ────────────────────────────────────────────────────────────────


class TestHelpToon:
    def test_help_toon_output(self, tracker_env: Path) -> None:
        output, rc = run_main(["--help-toon"])
        assert rc == EXIT_OK
        assert "commands:" in output


# ── Error handling / BUG regressions ─────────────────────────────────────────


class TestErrorHandling:
    def test_unexpected_error_no_stacktrace(self, tracker_env: Path) -> None:
        with patch(
            "tracker.cli.get_runtime_config",
            side_effect=RuntimeError("simulated"),
        ):
            output, rc = run_main(["list"])
        assert rc == 5
        assert "Traceback" not in output
        assert "UnexpectedError" in output

    def test_config_error_exit_code(self, tracker_env: Path) -> None:
        paths = get_paths()
        paths.workflow_file.unlink()
        invalidate_config()
        output, rc = run_main(["list"])
        assert rc == EXIT_CONFIG_ERROR
        assert "ConfigurationError" in output


class TestBugRegressions:
    def test_bug001_module_docstring_author_optional(self) -> None:
        """BUG-001/D3: module docstring should show [--author AUTHOR]."""
        import tracker.cli
        doc = tracker.cli.__doc__ or ""
        assert "[--author AUTHOR]" in doc

    def test_bug003_clean_error_no_usage_dump(self, tracker_env: Path) -> None:
        """BUG-003: argparse errors should not dump full usage block."""
        output, rc = run_main(["comment"])
        assert rc == EXIT_VALIDATION_ERROR
        # Should NOT contain the full argparse usage block
        lines = output.strip().splitlines()
        # The output should be reasonably short (no usage dump)
        assert len(lines) < 50

    def test_bug003_ascii_arrow_in_transition_error(
        self, rich_tracker_env: Path,
    ) -> None:
        """BUG-003: transition errors must use ASCII ``->``."""
        run_main([
            "create", "task", "Transition",
            "--author", "a", "--assignee", "b",
        ])
        output, rc = run_main([
            "update", "TASK-001", "--author", "a", "--status", "Closed",
        ])
        assert rc == EXIT_VALIDATION_ERROR
        assert "->" in output
        assert "\u2192" not in output

    def test_field_validation_errors(self, tracker_env: Path) -> None:
        """Unknown --field names must produce a clear validation error."""
        output, rc = run_main([
            "create", "task", "F",
            "--author", "a", "--assignee", "b",
            "--field", "nonexistent=value",
        ])
        assert rc == EXIT_VALIDATION_ERROR
        assert "Unknown field" in output
