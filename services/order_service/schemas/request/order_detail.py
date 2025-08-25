from pydantic import BaseModel, Field
from uuid import UUID

 
class OrderDetailRequestDto(BaseModel):
    """주문 상세 조회 요청 schema"""
    order_id: UUID = Field(..., description="주문 ID") 