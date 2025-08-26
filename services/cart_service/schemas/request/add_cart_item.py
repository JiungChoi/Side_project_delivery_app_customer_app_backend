from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID


class CartItemOptionDto(BaseModel):
    """장바구니 아이템 옵션"""
    menu_option_id: UUID = Field(..., description="메뉴 옵션 ID")
    price: int = Field(..., description="옵션 가격", ge=0)


class AddCartItemRequestDto(BaseModel):
    """장바구니 아이템 추가 요청"""
    user_id: UUID = Field(..., description="사용자 ID")
    restaurant_id: UUID = Field(..., description="매장 ID")
    menu_id: UUID = Field(..., description="메뉴 ID")
    quantity: int = Field(..., description="수량", ge=1)
    price: int = Field(..., description="메뉴 가격", ge=0)
    options: Optional[List[CartItemOptionDto]] = Field(None, description="선택 옵션 목록")