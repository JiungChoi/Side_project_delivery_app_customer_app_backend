# -*- coding: utf-8 -*-
from enum import Enum

class SupportStatus(Enum):
    PENDING = "pending"        # 대기중
    IN_PROGRESS = "in_progress"  # 처리중  
    COMPLETED = "completed"    # 완료
    CANCELLED = "cancelled"    # 취소됨

class SupportType(Enum):
    ORDER_INQUIRY = "order_inquiry"           # 주문 문의
    PAYMENT_ISSUE = "payment_issue"           # 결제 문제
    DELIVERY_ISSUE = "delivery_issue"         # 배달 문제  
    RESTAURANT_INQUIRY = "restaurant_inquiry" # 레스토랑 문의
    APP_BUG = "app_bug"                      # 앱 버그
    GENERAL_INQUIRY = "general_inquiry"       # 일반 문의
    REFUND_REQUEST = "refund_request"         # 환불 요청
    OTHER = "other"                          # 기타

class SupportPriority(Enum):
    LOW = "low"        # 낮음
    MEDIUM = "medium"  # 보통
    HIGH = "high"      # 높음
    URGENT = "urgent"  # 긴급