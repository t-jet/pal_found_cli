Subject: Implementation and root-cause evidence
Created: 2026-08-17T14:45:22
Updated: 2026-08-17T14:45:22
---
Implemented and published the repository-hygiene fix in dependency order. Skills commit b961b2186ad2c8c98f67ab98d708beff6c944281, tool commit 0dd826b02c4489eb35aa45cf689efcad4b0c31c9, and root commit 1b20819d7993629faa9e85453f1c82189d665c4b, which pins both dependency commits. Each .gitignore now consistently ignores .env, .env.*, *.pem, *.key, *.p12, and *.pfx, while preserving .env.example and .env.template. Each repository adds 	ests/test_repository_hygiene.py for ignored patterns, template trackability, and tracked-file inventory. Root cause remains the previously documented narrow, inconsistent per-repository rules with no cross-repository regression gate.
