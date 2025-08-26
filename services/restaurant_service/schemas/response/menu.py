# -*- coding: utf-8 -*-
from typing import List
from pydantic import BaseModel, Field
from uuid import UUID
from schemas.common import create_success_result

class MenuItemDto(BaseModel):
    uuid: UUID = Field(..., description="메뉴 UUID")
    name: str = Field(..., description="메뉴명")
    description: str = Field(..., description="메뉴 설명")
    price: int = Field(..., description="메뉴 가격")
    category: str = Field(..., description="메뉴 카테고리")
    image_url: str = Field(None, description="메뉴 이미지 URL")
    is_available: bool = Field(..., description="메뉴 이용 가능 여부")

class RestaurantMenusResponseDto(BaseModel):
    menus: List[MenuItemDto] = Field(..., description="메뉴 목록")
    
    @classmethod
    def from_domain(cls, menus):
        # 실제로는 menu_service에서 데이터를 가져와야 하지만, 
        # 현재는 restaurant_service 내에서 임시 구조로 작성
        menu_items = []
        for menu in menus:
            menu_items.append(MenuItemDto(
                uuid=menu.uuid,
                name=menu.name,
                description=menu.description,
                price=menu.price,
                category=menu.category,
                image_url=menu.image_url,
                is_available=menu.is_available
            ))
        return cls(menus=menu_items)
    
    @classmethod
    def create_result(cls, menus):
        response_data = cls.from_domain(menus)
        return create_success_result(response_data)

class CategoryDto(BaseModel):
    name: str = Field(..., description="카테고리명")
    menu_count: int = Field(..., description="해당 카테고리의 메뉴 수")

class RestaurantCategoriesResponseDto(BaseModel):
    categories: List[CategoryDto] = Field(..., description="카테고리 목록")
    
    @classmethod
    def from_domain(cls, categories):
        category_items = []
        for category in categories:
            category_items.append(CategoryDto(
                name=category.name,
                menu_count=category.menu_count
            ))
        return cls(categories=category_items)
    
    @classmethod
    def create_result(cls, categories):
        response_data = cls.from_domain(categories)
        return create_success_result(response_data)