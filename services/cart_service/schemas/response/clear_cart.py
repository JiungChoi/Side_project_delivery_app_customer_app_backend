from pydantic import BaseModel, Field
from datetime import datetime


class ClearCartResponseDto(BaseModel):
    """장바구니 비우기 응답"""
    cleared_at: datetime = Field(..., description="비우기 완료일시")