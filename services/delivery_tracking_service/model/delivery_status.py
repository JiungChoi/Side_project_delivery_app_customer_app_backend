from sqlalchemy import (
    Column, String, Float, Uuid, DateTime, Boolean, func
)
from utility.db import Base


class DeliveryStatus(Base):
    __tablename__ = "delivery_status"
    __table_args__ = {"schema": "delivery_tracking_service"}

    uuid = Column(Uuid, primary_key=True)
    order_id = Column(Uuid, nullable=False)
    courier_id = Column(Uuid, nullable=False)  # 라이더 또는 로봇 ID
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    heading = Column(Float)  # 방향 (0~360도)
    speed = Column(Float)  # m/s 또는 km/h
    is_delivered = Column(Boolean, default=False, nullable=False)
    last_updated = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)