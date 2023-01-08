from collections import Counter

from django.db.models import Sum
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Truck, Stock, FoodItem, Purchase
from .serializers import TruckSerializer, StockSerializer, PurchaseSerializer


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.annotate(total_money=Sum("purchases__price")).all()
    print(queryset.get(id=1).purchases)
    serializer_class = TruckSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["post"])
    def purchase(self, request, pk=None):
        truck = self.get_object()
        items = [item["id"] for item in request.data["items"]]
        item_objs = [FoodItem.objects.get(pk=item) for item in items]
        purchase = PurchaseSerializer(data={"truck": truck, "items": item_objs})
        if not purchase.is_valid():
            print(purchase.errors)
            return Response(
                {"error": "Invalid purchase"}, status=status.HTTP_400_BAD_REQUEST
            )
        print(purchase.validated_data)

        items_counter = Counter(items)
        affected_stock = []
        for item, quantity in items_counter.items():
            in_stock = truck.stock.get(food_item=item)
            if quantity > in_stock.quantity:
                return Response({"response": "SORRY!"})
            in_stock.quantity -= quantity
            affected_stock.append(in_stock)

        for stock in affected_stock:
            stock.save()
        purchase.save()
        return Response({"response": "ENJOY!"})


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request):
        serializer = PurchaseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        truck = validated_data["truck"]
        items_counter = Counter(validated_data["items"])
        affected_stock = []
        price = 0
        for item, quantity in items_counter.items():
            in_stock = truck.stock.get(food_item=item)
            if quantity > in_stock.quantity:
                return Response({"response": "SORRY!"})
            in_stock.quantity -= quantity
            affected_stock.append(in_stock)
            price += quantity * item.price

        for stock in affected_stock:
            stock.save()
        purchase = serializer.save(calculated_price=price)
        return Response({"response": "ENJOY!"})
