from pydantic import BaseModel
from typing import Optional

class MenuBase(BaseModel):
    name: str
    price: int
    description: Optional[str] = None
    is_available: Optional[bool] = True

class MenuCreate(MenuBase):
    restaurant_id: str

class MenuUpdate(MenuBase):
    pass

class MenuResponse(MenuBase):
    id: str
    restaurant_id: str

class MenuOptionBase(BaseModel):
    name: str
    price: int
    is_available: Optional[bool] = True

class MenuOptionCreate(MenuOptionBase):
    menu_id: str

class MenuOptionUpdate(MenuOptionBase):
    pass

class MenuOptionResponse(MenuOptionBase):
    id: str
    menu_id: str 