from pydantic import BaseModel
from typing import Any, Optional

class GatewayResponse(BaseModel):
    """Standard gateway response format"""
    data: Any = None
    error: Optional[str] = None
    service: Optional[str] = None

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str