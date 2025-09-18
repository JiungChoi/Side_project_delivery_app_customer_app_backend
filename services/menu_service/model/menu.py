from sqlalchemy import (
    Column, String, Integer, ForeignKey, Uuid, DateTime,
    Boolean, func, Float
)
from sqlalchemy.orm import relationship
from utility.db import Base


class MenuCategory(Base):
    __tablename__ = "menu_category"
    __table_args__ = {"schema": "menu_service"}

    uuid = Column(Uuid, primary_key=True)
    restaurant_id = Column(Uuid, nullable=False)
    name = Column(String, nullable=False)
    ordering = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    menus = relationship("Menu", backref="category", lazy="joined")


class Menu(Base):
    __tablename__ = "menu"
    __table_args__ = {"schema": "menu_service"}

    uuid = Column(Uuid, primary_key=True)
    category_id = Column(Uuid, ForeignKey("menu_service.menu_category.uuid"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    image_url = Column(String)
    is_sold_out = Column(Boolean, default=False, nullable=False)
    ordering = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    option_groups = relationship("MenuOptionGroup", backref="menu", lazy="joined")


class MenuOptionGroup(Base):
    __tablename__ = "menu_option_group"
    __table_args__ = {"schema": "menu_service"}

    uuid = Column(Uuid, primary_key=True)
    menu_id = Column(Uuid, ForeignKey("menu_service.menu.uuid"), nullable=False)
    name = Column(String, nullable=False)
    is_required = Column(Boolean, default=False, nullable=False)
    max_select = Column(Integer, default=1)
    ordering = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    options = relationship("MenuOption", backref="group", lazy="joined")


class MenuOption(Base):
    __tablename__ = "menu_option"
    __table_args__ = {"schema": "menu_service"}

    uuid = Column(Uuid, primary_key=True)
    group_id = Column(Uuid, ForeignKey("menu_service.menu_option_group.uuid"), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    ordering = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)


class MenuReview(Base):
    __tablename__ = "menu_review"
    __table_args__ = {"schema": "menu_service"}

    uuid = Column(Uuid, primary_key=True)
    menu_id = Column(Uuid, ForeignKey("menu_service.menu.uuid"), nullable=False)
    customer_id = Column(Uuid, nullable=False)  # Reference to customer
    rating = Column(Float, nullable=False)  # 1.0 to 5.0
    comment = Column(String)
    
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
