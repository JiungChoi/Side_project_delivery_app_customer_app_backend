# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class CreateSupportRequestDto(BaseModel):
    """1:1 문의 등록 요청 DTO"""
    support_type: str = Field(..., description="문의 유형", example="order_inquiry")
    title: str = Field(..., description="문의 제목", example="주문 취소 문의")
    content: str = Field(..., description="문의 내용", example="주문한 음식을 취소하고 싶습니다.")
    priority: Optional[str] = Field("medium", description="우선순위", example="medium")
    user_id: UUID = Field(..., description="사용자 ID")