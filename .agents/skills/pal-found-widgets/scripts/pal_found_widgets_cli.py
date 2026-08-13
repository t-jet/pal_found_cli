#!/usr/bin/env python3
"""Thin launcher for packaged Foundry Widgets CLI."""

from pal_found_cli.widgets.scripts.pal_found_widgets_cli import (  # noqa: E402
    build_parser,
    console_main,
    main,
)

__all__ = ["build_parser", "console_main", "main"]


if __name__ == "__main__":
    raise SystemExit(console_main())
