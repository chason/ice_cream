Ice Cream Truck
================

This is a sample application for a Django REST API implementing a basic ice
cream truck functionality.

Getting Started
---------

First, install the python modules from the `requirements.txt` file, preferably
into a virtual environment:
```bash
pip install -r requirements.txt
```

Then you'll want to apply the migrations to instantiate your SQLite
database:
```bash
python manage.py migrate
```

After that, you'll want to create a superuser account that you can use to
login to the admin site and authenticate against the API with:
```bash
python manage.py createsuperuser
```

You can optionally load a fixture containing some sample data:
```bash
python manage.py loaddata trucks/fixture.json
```

Starting the Server
--------

From here you can proceed in a couple of ways. If you login to the admin
website with the superuser credentials you created above, you can manually
edit the database, especially if you didn't use the fixture.

To proceed, you'll want to start the server:
```bash
python manage.py runserver
```

If you want to add or edit any of the data in the database, proceed to the
[Admin Website](http://localhost:8000/admin).

Listing Trucks
------

Otherwise, you can start hitting the API. For instance, this will return a
list of all the trucks as well as what they have in stock:
```bash
curl http://localhost:8000/trucks/ \
-H "Content-Type: application/json"
```

Adding a Truck
-------

To make any POST requests, you'll need to authenticate with the API (with the
exception of purchases which don't require authentication).

This can be done with HTTP basic authentication like the following:
```bash 
curl -X PUT http://localhost:8000/trucks/1/ \
-H "Content-Type: application/json" \
-d '{"name": "Foo Truck"}' \
--user "admin:password123"
```

Making a Purchase
-------

To make a purchase, you'll send a request like this:
```bash
curl -X POST http://localhost:8000/purchases/ \
-H "Content-Type: application/json" \
-d "{truck: 1, items: [1]}"
```

The purchase request format is to provide the ID of the truck you are
purchasing from under the `truck` attribute and a list of food item
IDs under the `items` attribute.

Running Tests
-------

To run the included unit tests, simply use the Django command:
```bash
python manage.py test
```