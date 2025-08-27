# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from uuid import UUID


class GetMyInfoRequestDto(BaseModel):
    """내 정보 조회 요청"""
    user_id: UUID = Field(..., description="사용자 ID")