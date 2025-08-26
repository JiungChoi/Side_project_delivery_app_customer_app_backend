from sqlalchemy.orm import Session
from schemas.request.delete_cart_item import DeleteCartItemRequestDto
from schemas.response.delete_cart_item import DeleteCartItemResponseDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import (
    AuthenticationException, 
    CartItemNotFoundException,
    AuthorizationException
)
from model.cart import Cart, CartItem, CartItemOption
from utility.db import get_db
from uuid import UUID
from datetime import datetime


async def try_delete_cart_item(item_id: UUID, request: DeleteCartItemRequestDto):
    session = next(get_db())
    
    try:
        if not request.user_id:
            raise AuthenticationException("사용자 ID가 필요합니다.")

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
            raise AuthorizationException("해당 장바구니 항목을 삭제할 권한이 없습니다.")

        # 장바구니 아이템 옵션 soft delete
        cart_item_options = session.query(CartItemOption).filter(
            CartItemOption.cart_item_id == cart_item.uuid,
            CartItemOption.is_deleted == False
        ).all()

        deleted_time = datetime.utcnow()
        for option in cart_item_options:
            option.is_deleted = True
            option.updated_at = deleted_time

        # 장바구니 아이템 soft delete
        cart_item.is_deleted = True
        cart_item.updated_at = deleted_time

        session.commit()

        response = DeleteCartItemResponseDto(deleted_at=deleted_time)
        return create_success_result(response)
        
    except (AuthenticationException, CartItemNotFoundException, AuthorizationException) as e:
        session.rollback()
        return create_error_result(e)
    except Exception as e:
        session.rollback()
        return create_unknown_error_result(e)
    finally:
        session.close()