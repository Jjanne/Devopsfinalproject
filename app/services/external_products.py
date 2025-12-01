# app/services/external_products.py
from typing import List, Dict
import os

import requests

FAKESTORE_BASE_URL = os.getenv("FAKESTORE_BASE_URL", "https://fakestoreapi.com")

# ------------------------------------------------------------------
# Local fallback catalogue (used if FakeStore is unreachable)
# ------------------------------------------------------------------
FALLBACK_PRODUCTS: List[Dict] = [
    # ELECTRONICS
    {
        "id": 1,
        "title": "Sports Watch",
        "price": 129.0,
        "category": "electronics",
        "description": "GPS sports watch with HR tracking.",
        "image": "https://images.pexels.com/photos/277319/pexels-photo-277319.jpeg",
    },
    {
        "id": 2,
        "title": "Wireless Earbuds",
        "price": 89.0,
        "category": "electronics",
        "description": "True wireless earbuds with noise isolation.",
        "image": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg",
    },
    {
        "id": 3,
        "title": "Action Camera",
        "price": 199.0,
        "category": "electronics",
        "description": "4K action camera for your bike rides and races.",
        "image": "https://images.pexels.com/photos/1683147/pexels-photo-1683147.jpeg",
    },

    # MEN'S CLOTHING
    {
        "id": 11,
        "title": "Men's Running T-Shirt",
        "price": 24.99,
        "category": "men's clothing",
        "description": "Breathable running tee for everyday training.",
        "image": "https://images.pexels.com/photos/1401797/pexels-photo-1401797.jpeg",
    },
    {
        "id": 12,
        "title": "Men's Training Shorts",
        "price": 29.99,
        "category": "men's clothing",
        "description": "Lightweight shorts with inner liner.",
        "image": "https://images.pexels.com/photos/1552249/pexels-photo-1552249.jpeg",
    },

    # WOMEN'S CLOTHING
    {
        "id": 21,
        "title": "Women's Performance Leggings",
        "price": 39.95,
        "category": "women's clothing",
        "description": "High-waist leggings with moisture-wicking fabric.",
        "image": "https://images.pexels.com/photos/2088180/pexels-photo-2088180.jpeg",
    },
    {
        "id": 22,
        "title": "Women's Running Top",
        "price": 34.50,
        "category": "women's clothing",
        "description": "Lightweight top for tempo sessions and races.",
        "image": "https://images.pexels.com/photos/842567/pexels-photo-842567.jpeg",
    },

    # SHOES
    {
        "id": 31,
        "title": "Carbon Race Shoes",
        "price": 189.0,
        "category": "shoes",
        "description": "Lightweight carbon-plate shoes for fast races.",
        "image": "https://images.pexels.com/photos/976873/pexels-photo-976873.jpeg",
    },
    {
        "id": 32,
        "title": "Daily Trainer Shoes",
        "price": 119.0,
        "category": "shoes",
        "description": "Cushioned shoes for everyday miles.",
        "image": "https://images.pexels.com/photos/2529159/pexels-photo-2529159.jpeg",
    },
]


def _fallback_categories() -> List[Dict]:
    """Build category list from the fallback products."""
    categories: Dict[str, Dict] = {}
    for p in FALLBACK_PRODUCTS:
        name = p["category"]
        if name not in categories:
            if name.lower() == "men's clothing":
                cid = "mens_clothing"
            elif name.lower() == "women's clothing":
                cid = "womens_clothing"
            else:
                cid = name.replace(" ", "_").lower()
            categories[name] = {"id": cid, "name": name}
    return list(categories.values())


# ------------------------------------------------------------------
# Public helpers used by the router
# ------------------------------------------------------------------
def get_categories() -> List[Dict]:
    """
    Try FakeStore /products/categories.
    On failure, return local fallback categories.
    """
    try:
        resp = requests.get(f"{FAKESTORE_BASE_URL}/products/categories", timeout=5)
        resp.raise_for_status()
        data = resp.json()  # FakeStore returns list of strings
        categories = []
        for c in data:
            if c.lower() == "men's clothing":
                cid = "mens_clothing"
            elif c.lower() == "women's clothing":
                cid = "womens_clothing"
            else:
                cid = c.replace(" ", "_").lower()
            categories.append({"id": cid, "name": c})
        return categories
    except Exception:
        # Use our local catalogue instead
        return _fallback_categories()


def get_products_by_category(category: str) -> List[Dict]:
    """
    Try FakeStore /products/category/{category}.
    `category` here can be 'electronics', 'mens_clothing', 'women's clothing', 'shoes', etc.
    """
    lookup = category.lower()

    # Map our IDs to FakeStore category names
    if lookup == "mens_clothing":
        fakestore_category = "men's clothing"
    elif lookup == "womens_clothing":
        fakestore_category = "women's clothing"
    else:
        fakestore_category = lookup.replace("_", " ")

    try:
        resp = requests.get(
            f"{FAKESTORE_BASE_URL}/products/category/{fakestore_category}",
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        # Fallback: use local products filtered by category name
        return [
            p
            for p in FALLBACK_PRODUCTS
            if p["category"].lower() == fakestore_category
        ]
