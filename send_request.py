#!/usr/bin/env python
import argparse

from autoscaler.client.sender import send_request_data


def main():
    parser = argparse.ArgumentParser(
        description='Send a timestamp to the autoscaler listener'
    )
    parser.add_argument(
        '--host',
        type=str,
        default='127.0.0.1',
        help='autoscaler host'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8740,
        help='autoscaler port'
    )
    args = parser.parse_args()

    send_request_data(args.host, args.port)


if __name__ == '__main__':
    main()
