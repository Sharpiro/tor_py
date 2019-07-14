from http.server import BaseHTTPRequestHandler, HTTPServer
from py_socket.clients import TorClient, Node, HttpGenerator, RouterService
from py_socket.sockets import create_tls_socket
import json


class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        self.paths = {
            "/hello"
        }
        super().__init__(request, client_address, server)

    # GET
    def do_GET(self):
        if self.path in self.paths:
            self.send_response(200)
            if self.path == "/hello":
                json_string = json.dumps(self.hello())
        else:
            self.send_response(404)
            json_string = "Not Found"

        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(json_string, "utf8"))

    def hello(self):
        guard_node = Node("128.31.0.61", "f+XpLjonwta50/OeD71k0oFenh2D+rL/P0f2CxhsbFo=",
                          "MIGJAoGBAMOi1FV0CdvtCBXiokmeYjyzs9aeSj3FOVbii64F8kE/+sshO2TbMv1PTjNnC6FeZ0v0AW6i35tWjFdyRzKdC3XPk1bS1A5C5xZupC+/jsPRB3w0GITWalSWLvbNQwuix9v4hS4wKySdypx7JU0KSFt1pbZHOf7OsbnO047w4EApAgMBAAE=")
        guard_node.socket = create_tls_socket(guard_node.ip_addr)
        exit_node = Node("176.10.99.201", "yOJokRL2ooq99RZPJ04mNDSfQIZtTA78dKp+c096zU0=",
                         "MIGJAoGBAMw558IiHkrZhEHW83ZjEdWj+vFOP0bHTQqHP+NI7umefWc4VMHcjD0JSclaU2QL/B3mbkNNsct1Zc3nF7HV8F4tG1us1caA36p/Wxzgd8vRHwTixvz82II4KLE02OudCmgWg956JhN0lrI/mRj2SMsOfIMsq+V09qFkrM1HzsDZAgMBAAE=")
        tor_client = TorClient(guard_node, exit_node)
        tor_client.create_circuit()
        return {"nodes": [guard_node.ip_addr, exit_node.ip_addr], "message": "circuit created"}


print('starting server...')
server_address = ('localhost', 8080)
httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
httpd.serve_forever()
