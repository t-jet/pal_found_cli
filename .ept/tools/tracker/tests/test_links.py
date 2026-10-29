"""Tests for tracker.links — create, list, remove links."""

from __future__ import annotations

import builtins
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from tests.conftest import make_task
from tracker.exceptions import ValidationError
from tracker.config import get_paths
from tracker.index import load_id_counters, read_index, read_link_index, write_link_index
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

    def test_duplicate_id_cannot_remove_multiple_links(self, tracker_env: Path) -> None:
        source = make_task("Source")
        target = make_task("Target")
        link_id = create_link(source, target, "RelatesTo", "tester")
        links = read_link_index()
        write_link_index([links[0], {**links[0], "target_ticket": source}])

        with pytest.raises(ValidationError, match="ambiguous"):
            remove_link(link_id)
        assert len(read_link_index()) == 2


def test_parallel_link_creates_keep_unique_ids_and_all_rows(tracker_env: Path) -> None:
    """Separate CLI processes must allocate IDs and update the index together."""
    source = make_task("Source")
    targets = [make_task(f"Target {i}") for i in range(8)]
    temp_dir = tracker_env / ".ept" / "tmp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    gate = temp_dir / "create-links-gate"
    env = os.environ.copy()
    env["EPT_TRACKER_ROOT_PATH"] = str(tracker_env / ".ept" / "tracker")
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    script = (
        "import sys, time\n"
        "from pathlib import Path\n"
        "from tracker.links import create_link\n"
        "ready, gate, source, target = sys.argv[1:]\n"
        "Path(ready).write_text('ready', encoding='utf-8')\n"
        "while not Path(gate).exists(): time.sleep(0.005)\n"
        "print(create_link(source, target, 'RelatesTo', 'tester'))\n"
    )
    processes = [
        subprocess.Popen(
            [
                sys.executable, "-c", script,
                str(temp_dir / f"ready-{i}"), str(gate), source, target,
            ],
            cwd=Path(__file__).resolve().parents[1],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for i, target in enumerate(targets)
    ]
    deadline = time.monotonic() + 20
    try:
        while not all((temp_dir / f"ready-{i}").exists() for i in range(len(targets))):
            assert time.monotonic() < deadline, "link workers did not start"
            time.sleep(0.01)
        gate.write_text("go", encoding="utf-8")
        results = [process.communicate(timeout=30) for process in processes]
        for process, (_, stderr) in zip(processes, results):
            assert process.returncode == 0, stderr
        ids = [stdout.strip() for stdout, _ in results]
        links = read_link_index()
        assert len(ids) == len(set(ids)) == len(targets)
        assert len(links) == len(targets)
        assert {link["target_ticket"] for link in links} == set(targets)
    finally:
        for process in processes:
            if process.poll() is None:
                process.kill()
                process.communicate()


def test_parallel_ticket_and_link_creates_preserve_both_counters(
    tracker_env: Path,
) -> None:
    """Ticket and link transactions must not overwrite each other's counters."""
    source = make_task("Source")
    targets = [make_task(f"Target {i}") for i in range(4)]
    existing_ticket_ids = {ticket["id"] for ticket in read_index()}
    temp_dir = tracker_env / ".ept" / "tmp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    gate = temp_dir / "mixed-create-gate"
    env = os.environ.copy()
    env["EPT_TRACKER_ROOT_PATH"] = str(tracker_env / ".ept" / "tracker")
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    script = (
        "import sys, time\n"
        "from pathlib import Path\n"
        "from tracker.links import create_link\n"
        "from tracker.tickets import create_ticket\n"
        "mode, ready, gate, source, target = sys.argv[1:]\n"
        "Path(ready).write_text('ready', encoding='utf-8')\n"
        "while not Path(gate).exists(): time.sleep(0.005)\n"
        "if mode == 'ticket': print(create_ticket('task', target, 'tester'))\n"
        "else: print(create_link(source, target, 'RelatesTo', 'tester'))\n"
    )
    jobs = [("ticket", f"New {i}") for i in range(4)] + [
        ("link", target) for target in targets
    ]
    processes = [
        subprocess.Popen(
            [
                sys.executable, "-c", script, mode,
                str(temp_dir / f"mixed-ready-{i}"), str(gate), source, target,
            ],
            cwd=Path(__file__).resolve().parents[1],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for i, (mode, target) in enumerate(jobs)
    ]
    deadline = time.monotonic() + 20
    try:
        while not all((temp_dir / f"mixed-ready-{i}").exists() for i in range(8)):
            assert time.monotonic() < deadline, "mixed workers did not start"
            time.sleep(0.01)
        gate.write_text("go", encoding="utf-8")
        results = [process.communicate(timeout=30) for process in processes]
        for process, (_, stderr) in zip(processes, results):
            assert process.returncode == 0, stderr
        new_ticket_ids = {ticket["id"] for ticket in read_index()} - existing_ticket_ids
        links = read_link_index()
        counters = load_id_counters()
        assert len(new_ticket_ids) == len(links) == 4
        assert len({link["link_id"] for link in links}) == 4
        assert counters["task"] >= max(int(tid.split("-")[-1]) for tid in new_ticket_ids)
        assert counters["link"] >= max(int(link["link_id"][5:]) for link in links)
    finally:
        for process in processes:
            if process.poll() is None:
                process.kill()
                process.communicate()


@pytest.mark.parametrize(
    "path_name,reader",
    [
        ("id_counters_file", load_id_counters),
        ("index_file", read_index),
        ("link_index_file", read_link_index),
    ],
)
def test_reader_recovers_from_transient_windows_sharing_error(
    tracker_env: Path, monkeypatch: pytest.MonkeyPatch, path_name: str, reader
) -> None:
    """A short sharing conflict during atomic replacement must not fail a read."""
    target = getattr(get_paths(), path_name)
    real_open = builtins.open
    rejected = False

    def flaky_open(file, *args, **kwargs):
        nonlocal rejected
        if Path(file) == target and not rejected:
            rejected = True
            raise PermissionError("sharing violation")
        return real_open(file, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", flaky_open)
    reader()
    assert rejected
