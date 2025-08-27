# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class GetMyInfoResponseDto(BaseModel):
    """내 정보 조회 응답"""
    user_id: UUID = Field(..., description="사용자 ID")
    email: str = Field(..., description="이메일")
    phone: str = Field(..., description="전화번호")
    name: str = Field(..., description="이름")
    profile_image_url: Optional[str] = Field(None, description="프로필 이미지 URL")
    status: str = Field(..., description="사용자 상태")
    created_at: datetime = Field(..., description="계정 생성일시")
    updated_at: datetime = Field(..., description="정보 수정일시")