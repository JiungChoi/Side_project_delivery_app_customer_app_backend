"""
Menu API Router

메뉴 관련 API 엔드포인트들을 정의합니다.
"""

from fastapi import APIRouter, HTTPException, status
import uuid

# Common schemas
from schemas.common import (
    ResultDto,
    create_success_result,
    create_error_result
)

# Exception classes
from model.exception import (
    MenuNotFoundException,
    MenuOptionNotFoundException,
    MenuValidationException
)

# Business logic functions
from .func.try_get_restaurant_menus import try_get_restaurant_menus
from .func.try_get_menu_detail import try_get_menu_detail
from .func.try_get_menu_options import try_get_menu_options
from .func.try_get_restaurant_categories import try_get_restaurant_categories

router = APIRouter(tags=["menu"])


@router.get("/restaurants/{restaurant_id}/menus", response_model=ResultDto)
async def get_restaurant_menus(
    restaurant_id: uuid.UUID
):
    """
    특정 매장의 전체 메뉴 조회
    
    매장 상세 페이지 진입 시, 메뉴 탭 로딩 시 호출됩니다.
    """
    try:
        result = await try_get_restaurant_menus(restaurant_id)
        return result
    except Exception as e:
        return create_error_result(e)


@router.get("/menus/{menu_id}", response_model=ResultDto)
async def get_menu_detail(
    menu_id: uuid.UUID
):
    """
    특정 메뉴 상세정보 조회
    
    고객이 메뉴 항목을 터치해 상세 팝업을 열었을 때 호출됩니다.
    """
    try:
        result = await try_get_menu_detail(menu_id)
        return result
    except MenuNotFoundException as e:
        return create_error_result(e)
    except Exception as e:
        return create_error_result(e)


@router.get("/menus/{menu_id}/options", response_model=ResultDto)
async def get_menu_options(
    menu_id: uuid.UUID
):
    """
    해당 메뉴에 포함된 옵션 그룹 및 옵션 목록 조회
    
    메뉴 상세 팝업 진입 시, 옵션 선택 영역 구성 시 호출됩니다.
    """
    try:
        result = await try_get_menu_options(menu_id)
        return result
    except MenuNotFoundException as e:
        return create_error_result(e)
    except Exception as e:
        return create_error_result(e)


@router.get("/restaurants/{restaurant_id}/categories", response_model=ResultDto)
async def get_restaurant_categories(
    restaurant_id: uuid.UUID
):
    """
    해당 매장의 메뉴 카테고리 조회
    
    메뉴 필터 탭 또는 스크롤 고정 영역 구성 시 호출됩니다.
    """
    try:
        result = await try_get_restaurant_categories(restaurant_id)
        return result
    except Exception as e:
        return create_error_result(e)


@router.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy", "service": "menu-service"}