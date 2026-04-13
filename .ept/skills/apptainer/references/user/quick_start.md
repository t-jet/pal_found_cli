# Quick Start
This guide is intended for running Apptainer on a computer where you will install Apptainer yourself.
If you need to request an installation on your shared resource, see [requesting an installation](quick_start.md#installation-request) for information to send to your system administrator.
For any additional help or support contact the Apptainer Community: <https://apptainer.org/support>
## Installation
You will need a Linux system to run Apptainer. Root access is not required if user namespaces are available.
To install from source, follow the instructions in the [INSTALL.md](https://github.com/apptainer/apptainer/blob/main/INSTALL.md) on github. Other installation options, including installing from a pre-built RPM, building an RPM or Debian package, installing Apptainer without root privileges, and using Apptainer on Mac and Windows machines are discussed in the [installation section of the admin guide](../admin/installation.md).
If you have an existing version of Apptainer installed from source, which you wish to upgrade or remove / uninstall, also see the [installation section of the admin guide](../admin/installation.md).
## Overview of the Apptainer Interface
Apptainer’s [command line interface](cli.md#cli) allows you to build and interact with containers transparently. You can run programs inside a container as if they were running on your host system. You can easily redirect I/O, use pipes, pass arguments, and access files, sockets, and ports on the host system from within a container.
The `help` command gives an overview of Apptainer options and subcommands as follows:

```
$ apptainer help

Linux container platform optimized for High Performance Computing (HPC) and
Enterprise Performance Computing (EPC)

Usage:
  apptainer [global options...]

Description:
  Apptainer containers provide an application virtualization layer enabling
  mobility of compute via both application and environment portability. With
  Apptainer one is capable of building a root file system that runs on any
  other Linux system where Apptainer is installed.

Options:
      --build-config    use configuration needed for building containers
  -c, --config string   specify a configuration file (for root or
                        unprivileged installation only) (default
                        "/etc/apptainer/apptainer.conf")
  -d, --debug           print debugging information (highest verbosity)
  -h, --help            help for apptainer
      --nocolor         print without color output (default False)
  -q, --quiet           suppress normal output
  -s, --silent          only print errors
  -v, --verbose         print additional information
      --version         version for apptainer

Available Commands:
  build       Build an Apptainer image
  cache       Manage the local cache
  capability  Manage Linux capabilities for users and groups
  checkpoint  Manage container checkpoint state (experimental)
  completion  Generate the autocompletion script for the specified shell
  config      Manage various apptainer configuration (root user only)
  delete      Deletes requested image from the library
  exec        Run a command within a container
  help        Help about any command
  inspect     Show metadata for an image
  instance    Manage containers running as services
  key         Manage OpenPGP keys
  keyserver   Manage apptainer keyservers
  oci         Manage OCI containers
  overlay     Manage an EXT3 writable overlay image
  plugin      Manage Apptainer plugins
  pull        Pull an image from a URI
  push        Upload image to the provided URI
  registry    Manage authentication to OCI/Docker registries
  remote      Manage apptainer remote endpoints
  run         Run the user-defined default command within a container
  run-help    Show the user-defined help for an image
  search      Search a Container Library for images
  shell       Run a shell within a container
  sif         Manipulate Singularity Image Format (SIF) images
  sign        Add digital signature(s) to an image
  test        Run the user-defined tests within a container
  verify      Verify digital signature(s) within an image
  version     Show the version for Apptainer

Examples:
  $ apptainer help <command> [<subcommand>]
  $ apptainer help build
  $ apptainer help instance start


For additional help or support, please visit https://apptainer.org/help/

```

Information about individual subcommands can also be viewed by using the `help` command:

```
$ apptainer help verify
Verify digital signature(s) within an image

Usage:
  apptainer verify [verify options...] <image path>

Description:
  The verify command allows a user to verify one or more digital signatures
  within a SIF image.

  Key material can be provided via PEM-encoded file, or via the PGP keyring. To
  manage the PGP keyring, see 'apptainer help key'.

Options:
  -a, --all                                verify all objects
      --certificate string                 path to the certificate
      --certificate-intermediates string   path to pool of intermediate
                                           certificates
      --certificate-roots string           path to pool of root certificates
  -g, --group-id uint32                    verify objects with the
                                           specified group ID
  -h, --help                               help for verify
  -j, --json                               output json
      --key string                         path to the public key file
      --legacy-insecure                    enable verification of
                                           (insecure) legacy signatures
  -l, --local                              only verify with local key(s)
                                           in keyring
      --ocsp-verify                        enable online revocation check
                                           for certificates
  -i, --sif-id uint32                      verify object with the specified ID
  -u, --url string                         specify a URL for a key server


Examples:
  Verify with a public key:
  $ apptainer verify --key public.pem container.sif

  Verify with PGP:
  $ apptainer verify container.sif

For additional help or support, please visit https://apptainer.org/help/

```

Apptainer uses positional syntax (i.e., the order of commands and options matters). Global options affecting the behavior of all commands follow immediately after the main `apptainer` command. Then come subcommands, followed by their options and arguments.
For example, to pass the `--debug` option to the main `apptainer` command and run Apptainer with debugging messages on:

```
$ apptainer --debug run docker://alpine

```

To pass the `--containall` option to the `run` command and run a Apptainer image in an isolated manner:

```
$ apptainer run --containall docker://alpine

```

Apptainer has the concept of command groups. For instance, to list Linux capabilities for a particular user, you would use the `list` command in the `capability` command group, as follows:

```
$ apptainer capability list myuser

```

Container authors might also write help docs specific to a container, or for an internal module called an “app”. If those help docs exist for a particular container, you can view them as follows:

```
$ apptainer inspect --helpfile container.sif  # See the container's help, if provided

$ apptainer inspect --helpfile --app=foo foo.sif  # See the help for the app foo, if provided

```

## Downloading images
You can use the [pull](https://apptainer.org/docs/user/main/cli/apptainer_pull.html#apptainer-pull) and [build](https://apptainer.org/docs/user/main/cli/apptainer_build.html#apptainer-build) commands to download images from an external resource like an OCI registry.
You can use `pull` with the `docker://` uri to reference OCI images served from an OCI registry. In this case `pull` does not just download an image file; OCI images are stored in layers, so `pull` must also combine those layers into a usable Apptainer image.

```
$ apptainer pull docker://alpine

```

You can also use the `build` command to download pre-built images from an external resource. When using `build` you must specify a name for your container like so:

```
$ apptainer build alpine.sif docker://alpine

```

Unlike `pull`, `build` will convert your image to the latest Apptainer image format after downloading it. `build` is like a “Swiss Army knife” for container creation. In addition to downloading images, you can use `build` to create images from other images or from scratch using a [definition file](definition_files.md#definition-files). You can also use `build` to convert an image between the container formats supported by Apptainer. To see a comparison of the Apptainer definition file with Dockerfile, please see [this section](docker_and_oci.md#sec-deffile-vs-dockerfile).
## Interacting with images
You can interact with images in several ways, each of which can accept image URIs in addition to local image paths.
As an example, the following command will pull a `lolcow_latest.sif` image from ghcr.io:

```
$ apptainer pull docker://ghcr.io/apptainer/lolcow

```

### Shell
The [shell](https://apptainer.org/docs/user/main/cli/apptainer_shell.html#apptainer-shell) command allows you to spawn a new shell within your container and interact with it as though it were a virtual machine.

```
$ apptainer shell lolcow_latest.sif

Apptainer>

```

The change in prompt indicates that you have entered the container (though you should not rely on prompt forms to determine whether you are in a container or not).
Once inside of an Apptainer container, you are the same user as you are on the host system.

```
Apptainer> whoami
david

Apptainer> id
uid=1000(david) gid=1000(david) groups=1000(david),65534(nfsnobody)

```

`shell` also works with the `docker://`, `oras://`, and `library://` URIs. This creates an ephemeral container that disappears when the shell is exited.

```
$ apptainer shell docker://ghcr.io/apptainer/lolcow

```

### Executing Commands
The [exec](https://apptainer.org/docs/user/main/cli/apptainer_exec.html#apptainer-exec) command allows you to execute a custom command within a container by specifying the image file. For instance, to execute the `cowsay` program within the `lolcow_latest.sif` container:

```
$ apptainer exec lolcow_latest.sif cowsay moo
 _____
< moo >
 -----
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

```

`exec` also works with the `docker://`, `oras://`, and `library://` URIs. This creates an ephemeral container that executes a command and disappears.

```
$ apptainer exec docker://ghcr.io/apptainer/lolcow cowsay 'Fresh from the internet'
 _________________________
< Fresh from the internet >
 -------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

```

### Running a container
Apptainer containers may contain [runscripts](definition_files.md#runscript). These are user-defined scripts that define the actions a container should perform when someone runs it. The runscript can be triggered with the [run](https://apptainer.org/docs/user/main/cli/apptainer_run.html#apptainer-run) command, or simply by calling the container as though it were an executable.

```
$ apptainer run lolcow_latest.sif
______________________________
< Mon Aug 16 13:01:55 CDT 2021 >
 ------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

$ ./lolcow_latest.sif
______________________________
< Mon Aug 16 13:12:50 CDT 2021 >
 ------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

```

`run` also works with the `docker://`, `oras://`, and `library://` URIs. This creates an ephemeral container that runs and then disappears.

```
$ apptainer run docker://ghcr.io/apptainer/lolcow
______________________________
< Mon Aug 16 13:12:33 CDT 2021 >
 ------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

```

#### Arguments to `run`
You can pass arguments to the runscript of a container, if it accepts them. For example, the default runscript of the `docker://alpine` container passes any arguments to a shell. We can ask the container to run `echo` command in this shell as follows:

```
$ apptainer run docker://alpine echo "hello"

hello

```

Because Apptainer runscripts are evaluated shell scripts, arguments can behave slightly differently than in Docker/OCI runtimes, if they contain expressions that have special meaning to the shell. Here is an illustrative example:

```
$ docker run -it --rm alpine echo "\$HOSTNAME"
$HOSTNAME

$ apptainer run docker://alpine echo "\$HOSTNAME"
p700

$ apptainer run docker://alpine echo "\\\$HOSTNAME"
$HOSTNAME

```

To replicate Docker/OCI behavior, you may need additional escaping or quoting of arguments.
Unlike the `run` command, the `exec` command does behave in the same manner as Docker/OCI, because it calls the specified executable directly:

```
$ apptainer exec docker://alpine echo "\$HOSTNAME"
$HOSTNAME

$ apptainer exec docker://alpine echo "\\\$HOSTNAME"
\$HOSTNAME

```

## Working with Files
Files on the host are reachable from within the container:

```
$ echo "Hello from inside the container" > $HOME/hostfile.txt

$ apptainer exec lolcow_latest.sif cat $HOME/hostfile.txt

Hello from inside the container

```

This example works because `hostfile.txt` exists in the user’s home directory (`$HOME`). By default, Apptainer bind mounts `$HOME`, the current working directory, and additional system locations from the host into the container.
You can specify additional directories to bind mount into your container with the `--bind` option. In the following example, the `data` directory on the host system is bind mounted to the `/mnt` directory inside the container.

```
$ echo "Drink milk (and never eat hamburgers)." > /data/cow_advice.txt

$ apptainer exec --bind /data:/mnt lolcow_latest.sif cat /mnt/cow_advice.txt
Drink milk (and never eat hamburgers).

```

Pipes and redirects also work with Apptainer commands, just like they do with normal Linux commands:

```
$ cat /data/cow_advice.txt | apptainer exec lolcow_latest.sif cowsay
 ________________________________________
< Drink milk (and never eat hamburgers). >
 ----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

```

## Building images from scratch
Apptainer produces immutable images in the Singularity Image File (SIF) format. This ensures reproducible and verifiable images and allows for many extra benefits such as the ability to sign and verify your containers.
However, during testing and debugging you may want an image format that is writable. This way you can `shell` into the image and install software and dependencies until you are satisfied that your container will fulfill your needs. For these scenarios, Apptainer also supports the `sandbox` format (which is really just a directory).
### Sandbox Directories
To build into a `sandbox` (container in a directory) use the `build --sandbox` command and option:

```
$ apptainer build --sandbox ubuntu/ docker://ubuntu

```

This command creates a directory called `ubuntu/` with an entire Ubuntu Operating System and some Apptainer metadata in your current working directory.
You can use commands like `shell`, `exec` , and `run` with this directory just as you would with an Apptainer image. If you pass the `--writable` option when you use your container, you can also write files within the sandbox directory (provided you have the permissions to do so).

```
$ apptainer exec --writable ubuntu touch /foo

$ apptainer exec ubuntu/ ls /foo
/foo

```

### Converting images from one format to another
The `build` command allows you to build a new container from an existing container. This means that you can use it to convert a container from one format to another. For instance, if you have already created a sandbox (directory) and want to convert it to the Singularity Image Format, you can do so as follows:

```
$ apptainer build new.sif sandbox

```

Note, however, that this approach may break reproducibility, in the event that you have altered your sandbox outside of the context of a [definition file](quick_start.md#qs-def-files), so you are advised to exercise care.
### Apptainer Definition Files
For a reproducible, verifiable and production-quality container, it is recommended that you build a SIF file using an Apptainer definition file. This also makes it easy to add files, environment variables, and install custom software. You can start with base images from Docker Hub and use images directly from official repositories such as Ubuntu, Debian, Fedora, Arch, and BusyBox.
A definition file has a header and a body. The header determines the base container to begin with, and the body is further divided into sections that perform tasks such as software installation, environment setup, and copying files into the container from host system.
Here is an example of a definition file:

```
BootStrap: docker
From: ubuntu:22.04

%post
   apt-get -y update
   apt-get -y install cowsay lolcat

%environment
   export LC_ALL=C
   export PATH=/usr/games:$PATH

%runscript
   date | cowsay | lolcat

%labels
   Author Alice

```

To build a container from this definition file (assuming it is a file named `lolcow.def`), you would call `build` as follows:

```
$ apptainer build lolcow.sif lolcow.def

```

In this example, the header tells Apptainer to use a base Ubuntu 22.04 image from the Container Library. The other sections in this definition file are as follows:
  * The `%post` section is executed within the container at build time, after the base OS has been installed. The `%post` section is therefore the place to perform installations of new libraries and applications.
  * The `%environment` section defines environment variables that will be available to the container at runtime.
  * The `%runscript` section defines actions for the container to take when it is executed. (These commands will therefore not be run at build time.)
  * And finally, the `%labels` section allows for custom metadata to be added to the container.


This is a very small example of the things that you can do with a [definition file](definition_files.md#definition-files). You can also use an existing container on your host system as a base. Definition files also support [“templating”](definition_files.md#sec-templating): the ability to pass values from the command-line, or from a definitions file, that will replace placeholders in the definition file at build time.
This quickstart document just scratches the surface of all of the things you can do with Apptainer!
If you need additional help or support, see <https://apptainer.org/help>.
## Apptainer on a shared resource
Perhaps you are a user who wants a few talking points and background to share with your administrator. Or maybe you are an administrator who needs to decide whether to install Apptainer.
This document and the accompanying administrator documentation provide answers to many common questions.
If you need to request an installation from your administrator, you may decide to draft a message similar to this:

```
Dear shared resource administrator,

We are interested in having Apptainer (https://apptainer.org)
installed on our shared resource. Apptainer containers will allow us to
build encapsulated environments, meaning that our work is reproducible and
we are empowered to choose all dependencies including libraries, operating
system, and custom software. Apptainer is already in use on many of the
top HPC centers around the world. Examples include:

    Texas Advanced Computing Center
    GSI Helmholtz Center for Heavy Ion Research
    Oak Ridge Leadership Computing Facility
    Purdue University
    National Institutes of Health HPC
    UFIT Research Computing at the University of Florida
    San Diego Supercomputing Center
    Lawrence Berkeley National Laboratory
    University of Chicago
    McGill HPC Centre/Calcul Québec
    Barcelona Supercomputing Center
    Sandia National Lab
    Argonne National Lab

Importantly, it has a vibrant team of developers, scientists, and HPC
administrators that invest heavily in the security and development of the
software, and are quick to respond to the needs of the community. To help
learn more about Apptainer, I thought these items might be of interest:

    - Security: A discussion of security concerns is discussed at
    https://apptainer.org/docs/admin/main/admin_quickstart.html

    - Installation:
    https://apptainer.org/docs/admin/main/installation.html

If you have questions about any of the above, you can contact one of the
sources listed at https://apptainer.org/help. I can do my best
to facilitate this interaction if help is needed.

Thank you kindly for considering this request!

Best,

User

```

