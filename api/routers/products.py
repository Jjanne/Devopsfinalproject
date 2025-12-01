# app/routers/products.py
from fastapi import APIRouter, HTTPException

from app.services.external_products import get_categories, get_products_by_category

router = APIRouter()


@router.get("/categories")
def list_categories():
    try:
        return get_categories()
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to fetch categories")


@router.get("/category/{category}")
def list_products(category: str):
    try:
        return get_products_by_category(category)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to fetch products")
