from datetime import datetime
from typing import Dict, List, Optional, Union

import certifi
from pydantic import UUID4, BaseModel, validator

from tktl.core import ExtendedEnum
from tktl.core.utils import flatten


class AccessKind(str, ExtendedEnum):

    # see also corresponding AccessKind on t-api
    OWNER = "owner"
    VIEWER = "viewer"


class TablePrintableBaseModelMixin:
    def table_repr(self, subset: List[str] = None) -> Dict:
        ...


class Endpoint(BaseModel):
    name: str
    kind: str
    deployment_id: Optional[UUID4]
    profiling_supported: bool

    class Config:
        validate_assignment = True

    @validator("deployment_id")
    def set_deployment_id(cls, deployment_id: UUID4):
        return deployment_id

    def table_repr(self, subset=None):
        as_dict = self.dict()
        as_dict["NAME"] = as_dict.pop("name")
        as_dict["KIND"] = str(as_dict.pop("kind"))
        as_dict["PROFILING SUPPORTED"] = str(as_dict.pop("profiling_supported"))
        as_dict["DEPLOYMENT ID"] = str(as_dict.pop("deployment_id"))
        return as_dict


class RepositoryDeployment(BaseModel, TablePrintableBaseModelMixin):
    id: UUID4
    created_at: datetime
    status: str
    public_docs_url: Optional[str]
    service_type: Optional[str]
    instance_type: Optional[str]
    replicas: Optional[int]
    git_ref: str
    commit_hash: str
    n_endpoints: Optional[int]

    @validator("n_endpoints", always=True)
    def validate_n_endpoints(cls, value):
        return value or 0

    def table_repr(self, subset=None):
        as_dict = self.dict(exclude={"service_type", "endpoints"})
        as_dict["ID"] = str(as_dict.pop("id"))
        as_dict[
            "BRANCH @ COMMIT"
        ] = f"{as_dict.pop('git_ref')} @ {as_dict.pop('commit_hash')[0:7]}"
        as_dict["STATUS"] = as_dict.pop("status")
        as_dict["CREATED AT"] = str(as_dict.pop("created_at"))
        as_dict["INSTANCE TYPE"] = as_dict.pop("instance_type")
        as_dict["REPLICAS"] = as_dict.pop("replicas")
        as_dict["REST DOCS URL"] = _format_http_url(as_dict.pop("public_docs_url"))
        as_dict["ENDPOINTS"] = as_dict.pop("n_endpoints")
        if subset:
            return {k: v for k, v in as_dict.items() if k in subset}
        return as_dict


class Repository(BaseModel, TablePrintableBaseModelMixin):
    id: UUID4
    ref_id: int
    repository_name: str
    repository_owner: str
    repository_description: Optional[str] = None
    access: AccessKind
    deployments: List[RepositoryDeployment]
    n_deployments: Optional[int] = None

    @validator("n_deployments", always=True)
    def validate_n_deployments(cls, _, values):
        return len(values["deployments"])

    def __hash__(self):
        return self.id.__hash__()

    def table_repr(self, subset=None):
        as_dict = self.dict(exclude={"ref_id", "deployments"})
        as_dict["ID"] = f"{as_dict.pop('id')}"
        as_dict[
            "NAME"
        ] = f"{as_dict.pop('repository_owner')}/{as_dict.pop('repository_name')}"
        as_dict["DEPLOYMENTS"] = as_dict.pop("n_deployments")
        as_dict["ACCESS"] = f"{as_dict.pop('access').value}"
        desc = as_dict.pop("repository_description")
        as_dict["DESCRIPTION"] = f"{desc[0:20] + '...' if desc else '-'}"
        if subset:
            return {k: v for k, v in as_dict.items() if k in subset}
        return as_dict


class RepositoryList(BaseModel):
    __root__: List[Repository]

    def get_repositories(self) -> List[Repository]:
        return flatten(
            [
                sum([len(r.deployments) if r.deployments else 1]) * [r]
                for r in self.__root__
            ]
        )

    def get_deployments(self) -> List[RepositoryDeployment]:
        return flatten([d for d in r.deployments] for r in self.__root__)


class ReportResponse(BaseModel):
    deployment_id: UUID4
    endpoint_name: str
    report_type: str
    chart_name: Optional[str] = None
    variable_name: Optional[str] = None
    value: Union[List, Dict]


def _format_http_url(url, docs: bool = True):
    if url and url != "UNAVAILABLE":
        return f"https://{url}/{'docs' if docs else ''}"
    return "UNAVAILABLE"


def _format_grpc_url(url):
    return f"grpc+tls://{url}:5005" if (url and url != "UNAVAILABLE") else "UNAVAILABLE"


def load_certs():
    with open(certifi.where(), "r") as cert:
        return cert.read()
