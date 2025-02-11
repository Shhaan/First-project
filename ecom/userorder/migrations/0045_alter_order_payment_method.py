# Generated by Django 4.2.7 on 2024-01-13 08:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userorder", "0044_alter_categoryoffer_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("cash_on_delivery", "Cash on Delivery"),
                    ("pay_by_wallet", "Wallet  payment"),
                    ("paypal", "PayPal"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]
