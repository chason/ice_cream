from rest_framework import serializers
from rest_framework.fields import Field
from .models import Truck, FoodItem, Stock, Purchase


class FoodItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the FoodItem model
    """

    class Meta:
        model = FoodItem
        fields = ["id", "category", "flavor", "price", "name"]


class StockSerializer(serializers.ModelSerializer):
    """
    Serializer for the Stock model

    We have two `write_only` fields which allow us to create new stock from
    the API.
    """

    food_item = FoodItemSerializer(read_only=True)
    truck: Field = serializers.StringRelatedField(read_only=True)
    food_item_id = serializers.PrimaryKeyRelatedField(
        write_only=True, required=True, queryset=FoodItem.objects.all()
    )
    truck_id = serializers.PrimaryKeyRelatedField(
        write_only=True, required=True, queryset=Truck.objects.all()
    )

    class Meta:
        model = Stock
        fields = ["id", "food_item", "quantity", "truck", "food_item_id", "truck_id"]

    def create(self, validated_data: dict):
        food = validated_data.pop("food_item_id")
        truck = validated_data.pop("truck_id")
        return Stock.objects.create(
            food_item=food, truck=truck, quantity=validated_data["quantity"]
        )


class TruckSerializer(serializers.ModelSerializer):
    """
    Serializer for the Truck model

    We have a field on here for `total_money` that is filled in by the
    ViewSet. It collates all the purchases for that truck. In the future,
    there should probably be options to see this total by date range.
    """

    total_money = serializers.DecimalField(
        max_digits=9, decimal_places=2, read_only=True
    )
    stock = StockSerializer(many=True, read_only=True)

    class Meta:
        model = Truck
        fields = ["id", "name", "stock", "total_money"]


class PurchaseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Purchase model

    We have a custom `create` method here because we don't want to accept
    the price from the client.
    """

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
