# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class GetSupportDetailResponseDto(BaseModel):
    """문의 상세 조회 응답 DTO"""
    support_id: UUID = Field(..., description="문의 ID")
    user_id: UUID = Field(..., description="사용자 ID")
    title: str = Field(..., description="문의 제목")
    content: str = Field(..., description="문의 내용")
    support_type: str = Field(..., description="문의 유형")
    priority: str = Field(..., description="우선순위")
    status: str = Field(..., description="문의 상태")
    
    # 관리자 답변 정보
    admin_response: Optional[str] = Field(None, description="관리자 답변")
    admin_id: Optional[UUID] = Field(None, description="답변한 관리자 ID")
    responded_at: Optional[datetime] = Field(None, description="답변 시간")
    
    # 메타데이터
    created_at: datetime = Field(..., description="생성 시간")
    updated_at: datetime = Field(..., description="수정 시간")