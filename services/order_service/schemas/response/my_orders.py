from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List
from schemas.common import ResultDto, create_success_result, create_error_result


class MyOrderSummaryDto(BaseModel):
    """내 주문 요약 응답 schema"""
    order_id: UUID = Field(..., description="주문 ID")
    restaurant_id: UUID = Field(..., description="매장 ID")
    status: str = Field(..., description="주문 상태")
    total_price: int = Field(..., ge=0, description="총 주문 금액")
    created_at: datetime = Field(..., description="주문 생성 시간")

    @classmethod
    def from_domain(cls, order):
        """도메인 모델에서 schema 생성"""
        return cls(
            order_id=order.uuid,
            restaurant_id=order.order_items[0].restaurant_id if order.order_items else None,
            status=order.status,
            total_price=order.total_price,
            created_at=order.created_at
        )


class MyOrdersResponseDto(BaseModel):
    """내 주문 목록 응답 schema"""
    orders: List[MyOrderSummaryDto] = Field(default=[], description="주문 목록")

    @classmethod
    def create_result(cls, orders):
        """도메인 모델에서 Result 생성"""
        response_data = cls(orders=[MyOrderSummaryDto.from_domain(order) for order in orders])
        return create_success_result(response_data) 