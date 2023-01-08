from rest_framework import serializers
from .models import Truck, FoodItem, Stock, Purchase


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ["id", "category", "flavor", "price", "name"]


class StockSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer(read_only=True)
    truck = serializers.StringRelatedField()

    class Meta:
        model = Stock
        fields = ["id", "food_item", "quantity", "truck"]


class TruckSerializer(serializers.ModelSerializer):
    total_money = serializers.DecimalField(
        max_digits=9, decimal_places=2, read_only=True
    )
    stock = StockSerializer(many=True, read_only=True)

    class Meta:
        model = Truck
        fields = ["id", "name", "stock", "total_money"]


class PurchaseSerializer(serializers.ModelSerializer):
    truck = serializers.PrimaryKeyRelatedField(queryset=Truck.objects.all())
    items = serializers.PrimaryKeyRelatedField(
        queryset=FoodItem.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Purchase
        read_only_fields = ["price"]
        fields = ["id", "truck", "purchase_date", "items"]
        depth = 1

    def create(self, validated_data):
        price = validated_data.get("calculated_price")
        truck = validated_data.get("truck")
        return Purchase.objects.create(truck=truck, price=price)
