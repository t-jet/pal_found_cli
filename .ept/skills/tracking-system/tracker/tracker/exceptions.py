"""Custom exception hierarchy for the tracker system."""

from __future__ import annotations


class TrackerError(Exception):
    """Base exception for all tracker operations."""


class ValidationError(TrackerError):
    """Raised when input validation fails (exit code 2)."""


class FileOperationError(TrackerError):
    """Raised when a file operation fails (exit code 4)."""


class ConfigurationError(TrackerError):
    """Raised when configuration is invalid or missing (exit code 3)."""
