import sys
import pickle

from matplotlib import pyplot


def main():
    with open(sys.argv[1], 'rb') as input_file:
        request_volumes, scaling_history = pickle.load(input_file)

    request_times = [
        request_time
        for request_time, request_count in request_volumes
    ]
    request_counts = [
        request_count
        for request_time, request_count in request_volumes
    ]

    rescale_times = [
        rescale_time
        for rescale_time, instance_count in scaling_history
    ]
    instance_counts = [
        instance_count
        for rescale_time, instance_count in scaling_history
    ]

    pyplot.plot(request_times, request_counts,
                label='Request volume', color='r')
    pyplot.plot(rescale_times, instance_counts,
                label='Autoscaler output', color='g')
    pyplot.legend(loc='upper right')
    pyplot.show()


if __name__ == '__main__':
    main()
