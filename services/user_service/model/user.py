from sqlalchemy import (
    Column, String, Uuid, DateTime, Boolean, func
)
from utility.db import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "user_service"}

    uuid = Column(Uuid, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True)
    name = Column(String)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
