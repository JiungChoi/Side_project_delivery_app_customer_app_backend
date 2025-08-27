# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List, Optional


class SupportSummaryDto(BaseModel):
    """문의 요약 정보"""
    support_id: UUID = Field(..., description="문의 ID")
    title: str = Field(..., description="문의 제목")
    support_type: str = Field(..., description="문의 유형")
    status: str = Field(..., description="문의 상태")
    priority: str = Field(..., description="우선순위")
    has_response: bool = Field(..., description="답변 여부")
    created_at: datetime = Field(..., description="생성 시간")
    responded_at: Optional[datetime] = Field(None, description="답변 시간")


class GetMySupportsResponseDto(BaseModel):
    """내 문의 목록 조회 응답 DTO"""
    supports: List[SupportSummaryDto] = Field(..., description="문의 목록")
    total_count: int = Field(..., description="전체 문의 수")
    page: int = Field(..., description="현재 페이지")
    size: int = Field(..., description="페이지 크기")
    total_pages: int = Field(..., description="전체 페이지 수")