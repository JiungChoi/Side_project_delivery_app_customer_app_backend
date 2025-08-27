# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from datetime import datetime


class UpdateReviewResponseDto(BaseModel):
    """리뷰 수정 응답"""
    updated_at: datetime = Field(..., description="수정일시")