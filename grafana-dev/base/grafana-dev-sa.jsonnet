function (
    redirect_url="unused",
    token_name="unknown"
)
[
{
  "apiVersion": "v1",
  "imagePullSecrets": [{ "name": token_name }],
  "kind": "ServiceAccount",
  "metadata":
    {
      "annotations":
        {
          "openshift.io/internal-registry-pull-secret-ref": token_name,
          "serviceaccounts.openshift.io/oauth-redirectreference.grafana": '{"kind":"OAuthRedirectReference","apiVersion":"v1","reference":{"kind":"Route","name":"grafana-dev"}}',
        },
      "name": "grafana-dev",
      "namespace": "open-cluster-management-observability",
    },
  "secrets": [{ "name": token_name }],
}
]