from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_create_and_get_product():
    created = client.post(
        "/products/",
        json={"title": "Espresso", "description": "Strong.", "price": 3.5, "currency": "EUR"},
    )
    assert created.status_code == 201
    pid = created.json()["id"]

    fetched = client.get(f"/products/{pid}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Espresso"
