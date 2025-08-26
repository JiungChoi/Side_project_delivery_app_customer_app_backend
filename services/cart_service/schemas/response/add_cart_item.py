from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class AddCartItemResponseDto(BaseModel):
    """장바구니 아이템 추가 응답"""
    cart_item_id: UUID = Field(..., description="생성된 장바구니 아이템 ID")
    created_at: datetime = Field(..., description="생성일시")