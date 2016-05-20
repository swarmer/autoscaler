import bisect
from datetime import datetime, timedelta


class RequestHistory:
    def __init__(self):
        self.request_timestamps = []

    def record_request(self, request_datetime):
        self.request_timestamps.append(request_datetime)

    def get_last_intervals(self, timespan_seconds, interval_count):
        intervals = []
        now = self.get_current_datetime()
        timespan = timedelta(seconds=timespan_seconds)

        first_relevant_dt = now - timespan * interval_count
        first_relevant_index = bisect.bisect_left(
            self.request_timestamps, first_relevant_dt
        )

        for i in range(interval_count):
            start = now - timespan * (i + 1)
            end = start + timespan
            intervals.append([
                dt
                for dt in self.request_timestamps[first_relevant_index:]
                if start <= dt < end
            ])

        return reversed(intervals)

    def get_current_datetime(self):
        return datetime.now()
