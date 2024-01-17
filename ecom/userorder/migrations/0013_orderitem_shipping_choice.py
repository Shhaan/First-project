# Generated by Django 4.2.7 on 2023-12-22 13:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userorder", "0012_order_slug_orderitem_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="shipping_choice",
            field=models.CharField(
                choices=[
                    ("free", "free Shipping"),
                    ("local ", "Local Pickup from store"),
                    ("express", "Express Shipping"),
                    ("standard", "Standard Shipping"),
                    ("same day", "Same day shipping"),
                ],
                default="free",
                max_length=10,
            ),
        ),
    ]
