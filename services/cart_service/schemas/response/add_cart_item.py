from pydantic import BaseModel, Field
from .get_cart import CartItemDto


class AddCartItemResponseDto(BaseModel):
    """Add cart item response"""
    cart_item: CartItemDto = Field(..., description="Created cart item")
