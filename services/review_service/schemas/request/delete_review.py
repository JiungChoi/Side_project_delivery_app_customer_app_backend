# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from uuid import UUID


class DeleteReviewRequestDto(BaseModel):
    """리뷰 삭제 요청"""
    user_id: UUID = Field(..., description="사용자 ID")