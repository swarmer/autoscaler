import requests
import warnings


class KubernetesClusterAdapter:
    def __init__(self, cluster_config):
        self.api_host = cluster_config['kubernetes_api_host']
        self.user = cluster_config['kubernetes_user']
        self.password = cluster_config['kubernetes_password']
        self.rc_name = cluster_config['kubernetes_rc_name']

    def scale(self, instance_count):
        scale_url = 'https://%s/api/v1/namespaces/default' \
                    '/replicationcontrollers/hello/scale' % self.api_host
        data = {
            'metadata': {
                'namespace': 'default',
                'name': self.rc_name,
            },
            'spec': {
                'replicas': instance_count,
            }
        }

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            requests.put(
                scale_url, json=data,
                auth=(self.user, self.password), verify=False
            )
