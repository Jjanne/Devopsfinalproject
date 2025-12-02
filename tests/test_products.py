import os
import sys
from fastapi.testclient import TestClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.main import app  

client = TestClient(app)


def test_list_categories():
    response = client.get("/products/categories")
    assert response.status_code == 200

    data = response.json()

    # API returns a simple list of category strings
    assert isinstance(data, list)
    assert set(data) == {
        "electronics",
        "jewelery",
        "men's clothing",
        "women's clothing",
    }


def test_get_products_for_electronics():
    response = client.get("/products/category/electronics")
    assert response.status_code == 200

    data = response.json()

    # API returns a list of product objects for this category
    assert isinstance(data, list)
    assert len(data) > 0

    # every product should be in the "electronics" category
    assert all(item["category"] == "electronics" for item in data)
