from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum
from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, String, DECIMAL, DateTime, func, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database.base import Base

if TYPE_CHECKING:
    from src.database.models.accounts import User
    from src.database.models.payments import Payment, PaymentItem
    from src.database.models.movies import Movie


class OrderStatus(PyEnum):
    PENDING = "pending"
    PAID = "paid"
    CANCELED = "canceled"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(
            OrderStatus,
            name="orderstatus_enum",
            values_callable=lambda x: [member.value for member in x],
            native_enum=False
        ),
        default=OrderStatus.PENDING,
        nullable=False
    )
    total_amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order")
    payments: Mapped[List["Payment"]] = relationship(
        "Payment", back_populates="order", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Order(id={self.id}, user_id={self.user_id}, "
            f"status={self.status}, total_amount={self.total_amount})>"
        )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    price_at_order: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    order: Mapped["Order"] = relationship("Order", back_populates="items")
    movie: Mapped["Movie"] = relationship("Movie", back_populates="order_items")
    payment_items: Mapped[List["PaymentItem"]] = relationship("PaymentItem", back_populates="order_item")

    def __repr__(self):
        return (
            f"<OrderItem(id={self.id}, order_id={self.order_id}, "
            f"movie_id={self.movie_id}, price_at_order={self.price_at_order})>"
        )
