# Generated by Django 4.2.7 on 2024-01-07 17:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userorder", "0032_coupon_is_deleted_tax_is_deleted"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coupon",
            name="discount_percentage",
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
