# Generated by Django 4.1 on 2024-12-31 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_alter_products_color_order_orderitem"),
    ]

    operations = [
        migrations.CreateModel(
            name="Color",
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
                ("name", models.CharField(max_length=100)),
                ("number", models.DecimalField(decimal_places=2, max_digits=10)),
                ("hex_value", models.CharField(max_length=10)),
            ],
        ),
    ]