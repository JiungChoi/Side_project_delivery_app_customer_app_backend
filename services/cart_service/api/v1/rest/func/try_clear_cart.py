from sqlalchemy.orm import Session
from schemas.request.clear_cart import ClearCartRequestDto
from schemas.response.clear_cart import ClearCartResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import (
    AuthenticationException, 
    CartNotFoundException
)
from model.cart import Cart, CartItem, CartItemOption
from utility.db import get_db
from datetime import datetime


async def try_clear_cart(request: ClearCartRequestDto):
    session = next(get_db())
    
    try:
        if not request.user_id:
            raise AuthenticationException("사용자 ID가 필요합니다.")

        # 사용자의 장바구니 조회
        cart = session.query(Cart).filter(
            Cart.user_id == request.user_id,
            Cart.is_deleted == False
        ).first()

        if not cart:
            raise CartNotFoundException("장바구니를 찾을 수 없습니다.")

        # 장바구니 아이템들 조회
        cart_items = session.query(CartItem).filter(
            CartItem.cart_id == cart.uuid,
            CartItem.is_deleted == False
        ).all()

        cleared_time = datetime.utcnow()

        # 모든 장바구니 아이템과 옵션들 soft delete
        for cart_item in cart_items:
            # 아이템 옵션들 삭제
            cart_item_options = session.query(CartItemOption).filter(
                CartItemOption.cart_item_id == cart_item.uuid,
                CartItemOption.is_deleted == False
            ).all()

            for option in cart_item_options:
                option.is_deleted = True
                option.updated_at = cleared_time

            # 아이템 삭제
            cart_item.is_deleted = True
            cart_item.updated_at = cleared_time

        # 장바구니 자체도 삭제 (또는 유지하고 아이템들만 삭제)
        cart.is_deleted = True
        cart.updated_at = cleared_time

        session.commit()

        response = ClearCartResponseDto(cleared_at=cleared_time)
        return create_success_result(response)
        
    except (AuthenticationException, CartNotFoundException) as e:
        session.rollback()
        return create_error_result(e)
    except Exception as e:
        session.rollback()
        return create_unknown_error_result(e)
    finally:
        session.close()