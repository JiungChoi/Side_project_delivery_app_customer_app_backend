from enum import Enum

class NotificationType(Enum):
    ORDER = "order"
    PROMOTION = "promotion"
    SYSTEM = "system"
    EVENT = "event"