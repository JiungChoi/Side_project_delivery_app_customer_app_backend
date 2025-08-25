from sqlalchemy.orm import Session
from schemas.request.cancel_order import CancelOrderRequestDto
from schemas.response.cancel_order import CancelOrderResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import OrderNotFoundException, OrderCancellationException, AuthorizationException
from model.order import Order
from utility.db import get_db

async def try_cancel_order(request: CancelOrderRequestDto):
    # DB 세션 직접 가져오기
    session = next(get_db())
    
    try:
        # 1. 주문 조회
        order = session.get(Order, request.order_id)
        if not order:
            raise OrderNotFoundException(f"주문 ID {request.order_id}를 찾을 수 없습니다.")

        # (실제 구현에서는 권한 체크 필요)
        # if not user_is_owner(order):
        #     raise AuthorizationException()

        # 2. 취소 가능한 상태인지 확인 및 취소 처리
        if order.status not in ["pending", "paid"]:
            raise OrderCancellationException("취소할 수 없는 주문 상태입니다.")
        order.status = "cancelled"
        session.commit()
        session.refresh(order)

        # 3. 응답 DTO 생성 및 반환
        return CancelOrderResponseDto.create_result(order)
    except (OrderNotFoundException, OrderCancellationException, AuthorizationException) as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)
    finally:
        session.close() 