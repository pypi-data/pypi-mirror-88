"""AWS EKS KFP helpers."""
from typing import Dict
from kfp import Client
import boto3
import os
import yaml
from pathlib import Path
from awscli.customizations.eks.get_token import TokenGenerator, STSClientFactory
import botocore.session


def KFPClientFactory(
    cluster_name: str,
    cluster_region: str,
    namespace: str = "kubeflow",
    role_arn=None,
):
    """Generate KFP client authed for AWS EKS.

    Args:
        cluster_name (str): cluster name
        cluster_region (str): cluster region
        namespace (str): k8 namespace
        role_arn (str): (optional) role to assume when requesting token for cluster

    Returns:
        kfp.Client: authenticated instance of kfp client
    """
    eks = _get_eks_client(cluster_region, role_arn)
    kube_config = _get_kube_config(eks, cluster_name)

    sts_client = _get_sts_client(cluster_region, role_arn)
    kube_token = _get_token(sts_client, cluster_name)

    kube_config["users"][0]["user"]["token"] = kube_token
    kubeconfig_filepath = _save_kube_config(kube_config)

    return Client(namespace=namespace), kubeconfig_filepath


def _get_eks_client(region_name, role_arn=None):
    service = "eks"
    if role_arn is None:
        return boto3.client(service, region_name=region_name)

    stsresponse = boto3.client("sts").assume_role(
        RoleArn=role_arn, RoleSessionName="kfputils"
    )
    return boto3.client(
        service,
        region_name=region_name,
        aws_access_key_id=stsresponse["Credentials"]["AccessKeyId"],
        aws_secret_access_key=stsresponse["Credentials"]["SecretAccessKey"],
        aws_session_token=stsresponse["Credentials"]["SessionToken"],
    )


def _get_sts_client(
    region_name,
    role_arn=None,
):
    client_factory = STSClientFactory(botocore.session.get_session())
    return client_factory.get_sts_client(region_name=region_name, role_arn=role_arn)


def _get_token(
    sts_client,
    cluster_name,
):
    return TokenGenerator(sts_client).get_token(cluster_name)


def _save_kube_config(config: Dict) -> str:
    kubeconfig_filepath = os.getenv("KUBECONFIG", "")
    if kubeconfig_filepath == "":
        kubeconfig_dir = f"{str(Path.home())}/.kube"
        os.makedirs(kubeconfig_dir, exist_ok=True)
        kubeconfig_filepath = f"{kubeconfig_dir}/config"

    with open(kubeconfig_filepath, "w") as f:
        yaml.dump(config, f, default_flow_style=False)

    return kubeconfig_filepath


def _get_kube_config(eks, cluster_name) -> Dict:
    cluster = eks.describe_cluster(name=cluster_name)
    cluster_cert = cluster["cluster"]["certificateAuthority"]["data"]
    cluster_ep = cluster["cluster"]["endpoint"]
    cluster_config = {
        "apiVersion": "v1",
        "kind": "Config",
        "clusters": [
            {
                "cluster": {
                    "server": str(cluster_ep),
                    "certificate-authority-data": str(cluster_cert),
                },
                "name": "kubernetes",
            }
        ],
        "contexts": [
            {"context": {"cluster": "kubernetes", "user": "aws"}, "name": "aws"}
        ],
        "current-context": "aws",
        "preferences": {},
        "users": [{"name": "aws", "user": {}}],
    }
    return cluster_config
