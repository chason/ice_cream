Ice Cream Truck
================

This is a sample application for a Django REST API implementing a basic ice
truck functionality.

To get started, you'll want to first create a superuser account:
```bash
python manage.py createsuperuser
```

After that, you can optionally load a fixture containing some sample data:
```bash
python manage.py loaddata trucks/fixture.json
```

From here you can proceed in a couple of ways. If you login to the admin
website with the superuser credentials you created above, you can manually
edit the database, especially if you didn't use the fixture.

Otherwise, you can start hitting the API. For instance, this will return a
list of all the trucks as well as what they have in stock:
```bash
curl http://localhost:8000/trucks/ \
-H "Content-Type: application/json"
```

To make any POST requests, you'll need to authenticate with the API (with the
exception of purchases which don't require authentication).

This can be done with HTTP basic authentication like the following:
```bash 
curl -X PUT http://localhost:8000/trucks/1/ \
-H "Content-Type: application/json" \
-d '{"name": "Foo Truck"}' \
--user "admin:password123"
```

To make a purchase, you'll send a request like this:
```bash
curl -X POST http://localhost:8000/purchases/ \
-H "Content-Type: application/json" \
-d "{truck: 1, items: [1]}"
```

The purchase request format is to provide the ID of the truck you are
purchasing from under the `truck` attribute and a list of food item
IDs under the `items` attribute.