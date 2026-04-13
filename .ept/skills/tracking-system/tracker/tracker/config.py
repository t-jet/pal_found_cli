"""Configuration management: path resolution, workflow loading, runtime config cache."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .constants import TICKET_CONTENT_FILE
from .exceptions import ConfigurationError


# ── Path container ───────────────────────────────────────────────────────────


@dataclass(frozen=True)
class TrackerPaths:
    """Immutable set of filesystem paths for the tracker layout.

    *tracker_root* is the top-level tracker directory (e.g.
    ``/project/.ept/tracker``).  All other paths are derived from it.
    """

    tracker_root: Path

    @property
    def config_dir(self) -> Path:
        return self.tracker_root / ".config"

    @property
    def workflow_file(self) -> Path:
        return self.config_dir / ".workflow.yaml"

    @property
    def id_counters_file(self) -> Path:
        return self.config_dir / ".id-counters.yaml"

    @property
    def index_file(self) -> Path:
        return self.config_dir / ".index.csv"

    @property
    def link_index_file(self) -> Path:
        return self.config_dir / ".link-index.csv"

    @property
    def instructions_dir(self) -> Path:
        return self.tracker_root / ".instructions"


# ── Module-level state ───────────────────────────────────────────────────────

_paths: TrackerPaths | None = None
_runtime_config: dict[str, Any] | None = None


# ── Path management ──────────────────────────────────────────────────────────


def _find_tracker_root() -> Path:
    """Find the tracker root directory (the ``.ept/tracker`` folder).

    Search order:
      1. Current working directory, if it contains ``.ept/tracker``.
      2. This file's directory and each ancestor.

    Returns the *tracker* directory itself (not the project root), so that
    multiple tracker instances can coexist inside a single project.
    """
    cwd = Path.cwd()
    tracker_in_cwd = cwd / ".ept" / "tracker"
    if tracker_in_cwd.exists():
        return tracker_in_cwd

    candidate = Path(__file__).resolve().parent
    while True:
        tracker_candidate = candidate / ".ept" / "tracker"
        if tracker_candidate.exists():
            return tracker_candidate
        parent = candidate.parent
        if parent == candidate:
            break
        candidate = parent

    # Fallback -- CWD/tracker (error surfaces naturally via missing .workflow.yaml)
    return cwd / ".ept" / "tracker"


def get_paths() -> TrackerPaths:
    """Return the active :class:`TrackerPaths`, auto-detecting on first call.

    Resolution order:
      1. Explicitly set via :func:`set_paths` (e.g. in test fixtures).
      2. ``EPT_TRACKER_ROOT_PATH`` environment variable -- must point directly
         to the tracker root directory (e.g. ``/project/.ept/tracker``).
      3. Auto-detection via :func:`_find_tracker_root`.
    """
    global _paths
    if _paths is None:
        env_root = os.environ.get("EPT_TRACKER_ROOT_PATH")
        if env_root:
            _paths = TrackerPaths(tracker_root=Path(env_root))
        else:
            _paths = TrackerPaths(tracker_root=_find_tracker_root())
    return _paths


def set_paths(paths: TrackerPaths) -> None:
    """Override the active paths (primarily for test fixtures)."""
    global _paths, _runtime_config
    _paths = paths
    _runtime_config = None


def reset() -> None:
    """Clear all cached state (paths **and** runtime config)."""
    global _paths, _runtime_config
    _paths = None
    _runtime_config = None


def invalidate_config() -> None:
    """Clear **only** the runtime-config cache, forcing a reload on next access."""
    global _runtime_config
    _runtime_config = None


# ── Workflow-loading helpers ─────────────────────────────────────────────────


def _extract_status_info(status_entry: Any) -> dict[str, Any]:
    """Extract ``description``, ``stage_goal``, ``responsible_roles`` from a status entry.

    Supports both the legacy *string* format and the newer *dict* format.
    ``responsible_roles`` is always normalised to a ``list[str]``.
    """

    def _to_roles_list(value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(v) for v in value]
        if isinstance(value, str) and value:
            return [v.strip() for v in value.split(",")]
        return []

    if isinstance(status_entry, str):
        return {"description": status_entry, "stage_goal": "", "responsible_roles": []}
    if isinstance(status_entry, dict):
        return {
            "description": status_entry.get("description", ""),
            "stage_goal": status_entry.get("stage_goal", ""),
            "responsible_roles": _to_roles_list(
                status_entry.get("responsible_roles", []),
            ),
        }
    return {"description": "", "stage_goal": "", "responsible_roles": []}


def _resolve_ticket_type_refs(
    ticket_types_raw: list[Any],
    config_dir: Path,
) -> list[dict[str, Any]]:
    """Resolve ``$ref`` entries in the ``ticket_types`` list.

    Entries of the form ``{"$ref": "tickets/task.yaml"}`` are loaded from
    *config_dir*.  Plain dict entries pass through unchanged, preserving
    backward-compatibility with inline definitions used in tests.
    """
    resolved: list[dict[str, Any]] = []
    for item in ticket_types_raw:
        if not isinstance(item, dict):
            continue
        ref_path = item.get("$ref")
        if ref_path is not None:
            abs_path = config_dir / ref_path
            try:
                with open(abs_path, "r", encoding="utf-8") as fh:
                    loaded = yaml.safe_load(fh)
            except FileNotFoundError:
                raise ConfigurationError(
                    f"Ticket type ref not found: {abs_path}. "
                    "Fix: create the missing file or correct the $ref path"
                )
            except Exception as exc:
                raise ConfigurationError(
                    f"Failed to parse ticket type ref {abs_path}: {exc}"
                )
            if not isinstance(loaded, dict):
                raise ConfigurationError(
                    f"Ticket type file {abs_path} must contain a YAML mapping, "
                    f"got {type(loaded).__name__}"
                )
            resolved.append(loaded)
        else:
            resolved.append(item)
    return resolved


def _load_workflow_config(paths: TrackerPaths) -> dict[str, Any]:
    """Load and validate ``.workflow.yaml``, resolving ``$ref`` entries."""
    try:
        with open(paths.workflow_file, "r", encoding="utf-8") as f:
            workflow = yaml.safe_load(f) or {}
    except FileNotFoundError:
        raise ConfigurationError(
            f"Workflow file not found: {paths.workflow_file}. "
            "Fix: create/restore .workflow.yaml"
        )
    except Exception as e:
        raise ConfigurationError(
            f"Failed to parse workflow file {paths.workflow_file}: {e}"
        )

    required_keys = ["type_registry", "link_types", "ticket_types", "fields"]
    missing = [k for k in required_keys if k not in workflow]
    if missing:
        raise ConfigurationError(
            f"Invalid workflow config: missing section(s): {', '.join(missing)}. "
            "Fix: add required sections to .workflow.yaml"
        )

    workflow["ticket_types"] = _resolve_ticket_type_refs(
        workflow["ticket_types"], paths.config_dir,
    )
    return workflow


def _get_ticket_type_entry(
    ticket_types: list[dict[str, Any]],
    ticket_type: str,
) -> dict[str, Any]:
    """Look up a ticket-type entry by its ``type`` key."""
    entry = next(
        (t for t in ticket_types if t.get("type") == ticket_type), None,
    )
    if entry:
        return entry
    raise ConfigurationError(
        f"Ticket type '{ticket_type}' missing in ticket_types configuration. "
        "Fix: add an explicit ticket type entry in .workflow.yaml"
    )


# ── Runtime configuration ────────────────────────────────────────────────────


def get_runtime_config() -> dict[str, Any]:
    """Load the runtime configuration, caching after first call.

    Call :func:`reset`, :func:`set_paths`, or :func:`invalidate_config`
    to force a reload.
    """
    global _runtime_config
    if _runtime_config is not None:
        return _runtime_config

    paths = get_paths()
    workflow = _load_workflow_config(paths)

    type_registry: dict[str, dict[str, Any]] = workflow["type_registry"]
    link_types_raw: list[dict[str, Any]] = workflow["link_types"]
    ticket_types_raw: list[dict[str, Any]] = workflow["ticket_types"]
    field_defs: list[dict[str, Any]] = workflow["fields"]

    ticket_types = sorted(type_registry.keys())
    link_types = [lt.get("type") for lt in link_types_raw if lt.get("type")]
    link_roles = {
        lt["type"]: (
            lt.get("source_role", lt["type"]),
            lt.get("target_role", lt["type"]),
        )
        for lt in link_types_raw
        if lt.get("type")
    }

    prefixes = {
        tt: entry.get("id_prefix", "")
        for tt, entry in type_registry.items()
    }
    invalid_prefix = [k for k, v in prefixes.items() if not v]
    if invalid_prefix:
        raise ConfigurationError(
            f"type_registry has missing id_prefix for: "
            f"{', '.join(sorted(invalid_prefix))}. Fix: set id_prefix for each type"
        )

    ticket_specs: dict[str, dict[str, Any]] = {}
    valid_field_names = {f.get("name") for f in field_defs if f.get("name")}
    priority_values: list[str] = []
    for f in field_defs:
        if f.get("name") == "priority":
            priority_values = f.get("values", [])
            break

    for tt in ticket_types:
        entry = _get_ticket_type_entry(ticket_types_raw, tt)
        raw_statuses: dict[str, Any] = entry.get("statuses") or {}
        ticket_specs[tt] = {
            "required_fields": entry.get("required_fields", []),
            "optional_fields": entry.get("optional_fields", []),
            "statuses": sorted(raw_statuses.keys()),
            "status_details": {
                name: _extract_status_info(val)
                for name, val in raw_statuses.items()
            },
            "allowed_transitions": entry.get("allowed_transitions") or {},
            "terminal_statuses": entry.get("terminal_statuses", []),
            "initial_status": type_registry[tt].get("initial_status", "New"),
            "content_file": type_registry[tt].get(
                "content_file", TICKET_CONTENT_FILE,
            ),
            "ticket_instructions": entry.get("ticket_instructions") or {},
        }

    _runtime_config = {
        "workflow": workflow,
        "type_registry": type_registry,
        "ticket_types": ticket_types,
        "link_types": link_types,
        "link_roles": link_roles,
        "ticket_id_prefixes": prefixes,
        "ticket_specs": ticket_specs,
        "valid_field_names": valid_field_names,
        "priority_values": priority_values,
    }
    return _runtime_config
