# Remote Endpoints
## Overview
The `remote` command group allows users to manage the service endpoints Apptainer will interact with for many common command flows. This includes managing credentials for image storage services and keyservers used to locate public keys for SIF image verification. Currently, there are three main types of remote endpoints managed by this command group: [Library API Registries](https://singularityhub.github.io/library-api/#/?id=library-api), OCI registries, and keyservers.
You are most likely interacting with remote endpoints on a regular basis using various Apptainer commands: [pull](https://apptainer.org/docs/user/main/cli/apptainer_pull.html), [push](https://apptainer.org/docs/user/main/cli/apptainer_push.html), [build](https://apptainer.org/docs/user/main/cli/apptainer_build.html), [key](https://apptainer.org/docs/user/main/cli/apptainer_key.html), [search](https://apptainer.org/docs/user/main/cli/apptainer_search.html), [verify](https://apptainer.org/docs/user/main/cli/apptainer_verify.html), [exec](https://apptainer.org/docs/user/main/cli/apptainer_exec.html), [shell](https://apptainer.org/docs/user/main/cli/apptainer_shell.html), [run](https://apptainer.org/docs/user/main/cli/apptainer_run.html), or [instance](https://apptainer.org/docs/user/main/cli/apptainer_instance.html).
## Managing Remote Endpoints
A fresh installation of Apptainer is configured with the `DefaultRemote`, which does not support the Library API as it is only configured with a functioning key server, `https://keys.openpgp.org`. Users or administrators should configure one of the Library API implementations listed [here](https://singularityhub.github.io/library-api/#/?id=library-api) if they would like to use a Library API registry.
Users can setup and switch between multiple remote endpoints, which are stored in their `~/.apptainer/remote.yaml` file. Alternatively, remote endpoints can be set system-wide by an administrator.
Generally, users and administrators should manage remote endpoints using the `apptainer remote` command, and avoid editing `remote.yaml` configuration files directly.
### List Remotes
To `list` existing remote endpoints, run the following:

```
$ apptainer remote list

NAME           URI                  DEFAULT?  GLOBAL?  EXCLUSIVE?  SECURE?
DefaultRemote  cloud.apptainer.org  ✓         ✓                    ✓

```

The `✓` in the `DEFAULT?` column for `DefaultRemote` shows that this is the current default remote endpoint.
### Add & Login To Remotes
To `add` a remote endpoint (for the current user only):

```
$ apptainer remote add <remote_name> <remote_uri>

```

For example, if you have an installation of Apptainer enterprise hosted at enterprise.example.com:

```
$ apptainer remote add myremote https://enterprise.example.com

INFO:    Remote "myremote" added.
Generate an access token at https://enterprise.example.com/auth/tokens, and paste it here.
Token entered will be hidden for security.
Access Token:

```

You will be prompted to setup an API key as the remote is added. As the example above shows, the output of the `add` subcommand will provide you with the web address you need to visit in order to generate your new access token.
To `add` a global remote endpoint (available to all users on the system), an administrative user should run:

```
$ sudo apptainer remote add --global <remote_name> <remote_uri>

# example...
$ sudo apptainer remote add --global company-remote https://enterprise7.example.com
INFO:    Remote "company-remote" added.
INFO:    Global option detected. Will not automatically log into remote.

```

Note
Global remote configurations can only be modified by the root user and are stored in the `etc/apptainer/remote.yaml` file under the Apptainer installation location.
To `login` to a remote, for the first time or if your token expires or was revoked:

```
# Login to the default remote endpoint
$ apptainer remote login

# Login to another remote endpoint
$ apptainer remote login <remote_name>

# example...
$ apptainer remote login myremote
apptainer remote login myremote
INFO:    Authenticating with remote: myremote
Generate an API Key at https://enterprise.example.com/auth/tokens, and paste here:
API Key:
INFO:    API Key Verified!

```

If you `login` to a remote that you already have a valid token for, you will be prompted, and the new token will be verified, before it replaces your existing credential. If you enter an incorrect token your existing token will not be replaced:

```
$ apptainer remote login
An access token is already set for this remote. Replace it? [N/y]y
Generate an access token at https://enterprise.example.com/auth/tokens, and paste it here.
Token entered will be hidden for security.
Access Token:
FATAL:   while verifying token: error response from server: Invalid Credentials

# Previous token is still in place

```

Note
It is important for users to be aware that the login command will store the supplied credentials or tokens unencrypted in your home directory.
### Remove Remotes
To `remove` an endpoint:

```
$ apptainer remote remove <remote_name>

```

Use the `--global` option as the root user to remove a global endpoint:

```
$ sudo apptainer remote remove --global <remote_name>

```

#### Insecure (HTTP) Endpoints
If you are using a endpoint that only exposes its service discovery file over an insecure HTTP connection, it can be added by specifying the `--insecure` flag:

```
$ sudo apptainer remote add --global --insecure test http://test.example.com
INFO:    Remote "test" added.
INFO:    Global option detected. Will not automatically log into remote.

```

This flag causes HTTP to be used instead of HTTPS _for service discovery only_. The protocol used to access individual library-, build- and keyservice-URLs is determined by the contents of the service discovery file.
### Set the Default Remote
To use a given remote endpoint as the default for commands such as `push`, `pull`, etc., use the `remote use` command:

```
$ apptainer remote use <remote_name>

```

The remote designated as default shows up with a `YES` under the `ACTIVE` column in the output of `remote list`:

```
$ apptainer remote list
Cloud Services Endpoints
========================

NAME            URI                      DEFAULT?  GLOBAL?  EXCLUSIVE?  SECURE?
DefaultRemote   cloud.apptainer.org                ✓                    ✓
company-remote  enterprise7.example.com            ✓                    ✓
myremote        enterprise.example.com   ✓                              ✓
test            test.example.com                   ✓                    ✓

$ apptainer remote use myremote
INFO:    Remote "myremote" now in use.

$ apptainer remote list
Cloud Services Endpoints
========================

NAME            URI                      DEFAULT?  GLOBAL?  EXCLUSIVE?  SECURE?
DefaultRemote   cloud.apptainer.org      ✓         ✓                    ✓
company-remote  enterprise7.example.com            ✓                    ✓
myremote        enterprise.example.com                                  ✓
test            test.example.com                   ✓                    ✓

```

In the example above, the default remote at the start (before being changed to `DefaultRemote`) was `myremote`. That is because adding a new remote endpoint automatically makes the newly-added endpoint the default one, and the same user had previously used the `remote add` command to add the `myremote` endpoint. This behavior can be suppressed by passing the `--no-default` flag to the `remote add` command, which will then add a new remote endpoint but leave the default endpoint unchanged:

```
 $ apptainer remote add --no-default myotherremote https://enterprise2.example.com
 INFO:    Remote "myotherremote" added.
 Generate an access token at https://enterprise2.example.com/auth/tokens, and paste it here.
 Token entered will be hidden for security.
 Access Token:

$ apptainer remote list

 NAME            URI                      DEFAULT?  GLOBAL?  EXCLUSIVE?  SECURE?
 DefaultRemote   cloud.apptainer.org      ✓         ✓                    ✓
 company-remote  enterprise7.example.com            ✓                    ✓
 myotherremote   enterprise2.example.com                                 ✓
 myremote        enterprise.example.com                                  ✓
 test            test.example.com                   ✓                    ✓

```

An administrator can make a remote the only usable remote for the system, using the `--exclusive` flag:

```
$ sudo apptainer remote use --exclusive company-remote
INFO:    Remote "company-remote" now in use.
$ apptainer remote list
Cloud Services Endpoints
========================

NAME            URI                      DEFAULT?  GLOBAL?  EXCLUSIVE?  SECURE?
DefaultRemote   cloud.apptainer.org                ✓                    ✓
company-remote  enterprise7.example.com  ✓         ✓        ✓           ✓
myotherremote   enterprise2.example.com                                 ✓
myremote        enterprise.example.com                                  ✓
test            test.example.com                   ✓                    ✓

```

This, in turn, prevents users from changing the remote they use:

```
$ apptainer remote use myremote
FATAL:   could not use myremote: remote company-remote has been set exclusive by the system administrator

```

If you do not want to switch remote with `remote use`, you can:
  * Instruct `push` and `pull` commands to use an alternative library server using the `--library` option (for example: `apptainer pull -F --library https://library.example.com library://alpine`). Note that the URL provided to the `--library` option is the URL of the library service itself, not the service discovery URL for the entire remote.
  * Instruct certain subcommands of the `key` command to use an alternative keyserver using the `--url` option (for example: `apptainer key search --url https://keys.example.com foobar`).


### Restoring pre-Apptainer library behavior
Apptainer’s default remote endpoint configures only a public key server, it does not support the `library://` protocol. Formerly the default was set to point to Sylabs servers, but the read/write support of the `oras://` protocol by for example the [GitHub Container Registry](docker_and_oci.md#github-container-registry) makes it unnecessary. The remote endpoint was also formerly used for builds using the build `--remote` option, but Apptainer does not support that. Instead, it supports [unprivileged local builds](fakeroot.md#build).
If you would still like to have the previous default, these are the commands to restore the library behavior from before Apptainer, where using the `library://` URI would download from the Sylabs Cloud anonymously:

```
$ apptainer remote add --no-login SylabsCloud cloud.sycloud.io
INFO:    Remote "SylabsCloud" added.
$ apptainer remote use SylabsCloud
INFO:    Remote "SylabsCloud" now in use.
$ apptainer remote list
Cloud Services Endpoints
========================

NAME           URI                  ACTIVE  GLOBAL  EXCLUSIVE
DefaultRemote  cloud.apptainer.org  NO      YES     NO
SylabsCloud    cloud.sycloud.io     YES     NO      NO

Keyservers
==========

URI                                 GLOBAL  INSECURE  ORDER
https://keys.production.sycloud.io  YES     NO        1*

* Active cloud services keyserver

```

To set the defaults system-wide see the corresponding section in the [admin guide](../admin/configfiles.md#restoring-pre-apptainer-library-behavior).
## Keyserver Configurations
By default, Apptainer will use the keyserver defined by the active remote’s service discovery file. This behavior can be changed or supplemented via the `add-keyserver` and `remove-keyserver` subcommands. These commands allow an administrator to create a global list of keyservers that will be used to verify container signatures by default, where `order 1` will be the first in the list. Other operations performed by Apptainer that reach out to a keyserver will only use the first, or `order 1`, keyserver.
When listing the default remotes, we can see that the default keyserver is `https://keys.openpgp.org` and the asterisk next to its order indicates that it is the keyserver associated with the current remote endpoint. We can also see the `INSECURE` column indicating that Apptainer will use TLS when communicating with the keyserver.

```
$ apptainer remote list
Cloud Services Endpoints
========================

NAME           URI                  ACTIVE  GLOBAL  EXCLUSIVE
DefaultRemote  cloud.apptainer.org  YES     YES     NO

Keyservers
==========

URI                       GLOBAL  INSECURE  ORDER
https://keys.openpgp.org  YES     NO        1*

* Active cloud services keyserver

```

We can add a key server to list of keyservers as follows:

```
$ sudo apptainer remote add-keyserver https://pgp.example.com
$ apptainer remote list
Cloud Services Endpoints
========================

NAME           URI                  ACTIVE  GLOBAL  EXCLUSIVE
DefaultRemote  cloud.apptainer.org  YES     YES     NO

Keyservers
==========

URI                       GLOBAL  INSECURE  ORDER
https://keys.openpgp.org  YES     NO        1*
https://pgp.example.com   YES     NO        2

* Active cloud services keyserver

```

Here, we see that the `https://pgp.example.com` keyserver was added to the list. We can specify the order in the list in which this keyserver should be added, by using the `--order` flag:

```
$ sudo apptainer remote add-keyserver --order 1 https://pgp.example.com
$ apptainer remote list
Cloud Services Endpoints
========================

NAME           URI                  ACTIVE  GLOBAL  EXCLUSIVE
DefaultRemote  cloud.apptainer.org  YES     YES     NO

Keyservers
==========

URI                      GLOBAL  INSECURE  ORDER
https://pgp.example.com  YES     NO        1
https://keys.openpgp.org YES     NO        2*

* Active cloud services keyserver

```

Since we specified `--order 1`, the `https://pgp.example.com` keyserver was added as the first entry in the list, and the default keyserver was moved to second in the list. With this keyserver configuration, all default image verification performed by Apptainer will, when searching for public keys, reach out to `https://pgp.example.com` first, and only then to `https://keys.openpgp.org`.
If a keyserver requires authentication prior to being used, users can login as follows, supplying the password or an API token at the prompt:

```
$ apptainer remote login --username myname https://pgp.example.com
Password (or token when username is empty):
INFO:    Token stored in /home/myname/.apptainer/remote.yaml

```

The output of remote list will now show that we are logged in to `https://pgp.example.com`:

```
$ apptainer remote list
Cloud Services Endpoints
========================

NAME           URI                  ACTIVE  GLOBAL  EXCLUSIVE
DefaultRemote  cloud.apptainer.org  YES     YES     NO

Keyservers
==========

URI                       GLOBAL  INSECURE  ORDER
https://pgp.example.com   YES     NO        1
https://keys.openpgp.org  YES     NO        2*

* Active cloud services keyserver

Authenticated Logins
=================================

URI                     INSECURE
https://pgp.example.com NO

```

Note
It is important for users to be aware that the `remote login` command will store the supplied credentials or tokens unencrypted in your home directory.
## Managing OCI Registries
OCI Registries used to also be managed using the apptainer `remote` command group, but those are deprecated in favor of apptainer `registry` commands. See the [OCI Image Registries](registry.md#registry) section in this guide.
