from django.db import models


class FoodItem(models.Model):
    """
    Model for a single food item.

    This can be an ice cream, candy bar, snocone, or whatever.
    """

    category = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.flavor} {self.category})"


class Truck(models.Model):
    """
    The model representing a single food truck. Right now we just store the
    name but in the future we could store opening hours, location, etc.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Stock(models.Model):
    """
    The model connecting food items to trucks, and storing how much stock they
    have on hand.
    """

    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name="stock")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


class Purchase(models.Model):
    """
    The model for purchases. Right now we just store the total bill and when
    it was ordered, but in the future we might want to note who purchased
    the items, which items were purchased, and payment method.
    """

    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name="purchases")
    price = models.DecimalField(max_digits=9, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
