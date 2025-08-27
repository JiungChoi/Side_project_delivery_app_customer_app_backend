# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from uuid import UUID


class DeleteMyAccountRequestDto(BaseModel):
    """회원 탈퇴 요청"""
    user_id: UUID = Field(..., description="사용자 ID")