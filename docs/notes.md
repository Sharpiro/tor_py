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

## Questions

* what is otheraddr in netinfo cell
  * Hello, can anyone tell me what the "OTHERADDR" ip address found in the NETINFO cell is used for?  The docs say it may help an initiator to learn which address their connections may be originating from.  But I have no idea what that would mean.
