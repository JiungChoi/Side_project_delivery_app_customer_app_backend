from sqlalchemy import Column, String, Boolean, DateTime, func
from utility.db import Base


class Restaurant(Base):
    __tablename__ = "restaurant"
    __table_args__ = {"schema": "order_service"}

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False) 