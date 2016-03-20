import argparse
import logging

import yaml

from .request_history import RequestHistory
from .listener import run_listener


def configure_logging(log_level_str):
    log_level = getattr(logging, log_level_str.upper())
    logging.basicConfig(
        format='[%(levelname)s %(asctime)s] %(message)s',
        level=log_level_str,
    )


def setup():
    parser = argparse.ArgumentParser(description='Autoscaling server')
    parser.add_argument(
        '--config',
        type=open,
        default='config.yaml',
        help='path to a configuration file'
    )
    args = parser.parse_args()

    config_file = args.config
    try:
        settings = yaml.load(config_file)
    finally:
        config_file.close()

    configure_logging(settings['log_level'])

    return settings


def main():
    settings = setup()

    request_history = RequestHistory()
    try:
        run_listener(
            request_history,
            settings['listen_host'],
            settings['listen_port']
        )
    except KeyboardInterrupt:
        logging.info('Exiting')
        pass


if __name__ == '__main__':
    main()
