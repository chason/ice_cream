from django.contrib import admin
from .models import Truck, FoodItem, Stock


class StockInline(admin.TabularInline):
    model = Stock
    extra = 1


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    inlines = (StockInline,)


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    pass
