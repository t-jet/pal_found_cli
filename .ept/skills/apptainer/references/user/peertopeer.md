# IPFS Peer-To-Peer (P2P) Clusters
It is possible for users of Apptainer to use [IPFS](https://ipfs.tech/) clusters as sources for their container images. This is done through an IPFS HTTP Gateway that fetches data from the IPFS network.
There are both private and public IPFS Gateways. Check with your IPFS Cluster administrator to find out which gateway to use.

```
$ export IPFS_GATEWAY=http://127.0.0.1:8080

$ export IPFS_GATEWAY=https://ipfs.io

```

It can be configured in `~/.ipfs/gateway` or `/etc/ipfs/gateway`.
A daemon on localhost will _automatically_ be detected as a gateway.
## Content addressing
In IPFS, data is chunked into blocks, which are assigned a unique identifier called a **Content Identifier (CID)**. This means that the content is addressable by _what_ it is, and not _where_ it is stored like with a regular HTTP URL.
A CID (version 1) is a long string in “[multiformat](https://multiformats.io/)”:
`bafkreihdwdcefgh4dqkjv67uzcmw7ojee6xedzdetojuzjevtenxquvyku`
The parts of a CID can be inspected with the [CID Inspector](https://cid.ipfs.tech/#bafkreihdwdcefgh4dqkjv67uzcmw7ojee6xedzdetojuzjevtenxquvyku):

```
base32 - cidv1 - raw - (sha2-256 : 256 : E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855)``

```

Note: There is an older CID version 0 as well, it is **not** supported by Apptainer.
## IPFS Kubo CLI
To upload an image to IPFS, use `ipfs`:

```
$ ipfs add --cid-version 1 lolcow.sif
added bafybeice667c6gxovimsb6gnk6vex7vhzluhkl5hjv4ac4lhilxn52c43m lolcow.sif

```

You can download as well, with `ipfs`:

```
$ ipfs get bafybeice667c6gxovimsb6gnk6vex7vhzluhkl5hjv4ac4lhilxn52c43m -o lolcow.sif

```

## Using IPFS
Running an image from IPFS is done like:

```
$ apptainer run ipfs://bafybeice667c6gxovimsb6gnk6vex7vhzluhkl5hjv4ac4lhilxn52c43m

```

Or you can pull it to a regular file first:

```
$ apptainer pull lolcow.sif ipfs://bafybeice667c6gxovimsb6gnk6vex7vhzluhkl5hjv4ac4lhilxn52c43m

```

## Advanced
To make version 1 the default, instead of having to use a flag, you can run:

```
ipfs config --json Import.CidVersion 1

```

You can wrap the image with a directory, to record the filename and details:

```
$ ipfs add -w lolcow.sif
added bafybeice667c6gxovimsb6gnk6vex7vhzluhkl5hjv4ac4lhilxn52c43m lolcow.sif
added bafybeiacfjtqrksxw5udplhs3rpvd7dyeqe7thzompdip635ps7o6sbp4q
$ apptainer run ipfs://bafybeiacfjtqrksxw5udplhs3rpvd7dyeqe7thzompdip635ps7o6sbp4q/lolcow.sif

```

For testing purposes, you can run a local-only IPFS daemon without connecting it:

```
$ ipfs daemon --offline
...
Swarm not listening, running in offline mode.
RPC API server listening on /ip4/127.0.0.1/tcp/5001
WebUI: http://127.0.0.1:5001/webui
Gateway server listening on /ip4/127.0.0.1/tcp/8080
Daemon is ready

```

## Archives
If you need to back up or transport content-addressed data using a non-IPFS medium, CID can be preserved with CAR files (similar to TAR, for data).

```
$ ipfs dag export bafybeice667c6gxovimsb6gnk6vex7vhzluhkl5hjv4ac4lhilxn52c43m >lolcow.car

$ ipfs dag import <lolcow.car
Pinned root  bafybeice667c6gxovimsb6gnk6vex7vhzluhkl5hjv4ac4lhilxn52c43m     success

```

