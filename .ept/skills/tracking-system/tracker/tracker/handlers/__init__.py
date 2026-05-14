"""Command handlers for the tracking system CLI.

This package contains modularized command handlers to keep the CLI module
organized and maintainable. Each module focuses on a specific command group.
"""

from __future__ import annotations

__all__ = [
    "handle_create",
    "handle_get",
    "handle_list",
    "handle_update",
    "handle_search",
    "handle_link",
    "handle_comment",
    "handle_workflow",
    "handle_type_info",
    "handle_build_queue",
]

from .ticket_handlers import (
    handle_create,
    handle_get,
    handle_list,
    handle_search,
    handle_update,
)
from .link_handlers import handle_link
from .comment_handlers import handle_comment
from .workflow_handlers import handle_workflow, handle_type_info
from .build_queue_handler import handle_build_queue
