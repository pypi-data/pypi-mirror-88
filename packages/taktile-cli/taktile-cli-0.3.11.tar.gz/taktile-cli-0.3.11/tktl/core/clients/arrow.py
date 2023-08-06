import math
from typing import Tuple

from pyarrow import Table
from pyarrow.flight import (
    ClientAuthHandler,
    FlightCancelledError,
    FlightClient,
    FlightDescriptor,
    FlightInfo,
    FlightUnauthenticatedError,
    FlightUnavailableError,
    Ticket,
)

from tktl.core.clients import Client
from tktl.core.config import settings
from tktl.core.exceptions import AuthenticationError
from tktl.core.exceptions.exceptions import APIClientException
from tktl.core.loggers import LOG, Logger
from tktl.core.schemas.repository import _format_grpc_url, load_certs
from tktl.core.serializers import deserialize_arrow, serialize_arrow
from tktl.core.t import ServiceT


class ApiKeyClientAuthHandler(ClientAuthHandler):
    """An example implementation of authentication via ApiKey."""

    def __init__(self, api_key: str):
        super(ApiKeyClientAuthHandler, self).__init__()
        self.api_key = api_key

    def authenticate(self, outgoing, incoming):
        outgoing.write(self.api_key)
        self.api_key = incoming.read()

    def get_token(self):
        return self.api_key


class ArrowFlightClient(Client):
    TRANSPORT = ServiceT.GRPC

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

    @staticmethod
    def format_url(url: str) -> str:
        return _format_grpc_url(url)

    @property
    def local_endpoint(self):
        return settings.LOCAL_ARROW_ENDPOINT

    def list_deployments(self):
        pass

    def list_commands(self):
        return self.client.list_actions()

    def authenticate(self, health_check: bool = False):
        if health_check:
            location = self.get_deployment_location()
        else:
            try:
                location = self.get_endpoint_and_location()
            except APIClientException as e:
                self.logger.error(f"Unable to authenticate: {e.detail}")
                return

        certs = load_certs()
        client = FlightClient(tls_root_certs=certs, location=location)
        self.logger.trace(f"Performing authentication request against {location}")
        client.authenticate(
            ApiKeyClientAuthHandler(api_key=self.taktile_client.api_key)
        )
        self.set_client_and_location(location=location, client=client)

    def predict(self, inputs):
        table = serialize_arrow(inputs)
        batch_size, batch_memory = get_chunk_size(table)
        descriptor = self.get_flight_info(command_name=str.encode(self.endpoint_name))
        writer, reader = self.client.do_exchange(descriptor.descriptor)
        self.logger.trace(
            f"Initiating prediction request with batches of {batch_size} records of "
            f"~{batch_memory:.2f} MB/batch"
        )
        batches = table.to_batches(max_chunksize=batch_size)
        chunks = []
        schema = None
        with writer:
            writer.begin(table.schema)
            for i, batch in enumerate(batches):
                self.logger.trace(f"Prediction for batch {i}/{len(batches)}")
                writer.write_batch(batch)
                chunk = reader.read_chunk()
                if not schema and chunk.data.schema is not None:
                    schema = chunk.data.schema
                chunks.append(chunk.data)
        return deserialize_arrow(Table.from_batches(chunks, schema))

    def get_sample_data(self):
        if not self.endpoint_name:
            raise AuthenticationError(
                "Please authenticate against a specific endpoint first"
            )
        x_ticket, y_ticket = (
            str.encode(f"{self.endpoint_name}__X"),
            str.encode(f"{self.endpoint_name}__y"),
        )
        return self._get_data(ticket=x_ticket), self._get_data(ticket=y_ticket)

    def _get_data(self, ticket):
        if not self.endpoint_name:
            raise AuthenticationError(
                "Please authenticate against a specific endpoint first"
            )
        self.logger.trace(f"Fetching sample data from server")
        reader = self.client.do_get(Ticket(ticket=ticket))
        return deserialize_arrow(reader.read_all())

    def get_schema(self):
        if not self.endpoint_name:
            raise AuthenticationError(
                "Please authenticate against a specific endpoint first"
            )
        info = self.get_flight_info(str.encode(self.endpoint_name))
        return info.schema

    def get_flight_info(self, command_name: bytes) -> FlightInfo:
        descriptor = FlightDescriptor.for_command(command_name)
        return self.client.get_flight_info(descriptor)

    def health(self):
        try:
            self.logger.trace(f"Connecting to server...")
            self.client.wait_for_available(timeout=1)
        except FlightUnauthenticatedError:
            self.logger.trace(f"Connection successful")
            return True
        except (FlightCancelledError, FlightUnavailableError):
            raise APIClientException(
                detail="Arrow flight is unavailable", status_code=502
            )
        return True


def get_chunk_size(sample_table: Table) -> Tuple[int, float]:
    mem_per_record = sample_table.nbytes / sample_table.num_rows
    batch_size = math.ceil(settings.ARROW_BATCH_MB * 1e6 / mem_per_record)
    batch_memory_mb = (batch_size * mem_per_record) / 1e6
    return batch_size, batch_memory_mb
