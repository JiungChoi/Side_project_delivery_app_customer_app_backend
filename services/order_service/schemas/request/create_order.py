from pydantic import BaseModel, Field
from uuid import UUID
from typing import List


class OrderItemOptionInput(BaseModel):
    """주문 아이템 옵션 입력 schema"""
    menu_option_id: UUID = Field(..., description="메뉴 옵션 ID")


class OrderItemInput(BaseModel):
    """주문 아이템 입력 schema"""
    menu_id: UUID = Field(..., description="메뉴 ID")
    quantity: int = Field(..., gt=0, description="수량")
    options: List[OrderItemOptionInput] = Field(default=[], description="메뉴 옵션 목록")


class CreateOrderRequestDto(BaseModel):
    """주문 생성 요청 schema"""
    restaurant_id: UUID = Field(..., description="매장 ID")
    address_id: UUID = Field(..., description="배송 주소 ID")
    payment_method: str = Field(..., description="결제 방법 (card, cash, kakao, naver)")
    items: List[OrderItemInput] = Field(..., min_items=1, description="주문 아이템 목록")

    def to_model(self):
        """도메인 모델로 변환"""
        return {
            "restaurant_id": self.restaurant_id,
            "address_id": self.address_id,
            "payment_method": self.payment_method,
            "items": [item.dict() for item in self.items],
        } 