"""CSV index read/write and ID-counter management."""

from __future__ import annotations

import csv
import errno
import os
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, TextIO

import yaml

from .config import get_paths, get_runtime_config
from .constants import INDEX_FIELDNAMES, LINK_INDEX_FIELDNAMES
from .exceptions import FileOperationError, ValidationError


@contextmanager
def interprocess_lock(name: str) -> Iterator[None]:
    """Lock a tracker transaction across processes on Windows and POSIX.

    Lock files live in ``.ept/tmp``. Keep the handle open for the full
    read-modify-write transaction; locking an individual file write is too late.
    """
    lock_dir = get_paths().tracker_root.parent / "tmp"
    lock_dir.mkdir(parents=True, exist_ok=True)
    lock_path = lock_dir / f"tracker-{name}.lock"
    deadline = time.monotonic() + 30
    try:
        with open(lock_path, "a+b") as handle:
            while True:
                try:
                    handle.seek(0)
                    if os.name == "nt":
                        import msvcrt

                        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    else:
                        import fcntl

                        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except OSError as exc:
                    if exc.errno not in (errno.EACCES, errno.EAGAIN) and getattr(
                        exc, "winerror", None
                    ) not in (33, 36):
                        raise
                    if time.monotonic() >= deadline:
                        raise FileOperationError(
                            f"Timed out waiting for tracker {name} lock"
                        ) from exc
                    time.sleep(0.05)
            try:
                yield
            finally:
                handle.seek(0)
                if os.name == "nt":
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    except OSError as exc:
        raise FileOperationError(f"Failed to lock tracker {name}: {exc}") from exc


def _temporary_file_path(destination: Path) -> tuple[Path, TextIO]:
    """Create a writable temp file in ``.ept/tmp`` for atomic replacement."""
    temp_dir = get_paths().tracker_root.parent / "tmp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="",
        dir=temp_dir,
        prefix=f"{destination.stem}-",
        suffix=".tmp",
        delete=False,
    )
    return Path(handle.name), handle


def _replace_with_retry(source: Path, destination: Path) -> None:
    """Replace an index file after brief Windows reader sharing conflicts."""
    deadline = time.monotonic() + 3
    while True:
        try:
            os.replace(source, destination)
            return
        except PermissionError:
            if time.monotonic() >= deadline:
                raise
            time.sleep(0.01)


# ── ID counters ──────────────────────────────────────────────────────────────


def load_id_counters() -> dict[str, int]:
    """Load ID counters from ``.id-counters.yaml``."""
    paths = get_paths()
    deadline = time.monotonic() + 3
    try:
        while True:
            try:
                with open(paths.id_counters_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                return data.get("counters", {}) if data else {}
            except PermissionError:
                if time.monotonic() >= deadline:
                    raise
                time.sleep(0.01)
    except FileNotFoundError:
        return {}
    except Exception as e:
        raise FileOperationError(f"Failed to load ID counters: {e}")


def save_id_counters(counters: dict[str, int]) -> None:
    """Persist ID counters back to ``.id-counters.yaml``."""
    paths = get_paths()
    try:
        with interprocess_lock("counters"):
            with open(paths.id_counters_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            current = data.get("counters", {})
            data["counters"] = {
                key: max(current.get(key, 0), counters.get(key, 0))
                for key in current.keys() | counters.keys()
            }
            temp_path, handle = _temporary_file_path(paths.id_counters_file)
            try:
                with handle:
                    yaml.dump(
                        data, handle,
                        default_flow_style=False, sort_keys=False, allow_unicode=True,
                    )
                _replace_with_retry(temp_path, paths.id_counters_file)
            finally:
                temp_path.unlink(missing_ok=True)
    except Exception as e:
        raise FileOperationError(f"Failed to save ID counters: {e}")


def get_next_ticket_id(ticket_type: str) -> tuple[str, int]:
    """Return the next ``(ticket_id, counter)`` for *ticket_type*."""
    prefix = get_runtime_config()["ticket_id_prefixes"].get(ticket_type)
    if not prefix:
        valid_types = ", ".join(get_runtime_config()["ticket_types"])
        raise ValidationError(
            f"Invalid ticket type: {ticket_type}. Valid types: {valid_types}. "
            "Fix: choose one of the listed types"
        )
    counters = load_id_counters()
    indexed_numbers = [
        int(suffix)
        for ticket in read_index()
        if ticket["type"] == ticket_type
        and ticket["id"].startswith(f"{prefix}-")
        and (suffix := ticket["id"][len(prefix) + 1:]).isdigit()
    ]
    next_counter = max(counters.get(ticket_type, 0), max(indexed_numbers, default=0)) + 1
    ticket_id = f"{prefix}-{next_counter:03d}"
    return ticket_id, next_counter


def increment_counter(ticket_type: str) -> None:
    """Increment the ticket counter for *ticket_type*."""
    counters = load_id_counters()
    prefix = get_runtime_config()["ticket_id_prefixes"][ticket_type]
    indexed_numbers = [
        int(suffix)
        for ticket in read_index()
        if ticket["type"] == ticket_type
        and ticket["id"].startswith(f"{prefix}-")
        and (suffix := ticket["id"][len(prefix) + 1:]).isdigit()
    ]
    counters[ticket_type] = max(
        counters.get(ticket_type, 0) + 1,
        max(indexed_numbers, default=0),
    )
    save_id_counters(counters)


def get_next_link_id() -> str:
    """Return the next link ID string."""
    counters = load_id_counters()
    existing = _max_link_number(read_link_index())
    return f"LINK-{max(counters.get('link', 0), existing) + 1:05d}"


def _max_link_number(links: list[dict[str, str]]) -> int:
    """Find the largest numeric link ID in an index."""
    numbers = [
        int(link_id[5:])
        for link in links
        if (link_id := link.get("link_id", "")).startswith("LINK-")
        and link_id[5:].isdigit()
    ]
    return max(numbers, default=0)


def increment_link_counter() -> None:
    """Increment the link counter."""
    counters = load_id_counters()
    counters["link"] = max(
        counters.get("link", 0) + 1,
        _max_link_number(read_link_index()),
    )
    save_id_counters(counters)


# ── Ticket index ─────────────────────────────────────────────────────────────


def read_index() -> list[dict[str, str]]:
    """Read the ticket index CSV."""
    paths = get_paths()
    deadline = time.monotonic() + 3
    try:
        while True:
            try:
                with open(paths.index_file, "r", encoding="utf-8", newline="") as f:
                    return list(csv.DictReader(f))
            except PermissionError:
                if time.monotonic() >= deadline:
                    raise
                time.sleep(0.01)
            except FileNotFoundError:
                try:
                    with open(paths.index_file, "x", encoding="utf-8", newline="") as f:
                        csv.DictWriter(f, fieldnames=INDEX_FIELDNAMES).writeheader()
                    return []
                except FileExistsError:
                    if time.monotonic() >= deadline:
                        raise
                    time.sleep(0.01)
    except Exception as e:
        raise FileOperationError(f"Failed to read index: {e}")


def canonicalize_ticket_status(
    indexed_ticket: dict[str, str],
) -> dict[str, str]:
    """Return one index row with status sourced from ticket frontmatter."""
    from .tickets import parse_ticket_file
    from .validators import validate_status_value

    ticket = dict(indexed_ticket)
    metadata, _ = parse_ticket_file(ticket)
    status = str(metadata.get("status", "")).strip()
    validate_status_value(status, ticket["type"])
    ticket["status"] = status
    return ticket


def read_canonical_index() -> list[dict[str, str]]:
    """Read index rows with status sourced from ticket frontmatter.

    Ticket files are authoritative for lifecycle status. The CSV index is a
    query accelerator and may lag after an interrupted write or manual repair.
    This function does not modify either persistence layer.
    """
    return [canonicalize_ticket_status(ticket) for ticket in read_index()]


def reconcile_index_statuses(*, apply: bool = False) -> list[dict[str, str]]:
    """Report status drift and optionally copy canonical values into the index.

    Reconciliation changes only the index ``status`` column. Ticket files,
    timestamps, comments, and links remain unchanged.
    """
    if apply:
        with interprocess_lock("tickets"):
            return _reconcile_index_statuses(apply=True)
    return _reconcile_index_statuses(apply=False)


def _reconcile_index_statuses(*, apply: bool) -> list[dict[str, str]]:
    """Read status drift and write corrections while caller holds any needed lock."""
    indexed = read_index()
    canonical_by_id = {ticket["id"]: ticket for ticket in read_canonical_index()}
    drift: list[dict[str, str]] = []

    for ticket in indexed:
        canonical_status = canonical_by_id[ticket["id"]]["status"]
        if ticket["status"] == canonical_status:
            continue
        drift.append({
            "ticket_id": ticket["id"],
            "index_status": ticket["status"],
            "canonical_status": canonical_status,
        })
        if apply:
            ticket["status"] = canonical_status

    if apply and drift:
        write_index(indexed)
    return drift


def write_index(tickets: list[dict[str, str]]) -> None:
    """Overwrite the ticket index CSV."""
    paths = get_paths()
    try:
        temp_path, handle = _temporary_file_path(paths.index_file)
        try:
            with handle:
                fieldnames = list(tickets[0].keys()) if tickets else INDEX_FIELDNAMES
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(tickets)
            _replace_with_retry(temp_path, paths.index_file)
        finally:
            temp_path.unlink(missing_ok=True)
    except Exception as e:
        raise FileOperationError(f"Failed to write index: {e}")


# ── Link index ───────────────────────────────────────────────────────────────


def read_link_index() -> list[dict[str, str]]:
    """Read the link index CSV."""
    paths = get_paths()
    deadline = time.monotonic() + 3
    try:
        while True:
            try:
                with open(paths.link_index_file, "r", encoding="utf-8", newline="") as f:
                    return list(csv.DictReader(f))
            except PermissionError:
                if time.monotonic() >= deadline:
                    raise
                time.sleep(0.01)
            except FileNotFoundError:
                try:
                    with open(paths.link_index_file, "x", encoding="utf-8", newline="") as f:
                        csv.DictWriter(f, fieldnames=LINK_INDEX_FIELDNAMES).writeheader()
                    return []
                except FileExistsError:
                    if time.monotonic() >= deadline:
                        raise
                    time.sleep(0.01)
    except Exception as e:
        raise FileOperationError(f"Failed to read link index: {e}")


def write_link_index(links: list[dict[str, str]]) -> None:
    """Overwrite the link index CSV."""
    paths = get_paths()
    try:
        temp_path, handle = _temporary_file_path(paths.link_index_file)
        try:
            with handle:
                fieldnames = list(links[0].keys()) if links else LINK_INDEX_FIELDNAMES
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(links)
            _replace_with_retry(temp_path, paths.link_index_file)
        finally:
            temp_path.unlink(missing_ok=True)
    except Exception as e:
        raise FileOperationError(f"Failed to write link index: {e}")


# ── Ticket lookup ────────────────────────────────────────────────────────────


def ticket_exists(ticket_id: str) -> bool:
    """Return ``True`` if *ticket_id* appears in the index."""
    return any(t["id"] == ticket_id for t in read_index())


def get_ticket(ticket_id: str) -> dict[str, str]:
    """Look up a ticket in the index.

    Raises :class:`~tracker.exceptions.ValidationError` when not found.
    """
    ticket = next((t for t in read_index() if t["id"] == ticket_id), None)
    if not ticket:
        raise ValidationError(f"Ticket {ticket_id} not found")
    return canonicalize_ticket_status(ticket)
