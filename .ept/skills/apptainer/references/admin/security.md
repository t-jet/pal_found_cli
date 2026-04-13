[ Apptainer Admin Guide  ](<index.html>)

  * [Admin Quickstart](admin_quickstart.md)
  * [Installing Apptainer](installation.md)
  * [Migrating from Singularity](singularity_migration.md)
  * [Configuration files](configfiles.md)
  * [User Namespaces & Fakeroot](user_namespace.md)
  * Security in Apptainer
    * Configuration & Runtime Options
  * [Monitoring](monitoring.md)
  * [License](license.md)



__[Apptainer Admin Guide](<index.html>)

  * [](<index.html>)
  * Security in Apptainer
  * [ Edit on GitHub](<https://github.com/apptainer/apptainer-admindocs/blob/main/security.rst>)



* * *

# Security in Apptainer

First please see the [Security section](../user/security.md) of the user guide.

## Configuration & Runtime Options

System administrators who manage Apptainer can use configuration files to set security restrictions, grant or revoke a user’s capabilities, manage resources and authorize containers etc.

For example, the [Execution Control List](configfiles.md#execution-control-list) file allows restricting usage of SIF containers based on their signature and the key used to sign them.

Configuration files and their parameters are [documented for administrators here](configfiles.md#apptainer-configfiles).

When running a container as root, Apptainer can apply hardening rules using seccomp and apparmor. Please see the [Security Options section](../user/security_options.md) of the user guide.

Limits on resource usage by containers can be enforced using cgroups. On systems that use cgroups v1, only the root user can set resource limits. On systems that use cgroups v2 and systemd, all users can apply resource limits as long as the system is configured for delegation to non-root users.

By default, EL9, Ubuntu 22.04, Debian 11, Fedora 31 and newer use cgroups v2 and are configured so that non-root users will be able to use the `--memory-*` and `--pids-limit` flags of Apptainer or limit those aspects with the `--apply-cgroups` flag. To enable the other resource limits follow the ‘Enabling CPU, CPUSET, and I/O delegation’ step at the [rootless containers website](<https://rootlesscontaine.rs/getting-started/common/cgroup2/>).

On EL8 and Ubuntu 20.04 it is possible to set up a compatible configuration by also following the ‘Enabling cgroup v2’ step at the above website.

See the [Limiting Container Resources section](../user/cgroups.md) of the user guide for more details of how to apply cgroups limits to containers at runtime.
