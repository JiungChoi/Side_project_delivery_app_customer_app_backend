# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field


class CheckExistsResponseDto(BaseModel):
    """이메일/전화번호 중복 확인 응답"""
    email_exists: bool = Field(..., description="이메일 존재 여부")
    phone_exists: bool = Field(..., description="전화번호 존재 여부")