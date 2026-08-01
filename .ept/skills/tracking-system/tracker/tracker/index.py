"""CSV index read/write and ID-counter management."""

from __future__ import annotations

import csv

import yaml

from .config import get_paths, get_runtime_config
from .constants import INDEX_FIELDNAMES, LINK_INDEX_FIELDNAMES
from .exceptions import FileOperationError, ValidationError


# ── ID counters ──────────────────────────────────────────────────────────────


def load_id_counters() -> dict[str, int]:
    """Load ID counters from ``.id-counters.yaml``."""
    paths = get_paths()
    try:
        with open(paths.id_counters_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("counters", {}) if data else {}
    except FileNotFoundError:
        return {}
    except Exception as e:
        raise FileOperationError(f"Failed to load ID counters: {e}")


def save_id_counters(counters: dict[str, int]) -> None:
    """Persist ID counters back to ``.id-counters.yaml``."""
    paths = get_paths()
    try:
        with open(paths.id_counters_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        data["counters"] = counters
        with open(paths.id_counters_file, "w", encoding="utf-8") as f:
            yaml.dump(
                data, f,
                default_flow_style=False, sort_keys=False, allow_unicode=True,
            )
    except Exception as e:
        raise FileOperationError(f"Failed to save ID counters: {e}")


def get_next_ticket_id(ticket_type: str) -> tuple[str, int]:
    """Return the next ``(ticket_id, counter)`` for *ticket_type*."""
    counters = load_id_counters()
    next_counter = counters.get(ticket_type, 0) + 1
    prefix = get_runtime_config()["ticket_id_prefixes"].get(ticket_type)
    if not prefix:
        valid_types = ", ".join(get_runtime_config()["ticket_types"])
        raise ValidationError(
            f"Invalid ticket type: {ticket_type}. Valid types: {valid_types}. "
            "Fix: choose one of the listed types"
        )
    ticket_id = f"{prefix}-{next_counter:03d}"
    return ticket_id, next_counter


def increment_counter(ticket_type: str) -> None:
    """Increment the ticket counter for *ticket_type*."""
    counters = load_id_counters()
    counters[ticket_type] = counters.get(ticket_type, 0) + 1
    save_id_counters(counters)


def get_next_link_id() -> str:
    """Return the next link ID string."""
    counters = load_id_counters()
    return f"LINK-{counters.get('link', 0) + 1:05d}"


def increment_link_counter() -> None:
    """Increment the link counter."""
    counters = load_id_counters()
    counters["link"] = counters.get("link", 0) + 1
    save_id_counters(counters)


# ── Ticket index ─────────────────────────────────────────────────────────────


def read_index() -> list[dict[str, str]]:
    """Read the ticket index CSV."""
    paths = get_paths()
    try:
        with open(paths.index_file, "r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        with open(paths.index_file, "w", encoding="utf-8", newline="") as f:
            csv.DictWriter(f, fieldnames=INDEX_FIELDNAMES).writeheader()
        return []
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
        with open(paths.index_file, "w", encoding="utf-8", newline="") as f:
            fieldnames = list(tickets[0].keys()) if tickets else INDEX_FIELDNAMES
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(tickets)
    except Exception as e:
        raise FileOperationError(f"Failed to write index: {e}")


# ── Link index ───────────────────────────────────────────────────────────────


def read_link_index() -> list[dict[str, str]]:
    """Read the link index CSV."""
    paths = get_paths()
    try:
        with open(paths.link_index_file, "r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        with open(paths.link_index_file, "w", encoding="utf-8", newline="") as f:
            csv.DictWriter(f, fieldnames=LINK_INDEX_FIELDNAMES).writeheader()
        return []
    except Exception as e:
        raise FileOperationError(f"Failed to read link index: {e}")


def write_link_index(links: list[dict[str, str]]) -> None:
    """Overwrite the link index CSV."""
    paths = get_paths()
    try:
        with open(paths.link_index_file, "w", encoding="utf-8", newline="") as f:
            fieldnames = list(links[0].keys()) if links else LINK_INDEX_FIELDNAMES
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(links)
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
