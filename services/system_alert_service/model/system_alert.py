from sqlalchemy import (
    Column, String, Uuid, DateTime, Boolean, Enum as PgEnum, func
)
from utility.db import Base
from utility.enums import AlertLevel

class SystemAlert(Base):
    __tablename__ = "system_alert"
    __table_args__ = {"schema": "system_alert_service"}

    uuid = Column(Uuid, primary_key=True)
    source = Column(String, nullable=False)  # 예: "order_service"
    level = Column(PgEnum(AlertLevel, name="alert_level"), nullable=False)
    message = Column(String, nullable=False)
    metadata = Column(String)  # JSON string 형태로 부가정보
    notified = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
