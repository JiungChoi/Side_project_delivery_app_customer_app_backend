from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

 
class MyOrdersRequestDto(BaseModel):
    """내 주문 목록 조회 요청 schema"""
    start_date: Optional[date] = Field(None, description="조회 시작 날짜")
    end_date: Optional[date] = Field(None, description="조회 종료 날짜")
    status: Optional[str] = Field(None, description="주문 상태 필터 (delivered, pending 등)") 