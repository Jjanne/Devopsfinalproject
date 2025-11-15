from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_session

router = APIRouter()

@router.get("/", response_model=List[schemas.ProductRead])
def list_products(q: Optional[str] = Query(default=None), db: Session = Depends(get_session)):
    """Return products, optionally filtered by title substring."""
    query = db.query(models.Product)
    if q:
        query = query.filter(models.Product.title.ilike(f"%{q}%"))
    return query.order_by(models.Product.id.desc()).all()

@router.post("/", response_model=schemas.ProductRead, status_code=201)
def create_product(data: schemas.ProductCreate, db: Session = Depends(get_session)):
    product = models.Product(**data.dict())
    db.add(product)
    db.flush()
    return product

@router.get("/{product_id}", response_model=schemas.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_session)):
    product = db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
