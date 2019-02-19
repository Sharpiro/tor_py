import socket as socket_lib
import ssl


class SocketInfo:
    url: str = ""
    host: str = ""
    port: int = ""
    socket: socket_lib.socket = None

    def __init__(self, url: str, host: str, port: int, socket: socket_lib.socket):
        self.url = url
        self.host = host
        self.port = port
        self.socket = socket


def _get_host_and_port(url):
    host_and_port = url.split(":")
    host = host_and_port[0]
    port = 443 if len(host_and_port) == 1 else int(host_and_port[1])
    return (host, port)


def _wrap_tls_socket(socket, host):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    tls_socket = context.wrap_socket(socket, server_hostname=host)
    return tls_socket


def create_tls_socket(url):
    host, port = _get_host_and_port(url)
    plain_socket = socket_lib.create_connection((host, port))
    tls_socket = _wrap_tls_socket(plain_socket, host)
    socket_info = SocketInfo(url, host, port, tls_socket)
    return socket_info


# headers_end = 0
# for i, _ in enumerate(initial_response):
#     if i + 4 >= len(initial_response): break
#     if initial_response[i] != ord("\r") or initial_response[i+1] != ord('\n'): continue
#     if initial_response[i+2] != ord("\r") or initial_response[i+3] != ord('\n'): continue
#     headers_end = i
#     break

# headers = initial_response[0:headers_end]
# headers_text = headers.decode()

# split = headers_text.split("\r\n")
# pprint.pprint(split)
# content_length = split[len(split)-1]
# pprint.pprint(int(content_length.split(":")[1].strip()))
