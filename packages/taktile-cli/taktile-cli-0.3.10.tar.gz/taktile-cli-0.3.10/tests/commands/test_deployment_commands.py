import pytest
from pydantic import UUID4

from tktl.commands.deployments import GetDeployments, GetEndpoints
from tktl.core.exceptions.exceptions import APIClientException
from tktl.login import logout


def test_get_deployment_commands(logged_in_context):
    cmd = GetDeployments()
    result = cmd.execute(UUID4("9b503d88-5f49-46d4-806a-aed3134ba973"), "", "", "")
    assert len(result) == 1

    result = cmd.execute("", "", "", "", return_all=True)
    assert len(result) >= 3

    cmd = GetEndpoints()
    result = cmd.execute(UUID4("7c0f6f48-0220-450a-b4d2-bfc731f94cc3"), "")
    assert len(result) == 1

    cmd = GetDeployments()
    with pytest.raises(APIClientException) as e:
        logout()
        cmd.execute(UUID4("7c0f6f48-0220-450a-b4d2-bfc731f94cc3"), "", "", "")
