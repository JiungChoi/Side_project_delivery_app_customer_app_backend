# -*- coding: utf-8 -*-
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from schemas.common import create_success_result, ResultDto

class RestaurantImageDto(BaseModel):
    uuid: UUID = Field(..., description="이미지 UUID")
    image_type: str = Field(..., description="이미지 타입")
    image_url: str = Field(..., description="이미지 URL")
    ordering: int = Field(..., description="정렬 순서")

class RestaurantDetailDto(BaseModel):
    uuid: UUID = Field(..., description="매장 UUID")
    name: str = Field(..., description="매장명")
    description: Optional[str] = Field(None, description="매장 설명")
    category: Optional[str] = Field(None, description="매장 카테고리")
    rating: int = Field(..., description="평점")
    review_count: int = Field(..., description="리뷰 수")
    min_order_amount: int = Field(..., description="최소 주문 금액")
    delivery_fee: int = Field(..., description="배달비")
    delivery_time: int = Field(..., description="배달 시간")
    operating_hours: Optional[str] = Field(None, description="영업시간")
    tags: Optional[str] = Field(None, description="태그")
    image_url: Optional[str] = Field(None, description="대표 이미지 URL")
    status: str = Field(..., description="매장 상태")
    created_at: datetime = Field(..., description="생성일시")
    updated_at: datetime = Field(..., description="수정일시")

class RestaurantListItemDto(BaseModel):
    uuid: UUID = Field(..., description="매장 UUID")
    name: str = Field(..., description="매장명")
    category: Optional[str] = Field(None, description="매장 카테고리")
    rating: int = Field(..., description="평점")
    review_count: int = Field(..., description="리뷰 수")
    min_order_amount: int = Field(..., description="최소 주문 금액")
    delivery_fee: int = Field(..., description="배달비")
    delivery_time: int = Field(..., description="배달 시간")
    image_url: Optional[str] = Field(None, description="대표 이미지 URL")
    status: str = Field(..., description="매장 상태")

class RestaurantsListResponseDto(BaseModel):
    restaurants: List[RestaurantListItemDto] = Field(..., description="매장 목록")
    
    @classmethod
    def from_domain(cls, restaurants):
        restaurant_items = []
        for restaurant in restaurants:
            restaurant_items.append(RestaurantListItemDto(
                uuid=restaurant.uuid,
                name=restaurant.name,
                category=restaurant.category,
                rating=restaurant.rating,
                review_count=restaurant.review_count,
                min_order_amount=restaurant.min_order_amount,
                delivery_fee=restaurant.delivery_fee,
                delivery_time=restaurant.delivery_time,
                image_url=restaurant.image_url,
                status=restaurant.status
            ))
        return cls(restaurants=restaurant_items)
    
    @classmethod
    def create_result(cls, restaurants):
        response_data = cls.from_domain(restaurants)
        return create_success_result(response_data)

class RestaurantDetailResponseDto(BaseModel):
    restaurant: RestaurantDetailDto = Field(..., description="매장 상세 정보")
    
    @classmethod
    def from_domain(cls, restaurant):
        restaurant_detail = RestaurantDetailDto(
            uuid=restaurant.uuid,
            name=restaurant.name,
            description=restaurant.description,
            category=restaurant.category,
            rating=restaurant.rating,
            review_count=restaurant.review_count,
            min_order_amount=restaurant.min_order_amount,
            delivery_fee=restaurant.delivery_fee,
            delivery_time=restaurant.delivery_time,
            operating_hours=restaurant.operating_hours,
            tags=restaurant.tags,
            image_url=restaurant.image_url,
            status=restaurant.status,
            created_at=restaurant.created_at,
            updated_at=restaurant.updated_at
        )
        return cls(restaurant=restaurant_detail)
    
    @classmethod
    def create_result(cls, restaurant):
        response_data = cls.from_domain(restaurant)
        return create_success_result(response_data)

class RestaurantImagesResponseDto(BaseModel):
    images: List[RestaurantImageDto] = Field(..., description="매장 이미지 목록")
    
    @classmethod
    def from_domain(cls, images):
        image_items = []
        for image in images:
            image_items.append(RestaurantImageDto(
                uuid=image.uuid,
                image_type=image.image_type,
                image_url=image.image_url,
                ordering=image.ordering
            ))
        return cls(images=image_items)
    
    @classmethod
    def create_result(cls, images):
        response_data = cls.from_domain(images)
        return create_success_result(response_data)

class RestaurantStatusResponseDto(BaseModel):
    restaurant_id: UUID = Field(..., description="매장 UUID")
    prev_status: str = Field(..., description="이전 상태")
    new_status: str = Field(..., description="새 상태")
    updated_at: datetime = Field(..., description="수정일시")
    
    @classmethod
    def from_domain(cls, restaurant_id: UUID, prev_status: str, new_status: str, updated_at: datetime):
        return cls(
            restaurant_id=restaurant_id,
            prev_status=prev_status,
            new_status=new_status,
            updated_at=updated_at
        )
    
    @classmethod
    def create_result(cls, restaurant_id: UUID, prev_status: str, new_status: str, updated_at: datetime):
        response_data = cls.from_domain(restaurant_id, prev_status, new_status, updated_at)
        return create_success_result(response_data)