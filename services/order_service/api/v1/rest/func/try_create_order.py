from sqlalchemy.orm import Session
from schemas.request.create_order import CreateOrderRequestDto
from schemas.response.create_order import CreateOrderResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import (
    OrderValidationException, PaymentException, RestaurantNotFoundException,
    MenuNotFoundException, AddressNotFoundException, UserNotFoundException
)
from model.order import Order
from model.restaurant import Restaurant
from model.menu import Menu
from model.address import Address
from utility.db import get_db

async def try_create_order(request: CreateOrderRequestDto):
    # DB 세션 직접 가져오기
    session = next(get_db())
    
    try:
        # 1. 입력 검증
        if not request.items:
            raise OrderValidationException("주문 아이템이 없습니다.")

        # 2. 매장, 주소, 메뉴 등 유효성 체크
        restaurant = session.get(Restaurant, request.restaurant_id)
        if not restaurant:
            raise RestaurantNotFoundException()
        address = session.get(Address, request.address_id)
        if not address:
            raise AddressNotFoundException()
        # (실제 구현에서는 사용자 인증 정보 활용)
        # user = session.get(User, user_id)
        # if not user:
        #     raise UserNotFoundException()
        for item in request.items:
            menu = session.get(Menu, item.menu_id)
            if not menu:
                raise MenuNotFoundException()

        # 3. 주문 생성
        new_order = Order(
            restaurant_id=request.restaurant_id,
            address_id=request.address_id,
            payment_method=request.payment_method,
            # 추가 필드 필요시 채우기
        )
        session.add(new_order)
        session.commit()
        session.refresh(new_order)

        # 4. 응답 DTO 생성 및 반환
        return CreateOrderResponseDto.create_result(new_order)
    except (OrderValidationException, PaymentException, RestaurantNotFoundException,
            MenuNotFoundException, AddressNotFoundException, UserNotFoundException) as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)
    finally:
        session.close() 