from sqlalchemy import Column, String, Integer, Boolean, DateTime, func
from utility.db import Base

class Menu(Base):
    __tablename__ = "menu"
    __table_args__ = {"schema": "order_service"}

    id = Column(String, primary_key=True)
    restaurant_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False) 