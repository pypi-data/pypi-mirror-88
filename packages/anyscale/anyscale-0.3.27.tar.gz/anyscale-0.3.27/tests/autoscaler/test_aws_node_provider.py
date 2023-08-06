from typing import Any, Mapping
from unittest.mock import Mock, patch

import pytest

from anyscale.autoscaler.aws.node_provider import AnyscaleAWSNodeProvider


@pytest.mark.parametrize(
    "cluster_config",
    [
        pytest.param({"provider": {"aws_credentials": {}}}, id="has aws_credentials"),
        pytest.param(
            {"provider": {"inner_provider": {"aws_credentials": {}}}},
            id="has inner_provider",
        ),
    ],
)
def test_ensure_no_credentials_on_head_node_config(
    cluster_config: Mapping[str, Any]
) -> None:
    with patch.multiple(
        "ray.autoscaler._private.aws.node_provider",
        make_ec2_client=Mock(return_value=None),
    ):
        node_provider = AnyscaleAWSNodeProvider(
            {"region": "us-west-2"}, "fake-cluster-name"
        )

    cleaned_config = node_provider.prepare_for_head_node(cluster_config)

    provider_config = cleaned_config.get("provider", {})

    assert "aws_credentials" not in provider_config
    assert "aws_credentials" not in provider_config.get("inner_provider", {})
