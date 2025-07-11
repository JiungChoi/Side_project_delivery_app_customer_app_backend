from sqlalchemy import (
    Column, String, Uuid, DateTime, Boolean, CheckConstraint, func
)
from sqlalchemy.orm import relationship
from utility.db import Base
from utility.enums import NotificationType


class Notification(Base):
    __tablename__ = "notification"
    __table_args__ = (
        CheckConstraint(
            "type IN (" + ",".join(f"'{t.value}'" for t in NotificationType) + ")",
            name="check_notification_type"
        ),
        {"schema": "notification_service"},
    )

    uuid = Column(Uuid, primary_key=True)
    user_id = Column(Uuid, nullable=False)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    type = Column(String, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    read_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
