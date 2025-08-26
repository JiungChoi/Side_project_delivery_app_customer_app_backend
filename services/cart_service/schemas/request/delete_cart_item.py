from pydantic import BaseModel, Field
from uuid import UUID


class DeleteCartItemRequestDto(BaseModel):
    """장바구니 아이템 삭제 요청"""
    user_id: UUID = Field(..., description="사용자 ID")