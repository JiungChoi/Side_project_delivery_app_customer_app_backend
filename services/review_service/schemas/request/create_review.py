# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class CreateReviewRequestDto(BaseModel):
    """리뷰 작성 요청"""
    user_id: UUID = Field(..., description="사용자 ID")
    order_id: UUID = Field(..., description="주문 ID")
    restaurant_id: UUID = Field(..., description="매장 ID")
    rating: int = Field(..., description="평점 (1-5)", ge=1, le=5)
    content: Optional[str] = Field(None, description="리뷰 내용")
    image_url: Optional[str] = Field(None, description="리뷰 이미지 URL")