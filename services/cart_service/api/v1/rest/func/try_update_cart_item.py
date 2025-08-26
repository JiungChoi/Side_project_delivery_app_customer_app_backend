from sqlalchemy.orm import Session
from schemas.request.update_cart_item import UpdateCartItemRequestDto
from schemas.response.update_cart_item import UpdateCartItemResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import (
    AuthenticationException, 
    CartItemNotFoundException,
    CartItemValidationException,
    AuthorizationException
)
from model.cart import Cart, CartItem, CartItemOption
from utility.db import get_db
from uuid import UUID, uuid4
from datetime import datetime


async def try_update_cart_item(item_id: UUID, request: UpdateCartItemRequestDto):
    session = next(get_db())
    
    try:
        if not request.user_id:
            raise AuthenticationException("사용자 ID가 필요합니다.")

        if request.quantity <= 0:
            raise CartItemValidationException("수량은 1개 이상이어야 합니다.")

        if request.price < 0:
            raise CartItemValidationException("가격은 0원 이상이어야 합니다.")

        # 장바구니 아이템 조회
        cart_item = session.query(CartItem).filter(
            CartItem.uuid == item_id,
            CartItem.is_deleted == False
        ).first()

        if not cart_item:
            raise CartItemNotFoundException("장바구니 항목을 찾을 수 없습니다.")

        # 사용자 권한 확인
        cart = session.query(Cart).filter(
            Cart.uuid == cart_item.cart_id,
            Cart.is_deleted == False
        ).first()

        if not cart or cart.user_id != request.user_id:
            raise AuthorizationException("해당 장바구니 항목을 수정할 권한이 없습니다.")

        # 기존 옵션 삭제 (soft delete)
        existing_options = session.query(CartItemOption).filter(
            CartItemOption.cart_item_id == cart_item.uuid,
            CartItemOption.is_deleted == False
        ).all()

        for option in existing_options:
            option.is_deleted = True
            option.updated_at = datetime.utcnow()

        # 장바구니 아이템 업데이트
        cart_item.quantity = request.quantity
        cart_item.price = request.price
        cart_item.updated_at = datetime.utcnow()

        # 새 옵션 추가
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

        response = UpdateCartItemResponseDto(updated_at=cart_item.updated_at)
        return create_success_result(response)
        
    except (AuthenticationException, CartItemNotFoundException, CartItemValidationException, AuthorizationException) as e:
        session.rollback()
        return create_error_result(e)
    except Exception as e:
        session.rollback()
        return create_unknown_error_result(e)
    finally:
        session.close()