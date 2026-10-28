"""Task 3: Flask test-client tests for the REST API."""
import unittest
from decimal import Decimal
from service import app
from service.models import Product, db, init_db
from service.common import status
from tests.factories import ProductFactory

BASE_URL = "/products"

class TestProductRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        init_db(app)

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        self.ctx.pop()

    def _create_products(self, count=1):
        products = []
        for product in ProductFactory.create_batch(count):
            product.id = None
            response = self.client.post(BASE_URL, json=product.serialize())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            product.id = response.get_json()["id"]
            products.append(product)
        return products

    def get_product_count(self):
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return len(response.get_json())

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Product Catalog Administration", response.data)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["message"], "OK")

    def test_create_product(self):
        product = ProductFactory()
        product.id = None
        response = self.client.post(BASE_URL, json=product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.headers.get("Location"))

    def test_read_product(self):
        """It should Read a Product"""
        product = self._create_products()[0]
        response = self.client.get(f"{BASE_URL}/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(data["id"], product.id)
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["description"], product.description)
        self.assertEqual(Decimal(data["price"]), product.price)
        self.assertEqual(data["available"], product.available)
        self.assertEqual(data["category"], product.category.name)


    def test_update_product(self):
        """It should Update an existing Product"""
        test_product = ProductFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_product = response.get_json()
        new_product["description"] = "unknown"
        response = self.client.put(
            f"{BASE_URL}/{new_product['id']}", json=new_product
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["description"], "unknown")


    def test_delete_product(self):
        """It should Delete a Product"""
        products = self._create_products(5)
        product_count = self.get_product_count()
        test_product = products[0]
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)

        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        new_count = self.get_product_count()
        self.assertEqual(new_count, product_count - 1)


    def test_list_all_products(self):
        """It should List all Products"""
        self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)


    def test_list_products_by_name(self):
        """It should List Products by Name"""
        self._create_products(3)
        product = ProductFactory(name="Unique Test Product")
        response = self.client.post(BASE_URL, json=product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(
            BASE_URL, query_string={"name": "Unique Test Product"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Unique Test Product")


    def test_list_products_by_category(self):
        """It should List Products by Category"""
        for category in ["FOOD", "FOOD", "TOOLS"]:
            product = ProductFactory()
            data = product.serialize()
            data["category"] = category
            response = self.client.post(BASE_URL, json=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(
            BASE_URL, query_string={"category": "FOOD"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertTrue(all(p["category"] == "FOOD" for p in data))


    def test_list_products_by_availability(self):
        """It should List Products by Availability"""
        for available in [True, True, False]:
            product = ProductFactory(available=available)
            response = self.client.post(BASE_URL, json=product.serialize())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(
            BASE_URL, query_string={"available": "true"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertTrue(all(p["available"] for p in data))

        response = self.client.get(
            BASE_URL, query_string={"available": "false"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertTrue(all(not p["available"] for p in data))
