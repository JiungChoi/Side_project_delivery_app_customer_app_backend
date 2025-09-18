from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class CartItemOptionDto(BaseModel):
    uuid: UUID = Field(..., description="Option ID")
    menu_option_id: Optional[UUID] = Field(None, description="Menu option ID")
    menu_option_name: Optional[str] = Field(None, description="Menu option name")
    price: int = Field(..., description="Option price")
    created_at: datetime = Field(..., description="Created at")
    updated_at: datetime = Field(..., description="Updated at")




class CartItemDto(BaseModel):
    uuid: UUID = Field(..., description="Cart item ID")
    menu_id: UUID = Field(..., description="Menu ID")
    menu_name: Optional[str] = Field(None, description="Menu name")
    menu_description: Optional[str] = Field(None, description="Menu description")
    menu_image_url: Optional[str] = Field(None, description="Menu image URL")
    quantity: int = Field(..., description="Quantity")
    price: int = Field(..., description="Menu price")
    created_at: datetime = Field(..., description="Created at")
    updated_at: datetime = Field(..., description="Updated at")
    options: Optional[List[CartItemOptionDto]] = Field(None, description="Selected options")


class CartDto(BaseModel):
    uuid: UUID = Field(..., description="Cart ID")
    user_id: UUID = Field(..., description="User ID")
    restaurant_id: UUID = Field(..., description="Restaurant ID")
    created_at: datetime = Field(..., description="Created at")
    updated_at: datetime = Field(..., description="Updated at")
    items: Optional[List[CartItemDto]] = Field(None, description="Cart items")


class GetCartResponseDto(BaseModel):
    cart: Optional[CartDto] = Field(None, description="Cart")

