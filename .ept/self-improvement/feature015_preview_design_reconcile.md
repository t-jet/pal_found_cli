## Improvement: Reconcile API warnings with design omissions

Condition:
- When archived design excludes SDK parameter needed by published endpoint contract

Action:
- Do verify each affected endpoint and SDK wire serialization, record a linked design correction, and identify QA cases that encode the old rule before retest.
