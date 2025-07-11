from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    PREPARING = "preparing"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    FAILED = "failed"


