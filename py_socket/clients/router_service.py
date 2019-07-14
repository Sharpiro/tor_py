import http.client


class RouterService:

    def __init__(self, ip_addr):
        self.ip_addr = ip_addr

    def get_router(self):
        conn = http.client.HTTPConnection(self.ip_addr)
        conn.request("GET", "/tor/server/authority")
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        data1 = r1.read()
        print(data1)
        return 1

    def get_routers(self):
        temp = b'a'
        pass
