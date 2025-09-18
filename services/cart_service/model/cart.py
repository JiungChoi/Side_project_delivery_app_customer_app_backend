from sqlalchemy import (
    Column, String, Integer, Uuid, ForeignKey, DateTime, Boolean, func
)
from sqlalchemy.orm import relationship
from utility.db import Base


class Cart(Base):
    __tablename__ = "cart"
    __table_args__ = {"schema": "cart_service"}

    uuid = Column(Uuid, primary_key=True)
    user_id = Column(Uuid, nullable=False)
    restaurant_id = Column(Uuid, nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    items = relationship("CartItem", backref="cart", lazy="select")


class CartItem(Base):
    __tablename__ = "cart_item"
    __table_args__ = {"schema": "cart_service"}

    uuid = Column(Uuid, primary_key=True)
    cart_id = Column(Uuid, ForeignKey("cart_service.cart.uuid"), nullable=False)
    menu_id = Column(Uuid, nullable=False)
    menu_name = Column(String, nullable=False)  # 메뉴 이름 저장
    menu_description = Column(String, nullable=True)  # 메뉴 설명
    menu_image_url = Column(String, nullable=True)    # 메뉴 이미지 URL
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    options = relationship("CartItemOption", backref="cart_item", lazy="select")


class CartItemOption(Base):
    __tablename__ = "cart_item_option"
    __table_args__ = {"schema": "cart_service"}

    uuid = Column(Uuid, primary_key=True)
    cart_item_id = Column(Uuid, ForeignKey("cart_service.cart_item.uuid"), nullable=False)
    # Frontend currently sends option name; menu_option_id is optional until menu-service integration
    menu_option_id = Column(Uuid, nullable=True)
    menu_option_name = Column(String, nullable=True)
    price = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
