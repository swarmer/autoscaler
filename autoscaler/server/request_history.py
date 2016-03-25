from datetime import datetime, timedelta


class RequestHistory:
    def __init__(self):
        self.request_timestamps = []

    def record_request(self, request_datetime):
        self.request_timestamps.append(request_datetime)

    def get_last_requests(self, timespan_seconds):
        now = datetime.now()
        boundary = now - timedelta(seconds=timespan_seconds)
        return [dt for dt in self.request_timestamps if dt >= boundary]
