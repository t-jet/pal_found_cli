"""Tests for tracker.config — path resolution, workflow loading, runtime config."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from tracker.config import (
    TrackerPaths,
    get_paths,
    get_runtime_config,
    invalidate_config,
    reset,
    set_paths,
)
from tracker.exceptions import ConfigurationError


# ── TrackerPaths ─────────────────────────────────────────────────────────────


class TestTrackerPaths:
    def test_derived_paths(self, tmp_path: Path) -> None:
        tracker_root = tmp_path / ".ept" / "tracker"
        paths = TrackerPaths(tracker_root=tracker_root)
        assert paths.tracker_root == tracker_root
        assert paths.config_dir == tracker_root / ".config"
        assert paths.workflow_file.name == ".workflow.yaml"
        assert paths.id_counters_file.name == ".id-counters.yaml"
        assert paths.index_file.name == ".index.csv"
        assert paths.link_index_file.name == ".link-index.csv"

    def test_frozen(self, tmp_path: Path) -> None:
        paths = TrackerPaths(tracker_root=tmp_path)
        with pytest.raises(AttributeError):
            paths.tracker_root = tmp_path / "other"  # type: ignore[misc]


# ── set_paths / get_paths / reset ────────────────────────────────────────────


class TestPathManagement:
    def test_set_and_get(self, tmp_path: Path) -> None:
        paths = TrackerPaths(tracker_root=tmp_path)
        set_paths(paths)
        assert get_paths() is paths
        reset()

    def test_reset_clears_cache(self, tmp_path: Path) -> None:
        set_paths(TrackerPaths(tracker_root=tmp_path))
        reset()
        # After reset, get_paths will try auto-detection (we don't care
        # about where it lands; just verify it runs without error).
        _ = get_paths()
        reset()

    def test_env_var_overrides_autodetect(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        reset()
        tracker_root = tmp_path / ".ept" / "tracker"
        monkeypatch.setenv("EPT_TRACKER_ROOT_PATH", str(tracker_root))
        paths = get_paths()
        assert paths.tracker_root == tracker_root
        reset()


# ── Runtime configuration ────────────────────────────────────────────────────


class TestRuntimeConfig:
    def test_loads_ticket_types(self, tracker_env: Path) -> None:
        cfg = get_runtime_config()
        assert sorted(cfg["ticket_types"]) == ["question", "task", "workitem"]

    def test_loads_link_types(self, tracker_env: Path) -> None:
        cfg = get_runtime_config()
        assert "Blocks" in cfg["link_types"]
        assert "RelatesTo" in cfg["link_types"]

    def test_loads_priority_values(self, tracker_env: Path) -> None:
        cfg = get_runtime_config()
        assert cfg["priority_values"] == ["Low", "Medium", "High", "Critical"]

    def test_cached(self, tracker_env: Path) -> None:
        cfg1 = get_runtime_config()
        cfg2 = get_runtime_config()
        assert cfg1 is cfg2

    def test_invalidate_config_clears_cache(self, tracker_env: Path) -> None:
        cfg1 = get_runtime_config()
        invalidate_config()
        cfg2 = get_runtime_config()
        assert cfg1 is not cfg2

    def test_ticket_specs_statuses(self, tracker_env: Path) -> None:
        cfg = get_runtime_config()
        statuses = cfg["ticket_specs"]["task"]["statuses"]
        assert "New" in statuses
        assert "Closed" in statuses

    def test_link_roles(self, tracker_env: Path) -> None:
        cfg = get_runtime_config()
        src, tgt = cfg["link_roles"]["Blocks"]
        assert src == "Blocks"
        assert tgt == "Is Blocked By"


# ── Workflow file errors ─────────────────────────────────────────────────────


class TestWorkflowErrors:
    def test_missing_workflow_file(self, tmp_path: Path) -> None:
        tracker = tmp_path / ".ept" / "tracker"
        tracker.mkdir(parents=True)
        (tracker / ".config").mkdir()
        set_paths(TrackerPaths(tracker_root=tracker))
        with pytest.raises(ConfigurationError, match="Workflow file not found"):
            get_runtime_config()
        reset()

    def test_missing_required_section(self, tracker_env: Path) -> None:
        paths = get_paths()
        paths.workflow_file.write_text(
            "ticket_types: []\nlink_types: []\n", encoding="utf-8",
        )
        invalidate_config()
        with pytest.raises(ConfigurationError, match="missing section"):
            get_runtime_config()


# ── $ref resolution ──────────────────────────────────────────────────────────


class TestRefResolution:
    def test_ref_ticket_type_loaded(self, tracker_env: Path) -> None:
        paths = get_paths()
        # Create a ref file
        tickets_dir = paths.config_dir / "tickets"
        tickets_dir.mkdir()
        (tickets_dir / "custom.yaml").write_text(textwrap.dedent("""\
            type: task
            required_fields: [id, type, title, status, priority, assignee, reporter, created, updated]
            optional_fields: [parent, addressed_to]
            statuses:
                New: Created
                Closed: Closed
        """), encoding="utf-8")

        # Rewrite workflow to use $ref
        wf_text = paths.workflow_file.read_text(encoding="utf-8")
        wf_text = wf_text.replace(
            "  - type: task\n"
            "    required_fields: [id, type, title, status, priority, assignee, reporter, created, updated]\n"
            "    optional_fields: [parent, addressed_to]\n"
            "    statuses:\n"
            "      New: Created\n"
            "      Open: Open\n"
            "      In Progress: In progress\n"
            "      Resolved: Resolved\n"
            "      Closed: Closed",
            '  - {"$ref": "tickets/custom.yaml"}',
        )
        paths.workflow_file.write_text(wf_text, encoding="utf-8")
        invalidate_config()
        cfg = get_runtime_config()
        assert "task" in cfg["ticket_types"]

    def test_ref_file_not_found_raises(self, tracker_env: Path) -> None:
        paths = get_paths()
        wf_text = paths.workflow_file.read_text(encoding="utf-8")
        # Replace an existing inline ticket type with a $ref to a nonexistent file
        wf_text = wf_text.replace(
            "  - type: task\n"
            "    required_fields: [id, type, title, status, priority, assignee, reporter, created, updated]\n"
            "    optional_fields: [parent, addressed_to]\n"
            "    terminal_statuses: [Closed]\n"
            "    statuses:\n"
            "      New: Created\n"
            "      Open: Open\n"
            "      In Progress: In progress\n"
            "      Resolved: Resolved\n"
            "      Closed: Closed",
            '  - $ref: tickets/nonexistent.yaml',
        )
        paths.workflow_file.write_text(wf_text, encoding="utf-8")
        invalidate_config()
        with pytest.raises(ConfigurationError, match="ref not found"):
            get_runtime_config()
