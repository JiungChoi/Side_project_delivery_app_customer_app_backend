from sqlalchemy import (
    Column, String, Integer, ForeignKey, Uuid, DateTime,
    Boolean, CheckConstraint, func
)
from sqlalchemy.orm import relationship
from utility.db import Base
from utility.enums import PaymentMethod, PaymentStatus


class Payment(Base):
    __tablename__ = "payment"
    __table_args__ = (
        CheckConstraint(
            "method IN (" + ",".join(f"'{m.value}'" for m in PaymentMethod) + ")",
            name="check_payment_method"
        ),
        CheckConstraint(
            "status IN (" + ",".join(f"'{s.value}'" for s in PaymentStatus) + ")",
            name="check_payment_status"
        ),
        {"schema": "payment_service"},
    )

    uuid = Column(Uuid, primary_key=True)
    order_id = Column(Uuid, nullable=False)
    user_id = Column(Uuid, nullable=False)
    amount = Column(Integer, nullable=False)
    method = Column(String, nullable=False)
    status = Column(String, nullable=False, default=PaymentStatus.PENDING.value)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    failure_reason = Column(String)
    pg_transaction_id = Column(String)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    refunds = relationship("Refund", backref="payment", lazy="joined")


class Refund(Base):
    __tablename__ = "refund"
    __table_args__ = {"schema": "payment_service"}

    uuid = Column(Uuid, primary_key=True)
    payment_id = Column(Uuid, ForeignKey("payment_service.payment.uuid"), nullable=False)
    amount = Column(Integer, nullable=False)
    reason = Column(String)
    refunded_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
