from sqlalchemy.orm import Session
from schemas.request.update_order_status import UpdateOrderStatusRequestDto
from schemas.response.update_order_status import UpdateOrderStatusResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import OrderNotFoundException, OrderStatusException, AuthorizationException
from model.order import Order
from utility.db import get_db

async def try_update_order_status(request: UpdateOrderStatusRequestDto):
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

        prev_status = order.status
        # 2. 상태 전이 검증 및 업데이트
        valid_transitions = {
            "pending": ["preparing", "cancelled"],
            "paid": ["preparing", "cancelled"],
            "preparing": ["delivering", "cancelled"],
            "delivering": ["delivered", "cancelled"],
            "delivered": [],
            "cancelled": []
        }
        if request.new_status not in valid_transitions.get(prev_status, []):
            raise OrderStatusException(f"{prev_status}에서 {request.new_status}로 상태 변경이 불가능합니다.")
        order.status = request.new_status
        session.commit()
        session.refresh(order)

        # 3. 응답 DTO 생성 및 반환
        return UpdateOrderStatusResponseDto.create_result(order, prev_status)
    except (OrderNotFoundException, OrderStatusException, AuthorizationException) as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)
    finally:
        session.close() 