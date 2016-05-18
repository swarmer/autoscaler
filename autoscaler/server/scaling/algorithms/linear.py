from autoscaler.server.request_history import RequestHistory
from autoscaler.server.scaling.utils import parse_interval


class LinearScalingAlgorithm:
    def __init__(self, algorithm_config):
        self.interval_seconds = parse_interval(
            algorithm_config['interval_seconds']
        )
        self.requests_per_instance_interval = (
            algorithm_config['requests_per_instance_interval']
        )

    def get_instance_count(self, request_history: RequestHistory):
        requests = request_history.get_last_requests(self.interval_seconds)
        return max(1, len(requests) // self.requests_per_instance_interval)
