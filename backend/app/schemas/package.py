from uuid import UUID

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    slug: str

class CategoryRead(CategoryBase):
    id: UUID

    class Config:
        from_attributes = True

class TagBase(BaseModel):
    name: str

class TagRead(TagBase):
    id: UUID

    class Config:
        from_attributes = True

class PackageBase(BaseModel):
    name: str
    description: str | None = None

class PackageCreate(PackageBase):
    # organization_id can be optional if we default to the current user's namespace, but for now it's globally unique
    organization_id: UUID | None = None

class PackageUpdate(BaseModel):
    description: str | None = None
    is_verified: bool | None = None

class PackageRead(PackageBase):
    id: UUID
    is_verified: bool
    organization_id: UUID | None = None
    category: CategoryRead | None = None
    tags: list[TagRead] = []

    class Config:
        from_attributes = True
