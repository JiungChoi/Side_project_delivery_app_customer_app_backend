# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional


class CheckExistsRequestDto(BaseModel):
    """이메일/전화번호 중복 확인 요청"""
    email: Optional[str] = Field(None, description="이메일")
    phone: Optional[str] = Field(None, description="전화번호")