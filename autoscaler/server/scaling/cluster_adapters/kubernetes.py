import requests
import warnings


class KubernetesClusterAdapter:
    def __init__(self, cluster_config):
        self.api_host = cluster_config['kubernetes_api_host']
        self.user = cluster_config['kubernetes_user']
        self.password = cluster_config['kubernetes_password']
        self.deployment = cluster_config['kubernetes_deployment']
        self.namespace = cluster_config['kubernetes_namespace']

    def scale(self, instance_count):
        scale_url = (
            'https://{api_host}/apis/extensions/v1beta1/namespaces/{namespace}'
            '/deployments/{deployment}/scale'
        ).format(
            api_host=self.api_host, deployment=self.deployment, namespace=self.namespace
        )

        data = {
            'metadata': {
                'namespace': self.namespace,
                'name': self.deployment,
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
