from collections import Counter

from django.db.models import Sum
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Truck, Stock, Purchase
from .serializers import TruckSerializer, StockSerializer, PurchaseSerializer


class TruckViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Trucks

    Annotates the queryset with `total_money` as specified in the Serializer
    """

    queryset = Truck.objects.annotate(total_money=Sum("purchases__price")).all()
    serializer_class = TruckSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class StockViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Stock
    """

    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PurchaseViewSet(viewsets.ModelViewSet):
    """
    Viewset for Purchases

    We take just truck ID and item IDs to create an object, so we need to do
    some custom logic to create a new purchase object. Additionally, we need
    to check the stock of the truck and change it if we have everything in
    stock.

    In the future we could optionally give someone a partial order if only
    some of their items are in stock, as well as calculate change.
    """

    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request):
        serializer = PurchaseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        truck = validated_data["truck"]
        # Create a counter so we can see the quantities of the items ordered
        items_counter = Counter(validated_data["items"])
        affected_stock = []
        price = 0
        for item, quantity in items_counter.items():
            in_stock = truck.stock.get(food_item=item)
            if quantity > in_stock.quantity:
                # We are out of stock so go ahead and return before saving anything
                # We could possibly return an error status code here but it is a
                # "valid" request so we return 200 for now
                return Response({"response": "SORRY!"})
            in_stock.quantity -= quantity
            affected_stock.append(in_stock)
            price += quantity * item.price

        for stock in affected_stock:
            stock.save()
        serializer.save(calculated_price=price)
        return Response({"response": "ENJOY!"})
