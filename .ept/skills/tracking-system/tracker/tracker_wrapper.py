#!/usr/bin/env python3
"""Shared helpers for the tracker wrapper scripts.

Every ``tracker-*.py`` script in ``.ept/skills/tracking-system/tracker/`` delegates to this module for
two tasks:

1. **Help output** – when ``--help`` / ``-h`` is passed, *or when called with
   no arguments*, render the TOON-formatted help block for *just* the command
   that the wrapper covers.
2. **Invocation** – forward the (possibly transformed) argument list to
   ``tracker.cli.main()`` and return its exit code.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# ── Path setup ───────────────────────────────────────────────────────────────

# This file lives inside implementations/tracker/, which is also the root
# of the tracker package – so we just need to make sure *this* directory
# is on sys.path.
_IMPL_DIR = Path(__file__).resolve().parent


def _ensure_importable() -> None:
    """Insert the tracker implementation directory into ``sys.path``."""
    impl = str(_IMPL_DIR)
    if impl not in sys.path:
        sys.path.insert(0, impl)


# ── Help rendering ────────────────────────────────────────────────────────────


def _get_node(data: dict[str, Any], key_path: list[str]) -> Any:
    """Return the nested value at *key_path* inside *data*."""
    node: Any = data
    for k in key_path:
        node = node[k]
    return node


def print_command_help(script_name: str, key_path: list[str]) -> None:
    """Print TOON-formatted help for the command at *key_path* and exit(0).

    *key_path* must navigate from the root of ``_build_help_data()`` to the
    specific command dict, for example::

        ["commands", "create"]
        ["commands", "link", "subcommands", "create"]
        ["commands", "workflow", "subcommands", "types"]
    """
    _ensure_importable()
    # These imports live inside the tracker package – only available after the
    # path is set up above.
    from tracker.cli import _build_help_data  # type: ignore[import]
    from tracker.formatters import to_toon    # type: ignore[import]

    data = _build_help_data()
    node = _get_node(data, key_path)

    print(to_toon(node), end="")
    sys.exit(0)


# ── Invocation ────────────────────────────────────────────────────────────────


def run_tracker(command_prefix: list[str], extra_args: list[str]) -> int:
    """Invoke ``tracker.cli.main()`` with *command_prefix* + *extra_args*.

    Returns the integer exit code produced by ``main()``.
    """
    _ensure_importable()
    old_argv = sys.argv[:]
    sys.argv = ["tracker_cli.py"] + command_prefix + extra_args
    try:
        from tracker.cli import main  # type: ignore[import]
        return main()
    finally:
        sys.argv = old_argv


# ── Argument helpers ──────────────────────────────────────────────────────────


def check_help(args: list[str], script_name: str, key_path: list[str]) -> None:
    """Print TOON help and exit when ``--help``, ``-h``, or no args are given."""
    if not args or "--help" in args or "-h" in args:
        print_command_help(script_name, key_path)
