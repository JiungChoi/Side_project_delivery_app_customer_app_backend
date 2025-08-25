from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from schemas.common import ResultDto, create_success_result, create_error_result


class UpdateOrderStatusResponseDto(BaseModel):
    """주문 상태 수동 업데이트 응답 schema"""
    order_id: UUID = Field(..., description="주문 ID")
    prev_status: str = Field(..., description="이전 주문 상태")
    new_status: str = Field(..., description="새로운 주문 상태")
    updated_at: datetime = Field(..., description="업데이트 시간")

    @classmethod
    def from_domain(cls, order, prev_status: str):
        """도메인 모델에서 schema 생성"""
        return cls(
            order_id=order.uuid,
            prev_status=prev_status,
            new_status=order.status,
            updated_at=order.updated_at
        )

    @classmethod
    def create_result(cls, order, prev_status: str):
        """도메인 모델에서 Result 생성"""
        response_data = cls.from_domain(order, prev_status)
        return create_success_result(response_data) 