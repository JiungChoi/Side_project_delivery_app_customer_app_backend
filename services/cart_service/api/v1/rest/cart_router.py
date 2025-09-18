"""
Cart API Router

장바구니 관련 API 엔드포인트들을 정의합니다.
"""

from fastapi import APIRouter, HTTPException, status, Depends, Request
from uuid import UUID
from sqlalchemy.orm import Session
from utility.db import get_db

# Request/Response DTOs
from schemas.request.get_cart import GetCartRequestDto
from schemas.request.add_cart_item import AddCartItemRequestDto
from schemas.request.update_cart_item import UpdateCartItemRequestDto
from schemas.request.delete_cart_item import DeleteCartItemRequestDto
from schemas.request.clear_cart import ClearCartRequestDto

from schemas.response.get_cart import GetCartResponseDto
from schemas.response.add_cart_item import AddCartItemResponseDto
from schemas.response.update_cart_item import UpdateCartItemResponseDto
from schemas.response.delete_cart_item import DeleteCartItemResponseDto
from schemas.response.clear_cart import ClearCartResponseDto

# Common schemas
from schemas.common import (
    ResultDto,
    create_success_result,
    create_error_result,
    create_unknown_error_result
)

# Exception classes
from model.exception import (
    CartNotFoundException,
    CartItemNotFoundException,
    CartValidationException,
    RestaurantMismatchException,
    MenuNotFoundException,
    UserNotFoundException,
    CartItemValidationException,
    AuthenticationException,
    AuthorizationException
)

# Business logic functions
from .func.try_get_cart import try_get_cart
from .func.try_add_cart_item import try_add_cart_item
from .func.try_update_cart_item import try_update_cart_item
from .func.try_delete_cart_item import try_delete_cart_item
from .func.try_clear_cart import try_clear_cart

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    print("[CART_ROUTER] Health check called")
    return {"status": "ok", "message": "Cart service is running"}

@router.post("/simple-test")
async def simple_post_test():
    """가장 단순한 POST 엔드포인트 테스트"""
    print("[CART_ROUTER] ========== SIMPLE POST TEST HIT ==========")
    return {"status": "success", "message": "Simple POST endpoint works"}

@router.get("/simple")
async def simple_test():
    """Simple test endpoint without database"""
    print("[CART_ROUTER] Simple test called")
    return {"status": "ok", "message": "Simple endpoint works"}


@router.get("", response_model=ResultDto)
async def get_cart(user_id: UUID):
    """
    장바구니 조회 API
    
    고객이 장바구니 페이지 진입 시 호출됩니다.
    """
    try:
        request = GetCartRequestDto(user_id=user_id)
        result = await try_get_cart(request)
        return result
    except AuthenticationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.post("/items-test")
async def add_cart_item_test(request: AddCartItemRequestDto):
    """
    Test endpoint for cart item addition without database
    """
    print(f"[CART_ROUTER] add_cart_item_test endpoint hit")
    print(f"[CART_ROUTER] Request received: {request}")
    return {"status": "success", "message": "Test endpoint works", "received_data": request.dict()}

@router.post("/items-bypass")
async def add_cart_item_bypass(request: Request):
    """
    Bypass endpoint to test without Pydantic validation
    """
    print(f"[CART_ROUTER] ========== BYPASS ENDPOINT HIT ==========")
    try:
        body = await request.body()
        body_str = body.decode('utf-8')
        print(f"[CART_ROUTER] Raw body: {body_str}")

        import json
        data = json.loads(body_str)
        print(f"[CART_ROUTER] Parsed data: {data}")

        # Try to call the cart service logic directly
        from schemas.request.add_cart_item import AddCartItemRequestDto
        cart_request = AddCartItemRequestDto(**data)
        print(f"[CART_ROUTER] Successfully created DTO: {cart_request}")

        result = await try_add_cart_item(cart_request)
        print(f"[CART_ROUTER] Business logic result: {result}")
        return result

    except Exception as e:
        print(f"[CART_ROUTER] Error in bypass: {e}")
        import traceback
        print(f"[CART_ROUTER] Traceback: {traceback.format_exc()}")
        return {"error": str(e), "traceback": traceback.format_exc()}

@router.post("/items", response_model=ResultDto, status_code=status.HTTP_201_CREATED)
async def add_cart_item(request: AddCartItemRequestDto):
    """
    장바구니에 메뉴 추가 API

    고객이 메뉴를 옵션과 함께 선택하고 "장바구니에 담기" 버튼을 눌렀을 때 호출됩니다.
    """
    print(f"[CART_ROUTER] ========== ADD_CART_ITEM ENDPOINT HIT ==========")
    print(f"[CART_ROUTER] Request type: {type(request)}")
    print(f"[CART_ROUTER] Request content: {request}")
    print(f"[CART_ROUTER] Request dict: {request.dict() if hasattr(request, 'dict') else 'No dict method'}")
    try:
        print(f"[CART_ROUTER] Calling try_add_cart_item with validated request")
        result = await try_add_cart_item(request)
        print(f"[CART_ROUTER] Request processed successfully, result: {result}")
        return result
    except CartValidationException as e:
        print(f"[CART_ROUTER] CartValidationException: {e}")
        return create_error_result(e)
    except RestaurantMismatchException as e:
        print(f"[CART_ROUTER] RestaurantMismatchException: {e}")
        return create_error_result(e)
    except CartItemValidationException as e:
        print(f"[CART_ROUTER] CartItemValidationException: {e}")
        return create_error_result(e)
    except MenuNotFoundException as e:
        print(f"[CART_ROUTER] MenuNotFoundException: {e}")
        return create_error_result(e)
    except UserNotFoundException as e:
        print(f"[CART_ROUTER] UserNotFoundException: {e}")
        return create_error_result(e)
    except AuthenticationException as e:
        print(f"[CART_ROUTER] AuthenticationException: {e}")
        return create_error_result(e)
    except Exception as e:
        print(f"[CART_ROUTER] Unexpected exception: {e}")
        import traceback
        print(f"[CART_ROUTER] Traceback: {traceback.format_exc()}")
        return create_unknown_error_result(e)


@router.patch("/items/{item_id}", response_model=ResultDto)
async def update_cart_item(item_id: UUID, request: UpdateCartItemRequestDto):
    """
    장바구니 항목 수정 API
    
    장바구니 페이지에서 수량 + 옵션 변경 시 저장 클릭할 때 호출됩니다.
    """
    try:
        result = await try_update_cart_item(item_id, request)
        return result
    except CartItemNotFoundException as e:
        return create_error_result(e)
    except CartItemValidationException as e:
        return create_error_result(e)
    except AuthenticationException as e:
        return create_error_result(e)
    except AuthorizationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.delete("/items/{item_id}", response_model=ResultDto)
async def delete_cart_item(item_id: UUID, user_id: UUID):
    """
    장바구니 항목 삭제 API
    
    고객이 장바구니에서 특정 메뉴를 제거할 때 호출됩니다.
    """
    try:
        request = DeleteCartItemRequestDto(user_id=user_id)
        result = await try_delete_cart_item(item_id, request)
        return result
    except CartItemNotFoundException as e:
        return create_error_result(e)
    except AuthenticationException as e:
        return create_error_result(e)
    except AuthorizationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.delete("", response_model=ResultDto)
async def clear_cart(user_id: UUID):
    """
    장바구니 전체 비우기 API
    
    고객이 "전체 비우기" 클릭 시 호출됩니다.
    """
    try:
        request = ClearCartRequestDto(user_id=user_id)
        result = await try_clear_cart(request)
        return result
    except CartNotFoundException as e:
        return create_error_result(e)
    except AuthenticationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)