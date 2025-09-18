from pydantic import BaseModel, Field
from .get_cart import CartItemDto


class UpdateCartItemResponseDto(BaseModel):
    """Update cart item response"""
    cart_item: CartItemDto = Field(..., description="Updated cart item")

