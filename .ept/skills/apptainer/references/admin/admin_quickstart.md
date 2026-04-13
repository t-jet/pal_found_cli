[ Apptainer Admin Guide  ](<index.html>)

  * Admin Quickstart
    * Architecture of Apptainer
    * Apptainer Security
    * Installation
    * Configuration
    * Testing
  * [Installing Apptainer](installation.md)
  * [Migrating from Singularity](singularity_migration.md)
  * [Configuration files](configfiles.md)
  * [User Namespaces & Fakeroot](user_namespace.md)
  * [Security in Apptainer](security.md)
  * [Monitoring](monitoring.md)
  * [License](license.md)



__[Apptainer Admin Guide](<index.html>)

  * [](<index.html>)
  * Admin Quick Start
  * [ Edit on GitHub](<https://github.com/apptainer/apptainer-admindocs/blob/main/admin_quickstart.rst>)



* * *

# Admin Quick Start

This quick start gives an overview of installation of Apptainer, a description of the architecture of Apptainer, and pointers to configuration files. More information, including alternate installation options and detailed configuration options can be found later in this guide.

## Architecture of Apptainer

Apptainer is designed to allow containers to be executed as if they were native programs or scripts on a host system. No daemon is required to build or run containers, and the security model is compatible with shared systems.

As a result, integration with clusters and schedulers such as Univa Grid Engine, Torque, SLURM, SGE, and many others is as simple as running any other command. All standard input, output, errors, pipes, IPC, and other communication pathways used by locally running programs are synchronized with the applications running locally within the container.

Apptainer favors an ‘integration over isolation’ approach to containers. By default only the mount and user namespaces are isolated for containers, so that they have their own filesystem view. Access to hardware such as GPUs, high speed networks, and shared filesystems is easy and does not require special configuration. Default access to user home directories, `/tmp` space, and installation specific mounts makes it simple for users to benefit from the reproducibility of containerized applications without major changes to their existing workflows. Where more complete isolation is important, Apptainer can use additional Linux namespaces and other security and resource limits to accomplish this.

## Apptainer Security

See the [Security section](../user/security.md) of the user guide.

## Installation

Apptainer can be installed from source directly, by building an RPM or Debian package from the source, or by downloading pre-built packages. Linux distributions may also package Apptainer, but their packages may or may not be up-to-date with the upstream version on GitHub.

To install from source, follow the instructions in [INSTALL.md](<https://github.com/apptainer/apptainer/blob/main/INSTALL.md>) on GitHub. Other methods are discussed in the [Installation](installation.md#installation) section of this guide.

## Configuration

Apptainer is configured using files under `etc/apptainer` in your `--prefix`, or `--syconfdir` if you used that option with `mconfig`. In a default installation from source without a `--prefix` set you will find them under `/usr/local/etc/apptainer`. In a default installation from RPM or Deb packages you will find them under `/etc/apptainer`.

You can edit these files directly, or using the `Apptainer config global` command as the root user to manage them.

`apptainer.conf` contains the majority of options controlling the runtime behavior of Apptainer. Additional files control security, network, and resource configuration. Head over to the [Configuration files](configfiles.md#apptainer-configfiles) section where the files and configuration options are discussed.

## Testing

You can run a quick test of Apptainer using a small alpine container:
    
    
    $ apptainer exec docker://alpine cat /etc/alpine-release
    3.9.2
    

See the [user guide](<https://apptainer.org/docs/user/main>) for more information about how to use Apptainer.
