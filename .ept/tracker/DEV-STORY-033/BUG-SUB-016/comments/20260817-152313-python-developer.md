Subject: Fix plan
Created: 2026-08-17T15:23:13
Updated: 2026-08-17T15:23:13
---
Replace the Windows example with native PowerShell. Define source and destination variables with Join-Path, use -LiteralPath, verify the source directory and sentinel files before creating or changing the destination, create the destination explicitly, copy each skill directory in a loop, then verify the copied count and sentinels before printing success. Preserve the existing POSIX and Claude instructions. Add pytest coverage that extracts and executes the real published PowerShell block with workspace-path substitution; assert all 19 exact skill names and sentinels; rerun after corrupting a destination file to prove idempotent overwrite with no nested directories; and verify a bad source fails before any destination mutation. Run the full skills pytest suite, Ruff, Markdown and link checks, then repeat from a clean public clone. Publish the skills commit first and update the root gitlink afterward.
