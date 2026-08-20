Subject: Implementation and root cause
Created: 2026-08-17T13:47:24
Updated: 2026-08-17T13:47:24
---
Root cause

Earlier split work registered empty destination gitlinks and public repository names, but never migrated the content or its history. Root therefore remained the owner of tool source, tests, package metadata, and skills.

Implementation

Used temporary git-filter-repo clones to extract tool and skills histories, then merged each filtered lineage into the published destination main branch without squashing. The existing public commits ac9c03f and dcbdb4e remain ancestors. No history rewrite or force push was used.

Final commits are root 240898c5daa7ed693e969369141d66e6e5123b6f, tool 370c971b4d05340d80a0dad009bc8b4c0233d345, and skills 34b6c404994cdcc4f97b18d2a493fff6c1d3d895. Root now owns zero moved source, test, skill, or package-metadata paths. The tool repository owns its source, tests, package metadata, CI, and documentation. The skills repository owns 19 skills plus its tests and validation CI.

Cross-repository references, DEV-024, DEV-027, and the document index were updated. The fix also corrected the Linux mypy lock import and replaced invalid setup-python and Codecov pins with verified commit SHAs.
