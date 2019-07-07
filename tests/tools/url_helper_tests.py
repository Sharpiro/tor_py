from unittest import TestCase
from py_socket.tools.url_helper import get_url_info


class NetInfoPayloadTests(TestCase):
    def test_http(self):
        url = "http://www.httpvshttps.com"
        protocol, hostname, port, path = get_url_info(url)
        self.assertEqual(protocol, "http")
        self.assertEqual(hostname, "www.httpvshttps.com")
        self.assertEqual(port, "80")
        self.assertEqual(path, "/")

    def test_http_slash(self):
        url = "http://www.httpvshttps.com/"
        protocol, hostname, port, path = get_url_info(url)
        self.assertEqual(protocol, "http")
        self.assertEqual(hostname, "www.httpvshttps.com")
        self.assertEqual(port, "80")
        self.assertEqual(path, "/")

    def test_https(self):
        url = "https://www.httpvshttps.com"
        protocol, hostname, port, path = get_url_info(url)
        self.assertEqual(protocol, "https")
        self.assertEqual(hostname, "www.httpvshttps.com")
        self.assertEqual(port, "80")
        self.assertEqual(path, "/")

    def test_no_protocol(self):
        url = "www.httpvshttps.com"
        protocol, hostname, port, path = get_url_info(url)
        self.assertEqual(protocol, "http")
        self.assertEqual(hostname, "www.httpvshttps.com")
        self.assertEqual(port, "80")
        self.assertEqual(path, "/")

    def test_path(self):
        url = "http://statichostsharp.blob.core.windows.net/misc/rules.json"
        protocol, hostname, port, path = get_url_info(url)
        self.assertEqual(protocol, "http")
        self.assertEqual(hostname, "statichostsharp.blob.core.windows.net")
        self.assertEqual(port, "80")
        self.assertEqual(path, "/misc/rules.json")
