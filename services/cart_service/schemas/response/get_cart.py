from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class CartItemOptionDto(BaseModel):
    """장바구니 아이템 옵션 응답"""
    uuid: UUID = Field(..., description="옵션 ID")
    menu_option_id: UUID = Field(..., description="메뉴 옵션 ID")
    price: int = Field(..., description="옵션 가격")
    created_at: datetime = Field(..., description="생성일시")
    updated_at: datetime = Field(..., description="수정일시")


class CartItemDto(BaseModel):
    """장바구니 아이템 응답"""
    uuid: UUID = Field(..., description="장바구니 아이템 ID")
    menu_id: UUID = Field(..., description="메뉴 ID")
    quantity: int = Field(..., description="수량")
    price: int = Field(..., description="메뉴 가격")
    created_at: datetime = Field(..., description="생성일시")
    updated_at: datetime = Field(..., description="수정일시")
    options: Optional[List[CartItemOptionDto]] = Field(None, description="선택 옵션 목록")


class CartDto(BaseModel):
    """장바구니 응답"""
    uuid: UUID = Field(..., description="장바구니 ID")
    user_id: UUID = Field(..., description="사용자 ID")
    restaurant_id: UUID = Field(..., description="매장 ID")
    created_at: datetime = Field(..., description="생성일시")
    updated_at: datetime = Field(..., description="수정일시")
    items: Optional[List[CartItemDto]] = Field(None, description="장바구니 아이템 목록")


class GetCartResponseDto(BaseModel):
    """장바구니 조회 응답"""
    cart: Optional[CartDto] = Field(None, description="장바구니 정보")