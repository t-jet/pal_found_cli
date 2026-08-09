#!/usr/bin/env python3
"""Thin launcher for packaged Foundry Models CLI."""

from foundry_cli.models.scripts.foundry_models_cli import (
    build_parser,
    console_main,
    main,
)

__all__ = ["build_parser", "console_main", "main"]


if __name__ == "__main__":
    raise SystemExit(console_main())
