from enum import Enum


class CertType(Enum):
    ignore_rsa_link_cert = 1
    ed25519_id_cert = 2
    ignore_rsa_auth_cert = 3
    ed25519_id_signing_cert = 4
    ed25519_signing_link_cert = 5
    ignore_ed25519_xxxxx = 6
    ed25519_rsa_x_cert = 7
