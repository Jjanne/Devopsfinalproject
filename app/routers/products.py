# app/routers/products.py
from fastapi import APIRouter, HTTPException
from typing import List
import urllib.parse

router = APIRouter()

# Simple in-memory product catalog so we don't depend on any external API.
PRODUCTS = [
    {
        "id": 1,
        "title": "Classic Men's T-Shirt",
        "price": 19.99,
        "category": "men's clothing",
        "description": "Soft cotton tee for everyday training or casual wear.",
        "image": "https://picsum.photos/seed/mens1/400/400",
    },
    {
        "id": 2,
        "title": "Women's Performance Leggings",
        "price": 39.95,
        "category": "women's clothing",
        "description": "High-waist leggings with moisture-wicking fabric.",
        "image": "https://picsum.photos/seed/womens1/400/400",
    },
    {
        "id": 3,
        "title": "Running Shoes",
        "price": 89.5,
        "category": "shoes",
        "description": "Neutral running shoes for daily training.",
        "image": "https://picsum.photos/seed/shoes1/400/400",
    },
    {
        "id": 4,
        "title": "Sports Watch",
        "price": 129.0,
        "category": "electronics",
        "description": "GPS sports watch with HR tracking.",
        "image": "https://picsum.photos/seed/electronics1/400/400",
    },
]


def _slugify_category(name: str) -> str:
    return (
        name.lower()
        .replace("'", "")
        .replace("+", " ")
        .replace("&", "and")
        .replace(" ", "_")
    )


@router.get("/categories")
def list_categories():
    """Return the list of unique product categories."""
    categories = sorted({p["category"] for p in PRODUCTS})
    return [
        {"id": _slugify_category(c), "name": c}
        for c in categories
    ]


@router.get("/category/{category}")
def get_products_by_category(category: str) -> List[dict]:
    """Return products for a given category."""
    decoded = urllib.parse.unquote(category)
    items = [p for p in PRODUCTS if p["category"].lower() == decoded.lower()]

    if not items:
        raise HTTPException(status_code=404, detail="No products in this category")

    return items
