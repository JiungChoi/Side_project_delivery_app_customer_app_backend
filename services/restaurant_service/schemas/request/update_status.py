# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from utility.enums import RestaurantStatus

class UpdateRestaurantStatusRequestDto(BaseModel):
    status: RestaurantStatus = Field(..., description="업데이트할 매장 상태")