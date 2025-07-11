from sqlalchemy import (
    Column, String, Uuid, DateTime, Boolean, CheckConstraint, func
)
from utility.db import Base
from utility.enums import SupportStatus


class SupportRequest(Base):
    __tablename__ = "support_request"
    __table_args__ = (
        CheckConstraint(
            "status IN (" + ",".join(f"'{s.value}'" for s in SupportStatus) + ")",
            name="check_support_status"
        ),
        {"schema": "support_service"},
    )

    uuid = Column(Uuid, primary_key=True)
    user_id = Column(Uuid, nullable=False)
    category = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    message = Column(String, nullable=False)
    status = Column(String, nullable=False, default=SupportStatus.OPEN.value)
    response = Column(String)
    responded_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
