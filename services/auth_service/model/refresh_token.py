from sqlalchemy import (
    Column, String, Uuid, DateTime, Boolean, func
)
from utility.db import Base


class RefreshToken(Base):
    __tablename__ = "refresh_token"
    __table_args__ = {"schema": "auth_service"}

    uuid = Column(Uuid, primary_key=True)
    user_id = Column(Uuid, nullable=False)
    token = Column(String, unique=True, nullable=False)
    user_agent = Column(String)
    ip_address = Column(String)
    expired_at = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
