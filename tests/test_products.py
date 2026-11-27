"""Product and order endpoint tests."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_products_endpoint_returns_products():
    response = client.get("/products")

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 3
    assert len(body["products"]) == 3
    assert body["products"][0]["name"] == "Cloud Rescue Hoodie"


def test_order_creation_succeeds():
    response = client.post("/orders", json={
        "product_id": 1,
        "quantity": 2,
        "customer_name": "Alex",
    })

    assert response.status_code == 200
    body = response.json()
    assert body["order_id"] == "CR-1-0002"
    assert body["quantity"] == 2
    assert body["customer_name"] == "Alex"
    assert body["total"] == 99.98
    assert body["status"] == "created"


def test_order_creation_rejects_unknown_product():
    response = client.post("/orders", json={
        "product_id": 999,
        "quantity": 1,
        "customer_name": "Alex",
    })

    assert response.status_code == 404
