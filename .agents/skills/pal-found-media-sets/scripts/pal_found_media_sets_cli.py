#!/usr/bin/env python3
"""Thin launcher for packaged Foundry Media Sets CLI."""

from pal_found_cli.media_sets.scripts.pal_found_media_sets_cli import (
    build_parser,
    console_main,
    main,
)

__all__ = ["build_parser", "console_main", "main"]


if __name__ == "__main__":
    raise SystemExit(console_main())
