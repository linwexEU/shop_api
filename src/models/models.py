import uuid
from datetime import datetime, timezone

from sqlalchemy import TIMESTAMP, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db import Base
from src.models.enums import (ActEnum, CategoriesEnum, NotificationsStateEnum,
                              NotificationsTypeEnum, OrdersStateEnum,
                              UsersRoleEnum)


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=True, unique=True)
    role: Mapped[UsersRoleEnum] = mapped_column(
        Enum(UsersRoleEnum), default=UsersRoleEnum.Customer
    )

    organizations = relationship("Organizations", back_populates="owner")


class Organizations(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)

    business_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    create_utc: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(timezone.utc)
    )
    delete_utc: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner = relationship("Users", back_populates="organizations")


class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    category: Mapped[CategoriesEnum] = mapped_column(
        Enum(CategoriesEnum), nullable=False
    )
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=False)

    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))

    rates = relationship("ProductRates", back_populates="products")


class OrganizationRates(Base):
    __tablename__ = "organization_rates"

    id: Mapped[int] = mapped_column(primary_key=True)

    stars: Mapped[int] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))


class OrganizationRatesInteraction(Base):
    __tablename__ = "organization_rates_interaction"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))


class ProductRateReplies(Base):
    __tablename__ = "product_rate_replies"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)

    rate_id: Mapped[int] = mapped_column(ForeignKey("product_rates.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class ProductRates(Base):
    __tablename__ = "product_rates"

    id: Mapped[int] = mapped_column(primary_key=True)

    stars: Mapped[int] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(nullable=True)
    likes: Mapped[int] = mapped_column(nullable=True, default=0)
    dislikes: Mapped[int] = mapped_column(nullable=True, default=0)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    products = relationship("Products", back_populates="rates")


class ProductRatesInteraction(Base):
    __tablename__ = "product_rates_interaction"

    id: Mapped[int] = mapped_column(primary_key=True)

    act: Mapped[ActEnum] = mapped_column(nullable=False, default=ActEnum.Like)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    rate_id: Mapped[int] = mapped_column(ForeignKey("product_rates.id"))


class Baskets(Base):
    __tablename__ = "baskets"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(default=1)

    product = relationship("Products")


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    uuid: Mapped[str] = mapped_column(nullable=False)
    total_price: Mapped[int] = mapped_column(nullable=True)
    state: Mapped[OrdersStateEnum] = mapped_column(
        Enum(OrdersStateEnum), default=OrdersStateEnum.Preparing
    )
    create_utc: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(timezone.utc)
    )
    delete_utc: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class OrderItems(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    quantity: Mapped[int] = mapped_column(nullable=False)

    order = relationship("Orders")
    product = relationship("Products")


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[CategoriesEnum] = mapped_column(Enum(CategoriesEnum), nullable=False)


class Notifications(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)

    state: Mapped[NotificationsStateEnum] = mapped_column(
        default=NotificationsStateEnum.New
    )
    type: Mapped[NotificationsTypeEnum] = mapped_column(nullable=False)
    create_utc: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(timezone.utc)
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
