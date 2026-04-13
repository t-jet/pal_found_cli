---
name: apptainer
description: >
  Expert knowledge for Apptainer (container platform). Use this skill whenever the user asks about
  Apptainer containers, SIF images, container builds, def files, running containers on HPC clusters,
  GPU/CUDA/ROCm workloads in containers, MPI parallel jobs, bind mounts, persistent overlays, fakeroot,
  container instances/services, signing/verifying images, OCI/Docker compatibility, or Apptainer
  administration (apptainer.conf, security, user namespaces). Also use for Singularity questions since
  Apptainer is its direct successor and highly compatible. Covers both user and admin perspectives.
---

# Apptainer Expert Skill

Apptainer is a container platform designed for HPC and scientific computing. Key differentiators:
- **No daemon required** — containers run like regular processes; integrates naturally with schedulers (Slurm, SGE, PBS)
- **Single-file SIF format** — portable, immutable, cryptographically signable
- **Integration over isolation** — home directory, `/tmp`, GPUs, and high-speed networks available by default
- **Same user inside and outside** — no privilege escalation; you cannot become root by running a container
- **Direct Docker/OCI compatibility** — pull and run Docker Hub images natively

---

## Core Concepts

### SIF (Singularity Image Format)
- Default output of `apptainer build`: compressed, read-only, portable `.sif` file
- Can embed definition file, labels, runscript, environment, overlays, and signatures
- Use `apptainer inspect` to view metadata, labels, runscript, and the embedded def file

### Container execution modes
| Command | What it does |
|---------|-------------|
| `apptainer run <image>` | Executes the `%runscript` defined in the image |
| `apptainer exec <image> <cmd>` | Runs a specific command inside the container |
| `apptainer shell <image>` | Opens an interactive shell inside the container |
| `apptainer instance start <image> <name>` | Starts a background service (daemon) |

### URI schemes for images
```
docker://ubuntu:22.04                        # Docker Hub
docker://registry.example.com/myimage:tag   # Private registry
oras://ghcr.io/org/image:tag                # OCI registry (ORAS)
library://lolcow                             # Apptainer library
shub://user/repo                             # Singularity Hub (legacy)
ipfs://<CID>                                 # IPFS
```

---

## Common Patterns and Recipes

### HPC batch job (Slurm)
```bash
#!/bin/bash
#SBATCH --gpus=1
module load apptainer
apptainer exec --nv --bind /scratch/$USER:/data \
  tensorflow.sif python3 /data/train.py
```

### Interactive development workflow
```bash
# 1. Build a sandbox for exploration
apptainer build --sandbox myenv/ docker://ubuntu:22.04
# 2. Modify interactively
apptainer shell --writable --fakeroot myenv/
# 3. Convert to production SIF via def file (for reproducibility)
apptainer build myenv.sif myenv.def
```

### Converting between formats
```bash
apptainer build myimage.sif docker://myimage:tag   # Docker image → SIF
apptainer build --sandbox mydir/ myimage.sif       # SIF → sandbox
apptainer build myimage.sif mydir/                 # Sandbox → SIF
```

---

## Reference Documentation

For detailed information, consult the reference files below. Each covers a complete topic area.

### User Guide

| File | Description |
|------|-------------|
| [references/user/introduction.md](references/user/introduction.md) | Overview of Apptainer's purpose, design goals, and why it is suited for HPC and shared systems. |
| [references/user/quick_start.md](references/user/quick_start.md) | Installation overview and first steps for pulling, running, building, and interacting with containers. |
| [references/user/build_a_container.md](references/user/build_a_container.md) | All `apptainer build` workflows: from Docker Hub, OCI registries, sandboxes, definition files, and Dockerfiles; all build flags. |
| [references/user/definition_files.md](references/user/definition_files.md) | Complete reference for def file structure (`%post`, `%environment`, `%files`, `%runscript`, multi-stage builds, bootstrap agents, template arguments). |
| [references/user/build_env.md](references/user/build_env.md) | Customizing the build environment: cache location, Docker credentials, temporary directories, and remote build options. |
| [references/user/bind_paths_and_mounts.md](references/user/bind_paths_and_mounts.md) | System and user-defined bind mounts, `--bind`, `--mount`, `APPTAINER_BINDPATH`, and disabling default bind paths. |
| [references/user/environment_and_metadata.md](references/user/environment_and_metadata.md) | Setting and overriding environment variables at build time and runtime (`APPTAINERENV_`, `--env`, `--env-file`), labels, and container metadata inspection. |
| [references/user/gpu.md](references/user/gpu.md) | Running NVIDIA CUDA (`--nv`, `--nvccli`) and AMD ROCm (`--rocm`) GPU workloads, including host driver requirements and OpenCL support. |
| [references/user/mpi.md](references/user/mpi.md) | MPI parallel job patterns: hybrid model (host MPI launches container), bind model, and example definition files for MPICH/OpenMPI. |
| [references/user/persistent_overlays.md](references/user/persistent_overlays.md) | Creating and using ext3 overlay images and in-memory `--writable-tmpfs` to add a writable layer on top of an immutable SIF. |
| [references/user/running_services.md](references/user/running_services.md) | Starting, managing, and stopping background container instances (`apptainer instance start/list/stop`) for services like web servers. |
| [references/user/fakeroot.md](references/user/fakeroot.md) | How fakeroot works (rootless, root-mapped namespace, fakeroot command), when each mode is used, and how to build/install packages as a non-root user. |
| [references/user/security_options.md](references/user/security_options.md) | Runtime security flags: Linux capabilities (`--add-caps`, `--drop-caps`), SELinux/AppArmor/seccomp profiles, and `--allow-setuid`. |
| [references/user/security.md](references/user/security.md) | Apptainer's security model: why containers run as the invoking user, setuid vs. user-namespace modes, and the security policy. |
| [references/user/encryption.md](references/user/encryption.md) | Building and running encrypted containers using a passphrase or RSA PEM key, with notes on privileged vs. unprivileged encryption. |
| [references/user/signNverify.md](references/user/signNverify.md) | Signing SIF images with PGP or X.509 keys, verifying signatures, and using the Execution Control List (ECL) to enforce trusted containers. |
| [references/user/docker_and_oci.md](references/user/docker_and_oci.md) | Pulling and running Docker Hub and OCI registry images, private registry authentication, and a Dockerfile-vs-def-file comparison. |
| [references/user/oci_runtime.md](references/user/oci_runtime.md) | The `apptainer oci` command group for strict OCI Runtime Specification compliance and OCI registry authentication via `--authfile`. |
| [references/user/networking.md](references/user/networking.md) | CNI-based network virtualization, `--net`, `--dns`, `--network`, `--network-args`, and port mapping for containers. |
| [references/user/registry.md](references/user/registry.md) | Managing OCI registry credentials with `apptainer registry login/logout` and using `--authfile` for custom credential files. |
| [references/user/endpoint.md](references/user/endpoint.md) | Managing remote service endpoints (Library API registries, OCI registries, keyservers) with `apptainer remote`. |
| [references/user/keyserver.md](references/user/keyserver.md) | Configuring and ordering keyservers used for signature verification with `apptainer keyserver add/remove/list`. |
| [references/user/key_commands.md](references/user/key_commands.md) | Importing, exporting, and managing PGP keys in the local and global keyrings for container signing and ECL. |
| [references/user/library_api.md](references/user/library_api.md) | Pushing and pulling SIF images to/from Library API registries using `apptainer push` and `apptainer pull`. |
| [references/user/cgroups.md](references/user/cgroups.md) | Limiting container CPU, memory, and other resources via per-resource flags or a `cgroups.toml` file; cgroups v2 requirements. |
| [references/user/checkpoint.md](references/user/checkpoint.md) | Experimental checkpoint/restore feature using DMTCP to save and resume containerized application state across failures or preemptions. |
| [references/user/peertopeer.md](references/user/peertopeer.md) | Using IPFS peer-to-peer gateways as a source for container images via the `ipfs://` URI scheme. |
| [references/user/plugins.md](references/user/plugins.md) | Installing and using Apptainer plugins that extend CLI commands, container configuration, or image driver behavior at runtime. |
| [references/user/singularity_compatibility.md](references/user/singularity_compatibility.md) | Compatibility guarantees between Apptainer and Singularity: SIF image format compatibility and `SINGULARITY_`/`SINGULARITYENV_` environment variable support. |
| [references/user/appendix.md](references/user/appendix.md) | Alphabetical reference of all `APPTAINER_*` environment variables and their effect on builds and container execution. |
| [references/user/cli.md](references/user/cli.md) | Links to the auto-generated CLI reference for every `apptainer` subcommand (build, exec, shell, run, instance, cache, key, etc.). |
| [references/user/contributing.md](references/user/contributing.md) | How to contribute to the Apptainer project: community channels, filing issues, writing documentation, and submitting code. |

### Admin Guide

| File | Description |
|------|-------------|
| [references/admin/admin_quickstart.md](references/admin/admin_quickstart.md) | High-level architecture overview for admins: Apptainer's security model, installation essentials, configuration, and a quick validation test. |
| [references/admin/installation.md](references/admin/installation.md) | Full installation instructions: system requirements, installing from source or pre-built packages (RPM/Deb), fakeroot setup, and uninstalling. |
| [references/admin/configfiles.md](references/admin/configfiles.md) | Complete reference for all Apptainer configuration files: `apptainer.conf` options, `ecl.toml`, `capability.json`, `cgroups.toml`, bind management, and networking options. |
| [references/admin/user_namespace.md](references/admin/user_namespace.md) | Enabling and configuring user namespaces and rootless fakeroot, including `/etc/subuid`/`/etc/subgid` setup and `apptainer config fakeroot`. |
| [references/admin/security.md](references/admin/security.md) | Admin perspective on Apptainer security: configuration options that affect security posture, setuid vs. rootless operation, and runtime hardening. |
| [references/admin/monitoring.md](references/admin/monitoring.md) | Monitoring container usage and resource consumption on a system with Apptainer, including available audit hooks. |
| [references/admin/singularity_migration.md](references/admin/singularity_migration.md) | Steps and considerations for migrating an HPC site from Singularity to Apptainer, including configuration file differences and compatibility notes. |
