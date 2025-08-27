# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from uuid import UUID


class GetMyReviewsRequestDto(BaseModel):
    """내가 작성한 리뷰 목록 조회 요청"""
    user_id: UUID = Field(..., description="사용자 ID")
    page: int = Field(1, description="페이지 번호", ge=1)
    limit: int = Field(10, description="페이지당 항목 수", ge=1, le=100)