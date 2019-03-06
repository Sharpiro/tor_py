from struct import unpack, pack
from py_socket.cells.payloads.cert_type import CertType


class Cert:

    def __init__(self, cert_type: CertType, certificate: bytes):
        self.cert_type = cert_type
        self.cert_size = len(certificate)
        self.cert = certificate


class CertsPayload:
    NUMBER_OF_CERTS_SIZE = 1
    CERT_TYPE_SIZE = 1
    CERT_LENGTH_SIZE = 2
    CERT_HEADER_SIZE = CERT_TYPE_SIZE + CERT_LENGTH_SIZE

    def __init__(self, certs: list = []):
        self.certs = certs

    def __repr__(self):
        return "(certs: {0})".format(self.certs)


def unpack_certs_payload(buffer: bytes) -> CertsPayload:
    number_of_certs = buffer[0]
    buffer = buffer[1:]

    certs_payload = CertsPayload()
    for _ in range(number_of_certs):
        cert_type_number, cert_length = unpack(
            ">BH", buffer[:CertsPayload.CERT_HEADER_SIZE])
        cert_type = CertType(cert_type_number)
        buffer = buffer[CertsPayload.CERT_HEADER_SIZE:]
        cert = unpack(f">{cert_length}s", buffer[:cert_length])[0]
        buffer = buffer[cert_length:]
        certs_payload.certs.append(Cert(cert_type, cert))
    pass


# def pack_certs_payload(certs_payload: VersionsPayload) -> bytes:
#     versions_buffer = pack('>' + 'H' * len(certs_payload.versions), *certs_payload.versions)
#     return versions_buffer
