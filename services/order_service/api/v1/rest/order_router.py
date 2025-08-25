"""
Order API Router

주문 관련 API 엔드포인트들을 정의합니다.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from datetime import date

# Request/Response DTOs
from schemas.request.create_order import CreateOrderRequestDto
from schemas.request.order_detail import OrderDetailRequestDto
from schemas.request.my_orders import MyOrdersRequestDto
from schemas.request.cancel_order import CancelOrderRequestDto
from schemas.request.update_order_status import UpdateOrderStatusRequestDto
from schemas.request.complete_order import CompleteOrderRequestDto

from schemas.response.create_order import CreateOrderResponseDto
from schemas.response.order_detail import OrderDetailResponseDto
from schemas.response.my_orders import MyOrdersResponseDto
from schemas.response.cancel_order import CancelOrderResponseDto
from schemas.response.update_order_status import UpdateOrderStatusResponseDto
from schemas.response.complete_order import CompleteOrderResponseDto

# Common schemas
from schemas.common import (
    ResultDto,
    create_success_result,
    create_error_result,
    create_unknown_error_result
)

# Exception classes
from model.exception import (
    OrderNotFoundException,
    OrderValidationException,
    OrderStatusException,
    OrderCancellationException,
    OrderCompletionException,
    PaymentException,
    RestaurantNotFoundException,
    MenuNotFoundException,
    AddressNotFoundException,
    UserNotFoundException,
    AuthenticationException,
    AuthorizationException
)

# Business logic functions
from .func.try_create_order import try_create_order
from .func.try_get_order_detail import try_get_order_detail
from .func.try_get_my_orders import try_get_my_orders
from .func.try_cancel_order import try_cancel_order
from .func.try_update_order_status import try_update_order_status
from .func.try_complete_order import try_complete_order

# Database - 이제 func 내부에서 직접 사용

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=ResultDto, status_code=status.HTTP_201_CREATED)
async def create_order(
    request: CreateOrderRequestDto
):
    """
    주문 생성 API
    
    고객이 장바구니에서 결제를 누른 순간 호출됩니다.
    """
    try:
        result = await try_create_order(request)
        return result
    except OrderValidationException as e:
        return create_error_result(e)
    except PaymentException as e:
        return create_error_result(e)
    except RestaurantNotFoundException as e:
        return create_error_result(e)
    except MenuNotFoundException as e:
        return create_error_result(e)
    except AddressNotFoundException as e:
        return create_error_result(e)
    except UserNotFoundException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.get("/{order_id}", response_model=ResultDto)
async def get_order_detail(
    order_id: str
):
    """
    주문 상세 조회 API
    
    주문완료 후 상세내역을 다시 확인할 때 호출됩니다.
    """
    try:
        result = await try_get_order_detail(order_id)
        return result
    except OrderNotFoundException as e:
        return create_error_result(e)
    except AuthorizationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.get("/my", response_model=ResultDto)
async def get_my_orders(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[str] = None
):
    """
    내 주문 목록 조회 API
    
    고객이 마이페이지 > 주문내역 보기를 클릭했을 때 호출됩니다.
    """
    try:
        request = MyOrdersRequestDto(
            start_date=start_date,
            end_date=end_date,
            status=status
        )
        result = await try_get_my_orders(request)
        return result
    except AuthenticationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.patch("/{order_id}/cancel", response_model=ResultDto)
async def cancel_order(
    order_id: str
):
    """
    주문 취소 API
    
    고객이 결제된 주문을 취소할 때 호출됩니다 (pending, paid 상태일 때만).
    """
    try:
        request = CancelOrderRequestDto(order_id=order_id)
        result = await try_cancel_order(request)
        return result
    except OrderNotFoundException as e:
        return create_error_result(e)
    except OrderCancellationException as e:
        return create_error_result(e)
    except AuthorizationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.patch("/", response_model=ResultDto)
async def update_order_status(
    request: UpdateOrderStatusRequestDto
):
    """
    주문 상태 수동 업데이트 API
    
    업주 앱에서 "조리시작" 버튼을 누르거나, 라이더가 "배달 시작"을 누를 때 호출됩니다.
    """
    try:
        result = await try_update_order_status(request)
        return result
    except OrderNotFoundException as e:
        return create_error_result(e)
    except OrderStatusException as e:
        return create_error_result(e)
    except AuthorizationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)


@router.post("/{order_id}/complete", response_model=ResultDto)
async def complete_order(
    order_id: str
):
    """
    주문 완료 처리 API
    
    라이더가 배달완료 버튼을 누를 때 호출됩니다.
    """
    try:
        request = CompleteOrderRequestDto(order_id=order_id)
        result = await try_complete_order(request)
        return result
    except OrderNotFoundException as e:
        return create_error_result(e)
    except OrderCompletionException as e:
        return create_error_result(e)
    except AuthorizationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e) 