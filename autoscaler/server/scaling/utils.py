import importlib
import re


def _import_class(path):
    tokens = path.split('.')
    module_path = '.'.join(tokens[:-1])
    module = importlib.import_module(module_path)
    return getattr(module, tokens[-1])


def get_algorithm(settings):
    algorithm_settings = settings['scaling_algorithm']
    algorithm_class_path = algorithm_settings['algorithm_class']
    algorithm_class = _import_class(algorithm_class_path)
    algorithm = algorithm_class(algorithm_settings)
    return algorithm


def get_cluster_adapter(settings):
    cluster_settings = settings['cluster_adapter']
    adapter_class_path = cluster_settings['adapter_class']
    cluster_adapter_class = _import_class(adapter_class_path)
    cluster_adapter = cluster_adapter_class(cluster_settings)
    return cluster_adapter


def parse_interval(interval_string: str):
    match = re.match(r'(\d+)s', interval_string)
    if match:
        return int(match.group(1))
    else:
        raise ValueError('Only intervals in seconds (ex. 30s) are supported')
