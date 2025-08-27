# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class CreateSupportResponseDto(BaseModel):
    """1:1 문의 등록 응답 DTO"""
    support_id: UUID = Field(..., description="생성된 문의 ID")
    title: str = Field(..., description="문의 제목")
    support_type: str = Field(..., description="문의 유형")
    status: str = Field(..., description="문의 상태")
    created_at: datetime = Field(..., description="생성 시간")