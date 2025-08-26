from sqlalchemy.orm import Session
from schemas.request.add_cart_item import AddCartItemRequestDto
from schemas.response.add_cart_item import AddCartItemResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import (
    AuthenticationException, 
    CartValidationException, 
    RestaurantMismatchException,
    CartItemValidationException
)
from model.cart import Cart, CartItem, CartItemOption
from utility.db import get_db
from uuid import uuid4
from datetime import datetime


async def try_add_cart_item(request: AddCartItemRequestDto):
    session = next(get_db())
    
    try:
        if not request.user_id:
            raise AuthenticationException("사용자 ID가 필요합니다.")

        if request.quantity <= 0:
            raise CartItemValidationException("수량은 1개 이상이어야 합니다.")

        if request.price < 0:
            raise CartItemValidationException("가격은 0원 이상이어야 합니다.")

        # 기존 장바구니 조회
        existing_cart = session.query(Cart).filter(
            Cart.user_id == request.user_id,
            Cart.is_deleted == False
        ).first()

        # 기존 장바구니가 있고 다른 매장인 경우 예외 발생
        if existing_cart and existing_cart.restaurant_id != request.restaurant_id:
            raise RestaurantMismatchException("다른 매장의 메뉴는 장바구니에 추가할 수 없습니다.")

        # 장바구니가 없으면 새로 생성
        if not existing_cart:
            cart = Cart(
                uuid=uuid4(),
                user_id=request.user_id,
                restaurant_id=request.restaurant_id
            )
            session.add(cart)
            session.flush()  # cart.uuid를 얻기 위해
        else:
            cart = existing_cart

        # 장바구니 아이템 생성
        cart_item = CartItem(
            uuid=uuid4(),
            cart_id=cart.uuid,
            menu_id=request.menu_id,
            quantity=request.quantity,
            price=request.price
        )
        session.add(cart_item)
        session.flush()  # cart_item.uuid를 얻기 위해

        # 옵션이 있다면 추가
        if request.options:
            for option in request.options:
                if option.price < 0:
                    raise CartItemValidationException("옵션 가격은 0원 이상이어야 합니다.")
                    
                cart_item_option = CartItemOption(
                    uuid=uuid4(),
                    cart_item_id=cart_item.uuid,
                    menu_option_id=option.menu_option_id,
                    price=option.price
                )
                session.add(cart_item_option)

        session.commit()

        response = AddCartItemResponseDto(
            cart_item_id=cart_item.uuid,
            created_at=cart_item.created_at
        )
        return create_success_result(response)
        
    except (AuthenticationException, CartValidationException, RestaurantMismatchException, CartItemValidationException) as e:
        session.rollback()
        return create_error_result(e)
    except Exception as e:
        session.rollback()
        return create_unknown_error_result(e)
    finally:
        session.close()