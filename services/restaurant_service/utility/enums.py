# utility/enums.py
from enum import Enum

class RestaurantImageType(Enum):
    BANNER = "banner"
    GALLERY = "gallery"
    MENU = "menu"

class RestaurantStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    TEMPORARILY_CLOSED = "temporarily_closed"
    BREAK_TIME = "break_time"