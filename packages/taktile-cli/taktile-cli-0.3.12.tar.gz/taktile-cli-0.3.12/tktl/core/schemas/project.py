from typing import List, Optional, Union

from pydantic import BaseModel

from tktl.core.t import InstanceTypeT, ProjectAssetSourceT, ProjectAssetT, ServiceT


class ProjectContentsBase(BaseModel):
    type: str
    name: str
    path: str


class ProjectFile(ProjectContentsBase):
    type: str = "file"


class ProjectFileWithContent(ProjectContentsBase):
    type: str = "file"
    content: str


class ProjectDirectory(ProjectContentsBase):
    type: str = "dir"


class ProjectAsset(ProjectContentsBase):
    calculated_sha: str
    kind: ProjectAssetT
    source: ProjectAssetSourceT
    requires_download: bool


class TktlServiceConfigSchema(BaseModel):
    replicas: int
    instance_type: InstanceTypeT
    service_type: ServiceT


class TktlYamlConfigSchema(BaseModel):

    """
    deployment_prefix?: master
    service:

      replicas: 2
      instance_type: gp.small
      service_type: rest


    version: version
    """

    deployment_prefix: Optional[str]
    service: TktlServiceConfigSchema
    version: str


class TktlYamlConfigValidationError(BaseModel):
    loc: str
    msg: str


class ProjectValidationOutput(BaseModel):
    title: str
    summary: str
    text: str


ProjectContentSingleItemT = Union[ProjectFile, ProjectDirectory]
ProjectContentMultiItemT = List[ProjectContentSingleItemT]
ProjectContentT = Union[
    ProjectContentSingleItemT, ProjectContentMultiItemT, ProjectFileWithContent
]
