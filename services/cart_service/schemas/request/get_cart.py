from pydantic import BaseModel, Field
from uuid import UUID


class GetCartRequestDto(BaseModel):
    """장바구니 조회 요청"""
    user_id: UUID = Field(..., description="사용자 ID")