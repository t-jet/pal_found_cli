# Keyserver Management
By default, Apptainer will use the keyserver defined by the active [remote endpoint](endpoint.md#endpoint)’s service discovery file. This behavior can be changed or supplemented using the `key` command and, in particular, its subcommands `add` and `remove`. These allow an administrator to create a global list of keyservers that will be used to verify container signatures by default. When verifying container signatures, Apptainer consults them according to a configured _order_ (with the keyserver whose order is `1` consulted first, then the one whose order is `2`, and so forth). Other operations performed by Apptainer that reach out to a keyserver will only use the first one (whose order is `1`).
Note
In previous versions of Apptainer, the functionality described here was grouped together with [remote endpoint management](endpoint.md#endpoint) under the `remote` command group. Beginning with version 4.0, this functionality has been given its own top-level command group, `keyserver`.
The `list` subcommand allows the user to examine the set of currently configured keyservers:

```
$ apptainer keyserver list

DefaultRemote *^
#1  https://keys.openpgp.org  TLS

(* = system endpoint, ^ = default endpoint)

```

We can see in the output of the `list` subcommand that “DefaultRemote” is the _default_ remote endpoint (in other words, the endpoint that will be used by all Apptainer commands unless otherwise specified), and that it is a _global_ (in other words, system-level) endpoint. As can be seen above, the output also indicates that TLS will be used when communicating with the `https://keys.openpgp.org` keyserver.
We can add a key server to list of keyservers as follows:

```
$ sudo apptainer keyserver add https://pgp.example.com
$ apptainer keyserver list

DefaultRemote *^
   #1  https://keys.openpgp.org   TLS
   #2  https://pgp.example.com    TLS

(* = system endpoint, ^ = default endpoint,
 + = user is logged in directly to this keyserver)

```

Here, we see that the `https://pgp.example.com` keyserver was added to the list. We can specify the order in the list in which this keyserver should be added, by using the `--order` flag:

```
$ sudo apptainer keyserver add --order 1 https://pgp.example.com
$ apptainer keyserver list

DefaultRemote *^
   #1  https://pgp.example.com    TLS
   #2  https://keys.openpgp.org   TLS

(* = system endpoint, ^ = default endpoint,
 + = user is logged in directly to this keyserver)

```

Since we specified `--order 1`, the `https://pgp.example.com` keyserver was added as the first entry in the list, and the default keyserver was moved to second in the list. With this keyserver configuration, all default image verification performed by Apptainer will, when searching for public keys, reach out to `https://pgp.example.com` first, and only then to `https://keys.openpgp.org`.
If a keyserver requires authentication prior to being used, users can login as follows, supplying the password or an API token at the prompt:

```
$ apptainer keyserver login --username myname https://pgp.example.com
Password / Token:
INFO:    Token stored in /home/myuser/.apptainer/remote.yaml

```

The output of keyserver list will now show that we are logged in to `https://pgp.example.com`:

```
$ apptainer keyserver list

DefaultRemote *^
   #1  https://pgp.example.com       TLS  +
   #2  https://keys.openpgp.org      TLS

(* = system endpoint, ^ = default endpoint,
 + = user is logged in directly to this keyserver)

```

Note
It is important for users to be aware that the `keyserver login` command will store the supplied credentials or tokens unencrypted in their home directory.
