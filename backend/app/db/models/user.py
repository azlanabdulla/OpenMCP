import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    # Relationships
    organizations = relationship("OrganizationMember", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    sessions = relationship("Session", back_populates="user")
    api_keys = relationship("APIKey", back_populates="user")

class Session(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    is_valid = Column(Boolean(), default=True)
    
    user = relationship("User", back_populates="sessions")

class APIKey(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    key_hash = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    is_active = Column(Boolean(), default=True)

    user = relationship("User", back_populates="api_keys")
