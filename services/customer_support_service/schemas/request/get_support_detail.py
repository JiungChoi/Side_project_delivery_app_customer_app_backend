# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from uuid import UUID


class GetSupportDetailRequestDto(BaseModel):
    """문의 상세 조회 요청 DTO"""
    support_id: UUID = Field(..., description="문의 ID")
    user_id: UUID = Field(..., description="사용자 ID")