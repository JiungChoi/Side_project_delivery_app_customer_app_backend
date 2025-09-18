from schemas.request.add_cart_item import AddCartItemRequestDto
from schemas.response.add_cart_item import AddCartItemResponseDto
from schemas.response.get_cart import CartItemDto, CartItemOptionDto
from schemas.common import (
    create_success_result,
    create_error_result,
    create_unknown_error_result,
)
from model.exception import (
    AuthenticationException,
    CartValidationException,
    RestaurantMismatchException,
    CartItemValidationException,
)
from model.cart import Cart, CartItem, CartItemOption
from utility.db import get_db
from uuid import uuid4, UUID


async def try_add_cart_item(request: AddCartItemRequestDto):
    print(f"[CART_SERVICE] Starting try_add_cart_item with request: {request}")

    # Create database session
    db_generator = get_db()
    session = next(db_generator)

    try:
        if not request.user_id:
            raise AuthenticationException("사용자 ID가 필요합니다.")
        if request.quantity <= 0:
            raise CartItemValidationException("수량은 1 이상이어야 합니다.")
        if request.price < 0:
            raise CartItemValidationException("가격은 0 이상이어야 합니다.")

        # Convert string IDs to UUID
        print(f"[CART_SERVICE] Converting UUIDs: user_id={request.user_id}, restaurant_id={request.restaurant_id}, menu_id={request.menu_id}")
        try:
            user_uuid = UUID(request.user_id) if isinstance(request.user_id, str) else request.user_id
            restaurant_uuid = UUID(request.restaurant_id) if isinstance(request.restaurant_id, str) else request.restaurant_id
            menu_uuid = UUID(request.menu_id) if isinstance(request.menu_id, str) else request.menu_id
            print(f"[CART_SERVICE] UUID conversion successful")
        except ValueError as e:
            print(f"[CART_SERVICE] UUID conversion failed: {e}")
            raise CartItemValidationException(f"잘못된 UUID 형식: {e}")

        # Find or create cart
        print(f"[CART_SERVICE] Searching for existing cart for user: {user_uuid}")
        existing_cart = (
            session.query(Cart)
            .filter(Cart.user_id == user_uuid, Cart.is_deleted == False)
            .first()
        )
        print(f"[CART_SERVICE] Existing cart found: {existing_cart is not None}")
        if existing_cart and existing_cart.restaurant_id != restaurant_uuid:
            raise RestaurantMismatchException("다른 매장의 메뉴는 장바구니에 추가할 수 없습니다.")

        if not existing_cart:
            print(f"[CART_SERVICE] Creating new cart")
            cart = Cart(uuid=uuid4(), user_id=user_uuid, restaurant_id=restaurant_uuid)
            session.add(cart)
            session.flush()
            print(f"[CART_SERVICE] New cart created with ID: {cart.uuid}")
        else:
            print(f"[CART_SERVICE] Using existing cart with ID: {existing_cart.uuid}")
            cart = existing_cart

        # Create cart item with menu information
        print(f"[CART_SERVICE] Creating cart item")
        cart_item = CartItem(
            uuid=uuid4(),
            cart_id=cart.uuid,
            menu_id=menu_uuid,
            menu_name=request.menu_name,
            quantity=request.quantity,
            price=request.price,
        )
        session.add(cart_item)
        session.flush()
        print(f"[CART_SERVICE] Cart item created with ID: {cart_item.uuid}")

        # Create cart item options if provided
        if request.options:
            print(f"[CART_SERVICE] Creating {len(request.options)} options")
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
            print(f"[CART_SERVICE] Options created")

        print(f"[CART_SERVICE] Committing transaction")
        session.commit()
        print(f"[CART_SERVICE] Transaction committed successfully")

        # Build response DTO
        options = (
            session.query(CartItemOption)
            .filter(CartItemOption.cart_item_id == cart_item.uuid, CartItemOption.is_deleted == False)
            .all()
        )
        option_dtos = [
            CartItemOptionDto(
                uuid=o.uuid,
                menu_option_id=o.menu_option_id,
                menu_option_name=o.menu_option_name,
                price=o.price,
                created_at=o.created_at,
                updated_at=o.updated_at,
            )
            for o in options
        ]

        item_dto = CartItemDto(
            uuid=cart_item.uuid,
            menu_id=cart_item.menu_id,
            menu_name=cart_item.menu_name,
            quantity=cart_item.quantity,
            price=cart_item.price,
            created_at=cart_item.created_at,
            updated_at=cart_item.updated_at,
            options=option_dtos if option_dtos else None,
        )

        response = AddCartItemResponseDto(cart_item=item_dto)
        return create_success_result(response)

    except (AuthenticationException, CartValidationException, RestaurantMismatchException, CartItemValidationException) as e:
        session.rollback()
        return create_error_result(e)
    except Exception as e:
        print(f"[CART_SERVICE] Exception occurred: {e}")
        session.rollback()
        return create_unknown_error_result(e)
    finally:
        print(f"[CART_SERVICE] Closing database session")
        session.close()
        # Close the generator
        try:
            next(db_generator)
        except StopIteration:
            pass

