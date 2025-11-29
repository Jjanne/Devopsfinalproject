# app/routers/products.py
from fastapi import APIRouter, HTTPException
from typing import List
import urllib.parse

router = APIRouter()

# In-memory product catalog that mimics the old FakeStore data shape.
PRODUCTS = [
    # ── Electronics ─────────────────────────────────────────────
    {
        "id": 1,
        "title": "Sports Watch",
        "price": 129.00,
        "category": "electronics",
        "description": "GPS sports watch with HR tracking.",
        "image": "https://images.pexels.com/photos/277583/pexels-photo-277583.jpeg",
    },
    {
        "id": 2,
        "title": "Wireless Sport Earbuds",
        "price": 79.99,
        "category": "electronics",
        "description": "Sweat-resistant earbuds with secure fit for training.",
        "image": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg",
    },
    {
        "id": 3,
        "title": "Bike Computer",
        "price": 149.50,
        "category": "electronics",
        "description": "Cycling computer with GPS and route tracking.",
        "image": "https://images.pexels.com/photos/276517/pexels-photo-276517.jpeg",
    },

    # ── Men's clothing ──────────────────────────────────────────
    {
        "id": 4,
        "title": "Classic Men's T-Shirt",
        "price": 19.99,
        "category": "men's clothing",
        "description": "Soft cotton tee for everyday training or casual wear.",
        "image": "https://images.pexels.com/photos/769732/pexels-photo-769732.jpeg",
    },
    {
        "id": 5,
        "title": "Men's Running Shorts",
        "price": 29.50,
        "category": "men's clothing",
        "description": "Lightweight shorts with inner brief and key pocket.",
        "image": "https://images.pexels.com/photos/936094/pexels-photo-936094.jpeg",
    },
    {
        "id": 6,
        "title": "Men's Lightweight Hoodie",
        "price": 49.90,
        "category": "men's clothing",
        "description": "Light hoodie for warm-ups and easy days.",
        "image": "https://images.pexels.com/photos/769746/pexels-photo-769746.jpeg",
    },

    # ── Women's clothing ────────────────────────────────────────
    {
        "id": 7,
        "title": "Women's Performance Leggings",
        "price": 39.95,
        "category": "women's clothing",
        "description": "High-waist leggings with moisture-wicking fabric.",
        "image": "https://images.pexels.com/photos/3823039/pexels-photo-3823039.jpeg",
    },
    {
        "id": 8,
        "title": "Women's Running Top",
        "price": 34.90,
        "category": "women's clothing",
        "description": "Breathable long-sleeve top for cooler runs.",
        "image": "https://images.pexels.com/photos/3760852/pexels-photo-3760852.jpeg",
    },
    {
        "id": 9,
        "title": "Women's Windbreaker",
        "price": 59.00,
        "category": "women's clothing",
        "description": "Packable windbreaker for windy sessions.",
        "image": "https://images.pexels.com/photos/7671166/pexels-photo-7671166.jpeg",
    },

    # ── Shoes ───────────────────────────────────────────────────
    {
        "id": 10,
        "title": "Neutral Running Shoes",
        "price": 89.50,
        "category": "shoes",
        "description": "Daily trainer for neutral runners.",
        "image": "https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg",
    },
    {
        "id": 11,
        "title": "Racing Flats",
        "price": 119.00,
        "category": "shoes",
        "description": "Lightweight shoes for tempo runs and race day.",
        "image": "https://images.pexels.com/photos/1598505/pexels-photo-1598505.jpeg",
    },
    {
        "id": 12,
        "title": "Trail Running Shoes",
        "price": 104.90,
        "category": "shoes",
        "description": "Aggressive outsole for technical trails.",
        "image": "https://images.pexels.com/photos/322207/pexels-photo-322207.jpeg",
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
