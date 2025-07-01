import datetime
from typing import List
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="cart", uselist=False)
    cart_items: Mapped[List["CartItem"]] = relationship(
        "CartItem", back_populates="cart", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Cart(id={self.id}, user_id={self.user_id})>"


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    added_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow, nullable=False)

    cart: Mapped["Cart"] = relationship("Cart", back_populates="cart_items")
    movie: Mapped["Movie"] = relationship("Movie")

    __table_args__ = (UniqueConstraint("cart_id", "movie_id", name="unique_cart_movie"),)

    def __repr__(self) -> str:
        return f"<CartItem(id={self.id}, cart_id={self.cart_id}, movie_id={self.movie_id})>"
