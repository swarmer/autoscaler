import sys
import pickle
import statistics

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
        rescale_times = [
            rescale_time
            for rescale_time, instance_count in scaling_history
        ]
        instance_counts = [
            instance_count
            for rescale_time, instance_count in scaling_history
        ]

        diffs = []
        overs = []
        unders = []
        changes = []
        for i, (req_count, inst_count) in enumerate(zip(request_counts[1:], instance_counts)):
            diffs.append(abs(inst_count - req_count))
            overs.append(inst_count - req_count if inst_count > req_count else 0)
            unders.append(req_count - inst_count if req_count > inst_count else 0)
            if i != 0:
                changes.append(abs(inst_count - instance_counts[i - 1]))

        print(algorithm_name)
        print('Average difference: %.2f' % statistics.mean(diffs))
        print('Average over: %.2f' % statistics.mean(overs))
        print('Average under: %.2f' % statistics.mean(unders))
        print('Average scale change: %.2f' % statistics.mean(changes))
        print()

        pyplot.plot(rescale_times, instance_counts,
                    label=algorithm_name, color=color, alpha=1)

    pyplot.legend(loc='lower right')
    pyplot.show()


if __name__ == '__main__':
    main()
