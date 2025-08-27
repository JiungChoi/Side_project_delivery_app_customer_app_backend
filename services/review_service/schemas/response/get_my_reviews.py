# -*- coding: utf-8 -*-
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class MyReviewDto(BaseModel):
    """내 리뷰 정보"""
    uuid: UUID = Field(..., description="리뷰 ID")
    order_id: UUID = Field(..., description="주문 ID")
    restaurant_id: UUID = Field(..., description="매장 ID")
    rating: int = Field(..., description="평점")
    content: Optional[str] = Field(None, description="리뷰 내용")
    image_url: Optional[str] = Field(None, description="리뷰 이미지 URL")
    status: str = Field(..., description="리뷰 상태")
    created_at: datetime = Field(..., description="생성일시")
    updated_at: datetime = Field(..., description="수정일시")


class GetMyReviewsResponseDto(BaseModel):
    """내가 작성한 리뷰 목록 조회 응답"""
    reviews: List[MyReviewDto] = Field(..., description="내 리뷰 목록")
    total_count: int = Field(..., description="전체 리뷰 수")
    page: int = Field(..., description="현재 페이지")
    limit: int = Field(..., description="페이지당 항목 수")
    total_pages: int = Field(..., description="전체 페이지 수")