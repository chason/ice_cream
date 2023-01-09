from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .models import Truck, FoodItem, Stock, Purchase


class TrucksTestCase(APITestCase):
    def setUp(self) -> None:
        self.truck = Truck.objects.create(name="My Test Truck")
        self.item = FoodItem.objects.create(
            name="Test Cream", flavor="Chocolate", category="Ice Cream", price=1
        )
        self.stock = Stock.objects.create(
            truck=self.truck, food_item=self.item, quantity=50
        )
        self.purchase = Purchase.objects.create(truck=self.truck, price=2)
        self.user = User.objects.create(username="test")

    def test_view_trucks(self):
        url = reverse("trucks-list")
        response = self.client.get(url)
        self.assertTrue(len(response.data) == 1)
        self.assertTrue(response.data[0]["name"] == self.truck.name)
        self.assertTrue(len(response.data[0]["stock"]) == 1)

    def test_unauthenticated_create_truck(self):
        url = reverse("trucks-list")
        response = self.client.post(url, {"name": "Don't Create"}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_authorized_create_truck(self):
        url = reverse("trucks-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {"name": "Please Create"}, format="json")
        self.assertEqual(response.status_code, 201)
        truck = Truck.objects.get(name="Please Create")
        self.assertTrue(truck)

    def test_detail_truck(self):
        url = reverse("trucks-detail", args=[self.truck.id])
        response = self.client.get(url)
        self.assertEqual(response.data["name"], self.truck.name)

    def test_list_stock(self):
        url = reverse("stock-list")
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

    def test_add_stock(self):
        url = reverse("stock-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            url, {"truck_id": 1, "food_item_id": 1, "quantity": 1}
        )
        self.assertEqual(response.status_code, 201)

    def test_update_quantity(self):
        url = reverse("stock-detail", args=[self.stock.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"quantity": 100})
        self.assertEqual(response.status_code, 200)
        # get new data
        stock = Stock.objects.get(pk=self.stock.id)
        self.assertEqual(stock.quantity, 100)

    def test_single_purchase(self):
        url = reverse("purchases-list")
        old_stock = self.stock.quantity
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            url, {"truck": self.truck.id, "items": [self.stock.id]}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"response": "ENJOY!"})
        stock = Stock.objects.get(pk=self.stock.id)
        self.assertEqual(stock.quantity, old_stock - 1)

    def test_multiple_purchase(self):
        new_fi = FoodItem.objects.create(
            name="Testy Crunch Bar", flavor="Chocolate", category="Candy Bar", price=2
        )
        new_stock = Stock.objects.create(
            truck=self.truck, food_item=new_fi, quantity=10
        )
        url = reverse("purchases-list")
        old_stock = self.stock.quantity
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            url,
            {
                "truck": self.truck.id,
                "items": [self.stock.id, self.stock.id, new_stock.id],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"response": "ENJOY!"})
        new_stock.refresh_from_db()
        self.assertEqual(new_stock.quantity, 9)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, old_stock - 2)

        price_url = reverse("trucks-detail", args=[self.truck.id])
        price_response = self.client.get(price_url)
        self.assertEqual(
            price_response.data["total_money"],
            f"{self.purchase.price + self.item.price * 2 + new_fi.price:.2f}",
        )

    def test_bad_quantity(self):
        url = reverse("purchases-list")
        self.stock.quantity = 0
        self.stock.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            url, {"truck": self.truck.id, "items": [self.stock.id]}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"response": "SORRY!"})
        old_stock = self.stock.quantity
        self.stock.refresh_from_db()
        self.assertEqual(old_stock, self.stock.quantity)
