import pytest
from pydantic import UUID4

from tktl.commands.deployments import GetDeployments, GetEndpoints
from tktl.core.exceptions.exceptions import APIClientException
from tktl.login import logout


def test_get_deployment_commands(logged_in_context):
    cmd = GetDeployments()
    result = cmd.execute(
        UUID4("33fb5b8f-e6a2-4dd2-86ef-d257d2c59b85"), None, None, None, None, None
    )  # noqa
    print(result)
    assert len(result) == 1

    result = cmd.execute(None, None, None, None, None, None, return_all=True)  # noqa
    assert len(result) >= 3

    cmd = GetEndpoints()
    result = cmd.execute(
        UUID4("7bc7ec16-b8fa-4513-bf2f-20334d9ebcd1"),
        None,
        None,
        None,
        None,
        None,
        None,
        None,  # noqa
    )
    assert len(result) == 2

    cmd = GetDeployments()
    with pytest.raises(APIClientException) as e:
        logout()
        cmd.execute(
            UUID4("7c0f6f48-0220-450a-b4d2-bfc731f94cc3"), None, None, None, None, None
        )  # noqa
