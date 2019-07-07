def get_url_info(url: str):
    end_protocol_index = _index_of(url, "://")
    protocol = "http"
    hostname_start_index = 0
    if end_protocol_index >= 0:
        protocol = url[:end_protocol_index]
        hostname_start_index = end_protocol_index + 3

    hostname_and_path = url[hostname_start_index:]
    hostname = hostname_and_path
    port = "80"
    path = "/"
    path_start_index = _index_of(hostname_and_path, "/")
    if path_start_index >= 0:
        hostname = hostname_and_path[:path_start_index]
        path = hostname_and_path[path_start_index:]

    return protocol, hostname, port, path


def _index_of(data: str, search: str):
    try:
        end_protocol_index = data.index(search)
    except:
        end_protocol_index = -1
    return end_protocol_index
