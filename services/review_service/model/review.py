# -*- coding: utf-8 -*-
from sqlalchemy import (
    Column, String, Integer, Uuid, DateTime, Boolean, CheckConstraint, func
)
from utility.db import Base
from utility.enums import ReviewStatus


class Review(Base):
    __tablename__ = "review"
    __table_args__ = (
        CheckConstraint(
            "status IN (" + ",".join(f"'{s.value}'" for s in ReviewStatus) + ")",
            name="check_review_status"
        ),
        {"schema": "review_service"},
    )

    uuid = Column(Uuid, primary_key=True)
    user_id = Column(Uuid, nullable=False)
    order_id = Column(Uuid, nullable=False)
    restaurant_id = Column(Uuid, nullable=False)
    rating = Column(Integer, nullable=False)
    content = Column(String)
    image_url = Column(String)
    status = Column(String, nullable=False, default=ReviewStatus.ACTIVE.value)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
