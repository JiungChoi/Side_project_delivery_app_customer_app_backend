from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.request.get_cart import GetCartRequestDto
from schemas.response.get_cart import GetCartResponseDto, CartDto, CartItemDto, CartItemOptionDto
from schemas.common import create_success_result, create_error_result, create_unknown_error_result
from model.exception import AuthenticationException
from model.cart import Cart, CartItem, CartItemOption
from utility.db import get_db
from uuid import UUID
from typing import Optional, List


async def try_get_cart(request: GetCartRequestDto):
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
            return create_success_result(GetCartResponseDto(cart=None))

        # 장바구니 아이템 조회
        cart_items = session.query(CartItem).filter(
            CartItem.cart_id == cart.uuid,
            CartItem.is_deleted == False
        ).all()

        # 활성 아이템이 없는 경우 Cart를 null로 반환
        if not cart_items:
            print(f"[GET_CART] No active items found for cart {cart.uuid}, returning null cart")
            return create_success_result(GetCartResponseDto(cart=None))

        # 응답 DTO 생성
        items = []
        for item in cart_items:
            # 아이템 옵션 조회
            item_options = session.query(CartItemOption).filter(
                CartItemOption.cart_item_id == item.uuid,
                CartItemOption.is_deleted == False
            ).all()

            option_dtos = []
            for option in item_options:
                # 저장된 옵션 이름 사용
                option_dtos.append(CartItemOptionDto(
                    uuid=option.uuid,
                    menu_option_id=option.menu_option_id,
                    menu_option_name=option.menu_option_name,  # DB에 저장된 이름 사용
                    price=option.price,
                    created_at=option.created_at,
                    updated_at=option.updated_at,
                ))

            # 저장된 메뉴 정보를 평면화하여 직접 포함
            item_dto = CartItemDto(
                uuid=item.uuid,
                menu_id=item.menu_id,
                menu_name=item.menu_name,
                menu_description=item.menu_description,
                menu_image_url=item.menu_image_url,
                quantity=item.quantity,
                price=item.price,
                created_at=item.created_at,
                updated_at=item.updated_at,
                options=option_dtos if option_dtos else None
            )
            items.append(item_dto)

        cart_dto = CartDto(
            uuid=cart.uuid,
            user_id=cart.user_id,
            restaurant_id=cart.restaurant_id,
            created_at=cart.created_at,
            updated_at=cart.updated_at,
            items=items if items else None
        )

        response = GetCartResponseDto(cart=cart_dto)
        return create_success_result(response)
        
    except AuthenticationException as e:
        return create_error_result(e)
    except Exception as e:
        return create_unknown_error_result(e)
    finally:
        session.close()
