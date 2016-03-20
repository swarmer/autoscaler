import socketserver
import logging
import json
from datetime import datetime


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def run_listener(history, listen_host, listen_port):
    class ListenerUdpHandler(socketserver.BaseRequestHandler):
        def handle(self):
            data_bytes, _ = self.request
            logging.debug('Listener got data: %s', repr(data_bytes))
            try:
                data_string = data_bytes.decode('utf-8')
                data_dict = json.loads(data_string)
            except (UnicodeDecodeError, json.JSONDecodeError):
                logging.error(
                    'Listener: cannot parse input data: %s',
                    data_bytes
                )
                return

            try:
                request_datetime = datetime.strptime(
                    data_dict['datetime'],
                    DATETIME_FORMAT,
                )
            except (ValueError, KeyError) as e:
                logging.error('Cannot extract request datetime: %s', e)
                return

            logging.info('Recording a request at %s', request_datetime)
            history.record_request(request_datetime)

    server = socketserver.UDPServer(
        (listen_host, listen_port),
        ListenerUdpHandler
    )
    server.serve_forever()
