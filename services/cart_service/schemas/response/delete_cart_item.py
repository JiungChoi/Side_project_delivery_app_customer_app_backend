from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class DeleteCartItemResponseDto(BaseModel):
    """Delete cart item response"""
    item_id: UUID = Field(..., description="Deleted cart item ID")
    deleted_at: datetime = Field(..., description="Deleted at")

