import random
import math
from datetime import timedelta

from scipy.stats import norm


class SpikeRequestGenerator:
    def __init__(self, constant_rpm, quantum_seconds, max_error,
                 start_datetime):
        self.quantum_seconds = quantum_seconds
        self.max_error = max_error
        self.constant_rpq = math.ceil(constant_rpm * (quantum_seconds / 60))
        self.current_timestamp = start_datetime

    def get_new_quantum_requests(self):
        self.current_timestamp += timedelta(seconds=self.quantum_seconds)

        rpq = self.constant_rpq + random.randint(
            -self.max_error, self.max_error
        )
        rpq += norm.pdf(self.current_timestamp.minute - 30, scale=10) * 20000
        rpq = int(rpq)

        request_datetimes = [
            self.current_timestamp for _ in range(rpq)
        ]
        return request_datetimes
