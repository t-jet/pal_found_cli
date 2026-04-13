[ Apptainer Admin Guide  ](<index.html>)

  * [Admin Quickstart](admin_quickstart.md)
  * [Installing Apptainer](installation.md)
  * Migrating from Singularity
  * [Configuration files](configfiles.md)
  * [User Namespaces & Fakeroot](user_namespace.md)
  * [Security in Apptainer](security.md)
  * [Monitoring](monitoring.md)
  * [License](license.md)



__[Apptainer Admin Guide](<index.html>)

  * [](<index.html>)
  * Migrating From Singularity
  * [ Edit on GitHub](<https://github.com/apptainer/apptainer-admindocs/blob/main/singularity_migration.rst>)



* * *

# Migrating From Singularity

Since the community decided to [move the project into the Linux Foundation](<https://apptainer.org/news/community-announcement-20211130>) with the constraint of a name change to the project, it has been a goal of the project to minimize the impact to the user base. If you experience issues making the move, please reach out to the [community](<https://apptainer.org/help>) so we can help you!

When migrating to Apptainer from Singularity, administrators that have modified the system configurations of their installation and want Apptainer to have identical configuration will need to migrate the configurations they have in place for Singularity to Apptainer. An exception is an RPM update from an already-installed singularity package; in that case, the RPM will automatically import the old configuration, but an administrator should verify the conversion.

All singularity system configuration files are typically located under `/etc/singularity` or `/usr/local/etc/singularity` when installed from a RPM/Deb package or source respectively, but options passed during source installations could cause this to be in another location. Apptainer will store its configurations in similar locations, but within a directory named `apptainer` instead of `singularity`.

Note

The `singularity` configuration directory at the prefix corresponding to your `apptainer` configuration directory (e.g. `/etc/singularity` or `/usr/local/etc/singularity`) needs to be manually removed to prevent Apptainer from producing a message at runtime about the cleanup being incomplete.

All system configuration names, file formats, and parameters for Apptainer are identical to their Singularity counterparts with the exception of `singularity.conf`, which has been renamed to `apptainer.conf` as a part of the project renaming. It is important to note that comments within `apptainer.conf` have been changed and the default contents of `remote.yaml` has changed. So, while you can copy files around, we **recommend** applying the same configuration changes to the new files instead of simply copying contents.

Warning

Take care to not wipe out all configuration in the Apptainer config directory as a part of your migration because it will remove configuration files that are new to the project like configurations for [checkpointing](configfiles.md#dmtcp-configuration).

If you are migrating from an installation with default configuration, there is no need to perform any configuration migration.

However, a big change from Singularity is that Apptainer does not install a setuid-root component by default. That means that either user namespaces needs to be enabled or the setuid-root component needs to be installed separately. See the [User Namespaces & Fakeroot](user_namespace.md#userns) section, or to find out about how to install the setuid-root component see the [Installation](installation.md#installation) section. An exception is with RPM packaging when updating from the `singularity` package: that case installs the `apptainer-suid` package by default, but since setuid-root is a higher security risk, consider removing that package after upgrade.

Also see the user guide documentation about [Singularity compatibility](../user/singularity_compatibility.md) for information about how the migration to Apptainer will impact users. In particular the system administrator may want to [restore pre-Apptainer library behavior](configfiles.md#no-default-remote) for all users.
