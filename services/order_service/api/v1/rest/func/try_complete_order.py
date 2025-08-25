from sqlalchemy.orm import Session
from schemas.request.complete_order import CompleteOrderRequestDto
from schemas.response.complete_order import CompleteOrderResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import OrderNotFoundException, OrderCompletionException, AuthorizationException
from model.order import Order
from utility.db import get_db

async def try_complete_order(request: CompleteOrderRequestDto):
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

        # 2. 완료 가능한 상태인지 확인 및 완료 처리
        if order.status != "delivering":
            raise OrderCompletionException("배달 중인 주문만 완료 처리할 수 있습니다.")
        order.status = "delivered"
        session.commit()
        session.refresh(order)

        # 3. 응답 DTO 생성 및 반환
        return CompleteOrderResponseDto.create_result(order)
    except (OrderNotFoundException, OrderCompletionException, AuthorizationException) as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)
    finally:
        session.close() 