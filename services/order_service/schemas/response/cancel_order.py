from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from schemas.common import ResultDto, create_success_result, create_error_result


class CancelOrderResponseDto(BaseModel):
    """주문 취소 응답 schema"""
    order_id: UUID = Field(..., description="주문 ID")
    status: str = Field(..., description="주문 상태 (cancelled)")
    cancelled_at: datetime = Field(..., description="취소 시간")

    @classmethod
    def from_domain(cls, order):
        """도메인 모델에서 schema 생성"""
        return cls(
            order_id=order.uuid,
            status=order.status,
            cancelled_at=order.updated_at
        )

    @classmethod
    def create_result(cls, order):
        """도메인 모델에서 Result 생성"""
        response_data = cls.from_domain(order)
        return create_success_result(response_data) 