from struct import unpack, pack

class VersionsPayload:
    VERSION_SIZE = 2

    versions: list = []

    def __init__(self, versions: list):
        self.versions = versions

    def __repr__(self):
        return "(versions: {0})".format(self.versions)


def unpack_versions_payload(buffer: bytes) -> (VersionsPayload, int):
    versions_list_length = int((len(buffer) / VersionsPayload.VERSION_SIZE))
    versions_list = list(unpack('>' + 'H' * versions_list_length, buffer))
    versions_payload = VersionsPayload(versions_list)
    return versions_payload


def pack_versions_payload(versions_payload: VersionsPayload) -> bytes:
    versions_buffer = pack('>' + 'H' * len(versions_payload.versions), *versions_payload.versions)
    return versions_buffer