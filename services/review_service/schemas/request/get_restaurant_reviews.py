# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field


class GetRestaurantReviewsRequestDto(BaseModel):
    """특정 매장의 리뷰 목록 조회 요청"""
    page: int = Field(1, description="페이지 번호", ge=1)
    limit: int = Field(10, description="페이지당 항목 수", ge=1, le=100)
    rating_filter: Optional[int] = Field(None, description="평점 필터 (1-5)", ge=1, le=5)