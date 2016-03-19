import socketserver


def run_listener(history, listen_host, listen_port):
    class ListenerUdpHandler(socketserver.BaseRequestHandler):
        def handle(self):
            data, _ = self.request[0]
            print('got data: ' + repr(data))

    server = socketserver.UDPServer(
        (listen_host, listen_port),
        ListenerUdpHandler
    )
    server.serve_forever()
