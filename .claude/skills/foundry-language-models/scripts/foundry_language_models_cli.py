#!/usr/bin/env python3
"""Thin launcher for packaged Foundry Language Models CLI."""

from foundry_cli.language_models.scripts.foundry_language_models_cli import (
    build_parser,
    console_main,
    main,
)

__all__ = ["build_parser", "console_main", "main"]


if __name__ == "__main__":
    raise SystemExit(console_main())
