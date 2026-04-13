# Singularity Compatibility
Since the community decided to [move the project into the Linux Foundation](https://apptainer.org/news/community-announcement-20211130) with the constraint of a name change to the project, it has been a goal of the project to minimize the impact to the user base. If you experience issues making the move, please reach out to the [community](https://apptainer.org/help) so we can help you!
## SIF Image Compatibility
The Apptainer project has decided to make no changes related to the project renaming at the image format level. This means that default metadata within SIF images and their filesystems will retain the `singularity` name without change. This will ensure that containers built with Apptainer will continue to work with installations of Singularity.
This decision was made to ensure that users can continue to package their applications and data with Apptainer without concerns of image format incompatibility when running in a different computing environment or collaborating with colleagues that still use a Singularity installation.
## Singularity Prefixed Environment Variable Support
Apptainer respects environment variables with the `SINGULARITY_` and `SINGULARITYENV_` prefixes when their respective `APPTAINER_` and `APPTAINERENV_` counterparts are not set.
This first command does not use any environment variable compatibility behavior as it is using the `APPTAINERENV_` prefix to command Apptainer to create an environment variable in the container with the name `FOO` and the value `BAR`:

```
$ APPTAINERENV_FOO=BAR apptainer exec docker://alpine env
[...]
FOO=BAR

```

We can see from the `env` output that this environment variable was properly set inside the container.
Next we can use the `SINGULARITYENV_` prefix to do the same thing, but this time we wil have the intended value be `BAZ`:

```
$ SINGULARITYENV_FOO=BAZ apptainer exec  docker://alpine env
WARNING: DEPRECATED USAGE: Forwarding SINGULARITYENV_FOO as environment variable will not be supported in the future, use APPTAINERENV_FOO instead
[...]
FOO=BAZ

```

Notice that we have a warning for `DEPRECATED USAGE` when doing so. This is because a future version of Apptainer may stop supporting environment variable compatibility once it is past this current period of transition.
Finally, if both are set, the value set by the `APPTAINERENV_` variable will take priority over the `SINGULARITYENV_` variable.

```
$ APPTAINERENV_FOO=BAR SINGULARITYENV_FOO=BAZ apptainer exec iqube_latest.sif env
WARNING: Skipping environment variable [SINGULARITYENV_FOO=BAZ], FOO is already overridden with different value [BAR]
[...]
FOO=BAR

```

In this case a warning is emitted to let the user know that two variables were set to create the same environment variable in the container in case they were unaware of one of them existing in their environment.
## Singularity Command Symlink
With the same intention as the environment variable handling, Apptainer installations will include a symlink to the `apptainer` binary named `singularity`. This will allow existing tooling and scripts using the `singularity` command to continue to operate after a migration to Apptainer has taken place. Below is an example of running the `version` command using either program name and getting the same output because we are running the same underlying binary:

```
$ apptainer --version
apptainer version 1.5.0-rc.1
$ singularity --version
apptainer version 1.5.0-rc.1

```

## Automatic User Configuration Migration
Apptainer stores user configuration in files and directories under `~/.apptainer`. Invocation of the `apptainer` command will automatically trigger Apptainer to create this directory, if it doesn’t exist. In order to ease the transition of users from Singularity to Apptainer, Apptainer will look for a `~/.singularity` directory when the `~/.apptainer` directory is being created and will migrate user configuration files and keyrings automatically. The following data will be migrated if it is found:
  * Remote endpoint configurations
  * OCI registry configurations stored in the Docker config format
  * Singularity Public PGP keyring
  * Singularity Private PGP keyring


Below we can see example output from when user configuration is being migrated:

```
$ apptainer exec docker://alpine echo
INFO:    Detected Singularity user configuration directory
INFO:    Detected Singularity remote configuration, migrating...
INFO:    Detected Singularity docker configuration, migrating...
INFO:    Detected public Singularity pgp keyring, migrating...
INFO:    Detected private Singularity pgp keyring, migrating...
INFO:    Converting OCI blobs to SIF format
INFO:    Starting build...
[...]

```

We can also see that subsequent use of Apptainer will not perform this migration again:

```
$ apptainer exec docker://alpine echo
WARNING: /usr/local/etc/singularity/ exists, migration to apptainer by system administrator is not complete
INFO:    Using cached SIF image
[...]

```

Note
Apptainer will not migrate cached container data such as OCI blobs and SIF images. User caches will need to be manually migrated or reconstructed through normal use of Apptainer.
The default remote configuration has changed in Apptainer, so if you did not previously set any remotes and want to continue to use the previous default for `library://` and/or pgp keys, see [Restoring pre-Apptainer library behavior](endpoint.md#restoring-pre-apptainer-library-behavior).
