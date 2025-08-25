from sqlalchemy.orm import Session
from schemas.response.order_detail import OrderDetailResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import OrderNotFoundException, AuthorizationException
from model.order import Order
from utility.db import get_db

async def try_get_order_detail(order_id: str):
    # DB 세션 직접 가져오기
    session = next(get_db())
    
    try:
        # 1. 주문 조회
        order = session.get(Order, order_id)
        if not order:
            raise OrderNotFoundException(f"주문 ID {order_id}를 찾을 수 없습니다.")

        # (실제 구현에서는 권한 체크 필요)
        # if not user_is_owner(order):
        #     raise AuthorizationException()

        # 2. 응답 DTO 생성 및 반환
        return OrderDetailResponseDto.create_result(order)
    except (OrderNotFoundException, AuthorizationException) as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)
    finally:
        session.close() 