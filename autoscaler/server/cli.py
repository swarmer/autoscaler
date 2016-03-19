import argparse

import yaml

from .request_history import RequestHistory
from .listener import run_listener


def main():
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

    request_history = RequestHistory()

    run_listener(
        request_history,
        settings['listen_host'],
        settings['listen_port']
    )


if __name__ == '__main__':
    main()
