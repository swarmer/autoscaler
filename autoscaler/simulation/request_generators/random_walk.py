import random
import math
from datetime import timedelta


class RandomWalkRequestGenerator:
    def __init__(self, starting_rpm, quantum_seconds, walk_speed,
                 start_datetime):
        self.quantum_seconds = quantum_seconds
        self.walk_speed = walk_speed
        self.current_rpq = math.ceil(starting_rpm * (quantum_seconds / 60))
        self.current_timestamp = start_datetime

    def get_new_quantum_requests(self):
        self.current_timestamp += timedelta(seconds=self.quantum_seconds)

        self.current_rpq += random.randint(
            max(-self.current_rpq, -self.walk_speed),
            self.walk_speed
        )

        request_datetimes = [
            self.current_timestamp for _ in range(self.current_rpq)
        ]
        return request_datetimes
