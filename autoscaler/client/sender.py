import socket
import json
from datetime import datetime

from autoscaler.server.listener import DATETIME_FORMAT


def send_request_data(autoscaler_host, autoscaler_port, request_datetime=None):
    if request_datetime is None:
        request_datetime = datetime.now()

    payload = {'datetime': request_datetime.strftime(DATETIME_FORMAT)}
    binary_data = json.dumps(payload).encode('utf-8')

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client_socket.sendto(binary_data, (autoscaler_host, autoscaler_port))
