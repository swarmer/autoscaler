from datetime import datetime, timedelta


class RequestHistory:
    def __init__(self):
        self.request_timestamps = []

    def record_request(self, request_datetime):
        self.request_timestamps.append(request_datetime)

    def get_last_intervals(self, timespan_seconds, interval_count):
        intervals = []

        now = datetime.now()
        timespan = timedelta(seconds=timespan_seconds)
        for i in range(interval_count):
            start = now - timespan * (i + 1)
            end = start + timespan
            intervals.append([
                dt
                for dt in self.request_timestamps
                if start <= dt < end
            ])

        return reversed(intervals)
