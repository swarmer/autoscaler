from autoscaler.server.request_history import RequestHistory


class LinearScalingAlgorithm:
    def __init__(self, algorithm_config):
        self.requests_per_instance_interval = (
            algorithm_config['requests_per_instance_interval']
        )

    def get_instance_count(self, request_history: RequestHistory,
                           interval_seconds):
        requests = request_history.get_last_requests(interval_seconds)
        return max(1, len(requests) // self.requests_per_instance_interval)
