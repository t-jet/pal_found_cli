"""Build-queue command handler for the tracking CLI.

This module contains the handler for the build-queue command.
"""

from __future__ import annotations

import argparse

from ..build_queue import build_queue
from ..exceptions import ValidationError


def handle_build_queue(
    args: argparse.Namespace,
    bq_parser: argparse.ArgumentParser,
) -> None:
    """Handle the 'build-queue' command and its subcommands.
    
    Args:
        args: Parsed command-line arguments
        bq_parser: The argument parser for the build-queue command (for help)
    
    Raises:
        ValidationError: If subcommand is missing
    """
    if not args.build_queue_command:
        bq_parser.print_help()
        raise ValidationError("build-queue subcommand required")
    
    author = getattr(args, "author", "build-queue") or "build-queue"
    stage = args.build_queue_command
    
    # Call build_queue with appropriate stage
    build_queue(author=author, stage=stage)
