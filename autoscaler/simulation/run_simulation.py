import pickle
from datetime import datetime, timedelta

from autoscaler.server.request_history import RequestHistory
from autoscaler.server.scaling.utils import get_algorithm
from .request_generators import (
    RandomWalkRequestGenerator,
    SpikeRequestGenerator,
)

QUANTUM_SECONDS = 30
SCALING_INTERVAL_SECONDS = 30
START_DATETIME = datetime(
    year=2000, month=1, day=1, hour=0, minute=0, second=0
)
END_DATETIME = datetime(
    year=2000, month=1, day=3, hour=0, minute=0, second=0
)
SCALING_ALGORITHM_CONFIGS = [
    {
        'algorithm_class':
            'autoscaler.server.scaling.algorithms.LinearScalingAlgorithm',
        'interval': '210s',
        'requests_per_instance_interval': 7,
    },
    {
        'algorithm_class':
            'autoscaler.server.scaling.algorithms.WeightedScalingAlgorithm',
        'interval': '210s',
        'weights': [0.1, 0.2, 0.7],
        'requests_per_instance_interval': 7,
    },
    {
        'algorithm_class':
            'autoscaler.server.scaling.algorithms.DerivativeScalingAlgorithm',
        'interval': '210s',
        'requests_per_instance_interval': 7,
    },
    {
        'algorithm_class':
            'autoscaler.server.scaling.algorithms.SplineScalingAlgorithm',
        'interval': '210s',
        'requests_per_instance_interval': 7,
    },
]
# REQUEST_GENERATOR_FACTORY = lambda: RandomWalkRequestGenerator(
#     starting_rpm=100, quantum_seconds=QUANTUM_SECONDS, walk_speed=3,
#     start_datetime=START_DATETIME
# )
REQUEST_GENERATOR_FACTORY = lambda: SpikeRequestGenerator(
    constant_rpm=100, quantum_seconds=QUANTUM_SECONDS, max_error=20,
    start_datetime=START_DATETIME
)
OUTPUT_FILE = 'simulation.pickle'


class SimulationRequestHistory(RequestHistory):
    def __init__(self, current_datetime):
        super().__init__()
        self._current_datetime = current_datetime

    def get_current_datetime(self):
        return self._current_datetime


def run():
    scaling_algorithms = []
    for algorithm_config in SCALING_ALGORITHM_CONFIGS:
        scaling_algorithms.append(
            get_algorithm({
                'scaling_algorithm': algorithm_config
            })
        )
    quantum_delta = timedelta(seconds=QUANTUM_SECONDS)

    scaling_histories = [[] for _ in scaling_algorithms]
    request_volumes = []
    request_generator = REQUEST_GENERATOR_FACTORY()
    request_history = SimulationRequestHistory(START_DATETIME)
    current_timestamp = START_DATETIME
    seconds_until_scaling = SCALING_INTERVAL_SECONDS

    print('Starting simulation...')
    while current_timestamp <= END_DATETIME:
        request_history._current_datetime = current_timestamp
        new_requests = request_generator.get_new_quantum_requests()
        request_volumes.append((current_timestamp, len(new_requests)))
        request_history.request_timestamps.extend(new_requests)

        if seconds_until_scaling <= 0:
            for i, scaling_algorithm in enumerate(scaling_algorithms):
                instance_count = scaling_algorithm.get_instance_count(
                    request_history
                )
                scaling_histories[i].append(
                    (current_timestamp, instance_count)
                )
            seconds_until_scaling += SCALING_INTERVAL_SECONDS

        current_timestamp += quantum_delta
        seconds_until_scaling -= QUANTUM_SECONDS

        if current_timestamp.minute == 0 and current_timestamp.second == 0:
            print('Current timestamp: %s' % current_timestamp)
    print('Done')

    scaling_history_data = {}
    for algorithm_config, scaling_history in zip(SCALING_ALGORITHM_CONFIGS,
                                                 scaling_histories):
        algorithm_name = algorithm_config['algorithm_class']
        scaling_history_data[algorithm_name] = scaling_history
    with open(OUTPUT_FILE, 'wb') as output_file:
        pickle.dump((request_volumes, scaling_history_data), output_file)
    print('Data saved')


if __name__ == '__main__':
    run()
