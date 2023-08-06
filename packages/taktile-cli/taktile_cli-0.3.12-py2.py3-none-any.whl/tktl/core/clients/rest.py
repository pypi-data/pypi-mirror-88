import json
import os

from openapi_schema_pydantic import OpenAPI

from tktl.core.clients import Client
from tktl.core.clients.http_client import API, interpret_response
from tktl.core.config import settings
from tktl.core.loggers import LOG, Logger
from tktl.core.schemas.repository import _format_http_url
from tktl.core.t import ServiceT


class RestClient(Client):
    def get_schema(self, *args, **kwargs):
        pass

    TRANSPORT = ServiceT.REST

    def __init__(
        self,
        api_key: str,
        repository_name: str,
        branch_name: str,
        endpoint_name: str,
        local: bool = False,
        logger: Logger = LOG,
        verbosity: int = 0,
        health_check: bool = False,
    ):
        super().__init__(
            api_key=api_key,
            repository_name=repository_name,
            branch_name=branch_name,
            endpoint_name=endpoint_name,
            local=local,
            logger=logger,
            verbosity=verbosity,
        )
        if not health_check:
            self.authenticate()

    def predict(self, inputs):
        response = self.client.post(
            url=f"model/{self.endpoint_name}", data=json.dumps(inputs)
        )
        return response.json()

    @staticmethod
    def format_url(url: str):
        return _format_http_url(url, docs=False)

    def authenticate(self, health_check: bool = False):
        if health_check:
            location = self.get_deployment_location()
        else:
            location = self.get_endpoint_and_location()
        client = API(api_url=location)
        self.set_client_and_location(location=location, client=client)

    @property
    def local_endpoint(self):
        return settings.LOCAL_REST_ENDPOINT

    def list_deployments(self):
        pass

    def get_sample_data(self):
        schema = self.client.get(url="openapi.json")
        openapi = OpenAPI.parse_obj(schema.json())
        request_reference, response_reference = get_endpoint_model_reference(
            openapi, endpoint=self.endpoint_name
        )
        sample_input = openapi.components.schemas[request_reference].example
        if not sample_input:
            self.logger.warning("No sample input found for endpoint")
        sample_output = openapi.components.schemas[response_reference].example
        if not sample_output:
            self.logger.warning("No sample output found for endpoint")
        return sample_input, sample_output

    def health(self):
        response = self.client.get(url=f"openapi.json")
        return interpret_response(response, model=None, ping=True)


def get_endpoint_model_reference(openapi: OpenAPI, endpoint: str):
    for k in openapi.paths.keys():
        if f"/model/{endpoint}" == k:
            request_ref = (
                openapi.paths[k]
                .post.requestBody.content["application/json"]
                .media_type_schema.ref
            )
            response_ref = (
                openapi.paths[k]
                .post.responses["200"]
                .content["application/json"]
                .media_type_schema.ref
            )
            return os.path.basename(request_ref), os.path.basename(response_ref)
    return None
