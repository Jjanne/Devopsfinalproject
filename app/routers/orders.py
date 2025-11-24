# app/routers/orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import (
    get_db,
    Order as OrderModel,
    Cart as CartModel,
    CartItem as CartItemModel,
    User as UserModel,
)
from app.schemas import Order
from app.logging_config import logger

router = APIRouter(tags=["Orders"])


@router.post("/{user_id}", response_model=Order)
def create_order(user_id: int, db: Session = Depends(get_db)):
    """
    Create an order for a user. The order total is computed based on their cart.
    """
    logger.info(f"Creating order for user {user_id}")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        logger.warning(f"Order creation failed: user {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")

    cart = db.query(CartModel).filter(CartModel.user_id == user_id).first()
    if not cart or not cart.items:
        logger.warning(f"Order creation failed: cart for user {user_id} is empty")
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Calculate total price
    total = sum(item.product.price * item.quantity for item in cart.items)
    logger.info(f"Calculated order total {total} for user {user_id}")

    # Create the order
    order = OrderModel(user_id=user_id, total=total)
    db.add(order)

    # Clear cart after ordering
    for item in list(cart.items):
        db.delete(item)

    db.commit()
    db.refresh(order)

    logger.info(f"Order {order.id} created for user {user_id}")
    return order


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching order {order_id}")

    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        logger.warning(f"Order {order_id} not found")
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/user/{user_id}", response_model=list[Order])
def get_orders_for_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Listing orders for user {user_id}")
    return db.query(OrderModel).filter(OrderModel.user_id == user_id).all()
