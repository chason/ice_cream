# Generated by Django 4.1.5 on 2023-01-08 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("trucks", "0002_fooditem_stock"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="fooditem",
            name="stock",
        ),
        migrations.RemoveField(
            model_name="fooditem",
            name="truck",
        ),
        migrations.CreateModel(
            name="Stock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                (
                    "food_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="trucks.fooditem",
                    ),
                ),
                (
                    "truck",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="trucks.truck"
                    ),
                ),
            ],
        ),
    ]
