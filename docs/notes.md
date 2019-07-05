# Notes

## Overview

* max payload size = 509
* negotiated link protocol version 3-5
  * using 3 for this

## tor in-protocol (v3) handshake

* client sends VERSIONS
* router sends VERSIONS
* router sends CERTS
* router sends AUTH_CHALLENGE
* router sends NETINFO
* client *optionally* sends CERTS
* client *optionally* sends AUTHENTICATE
* client sends NETINFO

## tor circuit creation

* client sends CREATE2
* server sends CREATED2 or DESTROY

## create2 cell

* not using fast
* using ntor crypto handshake
* handshake length = 84 (or 88?)

### the ntor handshake

* requirements
  * identity key digest (fingerprint)
    * sha 1 hash of one of the rsa public keys (2nd one in my test)
    * the signing key!
    * 1024 bits public key?
    * 1120 bits total
  * ntor onion key
    * curve25519
    * 32 bytes

## useful source locations

* extend2
  * onion.c: 621
  * onion_crypt.c: 110
  * onion_ntor.c: 93
* relay_crypto.c: 262
  * relay_crypto_init
  * generate keys and sha1 digests
* relay_crypto.c: 185
  * relay_encrypt_cell_outbound
* relay_crypto.c: 111
  * relay decrypt cell
* relay.c: 548
  * create relay cell
* circuitbuild.c: 939
  * backbone function for building circuits
* connection.c: 4314
  * writing to buffer
* connection_or.c: 2334
  * write variable length cell (versions)
* channeltls.c: 1435
  * process versions cell
* src/test/ntor_ref.py

## Directories

### Directory Links

* <http://128.31.0.61/tor/server/authority>
* <http://128.31.0.61/tor/server/all>

### Feedback

#### tor-spec

* It was very difficult to figure out where to find the Server Identity and how to figure out its "digest"
* 5.1.2 EXTEND AND EXTENDED cells
  * Ed25519 identity says it is a 32 byte fingerprint.  However the explanation a few paragraphs down says that it is the Ed25519 identity key of the target node.
* 5.5.1 has redundant paragraph
* some libraries like nacl compute shared secret differently
* when sending a created2 cell, if an invalid ntor onion key is sent, the server doesn't send back an error, only after the auth is computed would you know there is an issue
* 0.3. Ciphers
  * What does it mean "We also require AES256" right after saying "we use 128-bit AES in counter mode"
  * May want to clarify that you use 256 bit keys instead
  * Though that actually doesn't make since since AES 256 requires 32 byte keys, and Tor uses 16 bytes keys for stream cipher
* onion skin unclear when using extend2/ntor
* no error received when sending relay extend2 as relay instead of relay early

## Questions

* what is otheraddr in netinfo cell
  * Hello, can anyone tell me what the "OTHERADDR" ip address found in the NETINFO cell is used for?  The docs say it may help an initiator to learn which address their connections may be originating from.  But I have no idea what that would mean.

## Debug

* relay debug
  * what are df/db for?
  * is hash input incorrect
  * aes counter param wrong
  * is sha 1 the correct hash
    * checked in tor code, seems to be
  * are aes key sizes accurate
    * seem like they have to be 16 bytes, despite confusing wording
  * are we encrypting the correct portion
    * should be cell payload - 509 bytes
  * is key derivation wrong
    * tested seems fine
  * are we using an exit node
    * yes

## Relay simple GET request

OP -> Begin
OR -> Connected
OP -> Data
OR -> Data
OR -> Data
OP -> End
