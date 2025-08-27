# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class UpdateMyInfoRequestDto(BaseModel):
    """내 정보 수정 요청"""
    user_id: UUID = Field(..., description="사용자 ID")
    name: Optional[str] = Field(None, description="이름")
    phone: Optional[str] = Field(None, description="전화번호")
    profile_image_url: Optional[str] = Field(None, description="프로필 이미지 URL")