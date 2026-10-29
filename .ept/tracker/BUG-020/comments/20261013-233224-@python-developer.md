Subject: Root cause and correction scope
Created: 2026-10-13T23:32:24
Updated: 2026-10-13T23:32:24
---
# Root cause
Models operation records copied SDK return names into CLI results and reused generic precondition/failure text. Models CLI _paginate_operation collects page data and main prints that list; PaginationHelper emits cursor metadata to stderr. BinaryDownloadHandler treats --output as a basename under configured download root. ResourceConfiguration requires memory and cpu.
# Correction
Update 14 QA-failed records in Models references only. Preserve SDK return names where useful but describe actual CLI output, input constraints, and recovery steps. Verify local gate and parser tests before requesting independent QA.
