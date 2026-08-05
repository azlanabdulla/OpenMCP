import uuid

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Review(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    package_id = Column(UUID(as_uuid=True), ForeignKey("package.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String)

    user = relationship("User", back_populates="reviews")
    package = relationship("Package", back_populates="reviews")

class Download(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    package_id = Column(UUID(as_uuid=True), ForeignKey("package.id"), nullable=False)
    version_id = Column(UUID(as_uuid=True), ForeignKey("version.id"), nullable=False)
    ip_address = Column(String)

    package = relationship("Package", back_populates="downloads")
    version = relationship("Version", back_populates="downloads")
