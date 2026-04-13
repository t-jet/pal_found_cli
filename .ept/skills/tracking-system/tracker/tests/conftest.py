"""Shared pytest fixtures for the tracker test suite."""

from __future__ import annotations

import csv
import io
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from tracker.config import TrackerPaths, invalidate_config, reset, set_paths
from tracker.constants import INDEX_FIELDNAMES, LINK_INDEX_FIELDNAMES

# ── Scaffold YAML (matches original test_tracker_cli.py) ────────────────────

WORKFLOW_YAML: str = """\
fields:
  - name: id
    type: string
  - name: type
    type: enum
    values: [task, workitem, question]
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
  - type: task
    required_fields: [id, type, title, status, priority, assignee, reporter, created, updated]
    optional_fields: [parent, addressed_to]
    statuses:
      New: Created
      Open: Open
      In Progress: In progress
      Resolved: Resolved
      Closed: Closed
  - type: workitem
    required_fields: [id, type, title, status, parent, created, updated]
    optional_fields: [priority, assignee, reporter]
    statuses:
      New: Created
      Open: Open
      In Progress: In progress
      Resolved: Resolved
      Closed: Closed
  - type: question
    required_fields: [id, type, title, status, parent, addressed_to, created, updated]
    optional_fields: [priority, assignee, reporter]
    statuses:
      New: Created
      Open: Open
      In Progress: In progress
      Resolved: Resolved
      Closed: Closed

link_types:
  - type: Blocks
    source_role: Blocks
    target_role: Is Blocked By
  - type: RelatesTo
    source_role: Relates To
    target_role: Relates To
  - type: ParentChild
    source_role: Is Parent Of
    target_role: Is Child Of

type_registry:
  task:     { id_prefix: TASK,     content_file: ticket.md, initial_status: New }
  workitem: { id_prefix: WORK,     content_file: ticket.md, initial_status: New }
  question: { id_prefix: QUESTION, content_file: ticket.md, initial_status: New }
"""

COUNTERS_YAML: str = """\
counters:
  task: 0
  workitem: 0
  question: 0
  link: 0
padding:
  ticket: 3
  link: 5
"""

RICH_WORKFLOW_YAML: str = """\
fields:
  - name: id
    type: string
  - name: type
    type: enum
    values: [task]
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
  - type: task
    required_fields: [id, type, title, status, priority, assignee, reporter, created, updated]
    optional_fields: [parent, addressed_to]
    terminal_statuses: [Closed]
    statuses:
      New:
        description: "Ticket just created."
        stage_goal: "Prepare ticket."
        responsible_roles: [Architect]
      Open:
        description: "In progress."
        stage_goal: "Do the work."
        responsible_roles: [Developer]
      Closed:
        description: "Done."
        stage_goal: ""
        responsible_roles: []
    allowed_transitions:
      New: [Open]
      Open: [Closed]
      Closed: []

link_types:
  - type: Blocks
    source_role: Blocks
    target_role: Is Blocked By

type_registry:
  task: { id_prefix: TASK, content_file: ticket.md, initial_status: New }
"""


# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture()
def tracker_env(tmp_path: Path) -> Path:
    """Create a minimal tracker environment and configure the package paths."""
    tracker = tmp_path / ".ept" / "tracker"
    tracker.mkdir(parents=True)
    config = tracker / ".config"
    config.mkdir()

    (config / ".workflow.yaml").write_text(WORKFLOW_YAML, encoding="utf-8")
    (config / ".id-counters.yaml").write_text(COUNTERS_YAML, encoding="utf-8")

    with (config / ".index.csv").open("w", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=INDEX_FIELDNAMES).writeheader()

    with (config / ".link-index.csv").open("w", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=LINK_INDEX_FIELDNAMES).writeheader()

    set_paths(TrackerPaths(tracker_root=tracker))
    yield tmp_path
    reset()


@pytest.fixture()
def rich_tracker_env(tmp_path: Path) -> Path:
    """Tracker environment with rich dict-style statuses and transitions."""
    tracker = tmp_path / ".ept" / "tracker"
    tracker.mkdir(parents=True)
    config = tracker / ".config"
    config.mkdir()

    (config / ".workflow.yaml").write_text(RICH_WORKFLOW_YAML, encoding="utf-8")
    (config / ".id-counters.yaml").write_text(
        "counters:\n  task: 0\n  link: 0\npadding:\n  ticket: 3\n  link: 5\n",
        encoding="utf-8",
    )

    with (config / ".index.csv").open("w", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=INDEX_FIELDNAMES).writeheader()

    with (config / ".link-index.csv").open("w", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=LINK_INDEX_FIELDNAMES).writeheader()

    set_paths(TrackerPaths(tracker_root=tracker))
    yield tmp_path
    reset()


# ── Helpers ──────────────────────────────────────────────────────────────────


def make_task(
    title: str = "Test Task",
    priority: str = "Medium",
    assignee: str = "dev",
) -> str:
    """Create a task ticket.  Requires an active ``tracker_env``."""
    from tracker.tickets import create_ticket

    return create_ticket(
        "task", title, author="architect",
        priority=priority, assignee=assignee,
    )


def make_workitem(parent_id: str, title: str = "Work Item") -> str:
    """Create a workitem under *parent_id*.  Requires an active ``tracker_env``."""
    from tracker.tickets import create_ticket

    return create_ticket("workitem", title, author="architect", parent=parent_id)


def run_main(args: list[str]) -> tuple[str, int]:
    """Execute ``tracker.cli.main()`` with patched ``sys.argv``.

    Returns ``(combined_output, exit_code)``.
    """
    from tracker.cli import main

    out = io.StringIO()
    err = io.StringIO()
    rc = 0
    with patch("sys.argv", ["tracker_cli.py", *args]):
        try:
            with redirect_stdout(out), redirect_stderr(err):
                result = main()
                if result is not None:
                    rc = result
        except SystemExit as exc:
            rc = exc.code if exc.code is not None else 0
    return out.getvalue() + err.getvalue(), rc
