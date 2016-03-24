class RequestHistory:
    def __init__(self):
        self.request_timestamps = []

    def record_request(self, request_datetime):
        self.request_timestamps.append(request_datetime)
