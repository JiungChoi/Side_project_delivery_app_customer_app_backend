# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class GetMySupportsRequestDto(BaseModel):
    """내 문의 목록 조회 요청 DTO"""
    user_id: UUID = Field(..., description="사용자 ID")
    status: Optional[str] = Field(None, description="문의 상태 필터", example="pending")
    page: int = Field(1, description="페이지 번호", ge=1)
    size: int = Field(10, description="페이지 크기", ge=1, le=100)