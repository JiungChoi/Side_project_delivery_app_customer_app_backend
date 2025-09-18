from schemas.request.update_cart_item import UpdateCartItemRequestDto
from schemas.response.update_cart_item import UpdateCartItemResponseDto
from schemas.response.get_cart import CartItemDto, CartItemOptionDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import (
    AuthenticationException,
    CartItemNotFoundException,
    CartItemValidationException,
    AuthorizationException,
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
            raise CartItemValidationException("수량은 1 이상이어야 합니다.")

        if request.price < 0:
            raise CartItemValidationException("가격은 0 이상이어야 합니다.")

        # Load cart item
        cart_item = (
            session.query(CartItem)
            .filter(CartItem.uuid == item_id, CartItem.is_deleted == False)
            .first()
        )

        if not cart_item:
            raise CartItemNotFoundException("장바구니 상품을 찾을 수 없습니다.")

        # Ownership check
        cart = (
            session.query(Cart)
            .filter(Cart.uuid == cart_item.cart_id, Cart.is_deleted == False)
            .first()
        )

        if not cart or cart.user_id != request.user_id:
            raise AuthorizationException("해당 장바구니 상품에 대한 권한이 없습니다.")

        # Soft delete existing options
        existing_options = (
            session.query(CartItemOption)
            .filter(CartItemOption.cart_item_id == cart_item.uuid, CartItemOption.is_deleted == False)
            .all()
        )

        for option in existing_options:
            option.is_deleted = True
            option.updated_at = datetime.utcnow()

        # Update cart item including menu info if provided
        cart_item.quantity = request.quantity
        cart_item.price = request.price
        if request.menu_name:
            cart_item.menu_name = request.menu_name
        if request.menu_description is not None:
            cart_item.menu_description = request.menu_description
        if request.menu_image_url is not None:
            cart_item.menu_image_url = request.menu_image_url
        cart_item.updated_at = datetime.utcnow()

        # Add new options
        if request.options:
            for option in request.options:
                if option.price < 0:
                    raise CartItemValidationException("옵션 가격은 0 이상이어야 합니다.")

                cart_item_option = CartItemOption(
                    uuid=uuid4(),
                    cart_item_id=cart_item.uuid,
                    menu_option_id=None,  # ID 연동 전: 이름만 저장
                    menu_option_name=option.menu_option_name,
                    price=option.price,
                )
                session.add(cart_item_option)

        session.commit()

        # Build updated item dto
        options = (
            session.query(CartItemOption)
            .filter(CartItemOption.cart_item_id == cart_item.uuid, CartItemOption.is_deleted == False)
            .all()
        )

        option_dtos = [
            CartItemOptionDto(
                uuid=o.uuid,
                menu_option_id=o.menu_option_id,
                price=o.price,
                created_at=o.created_at,
                updated_at=o.updated_at,
            )
            for o in options
        ]

        item_dto = CartItemDto(
            uuid=cart_item.uuid,
            menu_id=cart_item.menu_id,
            quantity=cart_item.quantity,
            price=cart_item.price,
            created_at=cart_item.created_at,
            updated_at=cart_item.updated_at,
            options=option_dtos if option_dtos else None,
        )

        response = UpdateCartItemResponseDto(cart_item=item_dto)
        return create_success_result(response)

    except (AuthenticationException, CartItemNotFoundException, CartItemValidationException, AuthorizationException) as e:
        session.rollback()
        return create_error_result(e)
    except Exception as e:
        session.rollback()
        return create_unknown_error_result(e)
    finally:
        session.close()

