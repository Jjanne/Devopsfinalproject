from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import httpx

from .. import models, schemas
from ..database import get_session

router = APIRouter()

FAKESTORE_BASE_URL = "https://fakestoreapi.com"

# Category metadata your frontend can use
CATEGORIES = [
    {"id": "electronics", "name": "Electronics"},
    {"id": "jewelery", "name": "Jewelery"},
    {"id": "mens_clothing", "name": "Men's clothing"},
    {"id": "womens_clothing", "name": "Women's clothing"},
]

# Map the ids used by your frontend/backend to FakeStore category names
CATEGORY_ID_TO_EXTERNAL = {
    "electronics": "electronics",
    "jewelery": "jewelery",
    "mens_clothing": "men's clothing",
    "womens_clothing": "women's clothing",
}


@router.get("/", response_model=List[schemas.ProductRead])
def list_products(
    q: Optional[str] = Query(default=None),
    db: Session = Depends(get_session),
):
    """Return products, optionally filtered by title substring."""
    query = db.query(models.Product)
    if q:
        query = query.filter(models.Product.title.ilike(f"%{q}%"))
    return query.order_by(models.Product.id.desc()).all()


@router.post("/", response_model=schemas.ProductRead, status_code=201)
def create_product(
    data: schemas.ProductCreate,
    db: Session = Depends(get_session),
):
    product = models.Product(**data.dict())
    db.add(product)
    db.flush()
    return product


# ---------- NEW ENDPOINTS FOR FRONTEND / FAKESTORE ----------

@router.get("/categories")
async def list_categories():
    """
    Return the list of product categories.

    Shape expected by the frontend:
      [
        {"id": "electronics", "name": "Electronics"},
        ...
      ]
    """
    return CATEGORIES


@router.get("/category/{category_id}")
async def get_products_for_category(category_id: str):
    """
    Fetch products for a given category from FakeStore API and
    return them via your backend.

    Response shape:
      {
        "category": "<category_id>",
        "products": [...]
      }
    """
    external_name = CATEGORY_ID_TO_EXTERNAL.get(category_id)
    if external_name is None:
        raise HTTPException(status_code=404, detail="Unknown category")

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(
                f"{FAKESTORE_BASE_URL}/products/category/{external_name}"
            )
            resp.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(
                status_code=502,
                detail="Failed to fetch products from FakeStore API",
            )

    products = resp.json()
    return {"category": category_id, "products": products}


# -------------------------------------------------------------


@router.get("/{product_id}", response_model=schemas.ProductRead)
def get_product(
    product_id: int,
    db: Session = Depends(get_session),
):
    product = db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
