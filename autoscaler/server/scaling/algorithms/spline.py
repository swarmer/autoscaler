import math

import scipy.interpolate

from autoscaler.server.request_history import RequestHistory
from autoscaler.server.scaling.utils import parse_interval


class SplineScalingAlgorithm:
    def __init__(self, algorithm_config):
        self.interval_seconds = parse_interval(
            algorithm_config['interval']
        )
        self.requests_per_instance_interval = (
            algorithm_config['requests_per_instance_interval']
        )

    def get_instance_count(self, request_history: RequestHistory):
        (interval1, interval2, interval3) = request_history.get_last_intervals(
            self.interval_seconds, 3
        )

        x_values = [1, 2, 3]
        y_values = [len(interval1), len(interval2), len(interval3)]
        interpolated_function = scipy.interpolate.InterpolatedUnivariateSpline(
            x_values, y_values, k=2,
        )

        expected_request_count = interpolated_function(len(x_values) + 1)
        return max(1, math.ceil(
            expected_request_count / self.requests_per_instance_interval)
        )
