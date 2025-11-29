# app/routers/cart.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests

from app.database import (
    get_db,
    Cart as CartModel,
    CartItem as CartItemModel,
    Product as ProductModel,
    User as UserModel,
)
from app.schemas import Cart, CartItemBase
from app.logging_config import logger

router = APIRouter(tags=["Cart"])

FAKESTORE_BASE_URL = "https://fakestoreapi.com"


def _get_or_create_cart_for_user(db: Session, user_id: int) -> CartModel:
    """Return an existing cart for a user or create a new one."""
    logger.info(f"Getting or creating cart for user {user_id}")

    cart = db.query(CartModel).filter(CartModel.user_id == user_id).first()
    if cart:
        logger.info(f"Found existing cart {cart.id} for user {user_id}")
        return cart

    # Make sure the user exists
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        logger.warning(f"Tried to create cart for non-existent user {user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    cart = CartModel(user_id=user_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    logger.info(f"Created new cart {cart.id} for user {user_id}")
    return cart


def _ensure_product_in_db(db: Session, product_id: int) -> ProductModel:
    """
    Ensure a Product row exists locally for the given FakeStore product id.
    If not, fetch from FakeStore API and insert.
    """
    logger.info(f"Ensuring product {product_id} exists in local DB")

    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product:
        logger.info(f"Product {product_id} already exists locally")
        return product

    # Fetch from FakeStore
    try:
        resp = requests.get(f"{FAKESTORE_BASE_URL}/products/{product_id}", timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch product {product_id} from FakeStore: {e}")
        raise HTTPException(
            status_code=502,
            detail="Could not fetch product details from FakeStore API",
        )

    data = resp.json()
    product = ProductModel(
        id=data["id"],
        title=data.get("title", f"Product {product_id}"),
        description=data.get("description"),
        price=float(data.get("price", 0.0)),
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    logger.info(f"Stored product {product_id} locally")
    return product


@router.post("/{user_id}", response_model=Cart)
def create_or_get_cart(user_id: int, db: Session = Depends(get_db)):
    """
    Create a cart for a user if none exists, otherwise return the existing one.
    """
    logger.info(f"Request to create/get cart for user {user_id}")
    cart = _get_or_create_cart_for_user(db, user_id)
    return cart


@router.get("/{cart_id}", response_model=Cart)
def get_cart(cart_id: int, db: Session = Depends(get_db)):
    """
    Fetch a cart and its items by id.
    """
    logger.info(f"Retrieving cart {cart_id}")
    cart = db.query(CartModel).filter(CartModel.id == cart_id).first()
    if not cart:
        logger.warning(f"Cart {cart_id} not found")
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.post("/{cart_id}/items", response_model=Cart)
def add_item_to_cart(
    cart_id: int,
    item: CartItemBase,
    db: Session = Depends(get_db),
):
    """
    Add or update a cart item.
    Body: { "product_id": int, "quantity": int }
    """
    logger.info(
        f"Adding product {item.product_id} (qty {item.quantity}) to cart {cart_id}"
    )

    cart = db.query(CartModel).filter(CartModel.id == cart_id).first()
    if not cart:
        logger.warning(f"Attempt to add item to non-existent cart {cart_id}")
        raise HTTPException(status_code=404, detail="Cart not found")

    # Ensure the product exists locally, backed by FakeStore API
    _ensure_product_in_db(db, item.product_id)

    cart_item = (
        db.query(CartItemModel)
        .filter(
            CartItemModel.cart_id == cart_id,
            CartItemModel.product_id == item.product_id,
        )
        .first()
    )

    if cart_item:
        cart_item.quantity += item.quantity
        logger.info(
            f"Updated cart_item {cart_item.id}: product {item.product_id}, "
            f"new quantity {cart_item.quantity}"
        )
    else:
        cart_item = CartItemModel(
            cart_id=cart_id,
            product_id=item.product_id,
            quantity=item.quantity,
        )
        db.add(cart_item)
        logger.info(
            f"Created new cart_item for cart {cart_id}, "
            f"product {item.product_id}, quantity {item.quantity}"
        )

    db.commit()
    db.refresh(cart)
    return cart
