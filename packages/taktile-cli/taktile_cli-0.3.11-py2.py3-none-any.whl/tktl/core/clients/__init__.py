from typing import Union

from pyarrow._flight import FlightClient

from tktl.core.clients.http_client import API
from tktl.core.clients.taktile import TaktileClient
from tktl.core.clients.utils import get_deployment_from_endpoint_and_branch
from tktl.core.config import settings
from tktl.core.loggers import LOG, Logger, set_verbosity
from tktl.core.t import ServiceT
from tktl.login import login


class Client(object):
    TRANSPORT: str = ServiceT

    def __init__(
        self,
        api_key: str,
        repository_name: str,
        branch_name: str,
        endpoint_name: str,
        local: bool = False,
        logger: Logger = LOG,
        verbosity: int = 0,
    ):
        set_verbosity(verbosity)
        login(api_key)
        self.local = local
        self.taktile_client = TaktileClient(
            api_url=settings.DEPLOYMENT_API_URL, logger=logger
        )
        self.repository_name = repository_name
        self.branch_name = branch_name
        self.endpoint_name = endpoint_name
        self.logger = logger
        self._location = None
        self._endpoint = None
        self._client = None

    def local_endpoint(self):
        raise NotImplementedError

    @staticmethod
    def format_url(url: str) -> str:
        raise NotImplementedError

    @property
    def client(self) -> Union[API, FlightClient]:
        return self._client

    @property
    def location(self):
        return self._location

    @client.setter
    def client(self, client: Union[API, FlightClient]):
        self._client = client

    @location.setter
    def location(self, value):
        self._location = value

    def predict(self, *args, **kwargs):
        raise NotImplementedError

    def set_client_and_location(self, location: str, client: Union[API, FlightClient]):
        self.location = location
        self.client = client

    def get_deployment_location(self):
        deployment = self.taktile_client.get_deployment_by_branch_name(
            repository_name=self.repository_name, branch_name=self.branch_name,
        )
        return self.format_url(deployment.public_docs_url)

    def get_endpoint_and_location(self):
        if self.local:
            location = self.local_endpoint
        else:
            location = self._get_endpoint_location()
        return location

    def _get_endpoint_location(self):
        deployment, endpoint = self.taktile_client.get_endpoint_by_name(
            repository_name=self.repository_name,
            endpoint_name=self.endpoint_name,
            branch_name=self.branch_name,
        )
        return self.format_url(deployment.public_docs_url)

    def list_deployments(self):
        raise NotImplementedError

    def get_sample_data(self):
        raise NotImplementedError

    def get_schema(self, *args, **kwargs):
        raise NotImplementedError

    def health(self):
        raise NotImplementedError
