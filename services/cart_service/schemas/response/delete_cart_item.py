from pydantic import BaseModel, Field
from datetime import datetime


class DeleteCartItemResponseDto(BaseModel):
    """장바구니 아이템 삭제 응답"""
    deleted_at: datetime = Field(..., description="삭제일시")