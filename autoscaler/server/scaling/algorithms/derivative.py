import math

from autoscaler.server.request_history import RequestHistory
from autoscaler.server.scaling.utils import parse_interval


class DerivativeScalingAlgorithm:
    def __init__(self, algorithm_config):
        self.interval_seconds = parse_interval(
            algorithm_config['interval']
        )
        self.requests_per_instance_interval = (
            algorithm_config['requests_per_instance_interval']
        )

    def get_instance_count(self, request_history: RequestHistory):
        (interval1, interval2) = request_history.get_last_intervals(
            self.interval_seconds, 2
        )

        expected_request_count = interval2 + (interval2 - interval1)
        return max(1, math.ceil(
            expected_request_count / self.requests_per_instance_interval)
        )
