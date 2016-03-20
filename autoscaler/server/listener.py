import socketserver
import logging


def run_listener(history, listen_host, listen_port):
    class ListenerUdpHandler(socketserver.BaseRequestHandler):
        def handle(self):
            data, _ = self.request
            logging.info('Listener got data: %s', repr(data))

    server = socketserver.UDPServer(
        (listen_host, listen_port),
        ListenerUdpHandler
    )
    server.serve_forever()
