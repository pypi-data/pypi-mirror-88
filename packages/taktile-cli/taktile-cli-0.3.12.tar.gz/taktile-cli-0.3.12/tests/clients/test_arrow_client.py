import os

import pytest

from tktl.core.clients.arrow import ArrowFlightClient
from tktl.core.exceptions import TaktileSdkError
from tktl.core.managers.auth import AuthConfigManager


def test_instantiate_client():

    key = os.environ["TEST_USER_API_KEY"]
    AuthConfigManager.set_api_key(key)

    with pytest.raises(TaktileSdkError):
        ArrowFlightClient(
            api_key=key,
            repository_name=f"{os.environ['TEST_USER']}/test-new",
            branch_name="master",
            endpoint_name="repayment",
        )
    client = ArrowFlightClient(
        api_key=key,
        repository_name=f"{os.environ['TEST_USER']}/integ-testing",
        branch_name="master",
        endpoint_name="repayment",
    )
    assert client.location is not None
