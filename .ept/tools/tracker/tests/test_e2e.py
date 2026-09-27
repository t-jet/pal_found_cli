"""E2E subprocess tests — run ``tracker_cli.py`` as a child process."""

from __future__ import annotations

import csv
import subprocess
import sys
import time
from pathlib import Path

import pytest

from tests.conftest import (
    COUNTERS_YAML,
    INDEX_FIELDNAMES,
    LINK_INDEX_FIELDNAMES,
    WORKFLOW_YAML,
)

CLI_PATH = Path(__file__).resolve().parent.parent / "tracker_cli.py"


def _run(
    *args: str,
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    """Run ``tracker_cli.py`` in *cwd* and return the completed process."""
    return subprocess.run(
        [sys.executable, str(CLI_PATH), *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )


@pytest.fixture()
def e2e_env(tmp_path: Path) -> Path:
    """Create a tracker scaffold for subprocess tests."""
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
    return tmp_path


# ── Basic smoke tests ────────────────────────────────────────────────────────


class TestE2E:
    def test_help_runs(self, e2e_env: Path) -> None:
        r = _run("--help", cwd=e2e_env)
        assert r.returncode == 0
        assert "Tracking System CLI" in r.stdout

    def test_create_and_get(self, e2e_env: Path) -> None:
        r = _run(
            "create", "task", "E2E ticket",
            "--author", "architect", "--assignee", "dev",
            cwd=e2e_env,
        )
        assert r.returncode == 0
        assert "TASK-001" in r.stdout

        r2 = _run("get", "TASK-001", cwd=e2e_env)
        assert r2.returncode == 0
        assert "TASK-001" in r2.stdout

    def test_invalid_type_clear_error(self, e2e_env: Path) -> None:
        r = _run(
            "create", "bogus", "Title",
            "--author", "a", "--assignee", "b",
            cwd=e2e_env,
        )
        assert r.returncode == 2
        assert "Invalid ticket type" in r.stdout

    def test_create_child_ticket(self, e2e_env: Path) -> None:
        _run(
            "create", "task", "Parent",
            "--author", "a", "--assignee", "b",
            cwd=e2e_env,
        )
        r = _run(
            "create", "workitem", "Child",
            "--author", "a", "--parent", "TASK-001",
            cwd=e2e_env,
        )
        assert r.returncode == 0
        assert "WORK-001" in r.stdout

    def test_parent_validation_error(self, e2e_env: Path) -> None:
        r = _run(
            "create", "workitem", "Child",
            "--author", "a", "--parent", "FAKE-999",
            cwd=e2e_env,
        )
        assert r.returncode == 2
        assert "does not exist" in r.stdout

    def test_comment_lifecycle(self, e2e_env: Path) -> None:
        _run(
            "create", "task", "C",
            "--author", "a", "--assignee", "b",
            cwd=e2e_env,
        )
        time.sleep(0.01)
        r = _run(
            "comment", "create", "TASK-001",
            "--author", "a", "--subject", "Hello", "--text", "World",
            cwd=e2e_env,
        )
        assert r.returncode == 0
        assert "Created comment" in r.stdout

        r2 = _run("comment", "list", "TASK-001", cwd=e2e_env)
        assert r2.returncode == 0
        assert "comment(s)" in r2.stdout

    def test_link_lifecycle(self, e2e_env: Path) -> None:
        _run("create", "task", "A", "--author", "a", "--assignee", "b", cwd=e2e_env)
        _run("create", "task", "B", "--author", "a", "--assignee", "b", cwd=e2e_env)
        r = _run(
            "link", "create", "TASK-001", "TASK-002", "Blocks",
            "--author", "a", cwd=e2e_env,
        )
        assert r.returncode == 0
        assert "LINK-" in r.stdout

        r2 = _run("link", "list", "TASK-001", cwd=e2e_env)
        assert r2.returncode == 0
        assert "1 link(s)" in r2.stdout

        r3 = _run("link", "remove", "LINK-00001", "--author", "a", cwd=e2e_env)
        assert r3.returncode == 0

    def test_search(self, e2e_env: Path) -> None:
        _run(
            "create", "task", "Searchable needle",
            "--author", "a", "--assignee", "b", cwd=e2e_env,
        )
        r = _run("search", "needle", cwd=e2e_env)
        assert r.returncode == 0
        assert "1 ticket(s)" in r.stdout

    def test_workflow_types(self, e2e_env: Path) -> None:
        r = _run("workflow", "types", cwd=e2e_env)
        assert r.returncode == 0
        assert "task" in r.stdout
