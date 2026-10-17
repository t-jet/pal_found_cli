## Improvement: exercise first-use races

Condition:
- When reviewing cross-process index locks and atomic writes

Action:
- Do pause one actor before its read or write, let another finish, then resume against an isolated fixture; verify retained rows, not only exit codes.
