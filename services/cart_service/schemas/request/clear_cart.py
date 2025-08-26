from pydantic import BaseModel, Field
from uuid import UUID


class ClearCartRequestDto(BaseModel):
    """장바구니 비우기 요청"""
    user_id: UUID = Field(..., description="사용자 ID")