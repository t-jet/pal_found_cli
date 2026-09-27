#!/usr/bin/env python3
"""Thin entry point — delegates to ``tracker.cli.main()``.

This file preserves backward compatibility so that existing scripts and CI
pipelines calling ``python tracker_cli.py <args>`` continue to work.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the tracker package (sibling directory) is importable.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from tracker.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
