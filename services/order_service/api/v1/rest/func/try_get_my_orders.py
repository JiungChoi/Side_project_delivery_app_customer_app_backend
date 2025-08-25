from sqlalchemy.orm import Session
from schemas.request.my_orders import MyOrdersRequestDto
from schemas.response.my_orders import MyOrdersResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import AuthenticationException
from model.order import Order
from typing import List
from utility.db import get_db

async def try_get_my_orders(request: MyOrdersRequestDto):
    # DB 세션 직접 가져오기
    session = next(get_db())
    
    try:
        # (실제 구현에서는 인증된 사용자 ID를 활용해야 함)
        # user_id = get_current_user_id()
        user_id = "user-456"  # 예시
        if not user_id:
            raise AuthenticationException("로그인이 필요합니다.")

        # 1. 주문 목록 조회
        query = session.query(Order).filter(Order.user_id == user_id)
        if request.start_date:
            query = query.filter(Order.created_at >= request.start_date)
        if request.end_date:
            query = query.filter(Order.created_at <= request.end_date)
        if request.status:
            query = query.filter(Order.status == request.status)
        orders: List[Order] = query.all()

        # 2. 응답 DTO 생성 및 반환
        return MyOrdersResponseDto.create_result(orders)
    except AuthenticationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)
    finally:
        session.close() 