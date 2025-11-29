import os
import sys

# Make sure we can import the app package
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_categories():
    response = client.get("/products/categories")
    assert response.status_code == 200

    data = response.json()
    # we expect a list of category objects with ids
    assert isinstance(data, list)

    ids = {item["id"] for item in data}
    assert ids == {"electronics", "jewelery", "mens_clothing", "womens_clothing"}


def test_get_products_for_electronics():
    response = client.get("/products/category/electronics")
    assert response.status_code == 200

    data = response.json()
    # structure: {"category": "electronics", "products": [...]}
    assert data["category"] == "electronics"
    assert isinstance(data["products"], list)
    # there should be at least one product from FakeStore
    assert len(data["products"]) > 0
