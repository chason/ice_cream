# Generated by Django 4.1.5 on 2023-01-08 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("trucks", "0008_remove_truck_stock_alter_stock_truck"),
    ]

    operations = [
        migrations.AddField(
            model_name="fooditem",
            name="name",
            field=models.CharField(default="default", max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="stock",
            name="truck",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="stock",
                to="trucks.truck",
            ),
        ),
    ]
