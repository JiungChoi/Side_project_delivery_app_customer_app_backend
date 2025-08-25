from sqlalchemy import (
    Column, String, Integer, ForeignKey, Uuid, DateTime, Boolean, CheckConstraint, func
)
from sqlalchemy.orm import relationship
from utility.db import Base
from utility.enums import OrderStatus


class Order(Base):
    __tablename__ = "order"
    __table_args__ = (
        CheckConstraint(
            "status IN (" + ",".join(f"'{s.value}'" for s in OrderStatus) + ")",
            name="check_order_status"
        ),
        {"schema": "order_service"},
    )

    uuid = Column(Uuid, primary_key=True)
    user_id = Column(Uuid, nullable=False)
    address_id = Column(Uuid, nullable=False)
    total_price = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default=OrderStatus.PENDING.value)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    order_items = relationship("OrderItem", backref="order", lazy="joined")


class OrderItem(Base):
    __tablename__ = "order_item"
    __table_args__ = {"schema": "order_service"}

    uuid = Column(Uuid, primary_key=True)
    order_id = Column(Uuid, ForeignKey("order_service.order.uuid"), nullable=False)
    menu_id = Column(Uuid, nullable=False)
    restaurant_id = Column(Uuid, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    order_item_options = relationship("OrderItemOption", backref="order_item", lazy="joined")


class OrderItemOption(Base):
    __tablename__ = "order_item_option"
    __table_args__ = {"schema": "order_service"}

    uuid = Column(Uuid, primary_key=True)
    order_item_id = Column(Uuid, ForeignKey("order_service.order_item.uuid"), nullable=False)
    menu_option_id = Column(Uuid, nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
