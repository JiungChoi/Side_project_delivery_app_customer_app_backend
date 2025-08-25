from pydantic import BaseModel, Field
from uuid import UUID


class CompleteOrderRequestDto(BaseModel):
    """주문 완료 처리 요청 schema"""
    order_id: UUID = Field(..., description="주문 ID (Path parameter)")

    def to_domain(self):
        """도메인 모델로 변환"""
        return {"order_id": self.order_id} 