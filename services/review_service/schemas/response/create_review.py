# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class CreateReviewResponseDto(BaseModel):
    """리뷰 작성 응답"""
    review_id: UUID = Field(..., description="생성된 리뷰 ID")
    created_at: datetime = Field(..., description="생성일시")