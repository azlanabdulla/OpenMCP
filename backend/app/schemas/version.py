from typing import Any
from uuid import UUID

from pydantic import BaseModel


class ManifestData(BaseModel):
    name: str
    description: str
    version: str
    author: str
    license: str
    repository: str | None = None
    homepage: str | None = None
    keywords: list[str] = []
    entry: str
    dependencies: list[str] = []

class VersionBase(BaseModel):
    version_string: str

class VersionCreate(VersionBase):
    manifest_data: ManifestData
    # the actual tarball is usually handled via file upload to S3, but we pass the URL in the schema
    tarball_url: str
    checksum: str

class VersionRead(VersionBase):
    id: UUID
    package_id: UUID
    manifest_data: Any # or dict
    tarball_url: str | None = None
    checksum: str | None = None

    class Config:
        from_attributes = True
