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

    items = relationship("CartItem", backref="cart", lazy="joined")


class CartItem(Base):
    __tablename__ = "cart_item"
    __table_args__ = {"schema": "cart_service"}

    uuid = Column(Uuid, primary_key=True)
    cart_id = Column(Uuid, ForeignKey("cart_service.cart.uuid"), nullable=False)
    menu_id = Column(Uuid, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    options = relationship("CartItemOption", backref="cart_item", lazy="joined")


class CartItemOption(Base):
    __tablename__ = "cart_item_option"
    __table_args__ = {"schema": "cart_service"}

    uuid = Column(Uuid, primary_key=True)
    cart_item_id = Column(Uuid, ForeignKey("cart_service.cart_item.uuid"), nullable=False)
    menu_option_id = Column(Uuid, nullable=False)
    price = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)