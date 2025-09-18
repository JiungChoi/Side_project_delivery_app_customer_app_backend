from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class ClearCartResponseDto(BaseModel):
    """Clear cart response"""
    cart_id: UUID = Field(..., description="Cleared cart ID")
    cleared_at: datetime = Field(..., description="Cleared at")

