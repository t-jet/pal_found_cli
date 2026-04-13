"""CLI integration tests — exercises ``tracker.cli.main()`` with patched sys.argv."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Generator
from unittest.mock import patch

import pytest

from tests.conftest import make_task, make_workitem, run_main
from tracker.config import TrackerPaths, get_paths, invalidate_config, reset, set_paths
from tracker.constants import (
    EXIT_CONFIG_ERROR,
    EXIT_OK,
    EXIT_VALIDATION_ERROR,
    INDEX_FIELDNAMES,
    LINK_INDEX_FIELDNAMES,
)


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


# ── Type-info ─────────────────────────────────────────────────────────────────

# Workflow YAML that uses $ref-style ticket-type entries.
_REF_WORKFLOW_YAML = """\
fields:
  - name: id
    type: string
  - name: type
    type: enum
    values: [task, workitem]
  - name: title
    type: string
  - name: status
    type: string
  - name: priority
    type: enum
    values: [Low, Medium, High, Critical]
  - name: assignee
    type: string
  - name: reporter
    type: string
  - name: parent
    type: string
  - name: addressed_to
    type: string
  - name: created
    type: date
  - name: updated
    type: date

ticket_types:
  - $ref: tickets/task.yaml
  - $ref: tickets/workitem.yaml

link_types:
  - type: Blocks
    source_role: Blocks
    target_role: Is Blocked By

type_registry:
  task:     { id_prefix: TASK, content_file: ticket.md, initial_status: New }
  workitem: { id_prefix: WORK, content_file: ticket.md, initial_status: New }
"""

_TASK_TYPE_YAML = """\
type: task
id_prefix: TASK
description: A basic task ticket used in tests.
required_fields: [id, type, title, status, created, updated]
optional_fields: [priority, assignee]
initial_status: New
terminal_statuses: [Closed]
statuses:
  New:
    description: "Just created."
    stage_goal: "Capture the task."
    responsible_roles: [Developer]
  Closed:
    description: "Done."
    stage_goal: "Archive."
    responsible_roles: []
allowed_transitions:
  New: [Closed]
  Closed: []
"""

_WORKITEM_TYPE_YAML = """\
type: workitem
id_prefix: WORK
description: A child work item.
required_fields: [id, type, title, status, created, updated]
optional_fields: [parent]
initial_status: New
terminal_statuses: [Closed]
statuses:
  New:
    description: "Created."
    stage_goal: "Start work."
    responsible_roles: [Developer]
  Closed:
    description: "Done."
    stage_goal: "Archive."
    responsible_roles: []
allowed_transitions:
  New: [Closed]
  Closed: []
"""


class TestTypeInfo:
    """Tests for the ``type-info`` command."""

    @pytest.fixture()
    def ref_tracker_env(self, tmp_path: Path) -> Generator[Path, None, None]:
        """Tracker env where ticket types are defined via ``$ref`` YAML files."""
        tracker = tmp_path / ".ept" / "tracker"
        tracker.mkdir(parents=True)
        config = tracker / ".config"
        config.mkdir()
        tickets_dir = config / "tickets"
        tickets_dir.mkdir()

        (config / ".workflow.yaml").write_text(_REF_WORKFLOW_YAML, encoding="utf-8")
        (config / ".id-counters.yaml").write_text(
            "counters:\n  task: 0\n  workitem: 0\n  link: 0\n"
            "padding:\n  ticket: 3\n  link: 5\n",
            encoding="utf-8",
        )
        (tickets_dir / "task.yaml").write_text(_TASK_TYPE_YAML, encoding="utf-8")
        (tickets_dir / "workitem.yaml").write_text(_WORKITEM_TYPE_YAML, encoding="utf-8")

        with (config / ".index.csv").open("w", encoding="utf-8", newline="") as f:
            csv.DictWriter(f, fieldnames=INDEX_FIELDNAMES).writeheader()
        with (config / ".link-index.csv").open("w", encoding="utf-8", newline="") as f:
            csv.DictWriter(f, fieldnames=LINK_INDEX_FIELDNAMES).writeheader()

        set_paths(TrackerPaths(tracker_root=tracker))
        yield tmp_path
        reset()

    # ── Happy-path ────────────────────────────────────────────────────────────

    def test_returns_raw_yaml_content(self, ref_tracker_env: Path) -> None:
        """type-info should print the raw content of the ticket-type YAML file."""
        output, rc = run_main(["type-info", "task"])
        assert rc == EXIT_OK
        assert "type: task" in output

    def test_content_includes_expected_fields(self, ref_tracker_env: Path) -> None:
        """Output should contain key fields written to the type YAML file."""
        output, rc = run_main(["type-info", "task"])
        assert rc == EXIT_OK
        assert "id_prefix: TASK" in output
        assert "terminal_statuses" in output
        assert "allowed_transitions" in output
        assert "A basic task ticket used in tests." in output

    def test_second_type_returns_its_own_content(self, ref_tracker_env: Path) -> None:
        """Requesting a different type returns that type's file, not the first."""
        output, rc = run_main(["type-info", "workitem"])
        assert rc == EXIT_OK
        assert "type: workitem" in output
        assert "id_prefix: WORK" in output
        assert "A child work item." in output

    def test_types_do_not_bleed_into_each_other(self, ref_tracker_env: Path) -> None:
        """Output for 'task' must not contain workitem-specific content."""
        output_task, _ = run_main(["type-info", "task"])
        output_work, _ = run_main(["type-info", "workitem"])
        assert "A child work item." not in output_task
        assert "A basic task ticket used in tests." not in output_work

    def test_output_contains_statuses_block(self, ref_tracker_env: Path) -> None:
        """The raw YAML output should include the statuses mapping."""
        output, rc = run_main(["type-info", "task"])
        assert rc == EXIT_OK
        assert "statuses:" in output
        assert "New:" in output
        assert "Closed:" in output

    # ── Error-path ────────────────────────────────────────────────────────────

    def test_invalid_type_exits_validation_error(self, ref_tracker_env: Path) -> None:
        """An unrecognised ticket type should exit with EXIT_VALIDATION_ERROR."""
        output, rc = run_main(["type-info", "bogus"])
        assert rc == EXIT_VALIDATION_ERROR
        assert "Invalid ticket type" in output

    def test_inline_type_definition_exits_config_error(self, tracker_env: Path) -> None:
        """When ticket_types use inline dicts (no $ref), ConfigurationError is raised."""
        output, rc = run_main(["type-info", "task"])
        assert rc == EXIT_CONFIG_ERROR
        assert "No configuration file found" in output

    # ── Help visibility ───────────────────────────────────────────────────────

    def test_command_appears_in_help(self, ref_tracker_env: Path) -> None:
        """``type-info`` must be listed in the standard ``--help`` output."""
        output, rc = run_main(["--help"])
        assert rc == EXIT_OK
        assert "type-info" in output

    def test_command_appears_in_help_toon(self, ref_tracker_env: Path) -> None:
        """``type-info`` must appear in the TOON-format help output."""
        output, rc = run_main(["--help-toon"])
        assert rc == EXIT_OK
        assert "type-info" in output

    def test_subcommand_help_describes_argument(self, ref_tracker_env: Path) -> None:
        """``type-info --help`` should describe the ticket_type positional arg."""
        output, rc = run_main(["type-info", "--help"])
        assert rc == EXIT_OK
        assert "ticket_type" in output


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
