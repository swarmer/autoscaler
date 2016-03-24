import logging
import threading
import time


class Rescaler:
    def __init__(self, request_history, algorithm,
                 cluster_adapter, interval_seconds):
        self.request_history = request_history
        self.algorithm = algorithm
        self.cluster_adapter = cluster_adapter
        self.interval_seconds = interval_seconds

        self.exit_condition = threading.Condition()

    def rescale(self):
        instance_count = self.algorithm.get_instance_count(
            self.request_history,
            self.interval_seconds
        )

        logging.info('Scaling cluster to %d instances', instance_count)
        self.cluster_adapter.scale(instance_count)

    def run(self):
        logging.info(
            'Running periodic rescaling every %d seconds',
            self.interval_seconds
        )

        try:
            while True:
                self.rescale()

                with self.exit_condition:
                    exit = self.exit_condition.wait(
                        timeout=self.interval_seconds
                    )
                if exit:
                    break
        except Exception as e:
            logging.error('Exception: %s', str(e))

    def start(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        return thread

    def stop(self):
        with self.exit_condition:
            self.exit_condition.notify()
