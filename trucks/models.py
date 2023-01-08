from django.db import models


class FoodItem(models.Model):
    category = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.flavor} {self.category})"


class Truck(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Stock(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name="stock")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


class Purchase(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name="purchases")
    price = models.DecimalField(max_digits=9, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
