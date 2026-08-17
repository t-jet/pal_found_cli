# Mandatory instructions

## Required preparation

Skills located in the `.ept/skills` folder available to AI agents and should be used from this location. 
Review  the  `.ept/skills/skill-index.md` in this folder to find available skills. You must know they descriptions and be ready to use them before starting any activities.
Do it now to understand instructions in this file and your role.

Project skills live in `.agents/skills`. The old `.claude/skills` path contains
only a migration pointer; add or update skills in the canonical tree.

## Mandatory instructions for all agents

1. Always use the `caveman` skill in the `ultra` mode for internal thinking, reasoning and delegating tasks to subagents.
2. Always use the `caveman` skill in the `full` mode for chat responses.
3. Focus on maintainability and clarity while modifying the code or writing documentation.
4. Always use `humanizer` skill when working with documents and comments to ensure your output is concise, clear, and free of AI-like patterns. All deliverables must be fully understandable and maintainable by human contributors.

## Temporary files location

Use the `.ept/tmp` folder for temporary files. This folder is ignored by git and will be cleaned up automatically. Do not use any other location for temporary files.
