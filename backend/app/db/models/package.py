import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Table
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base_class import Base

package_tag_association = Table(
    'package_tag',
    Base.metadata,
    Column('package_id', UUID(as_uuid=True), ForeignKey('package.id')),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tag.id'))
)

class Package(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=True)
    description = Column(String)
    is_verified = Column(Boolean(), default=False)
    
    category_id = Column(UUID(as_uuid=True), ForeignKey("category.id"), nullable=True)

    organization = relationship("Organization", back_populates="packages")
    versions = relationship("Version", back_populates="package")
    reviews = relationship("Review", back_populates="package")
    downloads = relationship("Download", back_populates="package")
    category = relationship("Category", back_populates="packages")
    tags = relationship("Tag", secondary=package_tag_association, back_populates="packages")

class Version(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    package_id = Column(UUID(as_uuid=True), ForeignKey("package.id"), nullable=False)
    version_string = Column(String, nullable=False, index=True)
    manifest_data = Column(JSONB)
    tarball_url = Column(String)
    checksum = Column(String)

    package = relationship("Package", back_populates="versions")
    downloads = relationship("Download", back_populates="version")

class Category(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)

    packages = relationship("Package", back_populates="category")

class Tag(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)

    packages = relationship("Package", secondary=package_tag_association, back_populates="tags")
