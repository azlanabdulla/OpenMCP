import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Organization(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)

    members = relationship("OrganizationMember", back_populates="organization")
    packages = relationship("Package", back_populates="organization")

class OrganizationMember(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False)
    role = Column(String, nullable=False, default="member") # admin, member

    user = relationship("User", back_populates="organizations")
    organization = relationship("Organization", back_populates="members")
