from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from schemas.common import ResultDto, create_success_result, create_error_result


class CreateOrderResponseDto(BaseModel):
    """주문 생성 응답 schema"""
    order_id: UUID = Field(..., description="주문 ID")
    status: str = Field(..., description="주문 상태 (pending, paid)")
    total_price: int = Field(..., ge=0, description="총 주문 금액")
    created_at: datetime = Field(..., description="주문 생성 시간")

    @classmethod
    def from_domain(cls, order):
        """도메인 모델에서 schema 생성"""
        return cls(
            order_id=order.uuid,
            status=order.status,
            total_price=order.total_price,
            created_at=order.created_at,
        )

    @classmethod
    def create_result(cls, order):
        """도메인 모델에서 Result 생성"""
        response_data = cls.from_domain(order)
        return create_success_result(response_data) 