# Generated by Django 4.1 on 2025-01-02 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_auto_20250102_1935"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="products",
            name="color",
        ),
        migrations.AddField(
            model_name="orderitem",
            name="color",
            field=models.ForeignKey(
                default="", on_delete=django.db.models.deletion.CASCADE, to="main.color"
            ),
            preserve_default=False,
        ),
    ]