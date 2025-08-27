# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from datetime import datetime


class DeleteMyAccountResponseDto(BaseModel):
    """회원 탈퇴 응답"""
    deleted_at: datetime = Field(..., description="탈퇴일시")