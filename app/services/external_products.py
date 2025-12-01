# app/services/external_products.py

from typing import List, Dict
from fastapi import HTTPException

# IMPORTANT:
# We reuse the same in-memory catalogue that the Products router uses,
# so the IDs, titles, prices, images, etc. are consistent everywhere.
from app.routers.products import PRODUCTS


def _category_id_from_name(name: str) -> str:
    """
    Convert a human-readable category name to the ID we expose via the API.

    Examples:
        "men's clothing"   -> "mens_clothing"
        "women's clothing" -> "womens_clothing"
        "Electronics"      -> "electronics"
    """
    n = name.lower()
    if n == "men's clothing":
        return "mens_clothing"
    if n == "women's clothing":
        return "womens_clothing"
    return n.replace(" ", "_")


def _category_name_from_id(category_id: str) -> str:
    """
    Convert an API category ID back to the human-readable name stored in PRODUCTS.

    Examples:
        "mens_clothing"    -> "men's clothing"
        "womens_clothing"  -> "women's clothing"
        "electronics"      -> "electronics"
    """
    cid = category_id.lower()
    if cid == "mens_clothing":
        return "men's clothing"
    if cid == "womens_clothing":
        return "women's clothing"
    return cid.replace("_", " ")


# ------------------------------------------------------------------
# Public helpers used by routers
# ------------------------------------------------------------------


def get_categories() -> List[Dict]:
    """
    Build the list of categories from the in-memory PRODUCTS list.

    Returns items like:
      { "id": "electronics", "name": "Electronics" }
      { "id": "mens_clothing", "name": "Men's Clothing" }
    """
    categories: Dict[str, Dict] = {}

    for p in PRODUCTS:
        name = p["category"]
        cid = _category_id_from_name(name)

        if cid not in categories:
            categories[cid] = {"id": cid, "name": name}

    return list(categories.values())


def get_products_by_category(category: str) -> List[Dict]:
    """
    Return all products in the given category from the in-memory catalogue.

    `category` is the *ID* used by the API:
        "electronics", "jewelery", "mens_clothing", "womens_clothing", etc.
    """
    # Map the API category ID back to the human-readable name stored in PRODUCTS
    category_name = _category_name_from_id(category)

    return [
        p
        for p in PRODUCTS
        if p["category"].lower() == category_name.lower()
    ]


def get_product_details(product_id: int) -> Dict:
    """
    Look up a single product by ID in the in-memory PRODUCTS list.

    This is used by the Cart endpoints when adding items so that
    the cart can include the product's price, title, image, etc.
    """
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p

    # If the product ID doesn't exist in our catalogue, return a clean 404
    raise HTTPException(status_code=404, detail="Product not found")
