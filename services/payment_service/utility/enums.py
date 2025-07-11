from enum import Enum

class PaymentMethod(Enum):
    CARD = "card"
    CASH = "cash"
    KAKAO = "kakao"
    NAVER = "naver"

class PaymentStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    CANCELLED = "cancelled"