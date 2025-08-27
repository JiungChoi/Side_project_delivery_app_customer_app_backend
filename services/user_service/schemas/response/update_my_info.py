# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from datetime import datetime


class UpdateMyInfoResponseDto(BaseModel):
    """내 정보 수정 응답"""
    updated_at: datetime = Field(..., description="수정일시")