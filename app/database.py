# app/database.py
import os
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# -------------------------
# Database configuration
# -------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # e.g. PostgreSQL on Azure
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
else:
    # Local sqlite fallback for local dev/tests
    engine = create_engine(
        "sqlite:///./data.db",
        connect_args={"check_same_thread": False},
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    FastAPI dependency to get a DB session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# SQLAlchemy models
# -------------------------


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)

    carts = relationship("Cart", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")


class Product(Base):
    """
    Optional local product table.

    Even though products are fetched from FakeStore API,
    we keep this table so CartItem can reference a product_id.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="carts")
    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan",
    )


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total = Column(Float, nullable=False)

    user = relationship("User", back_populates="orders")
