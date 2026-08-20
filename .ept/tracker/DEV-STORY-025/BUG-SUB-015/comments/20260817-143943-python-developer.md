Subject: Reproduction and root cause
Created: 2026-08-17T14:39:43
Updated: 2026-08-17T14:39:43
---
Reproduced against all three canonical repositories with git check-ignore -v -- .env .env.local .env.production qa-private-key.pem qa-private-key.key qa-private-key.p12 qa-private-key.pfx plus tracked-file inventory checks. Root and tool ignore only .env and .env.local; both fail .env.production. Skills ignores neither .env nor .env.local, and also fails .env.production. All three fail the PEM, KEY, P12, and PFX fixtures. Root and tool intentionally track .env.example placeholders. No tracked live environment file, private key, or certificate container was found. The defect comes from narrow, inconsistent repository-local ignore rules and the absence of a regression gate that checks credential-like names and approved example exceptions across the split repositories.
