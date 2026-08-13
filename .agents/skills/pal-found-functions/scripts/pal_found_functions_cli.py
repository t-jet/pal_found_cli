#!/usr/bin/env python3
"""Launcher for the packaged Foundry Functions CLI."""

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT: str | None = None
_candidate = _SCRIPT_DIR
for _depth in range(8):
    if (_candidate / "src" / "pal_found_cli" / "__init__.py").exists():
        _PROJECT_ROOT = str(_candidate)
        break
    if _candidate.parent == _candidate:
        break
    _candidate = _candidate.parent
if _PROJECT_ROOT is None:
    _PROJECT_ROOT = str(_SCRIPT_DIR.parents[3])
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from pal_found_cli.functions.scripts.pal_found_functions_cli import (  # noqa: E402
    build_parser,
    console_main,
    main,
)

__all__ = ["build_parser", "console_main", "main"]


if __name__ == "__main__":
    raise SystemExit(console_main())

