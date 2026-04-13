# Appendix
## Apptainer’s environment variables
Apptainer comes with some environment variables you can set or modify depending on your needs. You can see them listed alphabetically below with their respective functionality.
###  `A`
  1. **APPTAINER_ADD_CAPS** : To specify a list (comma separated string) of capabilities to be added. Default is an empty string.
  2. **APPTAINER_ALL** : List all the users and groups capabilities.
  3. **APPTAINER_ALLOW_SETUID** : To specify that setuid binaries should or not be allowed in the container. (root only) Default is set to false.
  4. **APPTAINER_ALLOW_UNSIGNED** : Set to true to allow pushing unsigned SIF images to a `library://` destination. Default is false.
  5. **APPTAINER_APP** and **APPTAINER_APPNAME** : Sets the name of an application to be run inside a container.
  6. **APPTAINER_APPLY_CGROUPS** : Used to apply cgroups from an input file for container processes. (it requires root privileges)
  7. **APPTAINER_PULL_ARCH** : Set the architecture (e.g. `arm64`) of an image to pull from a `library://` or OCI source. Defaults to the host architecture.
  8. **APPTAINER_AUTHFILE** : Specify a non-standard location for storing / reading login credentials for OCI/Docker registries. See the [authfile documentation](registry.md#sec-authfile).


###  `B`
  1. **APPTAINER_BIND** and **APPTAINER_BINDPATH** : Comma separated string `source:<dest>` list of paths to bind between the host and the container, applied in that order. Note that `APPTAINER_BIND` is also automatically set inside a container to list all the paths bound to it, so that by default all the same binds will be applied to nested apptainer commands.
  2. **APPTAINER_BLKIO_WEIGHT** : Specify a relative weight for block device access during contention. Range 10-1000. Default is 0 (disabled).
  3. **APPTAINER_BLKIO_WEIGHT_DEVICE** : Specify a relative weight for block device access during contention on a specific device. Must be supplied in `<device path>:weight` format. Default is unset.
  4. **APPTAINER_BOOT** : Set to false by default, considers if executing `/sbin/init` when container boots (root only).
  5. **APPTAINER_BUILDKIT_HOST** : Host address / socket to use when building images from a `buildkit` or `dockerfile` source. `BUILDKIT_HOST` without the `APPTAINER_` prefix is also accepted.


###  `C`
  1. **APPTAINER_CACHEDIR** : Specifies the directory for image downloads to be cached in. See [Cache Folders](build_env.md#sec-cache).
  2. **APPTAINER_CAP_GROUP** : Specify a group to modify when managing permitted capabilities with the `capability` command.
  3. **APPTAINER_CAP_USER** : Specify a user to modify when managing permitted capabilities with the `capability` command.
  4. **APPTAINER_CLEANENV** : Specifies if the environment should be cleaned or not before running the container. Default is set to false.
  5. **APPTAINER_COMPAT** : Set to true to enable Docker/OCI compatibility mode. Equivalent to setting `--containall --no-eval --no-init --no-umask --writable-tmpfs`. Default is false.
  6. **APPTAINER_CONFIG_FILE** : Use a custom `apptainer.conf` configuration file. Only supported for non-root users in non-setuid mode.
  7. **APPTAINER_CONFIGDIR** : Specifies the directory to use for per-user configuration. The default is `$HOME/.apptainer`.
  8. **APPTAINER_CONTAIN** : To use minimal `/dev` and empty other directories (e.g. `/tmp` and `$HOME`) instead of sharing filesystems from your host. Default is set to false.
  9. **APPTAINER_CONTAINALL** : To contain not only file systems, but also PID, IPC, and environment. Default is set to false.
  10. **APPTAINER_CONTAINLIBS** : Used to specify a string of file names (comma separated string) to bind to the `/.singularity.d/libs` directory.
  11. **APPTAINER_CPU_SHARES** : Specify a relative share of CPU time available to the container. Default is -1 (disabled).
  12. **APPTAINER_CPUS** : Specify a fractional number of CPUs available to the container. Default is unset.
  13. **APPTAINER_CPUSET_CPUS** : Specify a list or range of CPU cores available to the container. Default is unset.
  14. **APPTAINER_CPUSET_MEMS** : Specify a list or range of memory nodes available to the container. Default is unset.
  15. **APPTAINER_CWD** (deprecated **APPTAINER_PWD** and **APPTAINER_TARGET_PWD**): The initial working directory for payload process inside the container.


###  `D`
  1. **APPTAINER_DEBUG** : Enable debug output when set. Equivalent to `-d / --debug`.
  2. **APPTAINER_DEFFILE** : Shows the Apptainer recipe that was used to generate the image.
  3. **APPTAINER_DESC** : Contains a description of the capabilities.
  4. **APPTAINER_DISABLE_CACHE** : To disable all caching of docker/oci, library, oras, etc. downloads and built SIFs. Default is set to false.
  5. **APPTAINER_DNS** : A list of the DNS server addresses separated by commas to be added in `resolv.conf`.
  6. **APPTAINER_DOCKER_HOST** : Host address / socket to use when pulling images from a `docker-daemon` source. `DOCKER_HOST` without the `APPTAINER_` prefix is also accepted.
  7. **APPTAINER_DOCKER_LOGIN** : To specify the interactive prompt for docker authentication.
  8. **APPTAINER_DOCKER_PASSWORD** : To specify the password for docker authentication. `DOCKER_PASSWORD` without the `APPTAINER_` prefix is also accepted.
  9. **APPTAINER_DOCKER_USERNAME** : To specify the username for docker authentication. `DOCKER_USERNAME` without the `APPTAINER_` prefix is also accepted.
  10. **APPTAINER_DOWNLOAD_CONCURRENCY** : To specify how many concurrent streams when downloading (pulling) an image from cloud library.
  11. **APPTAINER_DOWNLOAD_PART_SIZE** : To specify the size of each part (bytes) when concurrent downloads are enabled.
  12. **APPTAINER_DOWNLOAD_BUFFER_SIZE** : To specify the transfer buffer size (bytes) when concurrent downloads are enabled.
  13. **APPTAINER_DROP_CAPS** : To specify a list (comma separated string) of capabilities to be dropped. Default is an empty string.


###  `E`
  1. **APPTAINER_ENCRYPTION_PASSPHRASE** : Used to specify the plaintext passphrase to encrypt the container.
  2. **APPTAINER_ENCRYPTION_PEM_DATA** : If it contains data from a public PEM file, Apptainer can use those data to encrypt a container. If it contains data from a private PEM file, Apptainer will try to use the data to run an encrypted container.
  3. **APPTAINER_ENCRYPTION_PEM_PATH** : Used to specify the path of the file containing public or private key to encrypt the container in PEM format.
  4. **APPTAINER_ENV_FILE** : Specify a file containing `KEY=VAL` environment variables that should be set in the container.
  5. **APPTAINER_ENVIRONMENT** : Set during a build to the path to a file into which `KEY=VAL` environment variables can be added. The file is evaluated at container startup.
  6. **APPTAINERENV_*** : Allows you to transpose variables into the container at runtime. You can see more in detail how to use this variable in our [environment and metadata section](environment_and_metadata.md#environment-and-metadata).
  7. **APPTAINERENV_APPEND_PATH** : Used to append directories to the end of the `$PATH` environment variable. You can see more in detail on how to use this variable in our [environment and metadata section](environment_and_metadata.md#environment-and-metadata).
  8. **APPTAINERENV_PATH** : A specified path to override the `$PATH` environment variable within the container. You can see more in detail on how to use this variable in our [environment and metadata section](environment_and_metadata.md#environment-and-metadata).
  9. **APPTAINERENV_PREPEND_PATH** : Used to prepend directories to the beginning of `$PATH` environment variable. You can see more in detail on how to use this variable in our [environment and metadata section](environment_and_metadata.md#environment-and-metadata).


###  `F`
  1. **APPTAINER_FAKEROOT** : Run or build a container using a user namespace with a root uid/gid mapping.
  2. **APPTAINER_FIXPERMS** : Set to true to ensure owner has `rwX` permissions on all files in a container built from an OCI source.
  3. **APPTAINER_FORCE** : Skip confirmation for destructive actions, e.g. overwriting a container image or killing an instance.
  4. **APPTAINER_FUSESPEC** : A FUSE filesystem mount specification of the form ‘<type>:<fuse command> <mountpoint>’, that will be mounted in the container.


###  `H`
  1. **APPTAINER_HELPFILE** : Specifies the runscript helpfile, if it exists.
  2. **APPTAINER_HOME** : A home directory specification, it could be a source or destination path. The source path is the home directory outside the container and the destination overrides the home directory within the container.
  3. **APPTAINER_HOSTNAME** : The container’s hostname.


###  `I`
  1. **APPTAINER_IMAGE** : Filename of the container.


###  `J`
  1. **APPTAINER_JSON** : Use JSON as an input or output format. Applies to the `build` and `instance list` commands. Default is false.


###  `K`
  1. **APPTAINER_KEEP_PRIVS** : To let root user keep privileges in the container. Default is set to false.


###  `L`
  1. **APPTAINER_LABELS** : Specifies the labels associated with the image.
  2. **APPTAINER_LIBRARY** : Specifies the library to pull from. Default is set to our Cloud Library.
  3. **APPTAINER_LOCAL_VERIFY** : Set to true to only use the local keyring when verifying PGP signed SIF images. Disables retrieval of public keys from configured keyservers. Default is false.
  4. **APPTAINER_LOGIN_USERNAME** : Set the username to use when logging in to a remote endpoint, registry, or keyserver.
  5. **APPTAINER_LOGIN_PASSWORD** : Set the password to use when logging in to a remote endpoint, registry, or keyserver.
  6. **APPTAINER_LOGIN_INSECURE** : Set to true to use HTTP (not HTTPS) when logging in to a remote endpoint. Default is false.
  7. **APPTAINER_LOGS** : Set to true to show the path to instance log files in `instance list` output. Default is false.


###  `M`
  1. **APPTAINER_MEMORY** : Specify a memory limit in bytes for the container. Default is unset (no limit).
  2. **APPTAINER_MEMORY_RESERVATION** : Specify a memory soft limit in bytes for the container. Default is unset (no limit).
  3. **APPTAINER_MEMORY_SWAP** : Specify a limit for memory + swap usage by the container. Default is unset. Effect depends on **APPTAINER_MEMORY**.
  4. **APPTAINER_MESSAGELEVEL** : Set numeric message level for output. Message levels are Fatal=-4, Error=-3, Warn=-2, Log=-1, Info=1, Verbose=2, Verbose2=3, Verbose3=4, Debug=5.
  5. **APPTAINER_MOUNT** : To specify host to container mounts, using the syntax understood by the `--mount` flag. Multiple mounts should be separated by newline characters.


###  `N`
  1. **APPTAINER_NAME** : Specifies a custom image name.
  2. **APPTAINER_NETWORK** : Used to specify a desired network. If more than one parameters is used, addresses should be separated by commas, where each network will bring up a dedicated interface inside the container.
  3. **APPTAINER_NETWORK_ARGS** : To specify the network arguments to pass to CNI plugins.
  4. **APPTAINER_NOCLEANUP** : To not clean up the bundle after a failed build, this can be helpful for debugging. Default is set to false.
  5. **APPTAINER_NOCOLOR** : Print mesages without color output. Default is set to false unless stderr is not a terminal.
  6. **APPTAINER_NO_HTTPS** and **APPTAINER_NOHTTPS** : Set to true to use HTTP (not HTTPS) to communicate with registry servers. Default is false.
  7. **APPTAINER_NO_EVAL** : Set to true in order to prevent Apptainer performing shell evaluation on environment variables / runscript arguments at startup.
  8. **APPTAINER_NO_HOME** : Considers not mounting users home directory if home is not the current working directory. Default is set to false.
  9. **APPTAINER_NO_INIT** and **APPTAINER_NOSHIMINIT** : Considers not starting the `shim` process with `--pid`.
  10. **APPTAINER_NO_MOUNT** : Disable an automatic mount that has been set in `apptainer.conf`. Accepts `proc / sys / dev / devpts / home / tmp / hostfs / cwd`, or the source path for a system specific bind.
  11. **APPTAINER_NO_NV** : Flag to disable Nvidia support. Opposite of `APPTAINER_NV`.
  12. **APPTAINER_NO_PID** : Set to true to disable the PID namespace, when it is inferred by other options (e.g.``–containall`` )
  13. **APPTAINER_NO_PRIVS** : To drop all the privileges from root user in the container. Default is false.
  14. **APPTAINER_NOTEST** : Set to true to disable execution of `%test` sections when building a container.
  15. **APPTAINER_NO_UMASK** : Set to true to prevent host umask propagating to container, and use a default 0022 umask instead. Default is false.
  16. **APPTAINER_NV** : To enable Nvidia GPU support. Default is set to false.
  17. **APPTAINER_NVCCLI** : To use nvidia-container-cli for container GPU setup (experimental, only unprivileged).


###  `O`
  1. **APPTAINER_OOM_KILL_DISABLE** : Set to true to disable OOM killer for container processes, if possible. Default is false.
  2. **APPTAINER_OVERLAY** and **APPTAINER_OVERLAYIMAGE** : To indicate the use of an overlay file system image for persistent data storage or as read-only layer of container.


###  `P`
  1. **APPTAINER_PULLDIR** and **APPTAINER_PULLFOLDER** : Specify destination directory when pulling a container image.
  2. **APPTAINER_PID_FILE** : When starting an instance, write the instance PID to the specified file.
  3. **APPTAINER_PIDS_LIMIT** : Specify maximum number of processes that the container may spawn. Default is 0 (no limit).


###  `Q`
  1. **APPTAINER_QUIET** : Suppresses all Info messages. Default is set to false.


###  `R`
  1. **APPTAINER_ROOTFS** : During a build `APPTAINER_ROOTFS` is set to the path of the rootfs for the container. It can be used within a definition file to manipulate the rootfs (e.g. from the `%setup` section).
  2. **APPTAINER_ROCM** : Set to true to expose ROCm devices and libraries inside the container. Default is false.
  3. **APPTAINER_RUNSCRIPT** : Specifies the runscript of the image.


###  `S`
  1. **APPTAINER_SANDBOX** : Set to true to specify that the format of the image should be a sandbox. Default is set to false.
  2. **APPTAINER_SCRATCH** and **APPTAINER_SCRATCHDIR** : Used to include a scratch directory within the container that is linked to a temporary directory. (use -W to force location)
  3. **APPTAINER_SECTION** : Set to specify a comma separated string of all the sections to be run from the deffile (setup, post, files, environment, test, labels, none)
  4. **APPTAINER_SECURITY** : Used to enable security features. (SELinux, Apparmor, Seccomp)
  5. **APPTAINER_SECRET** : Lists all the private keys instead of the default which display the public ones.
  6. **APPTAINER_SHELL** : The path to the program to be used as an interactive shell.
  7. **APPTAINER_SIGNAL** : Specifies a signal sent to the instance.
  8. **APPTAINER_SILENT** : Suppresses all Info and Warning messages. Default is set to false.
  9. **APPTAINER_SIGNAL** : Specifies the signal to send to an instance with `apptainer instance stop`.
  10. **APPTAINER_SIGN_KEY** : Set the path to a key file to be used when signing a SIF image.
  11. **APPTAINER_SPARSE** : Set to true to create sparse overlay image files with the `apptainer overlay create` command.
  12. **APPTAINER_SHARENS** : Share the namespace and image with other containers launched from the same parent process.


###  `T`
  1. **APPTAINER_TEST** : Specifies the test script for the image.
  2. **APPTAINER_TMPDIR** : Specify a location for temporary files to be used when pulling and building container images. See [Temporary Folders](build_env.md#sec-temporaryfolders).


###  `U`
  1. **APPTAINER_UNSHARE_PID** : To specify that the container will run in a new PID namespace. Default is set to false.
  2. **APPTAINER_UNSHARE_IPC** : To specify that the container will run in a new IPC namespace. Default is set to false.
  3. **APPTAINER_UNSHARE_NET** : To specify that the container will run in a new network namespace (sets up a bridge network interface by default). Default is set to false.
  4. **APPTAINER_UNSHARE_UTS** : To specify that the container will run in a new UTS namespace. Default is set to false.
  5. **APPTAINER_UNSQUASH** : To convert SIF files to temporary sandboxes before running a container. Default is set to false.
  6. **APPTAINER_UPDATE** : To run the definition over an existing container (skips the header). Default is set to false.
  7. **APPTAINER_URL** : Specifies the key server `URL`.
  8. **APPTAINER_USER** : As root, specify a user to manage that user’s instances with the `instance` commands.
  9. **APPTAINER_USERNS** and **APPTAINER_UNSHARE_USERNS** : To specify that the container will run in a new user namespace, allowing Apptainer to run completely unprivileged even with a setuid installation. Default is set to false.


###  `V`
  1. **APPTAINER_VERBOSE** : Print additional information. Default is set to false.


###  `V`
  1. **APPTAINER_VERIFY_CERTIFICATE** : Set the path to a PEM file containing the certificate to be used when verifying an x509 signed SIF image.
  2. **APPTAINER_VERIFY_INTERMEDIATES** : Set the path to a PEM file containing an intermediate certificate / chain to be used when verifying an x509 signed SIF image.
  3. **APPTAINER_VERIFY_KEY** : Set the path to a key file to be used when verifying a key signed SIF image.
  4. **APPTAINER_VERIFY_OCSP** : Set to true to enable OCSP verification of certificates. Default is false.
  5. **APPTAINER_VERIFY_ROOTS** : Set the path to a PEM file containing root certificate(s) to be used when verifying an x509 signed SIF image.


###  `W`
  1. **APPTAINER_WORKDIR** : The working directory to be used for `/tmp`, `/var/tmp` and `$HOME` (if `-c` or `--contain` was also used)
  2. **APPTAINER_WRITABLE** : By default, all Apptainer containers are available as read only, this option makes the file system accessible as read/write. Default set to false.
  3. **APPTAINER_WRITABLE_TMPFS** : Makes the file system accessible as read-write with non-persistent data (with overlay support only). Default is set to false.


## Build Modules
###  `library` bootstrap agent
#### Overview
You can use an existing container in a Container Library as your “base” and then add customization. This allows you to build multiple images from the same starting point. For example, you may want to build several containers with the same custom python installation, the same custom compiler toolchain, or the same base MPI installation. Instead of building these from scratch each time, you could create a base container in the Container Library and then build new containers from that existing base container adding customizations in `%post`, `%environment`, `%runscript`, etc.
This requires setting up a Container Library as shown in the [Managing Remote Endpoints](endpoint.md#sec-managing-remote-endpoints) section.
#### Keywords

```
Bootstrap: library

```

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

```
From: <entity>/<collection>/<container>:<tag>

```

The `From` keyword is mandatory. It specifies the container to use as a base. `entity` is optional and defaults to `library`. `collection` is optional and defaults to `default`. This is the correct namespace to use for some official containers (`alpine` for example). `tag` is also optional and will default to `latest`.

```
Library: http://custom/library

```

The Library keyword is mandatory. It is the URL for the library server.

```
Fingerprints: 22045C8C0B1004D058DE4BEDA20C27EE7FF7BA84

```

The Fingerprints keyword is optional. It specifies one or more comma separated fingerprints corresponding to PGP public keys. If present, the bootstrap image will be verified and the build will only proceed if it is signed by keys matching _all_ of the specified fingerprints.
###  `docker` bootstrap agent
#### Overview
Docker images are comprised of layers that are assembled at runtime to create an image. You can use Docker layers to create a base image, and then add your own custom software. For example, you might use Docker’s Ubuntu image layers to create an Ubuntu Apptainer container. You could do the same with Fedora, Debian, Arch, Suse, Alpine, BusyBox, etc.
Or maybe you want a container that already has software installed. For instance, maybe you want to build a container that uses CUDA and cuDNN to leverage the GPU, but you don’t want to install from scratch. You can start with one of the `nvidia/cuda` containers and install your software on top of that.
Or perhaps you have already invested in Docker and created your own Docker containers. If so, you can seamlessly convert them to Apptainer with the `docker` bootstrap module.
#### Keywords

```
Bootstrap: docker

```

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

```
From: <registry>/<namespace>/<container>:<tag>@<digest>

```

The `From` keyword is mandatory. It specifies the container to use as a base. `registry` is optional and defaults to `index.docker.io`. `namespace` is optional and defaults to `library`. This is the correct namespace to use for some official containers (ubuntu for example). `tag` is also optional and will default to `latest`
See [Apptainer and Docker](docker_and_oci.md#docker-and-oci) for more detailed info on using Docker registries.

```
Registry: http://custom_registry

```

The Registry keyword is optional. It will default to `index.docker.io`.

```
Namespace: namespace

```

The Namespace keyword is optional. It will default to `library`.
#### Notes
Docker containers are stored as a collection of tarballs called layers. When building from a Docker container the layers must be downloaded and then assembled in the proper order to produce a viable file system. Then the file system must be converted to Singularity Image File (sif) format.
For detailed information about setting your build environment see [Build Customization](build_env.md#build-environment).
###  `shub` bootstrap agent
#### Overview
You can use an existing container on Singularity Hub as your “base” and then add customization. This allows you to build multiple images from the same starting point. For example, you may want to build several containers with the same custom python installation, the same custom compiler toolchain, or the same base MPI installation. Instead of building these from scratch each time, you could create a base container on Singularity Hub and then build new containers from that existing base container adding customizations in `%post` , `%environment`, `%runscript`, etc.
#### Keywords

```
Bootstrap: shub

```

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

```
From: shub://<registry>/<username>/<container-name>:<tag>@digest

```

The `From` keyword is mandatory. It specifies the container to use as a base. `registry is optional and defaults to ``singularity-hub.org`. `tag` and `digest` are also optional. `tag` defaults to `latest` and `digest` can be left blank if you want the latest build.
#### Notes
When bootstrapping from a Singularity Hub image, all previous definition files that led to the creation of the current image will be stored in a directory within the container called `/.singularity.d/bootstrap_history`. Apptainer will also alert you if environment variables have been changed between the base image and the new image during bootstrap.
###  `oras` bootstrap agent
#### Overview
Using, this module, a container from supporting OCI Registries - Eg: ACR (Azure Container Registry), local container registries, etc can be used as your “base” image and later customized. This allows you to build multiple images from the same starting point. For example, you may want to build several containers with the same custom python installation, the same custom compiler toolchain, or the same base MPI installation. Instead of building these from scratch each time, you could make use of `oras` to pull an appropriate base container and then build new containers by adding customizations in `%post` , `%environment`, `%runscript`, etc.
#### Keywords

```
Bootstrap: oras

```

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

```
From: registry/namespace/image:tag

```

The `From` keyword is mandatory. It specifies the container to use as a base. Also,``tag`` is mandatory that refers to the version of image you want to use.

```
Fingerprints: 22045C8C0B1004D058DE4BEDA20C27EE7FF7BA84

```

The Fingerprints keyword is optional. It specifies one or more comma separated fingerprints corresponding to PGP public keys. If present, the SIF file will be verified and the build will only proceed if it is signed by keys matching _all_ of the specified fingerprints.
###  `localimage` bootstrap agent
This module allows you to build a container from an existing Apptainer container on your host system. The name is somewhat misleading because your container can be in either image or directory format.
#### Overview
You can use an existing container image as your “base”, and then add customization. This allows you to build multiple images from the same starting point. For example, you may want to build several containers with the same custom python installation, the same custom compiler toolchain, or the same base MPI installation. Instead of building these from scratch each time, you could start with the appropriate local base container and then customize the new container in `%post`, `%environment`, `%runscript`, etc.
#### Keywords

```
Bootstrap: localimage

```

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

```
From: /path/to/container/file/or/directory

```

The `From` keyword is mandatory. It specifies the local container to use as a base.

```
Fingerprints: 22045C8C0B1004D058DE4BEDA20C27EE7FF7BA84

```

The Fingerprints keyword is optional. It specifies one or more comma separated fingerprints corresponding to PGP public keys. If present, and the `From:` keyword points to a SIF format image, it will be verified and the build will only proceed if it is signed by keys matching _all_ of the specified fingerprints.
#### Notes
When building from a local container, all previous definition files that led to the creation of the current container will be stored in a directory within the container called `/.singularity.d/bootstrap_history`. Apptainer will also alert you if environment variables have been changed between the base image and the new image during bootstrap.
###  `yum` or `dnf` bootstrap agent
This module allows you to build a Red Hat style container from a mirror URI based on yum or dnf.
#### Overview
Use the `yum` or `dnf` module to specify a base for a RHEL-like container. You must also specify the URI for the mirror you would like to use.
#### Keywords

```
Bootstrap: yum

```

or

```
Bootstrap: dnf

```

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

```
OSVersion: 9

```

The OSVersion keyword is optional. It specifies the OS version you would like to use. It is only required if you have specified a %{OSVERSION} variable in the `MirrorURL` keyword.

```
MirrorURL: http://repo.almalinux.org/almalinux/%{OSVERSION}/BaseOS/x86_64/os

```

The MirrorURL keyword is mandatory. It specifies the URI to use as a mirror to download the OS. If you define the `OSVersion` keyword, then you can use it in the URI as in the example above.

```
Include: dnf

```

The Include keyword is optional. It allows you to install additional packages into the core operating system. It is a best practice to supply only the bare essentials such that the `%post` section has what it needs to properly complete the build. One common package you may want to install when using the `yum` or `dnf` build module is YUM or DNF itself.
#### Notes
There is a major limitation with using YUM/DNF to bootstrap a container. The RPM database that exists within the container will be created using the RPM library and Berkeley DB implementation that exists on the host system. If the RPM implementation inside the container is not compatible with the RPM database that was used to create the container, RPM and YUM/DNF commands inside the container may fail. This issue can be easily demonstrated by bootstrapping an older RHEL compatible image by a newer one (e.g. bootstrap a RHEL 8 container from a RHEL 9 host).
In order to use the `yum` or `dnf` build module, you must have `yum` or `dnf` installed on your system. It may seem counter-intuitive to install YUM or DNF on a system that uses a different package manager, but you can do so. For instance, on Ubuntu you can install it like so:

```
$ sudo apt-get update && sudo apt-get install dnf

```

When building a container as an unprivileged user using this bootstrap, not all of the fakeroot modes work well. See [Building container images](fakeroot.md#build) for details.
###  `debootstrap` build agent
This module allows you to build a Debian/Ubuntu style container from a mirror URI.
#### Overview
Use the `debootstrap` module to specify a base for a Debian-like container. You must also specify the OS version and a URI for the mirror you would like to use.
#### Keywords

```
Bootstrap: debootstrap

```

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

```
OSVersion: xenial

```

The OSVersion keyword is mandatory. It specifies the OS version you would like to use. For Ubuntu you can use code words like `trusty` (14.04), `xenial` (16.04), and `yakkety` (17.04). For Debian you can use values like `stable`, `oldstable`, `testing`, and `unstable` or code words like `wheezy` (7), `jesse` (8), and `stretch` (9).
> 
```
MirrorURL:  http://us.archive.ubuntu.com/ubuntu/

```

The MirrorURL keyword is mandatory. It specifies a URI to use as a mirror when downloading the OS.

```
Include: somepackage

```

The Include keyword is optional. It allows you to install additional packages into the core operating system. It is a best practice to supply only the bare essentials such that the `%post` section has what it needs to properly complete the build.
#### Notes
In order to use the `debootstrap` build module, you must have `debootstrap` installed on your system. On Ubuntu you can install it like so:

```
$ sudo apt-get update && sudo apt-get install debootstrap

```

On RHEL you can install it from the epel repos like so:

```
$ sudo dnf update && sudo dnf install epel-release && sudo dnf install debootstrap.noarch

```

When building a container as an unprivileged user using this bootstrap, not all of the fakeroot modes work well. See [Building container images](fakeroot.md#build) for details.
###  `arch` bootstrap agent
This module allows you to build a Arch Linux based container.
#### Overview
Use the `arch` module to specify a base for an Arch Linux based container. Arch Linux uses the aptly named `pacman` package manager (all puns intended).
#### Keywords

```
Bootstrap: arch

```

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.
The Arch Linux bootstrap module does not name any additional keywords at this time. By defining the `arch` module, you have essentially given all of the information necessary for that particular bootstrap module to build a core operating system.
#### Notes
Arch Linux is, by design, a very stripped down, light-weight OS. You may need to perform a significant amount of configuration to get a usable OS. Please refer to this [README.md](https://github.com/apptainer/apptainer/blob/main/examples/arch/README.md) and the [Arch Linux example](https://github.com/apptainer/apptainer/blob/main/examples/arch/) for more info.
###  `busybox` bootstrap agent
This module allows you to build a container based on BusyBox.
#### Overview
Use the `busybox` module to specify a BusyBox base for container. You must also specify a URI for the mirror you would like to use.
#### Keywords

```
Bootstrap: busybox

```

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

```
MirrorURL: https://www.busybox.net/downloads/binaries/1.35.0-x86_64-linux-musl/busybox

```

The MirrorURL keyword is mandatory. It specifies a URI to use as a mirror when downloading the OS.
#### Notes
You can build a fully functional BusyBox container that only takes up ~700kB of disk space!
###  `zypper` bootstrap agent
This module allows you to build a Suse style container from a mirror URI.
Note
`zypper` version 1.11.20 or greater is required on the host system, as Apptainer requires the `--releasever` flag.
#### Overview
Use the `zypper` module to specify a base for a Suse-like container. You must also specify a URI for the mirror you would like to use.
#### Keywords

```
Bootstrap: zypper

```

The Bootstrap keyword is always mandatory. It describes the bootstrap module to use.

```
OSVersion: 42.2

```

The OSVersion keyword is optional. It specifies the OS version you would like to use. It is only required if you have specified a %{OSVERSION} variable in the `MirrorURL` keyword.

```
Include: somepackage

```

The Include keyword is optional. It allows you to install additional packages into the core operating system. It is a best practice to supply only the bare essentials such that the `%post` section has what it needs to properly complete the build. One common package you may want to install when using the zypper build module is `zypper` itself.
###  `docker-daemon` bootstrap agent
#### Overview
`docker-daemon` allows you to build a SIF from any Docker image currently residing in the Docker daemon’s internal storage:

```
$ docker images alpine
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
alpine              latest              965ea09ff2eb        7 weeks ago         5.55MB

$ apptainer run docker-daemon:alpine:latest
INFO:    Converting OCI blobs to SIF format
INFO:    Starting build...
Getting image source signatures
Copying blob 77cae8ab23bf done
Copying config 759e71f0d3 done
Writing manifest to image destination
Storing signatures
2019/12/11 14:53:24  info unpack layer: sha256:eb7c47c7f0fd0054242f35366d166e6b041dfb0b89e5f93a82ad3a3206222502
INFO:    Creating SIF file...
[=====================================================================] 100 % 0s
Apptainer>

```

The `APPTAINER_DOCKER_HOST` or `DOCKER_HOST` environment variables may be set to instruct Apptainer to pull images from a Docker daemon that is not running at the default location. For example, when using a virtualized Docker you may be instructed to set `DOCKER_HOST` e.g.

```
To connect the Docker client to the Docker daemon, please set
export DOCKER_HOST=tcp://192.168.59.103:2375

```

#### Keywords
In a definition file, the `docker-daemon` bootstrap agent requires the source container reference to be provided with the `From:` keyword:

```
Bootstrap: docker-daemon
From: <image>:<tag>

```

where both `<image>` and `<tag>` are mandatory fields that must be written explicitly.
###  `docker-archive` bootstrap agent
#### Overview
The `docker-archive` bootstrap agent allows you to create a Apptainer image from a docker image stored in a `docker save` formatted tar file:
The alternative bootstrap agent `oci-archive` can also be used with these, since Docker saves archives compatible with _both_ formats (since version 25).

```
$ docker save -o alpine.tar alpine:latest

$ apptainer run docker-archive:$(pwd)/alpine.tar
INFO:    Converting OCI blobs to SIF format
INFO:    Starting build...
Getting image source signatures
Copying blob 77cae8ab23bf done
Copying config 759e71f0d3 done
Writing manifest to image destination
Storing signatures
2019/12/11 15:25:09  info unpack layer: sha256:eb7c47c7f0fd0054242f35366d166e6b041dfb0b89e5f93a82ad3a3206222502
INFO:    Creating SIF file...
[=====================================================================] 100 % 0s
Apptainer>

```

#### Keywords
In a definition file, the `docker-archive` bootstrap agent requires the path to the tar file containing the image to be specified with the `From:` keyword.

```
Bootstrap: docker-archive
From: <path-to-tar-file>

```

###  `dockerfile` bootstrap agent
#### Overview
The `dockerfile` bootstrap agent allows you to create a Apptainer image from a Dockerfile stored in a build context directory (which can be `.`):
It is an alias for the `buildkit` bootstrap agent, since BuildKit is also known from the `docker buildx` plugin that has replaced `docker build`.

```
$ cat Dockerfile
FROM alpine
CMD ["echo", "Hello", "World"]

$ apptainer build hello-world.sif dockerfile:.
INFO:    Starting build...
INFO:    Building OCI image...
[+] Building 1.6s (5/5) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 80B
 => [internal] load metadata for docker.io/library/alpine:latest
 => [internal] load .dockerignore
 => => transferring context: 2B
 => CACHED [1/1] FROM docker.io/library/alpine:latest@sha256:25109184c71bdad752c8312a8623239686a9a2071e8825f20acb8f2198c3f659
 => => resolve docker.io/library/alpine:latest@sha256:25109184c71bdad752c8312a8623239686a9a2071e8825f20acb8f2198c3f659
 => exporting to oci image format
 => => exporting layers
 => => exporting manifest sha256:54abfa35ab6a349b9e10226b913f3f13733630dcdbc4338056aa63c4e499cc28
 => => exporting config sha256:92a056a793e53aac2acbdbe429709a76eaab586e634833866eca773d30236bd0
 => => sending tarball
INFO:    Extracting OCI image...
INFO:    Inserting Apptainer configuration...
INFO:    Creating SIF file...
[=====================================================================] 100 % 0s
INFO:    Build complete: hello-world.sif

$ apptainer run hello-world.sif
Hello World

```

The `APPTAINER_BUILDKIT_HOST` or `BUILDKIT_HOST` environment variables may be set to instruct Apptainer to build images with a BuildKit daemon that is not running at the default location. For example, when using a rootless BuildKit daemon started with `rootlesskit buildkitd &`:

```
export BUILDKIT_HOST=unix:///run/user/1000/buildkit/buildkitd.sock

```

The `DOCKER_BUILDKIT` and `DOCKER_HOST` environment variables may also be set to use an already existing Docker daemon _instead_ of a BuildKit daemon, but some features like the build log will be missing.

```
export DOCKER_BUILDKIT=1 DOCKER_HOST=unix:///run/user/1000/docker.sock

```

#### Keywords
In a definition file, the `dockerfile` bootstrap agent requires the path to the build context directory containing the Dockerfile to be specified with the `From:` keyword.

```
Bootstrap: dockerfile
From: <path-to-build-context>

```

###  `scratch` bootstrap agent
The scratch bootstrap agent allows you to start from a completely empty container. You are then responsible for adding any and all executables, libraries etc. that are required. Starting with a scratch container can be useful when you are aiming to minimize container size, and have a simple application / static binaries.
#### Overview
A minimal container providing a shell can be created by copying the `busybox` static binary into an empty scratch container:

```
Bootstrap: scratch

%setup
    # Runs on host - fetch static busybox binary
    curl -o /tmp/busybox https://www.busybox.net/downloads/binaries/1.31.0-i686-uclibc/busybox
    # It needs to be executable
    chmod +x /tmp/busybox

%files
    # Copy from host into empty container
    /tmp/busybox /bin/sh

%runscript
   /bin/sh

```

The resulting container provides a shell, and is 696KiB in size:

```
$ ls -lah scratch.sif
-rwxr-xr-x. 1 dave dave 696K May 28 13:29 scratch.sif

$ apptainer run scratch.sif
WARNING: passwd file doesn't exist in container, not updating
WARNING: group file doesn't exist in container, not updating
Apptainer> echo "Hello from a 696KiB container"
Hello from a 696KiB container

```

#### Keywords

```
Bootstrap: scratch

```

There are no additional keywords for the scratch bootstrap agent.
#### Notes
When building a container as an unprivileged user using this bootstrap, not all of the fakeroot modes work well. See [Building container images](fakeroot.md#build) for details.
