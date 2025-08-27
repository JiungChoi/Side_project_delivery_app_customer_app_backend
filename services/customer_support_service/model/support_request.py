# -*- coding: utf-8 -*-
from sqlalchemy import (
    Column, String, Uuid, DateTime, Boolean, Text, CheckConstraint, func
)
from utility.db import Base
from utility.enums import SupportStatus, SupportType, SupportPriority


class SupportRequest(Base):
    __tablename__ = "support_request"
    __table_args__ = (
        CheckConstraint(
            "status IN (" + ",".join(f"'{s.value}'" for s in SupportStatus) + ")",
            name="check_support_status"
        ),
        CheckConstraint(
            "support_type IN (" + ",".join(f"'{s.value}'" for s in SupportType) + ")",
            name="check_support_type"
        ),
        CheckConstraint(
            "priority IN (" + ",".join(f"'{s.value}'" for s in SupportPriority) + ")",
            name="check_support_priority"
        ),
        {"schema": "customer_support_service"},
    )

    uuid = Column(Uuid, primary_key=True)
    user_id = Column(Uuid, nullable=False)
    support_type = Column(String, nullable=False)  # 문의 유형
    priority = Column(String, nullable=False, default=SupportPriority.MEDIUM.value)  # 우선순위
    title = Column(String, nullable=False)  # 문의 제목
    content = Column(Text, nullable=False)  # 문의 내용
    status = Column(String, nullable=False, default=SupportStatus.PENDING.value)
    
    # 관리자 답변 관련 필드
    admin_response = Column(Text)  # 관리자 답변
    admin_id = Column(Uuid)  # 답변한 관리자 ID
    responded_at = Column(DateTime(timezone=True))  # 답변 시간

    # 메타데이터
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
