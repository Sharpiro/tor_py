from enum import Enum


class CellType(Enum):
    destroy = 4
    versions = 7
    net_info = 8
    create2 = 10
    created2 = 11
    certs = 129
    auth_challenge = 130


class ErrorCode(Enum):
    none = 0
    # 1 = PROTOCOL(Tor protocol violation.)
    protocol = 1
    # 2 = INTERNAL(Internal error.)
    internal = 2
    # 3 = REQUESTED(A client sent a TRUNCATE command.)
    requested = 3
    # 4 = HIBERNATING(Not currently operating/trying to save bandwidth.)
    hibernating = 4
    # 5 = RESOURCELIMIT(Out of memory, sockets, or circuit IDs.)
    resourcelimit = 5
    # 6 = CONNECTFAILED(Unable to reach relay.)
    connectfailed = 6
    # 7 = OR_IDENTITY(Connected to relay, but its OR identity was not as expected.)
    or_identity = 7
    # 8 = OR_CONN_CLOSED(The OR connection that was carrying this circuit died.)
    or_conn_closed = 8
    # 9 = FINISHED(The circuit has expired for being dirty or old.)
    finished = 9
    # 10 = TIMEOUT(Circuit construction took too long)
    timeout = 10
    # 11 = DESTROYED(The circuit was destroyed w/o client TRUNCATE)
    destroyed = 11
    # 12 = NOSUCHSERVICE(Request for unknown hidden service)
    no_such_service = 12
