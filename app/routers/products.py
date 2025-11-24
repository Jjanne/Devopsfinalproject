# app/routers/products.py
from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()  # <- no prefix

FAKESTORE_BASE_URL = "https://fakestoreapi.com"


@router.get("/categories")
def list_categories():
    """
    Returns the list of categories from the FakeStore API.
    """
    try:
        resp = requests.get(f"{FAKESTORE_BASE_URL}/products/categories", timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Failed to fetch categories")

    return resp.json()


@router.get("/category/{category}")
def get_products_by_category(category: str):
    """
    Returns products for a given category from FakeStore API.
    """
    try:
        resp = requests.get(
            f"{FAKESTORE_BASE_URL}/products/category/{category}", timeout=10
        )
        resp.raise_for_status()
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Failed to fetch products")

    return resp.json()
