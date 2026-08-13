# PyPI release verification

The release workflow is tag-driven. A maintainer pushes `vX.Y.Z`; the workflow
builds the wheel and source archive, runs `twine check`, publishes to Test PyPI,
installs that exact version into a clean virtual environment, and runs
`pal-found-datasets --help`. Only that verified artifact is sent to PyPI.

Trusted publishing uses GitHub OIDC (`id-token: write`). No PyPI API token is
read by the workflow and no credential belongs in the repository or artifact.
The project name is `pal_found_cli`; legacy `foundry-*` entry points remain as
compatibility aliases until the separate rename migration is complete.
