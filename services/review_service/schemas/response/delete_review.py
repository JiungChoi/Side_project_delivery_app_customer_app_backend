# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from datetime import datetime


class DeleteReviewResponseDto(BaseModel):
    """리뷰 삭제 응답"""
    deleted_at: datetime = Field(..., description="삭제일시")