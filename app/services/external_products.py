# api/services/external_products.py

from typing import List, Dict
from fastapi import HTTPException

# ------------------------------------------------------------------
# In-memory product catalogue (no calls to FakeStore)
# ------------------------------------------------------------------

PRODUCTS: List[Dict] = [
    # ----------------- ELECTRONICS -----------------
    {
        "id": 1,
        "title": "WD 2TB Elements Portable External Hard Drive - USB 3.0",
        "price": 64.0,
        "description": "USB 3.0 and USB 2.0 compatibility. Fast data transfers and high capacity.",
        "category": "electronics",
        "image": "/images/electronics-1.png",
    },
    {
        "id": 2,
        "title": "SanDisk SSD PLUS 1TB Internal SSD - SATA III 6 Gb/s",
        "price": 109.0,
        "description": "Easy upgrade for faster boot-up, shutdown and application response.",
        "category": "electronics",
        "image": "/images/electronics-2.png",
    },
    {
        "id": 3,
        "title": "Silicon Power 256GB SSD 3D NAND A55",
        "price": 109.0,
        "description": "High transfer speeds and better boot-up and load performance.",
        "category": "electronics",
        "image": "/images/electronics-3.png",
    },
    {
        "id": 4,
        "title": "WD 4TB Gaming Drive Works with Playstation 4",
        "price": 114.0,
        "description": "Expand your PS4 gaming experience with a sleek high-capacity drive.",
        "category": "electronics",
        "image": "/images/electronics-4.png",
    },
    {
        "id": 5,
        "title": "Acer 21.5\" Full HD IPS Ultra-Thin Monitor",
        "price": 599.0,
        "description": "Full HD IPS display with ultra-thin design.",
        "category": "electronics",
        "image": "/images/electronics-5.png",
    },
    {
        "id": 6,
        "title": "Samsung 49\" CHG90 144Hz Curved Gaming Monitor",
        "price": 999.99,
        "description": "Super ultrawide QLED gaming monitor.",
        "category": "electronics",
        "image": "/images/electronics-6.png",
    },

    # ----------------- JEWELERY -----------------
    {
        "id": 7,
        "title": "John Hardy Women's Legends Naga Gold & Silver Dragon Station Chain Bracelet",
        "price": 695.0,
        "description": "From the Legends collection, inspired by the mythical water dragon.",
        "category": "jewelery",
        "image": "/images/jewelery-1.png",
    },
    {
        "id": 8,
        "title": "Solid Gold Petite Micropave",
        "price": 168.0,
        "description": "Satisfaction guaranteed. Return or exchange any order within 30 days.",
        "category": "jewelery",
        "image": "/images/jewelery-2.png",
    },
    {
        "id": 9,
        "title": "White Gold Plated Princess",
        "price": 9.99,
        "description": "Classic wedding engagement solitaire diamond ring.",
        "category": "jewelery",
        "image": "/images/jewelery-3.png",
    },
    {
        "id": 10,
        "title": "Pierced Owl Rose Gold Plated Stainless Steel Double",
        "price": 10.99,
        "description": "Rose gold plated stainless steel double flare plugs.",
        "category": "jewelery",
        "image": "/images/jewelery-4.png",
    },

    # ----------------- MEN'S CLOTHING -----------------
    {
        "id": 11,
        "title": "Fjallraven - Foldsack No. 1 Backpack, Fits 15\" Laptops",
        "price": 109.95,
        "description": "Perfect pack for everyday use and walks in the forest.",
        "category": "men's clothing",
        "image": "/images/mens-1.png",
    },
    {
        "id": 12,
        "title": "Mens Casual Premium Slim Fit T-Shirts",
        "price": 22.3,
        "description": "Slim-fitting style, contrast raglan sleeve, three-button henley placket.",
        "category": "men's clothing",
        "image": "/images/mens-2.png",
    },
    {
        "id": 13,
        "title": "Mens Cotton Jacket",
        "price": 55.99,
        "description": "Great outerwear jacket for many occasions.",
        "category": "men's clothing",
        "image": "/images/mens-3.png",
    },
    {
        "id": 14,
        "title": "Mens Casual Slim Fit",
        "price": 15.99,
        "description": "The color could be slightly different between the screen and in practice.",
        "category": "men's clothing",
        "image": "/images/mens-4.png",
    },

    # ----------------- WOMEN'S CLOTHING -----------------
    {
        "id": 15,
        "title": "BIYLACLESEN Women's 3-in-1 Snowboard Jacket Winter Coats",
        "price": 56.99,
        "description": "3-in-1 jacket for US standard size, detachable design.",
        "category": "women's clothing",
        "image": "/images/womens-1.png",
    },
    {
        "id": 16,
        "title": "Lock and Love Women's Removable Hooded Faux Leather Moto Biker Jacket",
        "price": 29.95,
        "description": "Faux leather jacket with removable hood.",
        "category": "women's clothing",
        "image": "/images/womens-2.png",
    },
    {
        "id": 17,
        "title": "Rain Jacket Women Windbreaker Striped Climbing Raincoats",
        "price": 39.99,
        "description": "Lightweight rain jacket for casual wear.",
        "category": "women's clothing",
        "image": "/images/womens-3.png",
    },
    {
        "id": 18,
        "title": "MBJ Women's Solid Short Sleeve Boat Neck V",
        "price": 9.85,
        "description": "Lightweight fabric with great stretch for comfort.",
        "category": "women's clothing",
        "image": "/images/womens-4.png",
    },
    {
        "id": 19,
        "title": "Opna Women's Short Sleeve Moisture",
        "price": 7.95,
        "description": "Moisture-wicking fabric, perfect for sports.",
        "category": "women's clothing",
        "image": "/images/womens-5.png",
    },
    {
        "id": 20,
        "title": "DANVOUY Womens T Shirt Casual Cotton Short",
        "price": 12.99,
        "description": "Casual short-sleeve cotton T-shirt.",
        "category": "women's clothing",
        "image": "/images/womens-6.png",
    },
]


# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------


def _normalize_category(category_id: str) -> str:
    """
    Map the category id used in the frontend (e.g. 'mens_clothing')
    to the underlying category string stored in the products
    (e.g. "men's clothing").
    """
    lower = category_id.lower()
    if lower in {"mens_clothing", "men's clothing"}:
        return "men's clothing"
    if lower in {"womens_clothing", "women's clothing"}:
        return "women's clothing"
    return lower  # 'electronics', 'jewelery', etc.


def get_categories() -> List[Dict]:
    """Return distinct categories derived from PRODUCTS."""
    seen = {}
    for p in PRODUCTS:
        cat = p["category"]
        if cat not in seen:
            # id used by frontend buttons
            if cat == "men's clothing":
                cid = "mens_clothing"
            elif cat == "women's clothing":
                cid = "womens_clothing"
            else:
                cid = cat
            seen[cat] = {"id": cid, "name": cat.title()}
    return list(seen.values())


def get_products_by_category(category_id: str) -> List[Dict]:
    """
    Return all products for a given category id
    (electronics, jewelery, mens_clothing, womens_clothing).
    """
    normalized = _normalize_category(category_id)
    return [p for p in PRODUCTS if p["category"] == normalized]


def get_product(product_id: int) -> Dict:
    """
    Return a single product by id, or raise 404.
    This is used when adding items to the cart so that
    the API never calls FakeStore.
    """
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")
