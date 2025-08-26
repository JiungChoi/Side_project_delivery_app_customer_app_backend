"""
Restaurant API Router

매장 관련 API 엔드포인트들을 정의합니다.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
import uuid

# Request/Response DTOs
from schemas.request.update_status import UpdateRestaurantStatusRequestDto

from schemas.response.restaurant import (
    RestaurantsListResponseDto, RestaurantDetailResponseDto, 
    RestaurantImagesResponseDto, RestaurantStatusResponseDto
)
from schemas.response.menu import RestaurantMenusResponseDto, RestaurantCategoriesResponseDto

# Common schemas
from schemas.common import (
    ResultDto,
    create_success_result,
    create_error_result,
    create_unknown_error_result
)

# Exception classes
from model.exception import (
    RestaurantNotFoundException,
    RestaurantValidationException,
    MenuNotFoundException,
    AuthenticationException,
    AuthorizationException
)

# Business logic functions
from .func.try_get_restaurants import try_get_restaurants
from .func.try_get_restaurant_detail import try_get_restaurant_detail
from .func.try_get_restaurant_images import try_get_restaurant_images
from .func.try_get_restaurant_menus import try_get_restaurant_menus
from .func.try_get_restaurant_categories import try_get_restaurant_categories
from .func.try_update_restaurant_status import try_update_restaurant_status

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get("/", response_model=ResultDto)
async def get_restaurants():
    """
    전체 매장 리스트 조회
    
    고객 앱에서 메인 화면 진입 시, 배달 가능한 매장 목록 요청 시 호출됩니다.
    """
    try:
        result = await try_get_restaurants()
        return result
    except Exception as e:
        return create_unknown_error_result(e)


@router.get("/{restaurant_id}", response_model=ResultDto)
async def get_restaurant_detail(restaurant_id: uuid.UUID):
    """
    특정 매장 상세정보 조회
    
    고객이 특정 매장 클릭 시 상세 페이지 진입할 때 호출됩니다.
    """
    try:
        result = await try_get_restaurant_detail(restaurant_id)
        return result
    except RestaurantNotFoundException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.get("/{restaurant_id}/images", response_model=ResultDto)
async def get_restaurant_images(restaurant_id: uuid.UUID):
    """
    매장의 이미지 리스트 조회 (배너/갤러리/메뉴용 등)
    
    매장 상세 페이지 진입 시, 상단 이미지 슬라이더 로딩 시 호출됩니다.
    """
    try:
        result = await try_get_restaurant_images(restaurant_id)
        return result
    except RestaurantNotFoundException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.get("/{restaurant_id}/menus", response_model=ResultDto)
async def get_restaurant_menus(restaurant_id: uuid.UUID):
    """
    해당 매장의 메뉴 전체 리스트 조회
    
    매장 상세 페이지에서 메뉴 리스트 로딩 시 호출됩니다.
    """
    try:
        result = await try_get_restaurant_menus(restaurant_id)
        return result
    except RestaurantNotFoundException as e:
        return create_error_result(e)
    except MenuNotFoundException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.get("/{restaurant_id}/categories", response_model=ResultDto)
async def get_restaurant_categories(restaurant_id: uuid.UUID):
    """
    해당 매장의 메뉴 카테고리 조회
    
    메뉴 탭 필터링 또는 좌측 카테고리 탭 구성 시 호출됩니다.
    """
    try:
        result = await try_get_restaurant_categories(restaurant_id)
        return result
    except RestaurantNotFoundException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.patch("/{restaurant_id}/status", response_model=ResultDto)
async def update_restaurant_status(restaurant_id: uuid.UUID, request: UpdateRestaurantStatusRequestDto):
    """
    매장의 영업 상태 업데이트 (예: 오픈/마감/휴무)
    
    업주가 업주용 앱 또는 백오피스에서 상태 전환 시 호출됩니다.
    """
    try:
        result = await try_update_restaurant_status(restaurant_id, request)
        return result
    except RestaurantNotFoundException as e:
        return create_error_result(e)
    except RestaurantValidationException as e:
        return create_error_result(e)
    except AuthorizationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)