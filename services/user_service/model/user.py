# -*- coding: utf-8 -*-
from sqlalchemy import (
    Column, String, Integer, Uuid, DateTime, Boolean, CheckConstraint, func
)
from utility.db import Base
from utility.enums import UserStatus


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        CheckConstraint(
            "status IN (" + ",".join(f"'{s.value}'" for s in UserStatus) + ")",
            name="check_user_status"
        ),
        {"schema": "user_service"},
    )

    uuid = Column(Uuid, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    profile_image_url = Column(String)
    status = Column(String, nullable=False, default=UserStatus.ACTIVE.value)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
