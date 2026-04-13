# Build a Container
The `build` command is the “Swiss army knife” of container creation. You can use it to download and assemble existing containers from external resources like [Docker Hub](https://hub.docker.com/) and other OCI registries. You can use it to convert containers between the formats supported by Apptainer. And you can use it in conjunction with a [Apptainer definition](definition_files.md#definition-files) file to create a container from scratch and customized it to fit your needs.
## Overview
The `build` command accepts a target as input and produces a container as output.
The type of target given determines the method that `build` will use to create the container. It can be one of the following:
  * URI beginning with **docker://** to build from Docker Hub
  * URI beginning with **oras://** to build from an OCI registry that supports OCI Artifacts
  * URI beginning with **ipfs://** to build from an IPFS cluster that supports CID images
  * URI beginning with **library://** to build from the Container Library
  * URI beginning with **shub://** to build from Singularity Hub
  * path to an **existing container** on your local machine
  * path to a **directory** to build from a sandbox
  * path to a [Apptainer definition file](definition_files.md#definition-files)


`build` can produce containers in two different formats, which can be specified as follows:
  * a compressed read-only **Singularity Image File (SIF)** format, suitable for production _(default)_
  * a writable **(ch)root directory** called a sandbox, for interactive development ( `--sandbox` option)


Because `build` can accept an existing container as a target and create a container in either supported format, you can use it to convert existing containers from one format to another.
Note
Apptainer leverages the user namespace kernel feature to give the illusion of elevated privileges while building containers. On some systems, the user namespace may be incompletely configured for individual users. In this case, Apptainer may bind mount the `fakeroot` program from the host into the container during the build, and this might fail in some containers with mismatching libraries. See the [fakeroot documentation](fakeroot.md#fakeroot) for more details.
## Downloading an existing container from Docker Hub
You can use `build` to download layers from Docker Hub and assemble them into Apptainer containers.

```
$ apptainer build alpine.sif docker://alpine

```

## Specifying an architecture
By default, `apptainer build` from a `docker://` URI will attempt to fetch a container that matches the architecture of your host system. If you need to retrieve a container that does not have the same architecture as your host (e.g. an `arm64` container on an `amd64` host), you can use the `--arch` options.

```
$ apptainer build --arch arm64 alpine.sif docker://alpine

```

Or to build an `arm32` container by using the `--arch-variant` option:

```
$ apptainer build --arch arm --arch-variant 7 alpine.sif docker://alpine

```

See [Specifying an architecture](docker_and_oci.md#specifying-an-architecture) and [CPU emulation](docker_and_oci.md#cpu-emulation) for more details.
## Downloading an existing container from a Library API Registry
If you have set up a library remote endpoint as described in [Managing Remote Endpoints](endpoint.md#sec-managing-remote-endpoints), you can use the build command to download a container from the Container Library.

```
$ apptainer build lolcow.sif library://lolcow

```

The first argument (`lolcow.sif`) specifies the path and name for your container. The second argument (`library://lolcow`) gives the Container Library URI from which to download. By default, the container will be converted to a compressed, read-only SIF. If you want your container in a writable format, use the `--sandbox` option.
## Creating writable `--sandbox` directories
If you want to create a container within a writable directory (called a _sandbox_) you can do so with the `--sandbox` option.

```
$ apptainer build --sandbox alpine/ docker://alpine

```

The resulting directory operates just like a container in a SIF file. To make persistent changes within the sandbox container, use the `--writable` flag when you invoke your container.

```
$ apptainer shell --writable alpine/

```

## Converting containers from one format to another
If you already have a container saved locally, you can use it as a target to build a new container. This allows you convert containers from one format to another. For example, if you had a sandbox container called `development/` and you wanted to convert it to a SIF container called `production.sif`, you could do so as follows:

```
$ apptainer build production.sif development/

```

Use care when converting a sandbox directory to the default SIF format. If changes were made to the writable container before conversion, there is no record of those changes in the Apptainer definition file, which compromises the reproducibility of your container. It is therefore preferable to build production containers directly from an Apptainer definition file instead.
## Building containers from Apptainer definition files
Apptainer definition files are the most powerful type of target when building a container. For detailed information on writing Apptainer definition files, please see the [Container Definitions documentation](definition_files.md). Suppose you already have the following container definition file called, `lolcow.def`, and you want to use it to build a SIF container:

```
Bootstrap: docker
From: ubuntu:20.04

%post
    apt-get -y update
    apt-get -y install cowsay lolcat

%environment
    export LC_ALL=C
    export PATH=/usr/games:$PATH

%runscript
    date | cowsay | lolcat

```

You can do so with the following command.

```
$ apptainer build lolcow.sif lolcow.def

```

## Building containers from Dockerfile with BuildKit
Apptainer can also build directly from an existing Dockerfile, by using an already running BuildKit daemon (or Docker daemon) process. For detailed information on Apptainer definition files vs Dockerfile, please see [Docker and OCI](docker_and_oci.md). Suppose you already have the following file called `Dockerfile`, and you want to use it to build a SIF container:

```
FROM ubuntu:20.04

RUN apt-get -y update && \
    apt-get -y install cowsay lolcat

ENV LC_ALL=C \
    PATH=/usr/games:$PATH

CMD date | cowsay | lolcat

```

You can do so with the following command.

```
$ apptainer build lolcow.sif dockerfile:.

```

## Alternative compressors
It is possible to use different compressors, see [--mksquashfs-args](build_a_container.md#mksquashfs-args):  
Compressors  
| `-comp`  | Default Level  | Optimized For  | Additional Notes  |  
| --- | --- | --- | --- |  
| `gzip`  | 9  | Compatibility  | Default  |  
| `lzo`  | 8  | Speed  | Obsolete (Use `lz4`)  |  
| `lz4`  | 1  | Speed  | Fastest  |  
| `xz`  | 6  | Size  | Obsolete (Use `zstd`)  |  
| `zstd`  | 15  | Size  | Smallest  |  
Example: `--mksquashfs-args="-comp gzip -Xcompression-level 1"` (`--fast` instead of `--best`)
The different compressors have (very) different compression levels, see the help text for each.
Note
Beware that it is possible to build an image on a host and have the image not work on a different host. This could be because of the default compressor supported by the host. For example, when building an image on a host in which the default compressor is `xz` and then trying to run that image on a node where the only compressor available is `gzip`.
## Building encrypted containers
With Apptainer it is possible to build and run encrypted containers. Encrypted containers are decrypted at runtime entirely in memory, meaning that no intermediate decrypted data is ever written to disk. See [encrypted containers](encryption.md#encryption) for more details.
## Build options
###  `--build-arg`
Specifies values of [defined template variables](definition_files.md#id2) in the definition file. Values passed via `--build-arg` follow the form of `variable=value`. Multiple `--build-arg` options are acceptable for build command.
###  `--build-arg-file`
Similar to `--build-arg` but specifiles values of defined template variables via a file, which contains multiple `variable=value` entries.
###  `--warn-unused-build-args`
By default, when users provide unused variables to the build process, fatal errors will return. This option makes the build process show warnings instead of returning fatal errors.
###  `--encrypt`
Specifies that Apptainer should use a secret saved in either the `APPTAINER_ENCRYPTION_PASSPHRASE` or `APPTAINER_ENCRYPTION_PEM_PATH` environment variable to build an encrypted container. See [encrypted containers](encryption.md#encryption) for more details.
###  `--fakeroot`
Gives users a way to build containers without root privileges. This option is implied when an unprivileged user invokes build on a definition file. See [the fakeroot feature](fakeroot.md#fakeroot) for details.
###  `--force`
The `--force` option will delete and overwrite an existing Apptainer image without presenting the normal interactive confirmation prompt.
###  `--json`
The `--json` option will force Apptainer to interpret a given definition file as JSON.
###  `--library`
This command allows you to set a different image library. Look [here](library_api.md#library-api-registries) for more information.
###  `--mksquashfs-args`
Extra arguments to pass to `mksquashfs`` when creating SIF files.
To show the available arguments, see the manual page or help:

```
$ mksquashfs -help

```

For instance, to limit the number of processors use `-processors`:

```
-processors <number>    use <number> processors.  By default will use number of
                        processors available

```

You might also be interested in the compressors and their options:

```
-comp <comp>            select <comp> compression
                        Compressors available:
                                gzip (default)
                                lzo
                                lz4
                                xz
                                zstd

-no-compression         do not compress any of the data or metadata.  This is
                        equivalent to specifying -noI -noD -noF and -noX

```

To show help about the options available for selected compressor:

```
$ mksquashfs squashfs-root out.squashfs -comp zstd -Xhelp

```

Non-gzip squashfs compression might not work with some installations. However, note that by default the apptainer command now uses its own bundled recent version of mksquashfs that should have the maximum compressors enabled. So you might want to explore the help on that version, for example by setting its directory early in your PATH like this:

```
$ PATH=$(apptainer buildcfg | sed -n 's,^LIBEXECDIR=\(.*\),\1/apptainer/bin,p'):$PATH

```

Also note that by using non-default compression methods that the resulting SIF file might not be usable by installations that do not have the decompression method available. This can be especially true for older versions of apptainer.
###  `--notest`
If you don’t want to run the `%test` section during the container build, you can skip it using the `--notest` option. For instance, you might be building a container intended to run in a production environment with GPUs, while your local build resource does not have GPUs. You want to include a `%test` section that runs a short validation, but you don’t want your build to exit with an error because it cannot find a GPU on your system. In such a scenario, passing the `--notest` flag would be appropriate.
###  `--passphrase`
This flag allows you to pass a plaintext passphrase to encrypt the container filesystem at build time. See [encrypted containers](encryption.md#encryption) for more details.
###  `--pem-path`
This flag allows you to pass the location of a public key to encrypt the container file system at build time. See [encrypted containers](encryption.md#encryption) for more details.
###  `--sandbox`
Build a sandbox (container in a directory) instead of the default SIF format.
###  `--section`
Instead of running the entire definition file, only run a specific section or sections. This option accepts a comma-delimited string of definition file sections. Acceptable arguments include `all`, `none` or any combination of the following: `setup`, `post`, `files`, `environment`, `test`, `labels`.
Under normal build conditions, the Apptainer definition file is saved into a container’s metadata so that there is a record of how the container was built. The `--section` option may render this metadata inaccurate, compromising reproducibility, and should therefore be used with care.
###  `--update`
You can build into the same sandbox container multiple times (though the results may be unpredictable, and under most circumstances, it is preferable to delete your container and start from scratch).
By default, if you build into an existing sandbox container, the `build` command will prompt you to decide whether or not to overwrite existing container data. Instead of this behavior, you can use the `--update` option to build _into_ an existing container. This will cause Apptainer to skip the definition-file’s header, and build any sections that are in the definition file into the existing container.
The `--update` option is only valid when used with sandbox containers.
###  `--nv`
This flag allows you to mount the Nvidia CUDA libraries from your host environment into your build environment. Libraries are mounted during the execution of `post` and `test` sections.
Note
This option can’t be set via the environment variable APPTAINER_NV. Apptainer will attempt to bind binaries listed in APPTAINER_CONFDIR/nvliblist.conf, if the mount destination doesn’t exist inside the container, they are ignored.
###  `--nvccli`
Experimental option to use Nvidia’s `nvidia-container-cli` for GPU setup. See more details in the [GPU Support](gpu.md#gpu) section.
###  `--rocm`
This flag allows you to mount the AMD Rocm libraries from your host environment into your build environment. Libraries are mounted during the execution of `post` and `test` sections.
Note
This option can’t be set via the environment variable APPTAINER_ROCM. Apptainer will attempt to bind binaries listed in APPTAINER_CONFDIR/rocmliblist.conf, if the mount destination doesn’t exist inside the container, they are ignored.
###  `--bind`
This flag allows you to mount a directory, file or image during build. It works the same way as `--bind` for the `shell`, `exec` and `run` subcommands of Apptainer, and can be specified multiple times. See [user defined bind paths](bind_paths_and_mounts.md#user-defined-bind-paths). Bind mounts occur during the execution of `post` and `test` sections.
Note
This option can’t be set via the environment variables APPTAINER_BIND and APPTAINER_BINDPATH
**Beware that the mount points must exist in the built image** prior to executing `post` and `test`. So if you want to bind `--bind /example` and it doesn’t exist in the bootstrap image, you have to workaround that by adding a `setup` section:

```
%setup
  mkdir $APPTAINER_ROOTFS/example

```

Note
Binding your directory to /mnt is another workaround, as this directory is often present in distribution images and is intended for that purpose, you could avoid the directory creation in the definition file.
###  `--writable-tmpfs`
This flag will run the `%test` section of the build with a writable `tmpfs` overlay filesystem in place. This allows the tests to create files, which will be discarded at the end of the build. Other portions of the build do not use this temporary filesystem.
## More Build topics
  * If you want to **customize the cache location** (where Docker layers are downloaded on your system), specify Docker credentials, or apply other custom tweaks to your build environment, see [build environment](build_env.md#build-environment).
  * If you want to make internally **modular containers** , check out the Getting Started guide [here](https://sci-f.github.io/tutorials).
  * If you want to **build a container with an encrypted file system** consult the Apptainer documentation on encryption [here](encryption.md#encryption).


