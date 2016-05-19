import math

from autoscaler.server.request_history import RequestHistory
from autoscaler.server.scaling.utils import parse_interval


class WeightedScalingAlgorithm:
    def __init__(self, algorithm_config):
        self.interval_seconds = parse_interval(
            algorithm_config['interval']
        )
        self.requests_per_instance_interval = (
            algorithm_config['requests_per_instance_interval']
        )
        self.weights = algorithm_config['weights']

    def get_instance_count(self, request_history: RequestHistory):
        intervals = request_history.get_last_intervals(
            self.interval_seconds, len(self.weights)
        )

        normalized_weights = self._normalized_weights(self.weights)
        weighted_request_count = sum(
            len(interval) * weight
            for weight, interval in zip(normalized_weights, intervals)
        )

        return max(1, math.ceil(
            weighted_request_count / self.requests_per_instance_interval)
        )

    @staticmethod
    def _normalized_weights(weights):
        weight_sum = sum(weights)
        return [weight / weight_sum for weight in weights]
