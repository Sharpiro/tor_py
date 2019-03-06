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
  * identity key digest
    * rsa or ed25519 signed by rsa
    * 1024 bits?
    * 4.4.2 check out?
  * ntor onion key
    * curve25519

## useful source locations

* connection.c: 4314
  * writing to buffer
* connection_or.c: 2334
  * write variable length cell (versions)
* channeltls.c: 1435
  * process versions cell

## what is otheraddr in netinfo cell

Hello, can anyone tell me what the "OTHERADDR" ip address found in the NETINFO cell is used for?  The docs say it may help an initiator to learn which address their connections may be originating from.  But I have no idea what that would mean.