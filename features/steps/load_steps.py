"""Task 5: Set up BDD background product data through REST."""
import requests
from behave import given

HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204


@given("the following products")
def load_products(context):
    rest_endpoint = f"{context.base_url}/products"
    response = requests.get(rest_endpoint, timeout=15)
    assert response.status_code == HTTP_200_OK, response.text

    for product in response.json():
        response = requests.delete(f"{rest_endpoint}/{product['id']}", timeout=15)
        assert response.status_code == HTTP_204_NO_CONTENT, response.text

    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": row["price"],
            "available": row["available"].lower() == "true",
            "category": row["category"]
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        assert context.resp.status_code == HTTP_201_CREATED
