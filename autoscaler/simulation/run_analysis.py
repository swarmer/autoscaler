import sys
import pickle

from matplotlib import pyplot


COLORS = ['green', 'blue', 'orange', 'cyan']


def main():
    with open(sys.argv[1], 'rb') as input_file:
        request_volumes, scaling_histories = pickle.load(input_file)

    request_times = [
        request_time
        for request_time, request_count in request_volumes
    ]
    request_counts = [
        request_count
        for request_time, request_count in request_volumes
    ]
    pyplot.plot(request_times, request_counts,
                label='Request volume', color='gray', alpha=0.5)

    for color, (algorithm_name, scaling_history) in zip(COLORS,
                                                        sorted(scaling_histories.items())):
        if not any(name in algorithm_name.lower() for name in ['spline', 'derivative', 'linear']):
            continue

        rescale_times = [
            rescale_time
            for rescale_time, instance_count in scaling_history
        ]
        instance_counts = [
            instance_count
            for rescale_time, instance_count in scaling_history
        ]
        pyplot.plot(rescale_times, instance_counts,
                    label=algorithm_name, color=color, alpha=1)

    pyplot.legend(loc='upper right')
    pyplot.show()


if __name__ == '__main__':
    main()
