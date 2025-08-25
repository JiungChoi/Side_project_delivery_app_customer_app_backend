from sqlalchemy import Column, String, Boolean, DateTime, func
from utility.db import Base

class Address(Base):
    __tablename__ = "address"
    __table_args__ = {"schema": "order_service"}

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    address = Column(String, nullable=False)
    detail_address = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    is_default = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False) 