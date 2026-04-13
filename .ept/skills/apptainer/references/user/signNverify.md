# Signing and Verifying Containers
Apptainer’s SIF images can be signed, and subsequently verified, so that a user can be confident that an image they have obtained is a bit-for-bit reproduction of the original container as the author intended it. The signature, over the metadata and content of the container, is created using a private key, and directly added to the SIF file. This means that a signed container carries it’s signature with it, avoiding the need for extra infrastructure to distribute signatures to end users of the container.
A user verifies the container has not been modified since it was signed using a public key or certificate. By default, Apptainer uses PGP keys to sign and verify containers. Signing and verifying containers with X.509 key material / certificates is also supported.
PGP Public keys for verification can be distributed manually, or can be uploaded to and automatically retrieved from a remote keyserver.
As well as indicating a container has not been modified, a valid signature may be used to indicate a container has undergone testing or review, and is approved for execution. Multiple signatures can be added to a container, to document its progress through an approval process. Apptainer’s Execution Control List (ECL) feature can be enable by administrators of privileged installations to restrict execution of containers based on their signatures (see the admin guide for more information).
Note
To verify containers signed with Singularity versions older than 3.6.0 the `--legacy-insecure` flag must be provided to the `apptainer verify` command.
## Verifying containers from remote sources
The `verify` command will check that a SIF container image has been signed using a PGP key or certificate. This ensures that the container image on your disk is a bit-for-bit reproduction of the original image.

```
$ apptainer verify alpine_latest.sif

[REMOTE]  Signing entity: Ian Kaneshiro (example key) <ikaneshiro@apptainer.org>
[REMOTE]  Fingerprint: 8232570480B868E1473AEEB03DBCBA1EE9D661E5
Objects verified:
ID  |GROUP   |LINK    |TYPE
------------------------------------------------
1   |1       |NONE    |Def.FILE
2   |1       |NONE    |JSON.Generic
3   |1       |NONE    |JSON.Generic
4   |1       |NONE    |FS
Container verified: my_container.sif

```

In this example you can see that **Ian Kaneshiro** has signed the container.
This feature is available with SIF images like those you can pull from container libraries or OCI registries via `oras://`.
Note
`apptainer verify` will only run against a local SIF file. You must `pull` an image to a local disk before you can verify it.
## Signing your own containers
### Generating and managing PGP keys
To sign your own containers with a PGP key you first need to generate one or more keys.
You can use the `newpair` subcommand in the `key` command group like so:

```
$ apptainer key newpair

Enter your name (e.g., John Doe) : Joe User
Enter your email address (e.g., john.doe@example.com) : myuser@example.com
Enter optional comment (e.g., development keys) : demo
Enter a passphrase :
Retype your passphrase :
Generating Entity and OpenPGP Key Pair... done

```

The `list` subcommand will show you all of the keys you have created or saved locally.

```
$ apptainer key list

Public key listing (/home/ian/.apptainer/keys/pgp-public):

0)  User:              Joe User (demo) <myuser@example.com>
    Creation time:     2019-11-15 09:54:54 -0600 CST
    Fingerprint:       E5F780B2C22F59DF748524B435C3844412EE233B
    Length (in bits):  4096

```

If you would like others in the community to easily be able to fetch your public key for image verification, you can push your key to a public keyserver.
First we can check which key server we have configured using:

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

Authenticated Logins
=================================

URI             INSECURE
oras://ghcr.io  NO

```

Here we can see that we will be pushing to <https://keys.openpgp.org>. Now we can use the following command to push our key:

```
$ apptainer key push 8232570480B868E1473AEEB03DBCBA1EE9D661E5

WARNING: No default remote in use, falling back to default keyserver: https://keys.openpgp.org
INFO:    Key server response: Upload successful. This is a new key, a welcome email has been sent.
public key '8232570480B868E1473AEEB03DBCBA1EE9D661E5' pushed to server successfully

```

Note
The default key server keys.openpgp.org requires you to verify your key via email before the public key material will be accessible.
If you delete your local public PGP key, you can always locate and download it again like so.

```
$ apptainer key search --long-list ikaneshiro@apptainer.org

Showing 1 results

KEY ID    BITS  NAME/EMAIL
12EE233B  4096  Joe User (demo) <myuser@example.com>

$ apptainer key pull 8232570480B868E1473AEEB03DBCBA1EE9D661E5
1 key(s) added to keyring of trust /home/ian/.apptainer/keys/pgp-public

```

But note that this only restores the _public_ key (used for verifying) to your local machine and does not restore the _private_ key (used for signing). **If you permanently delete your private key, there is no way to recover it.**
### Searching for keys
Apptainer allows you to search the keystore for public keys. You can search for names, emails, and fingerprints (key IDs) provided that the backend keystore supports these actions. When searching for a fingerprint, you need to use `0x` before the fingerprint, check the example:

```
# search for key ID:
$ apptainer key search 0x8883491F4268F173C6E5DC49EDECE4F3F38D871E

# search for the sort ID:
$ apptainer key search 0xF38D871E

# search for user:
$ apptainer key search Godlove

# search for email:
$ apptainer key search @gmail.com

```

### Signing and validating your own containers
Now that you have a key generated, you can use it to sign images like so:

```
$ apptainer sign my_container.sif

Signing image: my_container.sif
Enter key passphrase :
Signature created and applied to my_container.sif

```

Because your public PGP key is saved locally you can verify the image without needing to contact the key server.

```
$ apptainer verify my_container.sif

Verifying image: my_container.sif
[LOCAL]   Signing entity: Joe User (Demo keys) <myuser@example.com>
[LOCAL]   Fingerprint: 65833F473098C6215E750B3BDFD69E5CEE85D448
Objects verified:
ID  |GROUP   |LINK    |TYPE
------------------------------------------------
1   |1       |NONE    |Def.FILE
2   |1       |NONE    |JSON.Generic
3   |1       |NONE    |JSON.Generic
4   |1       |NONE    |FS
Container verified: my_container.sif

```

If you’ve pushed your key to a key server you can also verify this image in the absence of a local public key. To demonstrate this, first `remove` your local public key, and then try to use the `verify` command again.

```
$ apptainer key remove 8232570480B868E1473AEEB03DBCBA1EE9D661E5

$ apptainer verify my_container.sif

Verifying image: my_container.sif
[REMOTE]   Signing entity: Joe User (Demo keys) <myuser@example.com>
[REMOTE]   Fingerprint: 65833F473098C6215E750B3BDFD69E5CEE85D448
Objects verified:
ID  |GROUP   |LINK    |TYPE
------------------------------------------------
1   |1       |NONE    |Def.FILE
2   |1       |NONE    |JSON.Generic
3   |1       |NONE    |JSON.Generic
4   |1       |NONE    |FS
Container verified: my_container.sif

```

Note that the `[REMOTE]` message shows the key used for verification was obtained from a key server, and is not present on your local computer. You can retrieve it, so that you can verify even if you are offline with `apptainer key pull`

```
$ apptainer key pull 8232570480B868E1473AEEB03DBCBA1EE9D661E5

1 key(s) added to keyring of trust /home/ian/.apptainer/keys/pgp-public

```

### Advanced Signing - SIF IDs and Groups
As well as the default behaviour, which signs all objects, fine-grained control of signing is possible.
If you `sif list` a SIF file you will see it is comprised of a number of objects. Each object has an `ID`, and belongs to a `GROUP`. Since signatures are _applied_ to objects, they have an `ID` but not a `GROUP`.

```
$ apptainer sif list my_container.sif

------------------------------------------------------------------------------
ID   |GROUP   |LINK    |SIF POSITION (start-end)  |TYPE
------------------------------------------------------------------------------
1    |1       |NONE    |32768-32800               |Def.FILE
2    |1       |NONE    |36864-39751               |JSON.Generic
3    |1       |NONE    |40960-41055               |JSON.Generic
4    |1       |NONE    |45056-2781184             |FS (Squashfs/*System/amd64)
5    |NONE    |1   (G) |2781184-2782981           |Signature (SHA-256)

```

Note
The `apptainer sif` commands will only run against a local SIF file. You must `pull` an image to a local disk before you can examine it.
I can choose to sign and verify a specific object with the `--sif-id` option to `sign` and `verify`.

```
$ apptainer sign --sif-id 1 my_container.sif

Signing image: my_container.sif
Enter key passphrase :
Signature created and applied to my_container.sif

$ apptainer verify --sif-id 1 my_container.sif

Verifying image: my_container.sif
[LOCAL]   Signing entity: Joe User (Demo keys) <myuser@example.com>
[LOCAL]   Fingerprint: 65833F473098C6215E750B3BDFD69E5CEE85D448
Objects verified:
ID  |GROUP   |LINK    |TYPE
------------------------------------------------
1   |1       |NONE    |Def.FILE
Container verified: my_container.sif

```

Note that running the `verify` command without specifying the specific sif-id gives a fatal error. The container is not considered verified as whole because other objects could have been changed without my knowledge.

```
$ apptainer verify my_container.sif

Verifying image: my_container.sif
[LOCAL]   Signing entity: Joe User (Demo keys) <myuser@example.com>
[LOCAL]   Fingerprint: 65833F473098C6215E750B3BDFD69E5CEE85D448

Error encountered during signature verification: object 2: object not signed
FATAL:   Failed to verify container: integrity: object 2: object not signed

```

I can sign a group of objects with the `--group-id` option to `sign`.

```
$ apptainer sign --group-id 1 my_container.sif
Signing image: my_container.sif
Enter key passphrase :
Signature created and applied to my_container.sif

```

This creates one signature over all objects in the group. I can verify that nothing in the group has been modified by running `verify` with the same `--group-id` option.

```
$ apptainer verify --group-id 1 my_container.sif

Verifying image: my_container.sif
[LOCAL]   Signing entity: Joe User (Demo keys) <myuser@example.com>
[LOCAL]   Fingerprint: 65833F473098C6215E750B3BDFD69E5CEE85D448
Objects verified:
ID  |GROUP   |LINK    |TYPE
------------------------------------------------
1   |1       |NONE    |Def.FILE
2   |1       |NONE    |JSON.Generic
3   |1       |NONE    |JSON.Generic
4   |1       |NONE    |FS
Container verified: my_container.sif

```

Because every object in the SIF file is within the signed group 1 the entire container is signed, and the default `verify` behavior without specifying `--group-id` can also verify the container:

```
$ apptainer verify my_container.sif

Verifying image: my_container.sif
[LOCAL]   Signing entity: Joe User (Demo keys) <myuser@example.com>
[LOCAL]   Fingerprint: 65833F473098C6215E750B3BDFD69E5CEE85D448
Objects verified:
ID  |GROUP   |LINK    |TYPE
------------------------------------------------
1   |1       |NONE    |Def.FILE
2   |1       |NONE    |JSON.Generic
3   |1       |NONE    |JSON.Generic
4   |1       |NONE    |FS
Container verified: my_container.sif

```

## PEM Key / X.509 Certificate Support
Apptainer also supports signing SIF container images using a PEM format private key, and verifying with a PEM format public key, or X.509 certificate. Non-PGP signatures are implemented using the [Dead Simple Signing Envelope](https://github.com/secure-systems-lab/dsse) (DSSE) standard.
The Apptainer GitHub repo contains keys and certificates useful for testing. If you want to use them to carry out the commands below, first, carry out the following commands:

```
$ git clone https://github.com/apptainer/apptainer.git

$ export KEYD="${PWD}/apptainer/test/keys"

$ export CERTD="${PWD}/apptainer/test/certs"

```

Information on creating PEM files can be found in the encrypted container docs, and the method for creating certificates is documented [here](https://github.com/apptainer/apptainer/blob/main/test/certs/gen_certs.go).
### Signing with a PEM key
To sign a container using a private key in PEM format, provide the private key material to the `sign` command using the `--key` flag.

```
$ apptainer sign --key $KEYD/rsa-private.pem lolcow.sif
INFO:    Signing image with key material from 'rsa_pri.pem'
INFO:    Signature created and applied to image 'lolcow.sif'

```

The DSSE signature descriptor can now be seen by inspecting the SIF file:

```
$ apptainer sif list lolcow.sif
------------------------------------------------------------------------------
ID   |GROUP   |LINK    |SIF POSITION (start-end)  |TYPE
------------------------------------------------------------------------------
1    |1       |NONE    |32176-32393               |Def.FILE
2    |1       |NONE    |32393-33522               |JSON.Generic
3    |1       |NONE    |33522-33718               |JSON.Generic
4    |1       |NONE    |36864-84656128            |FS (Squashfs/*System/amd64)
5    |NONE    |1   (G) |84656128-84658191         |Signature (SHA-256)

$ apptainer sif dump 5 lolcow.sif | jq
{
"payloadType": "application/vnd.apptainer.sif-metadata+json",
...

```

Attempting to `verify` the image without options will fail, as it is not signed with a PGP key:

```
$ apptainer verify lolcow.sif
INFO:    Verifying image with PGP key material
FATAL:   Failed to verify container: integrity: key material not provided for DSSE envelope signature

```

Note that the error message shows that the container image has a DSSE signature present.
### Verifying with a PEM key
To verify a container using a PEM public key directly, provide the key material to the `verify` command using the `key` flag:

```
$ apptainer verify --key $KEYD/rsa-public.pem lolcow.sif
INFO:    Verifying image with key material from 'rsa_pub.pem'
Objects verified:
ID  |GROUP   |LINK    |TYPE
------------------------------------------------
1   |1       |NONE    |Def.FILE
2   |1       |NONE    |JSON.Generic
3   |1       |NONE    |JSON.Generic
4   |1       |NONE    |FS
INFO:    Verified signature(s) from image 'lolcow.sif'

```

### Verifying with an X.509 certificate
To verify a container that was signed with a PEM private key, using an X.509 certificate, pass the certificate to the `verify` command using the `--certificate` flag. If the certificate is part of a chain, provide intermediate and valid root certificates with the `--certificate-intermediates` and `--certificate-roots` flags:

```
$ apptainer verify \
   --certificate $CERTD/leaf.pem \
   --certificate-intermediates $CERTD/intermediate.pem \
   --certificate-roots $CERTD/root.pem \
   lolcow.sif

```

Note
The certificate must have a usage field that allows code signing in order to verify container images.
### OSCP Certificate Revocation Checks
When verifying a container using X.509 certificates, Apptainer can perform online revocation checks using the Online Certificate Status Protocol (OCSP). To enable OCSP checks, add the `--ocsp-verify` flag to your `verify` command:

```
$ apptainer verify \
   --certificate $CERTD/leaf.pem \
   --certificate-intermediates $CERTD/intermediate.pem \
   --certificate-roots $CERTD/root.pem \
   --ocsp-verify
   lolcow.sif

```

Apptainer will then attempt to contact the prescribed OCSP responder for each certificate in the chain, in order to check that the relevant certificate has not been revoked. In the event that an OCSP responder cannot be contacted, or a certificate has been revoked, verification will fail with a validation error:

```
INFO:    Validate: cert:leaf  issuer:intermediate
FATAL:   Failed to verify container: OCSP verification has failed

```

