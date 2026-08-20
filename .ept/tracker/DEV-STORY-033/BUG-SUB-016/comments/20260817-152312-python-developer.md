Subject: Reproduction, root cause, and application logs
Created: 2026-08-17T15:23:12
Updated: 2026-08-17T15:23:12
---
Reproduced with the literal published README block on PowerShell 7.6.5. The block exits successfully but copies 0 skill folders. After the documented cd, Get-ChildItem enumerates the repository root instead of .agents/skills. The trailing POSIX backslash is parsed by PowerShell as the path '\', so the pipeline searches the drive root rather than continuing the command. Expected: copy exactly 19 published skill folders or fail before changing the destination. Actual: exit success, 0 copied folders, and no useful failure message. A corrected control that reads .agents/skills copies 19. This is the root cause; repository publication and anonymous clone access are healthy.
