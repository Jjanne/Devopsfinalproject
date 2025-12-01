# app/routers/products.py
from fastapi import APIRouter
from typing import List

router = APIRouter()

# ------------------------------------------------------------------
# Static product catalogue – under YOUR control, no external API.
# You can tweak titles / prices / images until the UI looks perfect.
# ------------------------------------------------------------------
PRODUCTS = [
    # ----------------- ELECTRONICS -----------------
    {
        "id": 1,
        "title": "WD 2TB Elements Portable External Hard Drive - USB 3.0",
        "price": 64.00,
        "description": "USB 3.0 and USB 2.0 compatibility. Fast data transfers and high capacity.",
        "category": "electronics",
        "image": "/images/electronics-1.png",
    },
    {
        "id": 2,
        "title": "SanDisk SSD PLUS 1TB Internal SSD - SATA III 6 Gb/s",
        "price": 109.00,
        "description": "Easy upgrade for faster boot-up, shutdown, and application response.",
        "category": "electronics",
        "image": "/images/electronics-2.png",
    },
    {
        "id": 3,
        "title": "Silicon Power 256GB SSD 3D NAND A55",
        "price": 109.00,
        "description": "High transfer speeds and reliable performance.",
        "category": "electronics",
        "image": "/images/electronics-3.png",
    },
    {
        "id": 4,
        "title": "WD 4TB Gaming Drive Works with Playstation 4",
        "price": 114.00,
        "description": "Expand your PS4 gaming experience with high-capacity storage.",
        "category": "electronics",
        "image": "/images/electronics-4.png",
    },
    {
        "id": 5,
        "title": "Acer SB220Q 21.5-inch Full HD Monitor",
        "price": 599.00,
        "description": "IPS display, ultra-thin design, great for work and play.",
        "category": "electronics",
        "image": "/images/electronics-5.png",
    },
    {
        "id": 6,
        "title": "Samsung 49-Inch CHG90 144Hz Ultrawide Gaming Monitor",
        "price": 999.99,
        "description": "Super ultrawide QLED gaming monitor with immersive performance.",
        "category": "electronics",
        "image": "/images/electronics-6.png",
    },

    # ----------------- JEWELERY -----------------
    {
        "id": 7,
        "title": "John Hardy Women's Legends Naga Gold & Silver Dragon Bracelet",
        "price": 695.00,
        "description": "Inspired by the mythical water dragon—symbol of protection.",
        "category": "jewelery",
        "image": "/images/jewelery-1.png",
    },
    {
        "id": 8,
        "title": "Solid Gold Petite Micropave Ring",
        "price": 168.00,
        "description": "Classic, elegant design with brilliant finish.",
        "category": "jewelery",
        "image": "/images/jewelery-2.png",
    },
    {
        "id": 9,
        "title": "White Gold Plated Princess Ring",
        "price": 9.99,
        "description": "Engagement-style solitaire ring at an affordable price.",
        "category": "jewelery",
        "image": "/images/jewelery-3.png",
    },
    {
        "id": 10,
        "title": "Pierced Owl Rose Gold Stainless Steel Earrings",
        "price": 10.99,
        "description": "Rose gold-plated stainless steel double flare plugs.",
        "category": "jewelery",
        "image": "/images/jewelery-4.png",
    },

    # ----------------- MEN'S CLOTHING -----------------
    {
        "id": 11,
        "title": "Fjallraven - Foldpack No.1 Backpack",
        "price": 109.95,
        "description": "Perfect for everyday carry with a stylish and durable build.",
        "category": "men's clothing",
        "image": "/images/mens-1.png",
    },
    {
        "id": 12,
        "title": "Men's Casual Premium Slim Fit T-Shirt",
        "price": 22.30,
        "description": "Slim-fit style with soft, comfortable fabric.",
        "category": "men's clothing",
        "image": "/images/mens-2.png",
    },
    {
        "id": 13,
        "title": "Men's Cotton Jacket",
        "price": 55.99,
        "description": "Great outerwear jacket for versatile outdoor use.",
        "category": "men's clothing",
        "image": "/images/mens-3.png",
    },
    {
        "id": 14,
        "title": "Men's Casual Slim Fit Long Sleeve",
        "price": 15.99,
        "description": "Soft and warm, ideal for cooler weather.",
        "category": "men's clothing",
        "image": "/images/mens-4.png",
    },

    # ----------------- WOMEN'S CLOTHING -----------------
    {
        "id": 15,
        "title": "BIYLACLESEN Women's 3-in-1 Snowboard Jacket",
        "price": 56.99,
        "description": "Warm, waterproof jacket suitable for winter sports.",
        "category": "women's clothing",
        "image": "/images/womens-1.png",
    },
    {
        "id": 16,
        "title": "Lock and Love Women's Faux Leather Moto Jacket",
        "price": 29.95,
        "description": "Faux leather moto jacket with removable hood.",
        "category": "women's clothing",
        "image": "/images/womens-2.png",
    },
    {
        "id": 17,
        "title": "Women's Windbreaker Raincoat",
        "price": 39.99,
        "description": "Lightweight rain jacket perfect for outdoor activities.",
        "category": "women's clothing",
        "image": "/images/womens-3.png",
    },
    {
        "id": 18,
        "title": "MBJ Women's Solid Short Sleeve Boat Neck Tee",
        "price": 9.85,
        "description": "Soft and breathable everyday top.",
        "category": "women's clothing",
        "image": "/images/womens-4.png",
    },
    {
        "id": 19,
        "title": "Opna Women's Short Sleeve Moisture-Wicking Shirt",
        "price": 7.95,
        "description": "Moisture-wicking interlock fabric great for workouts.",
        "category": "women's clothing",
        "image": "/images/womens-5.png",
    },
    {
        "id": 20,
        "title": "DANVOUY Women's T-Shirt Casual Cotton Top",
        "price": 12.99,
        "description": "Soft cotton t-shirt with a flattering fit.",
        "category": "women's clothing",
        "image": "/images/womens-6.png",
    },
]

# The four categories your frontend expects
CATEGORIES = ["electronics", "jewelery", "men's clothing", "women's clothing"]


@router.get("/categories", response_model=List[str])
def list_categories():
    """
    Return the fixed list of categories.
    """
    return CATEGORIES


@router.get("/category/{category}")
def get_products_by_category(category: str):
    """
    Return all products for a given category.
    Always 200 OK. If category is unknown, returns [].
    """
    return [p for p in PRODUCTS if p["category"] == category]
