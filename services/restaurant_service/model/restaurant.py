from sqlalchemy import (
    Column, String, Integer, ForeignKey, Uuid, DateTime, Boolean, CheckConstraint, func
)
from sqlalchemy.orm import relationship
from utility.db import Base
from utility.enums import RestaurantImageType


class Restaurant(Base):
    __tablename__ = "restaurant"
    __table_args__ = {"schema": "restaurant_service"}

    uuid = Column(Uuid, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)
    rating = Column(Integer, default=0)
    review_count = Column(Integer, default=0)
    min_order_amount = Column(Integer, default=0)
    delivery_fee = Column(Integer, default=0)
    delivery_time = Column(Integer, default=0)
    operating_hours = Column(String)
    tags = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    images = relationship("RestaurantImage", backref="restaurant", lazy="joined")


class RestaurantImage(Base):
    __tablename__ = "restaurant_image"
    __table_args__ = (
        CheckConstraint(
            "image_type IN (" + ",".join(f"'{t.value}'" for t in RestaurantImageType) + ")",
            name="check_image_type"
        ),
        {"schema": "restaurant_service"},
    )

    uuid = Column(Uuid, primary_key=True)
    restaurant_id = Column(Uuid, ForeignKey("restaurant_service.restaurant.uuid"), nullable=False)
    image_type = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    ordering = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
