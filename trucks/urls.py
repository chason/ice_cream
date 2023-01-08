from .views import TruckViewSet

truck_list = TruckViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

truck_detail = TruckViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

truck_purchase = TruckViewSet.as_view({"post": "purchase"})
