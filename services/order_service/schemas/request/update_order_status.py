from pydantic import BaseModel, Field
from uuid import UUID


class UpdateOrderStatusRequestDto(BaseModel):
    """주문 상태 수동 업데이트 요청 schema"""
    order_id: UUID = Field(..., description="주문 ID")
    new_status: str = Field(..., description="새로운 주문 상태 (preparing, delivering 등)")

    def to_domain(self):
        """도메인 모델로 변환"""
        return {
            "order_id": self.order_id,
            "new_status": self.new_status
        } 