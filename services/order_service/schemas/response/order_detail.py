from pydantic import BaseModel, Field
from uuid import UUID
from typing import List
from datetime import datetime
from schemas.common import ResultDto, create_success_result, create_error_result


class OrderItemOptionResponseDto(BaseModel):
    """주문 아이템 옵션 응답 schema"""
    menu_option_id: UUID = Field(..., description="메뉴 옵션 ID")
    price: int = Field(..., ge=0, description="옵션 가격")

    @classmethod
    def from_domain(cls, option):
        """도메인 모델에서 schema 생성"""
        return cls(
            menu_option_id=option.menu_option_id,
            price=option.price
        )


class OrderItemResponseDto(BaseModel):
    """주문 아이템 응답 schema"""
    menu_id: UUID = Field(..., description="메뉴 ID")
    restaurant_id: UUID = Field(..., description="매장 ID")
    quantity: int = Field(..., gt=0, description="수량")
    price: int = Field(..., ge=0, description="아이템 가격")
    options: List[OrderItemOptionResponseDto] = Field(default=[], description="옵션 목록")

    @classmethod
    def from_domain(cls, item):
        """도메인 모델에서 schema 생성"""
        return cls(
            menu_id=item.menu_id,
            restaurant_id=item.restaurant_id,
            quantity=item.quantity,
            price=item.price,
            options=[
                OrderItemOptionResponseDto.from_domain(opt)
                for opt in item.order_item_options
            ]
        )


class OrderDetailResponseDto(BaseModel):
    """주문 상세 응답 schema"""
    order_id: UUID = Field(..., description="주문 ID")
    user_id: UUID = Field(..., description="사용자 ID")
    address_id: UUID = Field(..., description="배송 주소 ID")
    total_price: int = Field(..., ge=0, description="총 주문 금액")
    status: str = Field(..., description="주문 상태")
    created_at: datetime = Field(..., description="주문 생성 시간")
    updated_at: datetime = Field(..., description="주문 수정 시간")
    items: List[OrderItemResponseDto] = Field(default=[], description="주문 아이템 목록")

    @classmethod
    def from_domain(cls, order):
        """도메인 모델에서 schema 생성"""
        return cls(
            order_id=order.uuid,
            user_id=order.user_id,
            address_id=order.address_id,
            total_price=order.total_price,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=[
                OrderItemResponseDto.from_domain(item)
                for item in order.order_items
            ]
        )

    @classmethod
    def create_result(cls, order):
        """도메인 모델에서 Result 생성"""
        response_data = cls.from_domain(order)
        return create_success_result(response_data) 