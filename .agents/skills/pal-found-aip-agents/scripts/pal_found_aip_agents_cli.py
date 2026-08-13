#!/usr/bin/env python3
"""Thin launcher for packaged Foundry AIP Agents CLI."""

from pal_found_cli.aip_agents.scripts.pal_found_aip_agents_cli import (
    build_parser,
    console_main,
    main,
)

__all__ = ["build_parser", "console_main", "main"]


if __name__ == "__main__":
    raise SystemExit(console_main())
