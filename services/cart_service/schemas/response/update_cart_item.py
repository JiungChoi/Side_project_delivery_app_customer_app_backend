from pydantic import BaseModel, Field
from datetime import datetime


class UpdateCartItemResponseDto(BaseModel):
    """장바구니 아이템 수정 응답"""
    updated_at: datetime = Field(..., description="수정일시")